#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys
import os
import re
import json
from collections import defaultdict, Counter
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta

from fmqlutils import VISTA_DATA_BASE_DIR
from fmqlutils.cacher.cacherUtils import FMQLReplyStore, FilteredResultIterator, metaOfVistA
from fmqlutils.reporter.reportUtils import MarkdownTable, reportPercent, reportAbsAndPercent, muBVC
from fmqlutils.typer.reduceTypeUtils import splitTypeDatas, checkDataPresent, singleValue, combineSubTypes, muBVCOfSTProp, refsOfST

from fmqlreports.webReportUtils import TOP_MD_TEMPL, SITE_DIR_TEMPL, ensureWebReportLocations, keyStats, flattenFrequencyDistribution, roundFloat, reduce4, flattenPropValues, vistasOfVISNByOne
from fmqlreports.webReportUtils import muPlotRef, makePlots 

from hl7Utils import HL7TemplateMaker, categorizeAndParseIFCHL7Message, makeBasicHL7Event, muMessageACKAPPACK, muMessageAPPACK, assembleMessageTextLines, gatherAndQA772_773OfProtocol, lookupConfig779_1

from webReportSPQHL7 import reduceSPQTBRHL7
 
"""
<------- if redo on next pass 668 or ...
More to do on new VDIF/CRNR (some due to test? Special link for incoming etc?)
See comments CRNRHL7SPECIAL
  * if remove then will see break of Expected First Ack to go back ... etc etc
  * need to work through expectations just for these (maybe send them off to another handler?)
-------------------------------------------

From: https://www.va.gov/vdl/documents/Clinical/CPRS-Consult_Request_Tracking/constm.pdf

... putting IFC in context of three 'remote' dispatches

+

> Created new routine GMRC75P to add the 'HCPS,APPLICATION PROXY' user to the NEW PERSON (#200) file. <------ new to check out

> Set up a new consult service that contains ‘NON VA CARE HCPS’ (e.g., NON VA
CARE HCPS HEMODIALYSIS). Note that the service name must contain “NON
VA CARE HCPS” as the prefix in order to be processed by HCPS. This naming
convention was created to adhere to existing Non VA Care (NVC) naming and
reporting standards.

> Interfacility Consults when used with Cerner Converted sites
The release of GMRC*3.0*154 adds three new components to the Interfacility Consults
(IFC) system.
1. VDIF (Veterans Data Integration and Federation) integration
2. MPI Patient Registration
3. Cerner Mail Groups

... Cerner means route through VDIF and not VistA direct

on 201 and delays ... see same process for Cerner and non Cerner interactions

> When a facility has been “converted” to Cerner, it will be necessary for the Interfacility Consults (IFC) system to recognize that the HL7 message should no longer be routed to the VistA instance but should be routed to the VDIF (Veterans Data Integration and Federation) router. The Master Patient Index (MPI) is queried to determine the status of the treating facility. If the status of the treating facility is “converted”, the system will reference the Parameter GMRC IFC REGIONAL ROUTER file (#8989.5) [ME: Parameter in there!]. This
Parameter contains the Logical Link (GMRC IFC1 – GMRC IFC6) used to connect to
one of the six VDIF (Veteran Data Integration and Federation) Regional Routers.
> 
> Once the patient is registered at the treating facility, a 201 error code is logged in the IFC Message Log (file #123.6). The IFC background job will read this message and resend the consult order as long as the message is at least one hour old. <------ here's the explanation for IFC delays 123.6
...
> A “converted” facility is not able to process HL7 application negative acknowledgement
(NACK) in the same manner as a “nonconverted” facility.  <--- mail groups
"""
 
"""
Background: to surface what HL7 and HL7 caused activity is logged in VistA to potentially (suggest this) aid tests for Cerner Migration and ICD and other document creation.

TODO BIGGER:
- [ ] REVISIT app ack only (showed in 757) vs 4 step and see # app ack only
- [ ] graphs/totals per month of 123s => HL7#s
- [ ] services in 123 section highlight the TIU ones
- [ ] FLOW CHART ala ICDs for ...
- [ ] TABLE ala ICD for msg contents like the embedded TIU
- [ ] detail errors (801s etc too)
- [ ] fit into wider look at SPQs (webReportHL7SPQ.py)
- [ ] add no examples of NAK (non simple ACK)

TODO EXTRA (round out before using for prop)
- [ ] F: P: back to I: O: for consistency so can do Placer and filler in one report w/o issues
- [ ] CONSULT ACTIVITY in A LOT more details ... see "STATUS CHANGE" as one in 692 (and SCHEDULE etc). Want to know all forms.
  see WCO and sched ex etc. <---- QA completely activity-eventtypes
- [ ] One off PID and MSH and ... ie/ next vary ing tables ... time zone too
  (make VDIF map easy) ie/ Show Table ala ICD ... [annex to show from real exs]
- [ ] call out an ADMIN ending things, not a TIU note ... see if can see examples
  (goes with getting exs of all states) ... given up front "air time"
- [ ] consider real de-ids for names or names like PROVIDER1,X ... PATIENT,NAME etc and reflect their diversity
------
- [ ] go to sample table for PID etc and to a flow chart or two? ... permitted nexts? ... all VistA's states

TODO FUTURE:
- [ ] TIU Audit Trail link in http://localhost:9100/schema#8925_5 ... what does it show for the HL7 transport?
- [ ] 123 to doc type? How link for that doctor menu pull up
  
From ICD Sept Review, bring out
- [ ] Figure 18/P70 TIU "Replicate VistA to VistA RPC call" seems to say ORU Message based on RPC data grab sends full document back to Cerner ... ditto for p70 addenda
ie/ notes vs comments ie/ WANT ADDENDA/TIU vs COMMENTs to come out [point to vista-vista doc sync]
- [ ] "Medicine Resulting" ... will lead to note or does now? Is this a custom HL7 trigger and one missing below as in a different subscriber?
- [ ] Scheduling ie/ can schedule an order
- [ ] VDIF Proxy PID ... “123^^^ICN^VETID~456^^^EDIPI^EDIPI” ie/ its exact remap from base
  ... base must be clearer here (IE/ UNIFORM one off PID table)
"""

def webReportHL7IFCSummary(hl7MessageReduction, ifcConsultsByIEN, hl7Config):
    
    stationNo = hl7MessageReduction["stationNo"]
    meta = metaOfVistA(stationNo)

    mu = TOP_MD_TEMPL.format("{} IFC HL7 Summary".format(stationNo))
    
    INTRO_BLURB = f"""

VistA holds logs of its HL7-based Interfacility Consult (IFC) communications with other VistAs in addition to the particulars of IFC activity itself. These descriptions are sufficient to __inform positive, negative and volume HL7 message testing as Cerner migrates VistAs__ while still supporting VistA's IFC messaging with unmigrated VistAs. In addition, during migration off VistA, __ICDs are being created to formally define its HL7 interfaces. These could be generated automatically__ based on this information.
    
The follow reports on a copy of production VistA {meta["name"]} cut on {meta["cutDate"]}.

"""
    mu += INTRO_BLURB

    # As services used picked out here but want to report the services first
    hmu, allToLocalServices, allToRemoteServices = webReportIFCHL7Basic(stationNo, hl7MessageReduction, ifcConsultsByIEN)
    
    mu += webReportIFC123(stationNo, hl7MessageReduction, ifcConsultsByIEN, allToLocalServices, allToRemoteServices)
        
    mu += hmu
    
    mu += webReportSPQTIU(stationNo, hl7Config)

    userSiteDir = SITE_DIR_TEMPL.format(stationNo)
    print(f'Serializing ifcHL7Summary Report to {userSiteDir}')
    open(f'{userSiteDir}ifcHL7Summary.md', "w").write(mu) 
    
def webReportIFC123(stationNo, hl7MessageReduction, ifcConsultsByIEN, allToLocalServices, allToRemoteServices):

    # #################### 30 Last Days of 123 IFCs ################
    
    mu = f"""## IFC Consults (123)
   
In this system, successful HL7 is only logged for <span class="yellowIt">{hl7MessageReduction["normalMsgRetentionDays"]}</span> days. By contrast, logs of IFC consult activity - inside file 123 - are kept for years. The following shows Placed and Filled consults for the last 30 days of the system. These logs of __HL7-backed activity__ enable an __estimate of IFC HL7 traffic loads__.
    
"""
    thirtyDaysBackDate = datetime.strftime(datetime.strptime(hl7MessageReduction["lastDate"], "%Y-%m-%dT%H:%M:%S") - relativedelta(days=30), "%Y-%m-%dT%H:%M:%S")
    tiuNotesReferencedByRole = defaultdict(lambda: set())
    tiuNotesReferencedByService = defaultdict(lambda: set())
    cntServiceByRole = defaultdict(lambda: Counter())
    # WILL BE MISSING [1] ERROR and [2] where incomplete report message is replaced
    # by complete report
    cntServiceMessagesByRole = defaultdict(lambda: Counter())
    for consultIEN in ifcConsultsByIEN:
        consultInfo = ifcConsultsByIEN[consultIEN]
        if consultInfo["file_entry_date"]["value"] < thirtyDaysBackDate:
            continue
        if consultInfo["request_type"] != "C:Consult":
            continue
        # Need to re-examine ... seems like Placer HL7 above has wrong service name
        toServiceLabel = consultInfo["to_service"]["label"] if consultInfo["ifc_role"] == "F:FILLER" else consultInfo["ifc_remote_service_name"]
        cntServiceByRole[consultInfo["ifc_role"]][toServiceLabel] += 1
        # TODO: may change to NOT count PRINT etc.
        noBasicMsgs = len(consultInfo["request_processing_activity"])
        cntServiceMessagesByRole[consultInfo["ifc_role"]][toServiceLabel] += noBasicMsgs
        # REF is stored a remote VPTR text (must be used for the SPQ)
        if "remote_results" in consultInfo:
            if consultInfo["ifc_role"] == "F:FILLER":
                raise Exception("Only expect remote results for P:PLACER")
            for rr in consultInfo["remote_results"]:
                if "remote_associated_result" not in rr:
                    continue
                tiuNotesReferencedByService[
                toServiceLabel].add(rr["remote_associated_result"])
                tiuNotesReferencedByRole["P:PLACER"].add(rr["remote_associated_result"]) 
        elif "associated_results" in consultInfo:
            if consultInfo["ifc_role"] == "P:PLACER":
                raise Exception("Only expect associated results for F:FILLER")
            for ar in consultInfo["associated_results"]:
                tiuNotesReferencedByService[
                toServiceLabel].add(ar["associated_results"]["id"])
                tiuNotesReferencedByRole["F:FILLER"].add(ar["associated_results"]["id"]) 
    tbl = MarkdownTable([":Placed Service", "Count", "HL7 (ORM O01/+ACKs)", "TIU Notes (Remote)", "HL7 Example?"])
    for service in sorted(cntServiceByRole["P:PLACER"], key=lambda x: cntServiceByRole["P:PLACER"][x], reverse=True):
        tbl.addRow([
            "__{}__".format(service),
            f'{cntServiceByRole["P:PLACER"][service]:,}',
            f'{cntServiceMessagesByRole["P:PLACER"][service]:,}/{4 * cntServiceMessagesByRole["P:PLACER"][service]:,}',
            f'{len(tiuNotesReferencedByService[service]):,}' if service in tiuNotesReferencedByService else "&nbsp;",
            "YES" if service in allToLocalServices else ""
        ])
                
    placerTTL = sum(cntServiceByRole['P:PLACER'][s] for s in cntServiceByRole['P:PLACER'])
    placerHL7TTL = sum(cntServiceMessagesByRole['P:PLACER'][s] for s in cntServiceMessagesByRole['P:PLACER'])
    placerTTLWithHL7Ex = sum(cntServiceByRole['P:PLACER'][s] for s in cntServiceByRole['P:PLACER'] if s in allToLocalServices)    
    tiuNoteBlurb = f"These IFCs ended in <span class='yellowIt'>{len(tiuNotesReferencedByRole['P:PLACER']):,}</span> TIU Notes references (see SPQ note below)" if len(tiuNotesReferencedByRole['P:PLACER']) else "No TIU Notes were created in this Filler VistA by these IFCs"
    mu += f"<span class='yellowIt'>{placerTTL:,}</span> interfacility consults were placed in the last 30 days of this VistA which led to at least <span class='yellowIt'>{placerHL7TTL:,}</span> HL7 messages or <span class='yellowIt'>{placerHL7TTL*4:,}</span> including acknowledgements. <span class='yellowIt'>{reportPercent(placerTTLWithHL7Ex, placerTTL)}</span> are to services with complete HL7 examples in 772/3. {tiuNoteBlurb}.\n\n"
    mu += tbl.md() + "\n\n" 
    tbl = MarkdownTable([":Filled Service", "Count", "HL7 (ORM O01/+ACKs)", "TIU Notes (Local)", "HL7 Example?"])
    for service in sorted(cntServiceByRole["F:FILLER"], key=lambda x: cntServiceByRole["F:FILLER"][x], reverse=True):
        tbl.addRow([
            "__{}__".format(service),
            f'{cntServiceByRole["F:FILLER"][service]:,}',
            f'{cntServiceMessagesByRole["F:FILLER"][service]:,}/{4 * cntServiceMessagesByRole["F:FILLER"][service]:,}',
            f'{len(tiuNotesReferencedByService[service]):,}' if service in tiuNotesReferencedByService else "&nbsp;",
            "YES" if service in allToRemoteServices else ""
        ])
    fillerTTL = sum(cntServiceByRole['F:FILLER'][s] for s in cntServiceByRole['F:FILLER'])
    fillerHL7TTL = sum(cntServiceMessagesByRole['F:FILLER'][s] for s in cntServiceMessagesByRole['F:FILLER'])
    fillerTTLWithHL7Ex = sum(cntServiceByRole['F:FILLER'][s] for s in cntServiceByRole['F:FILLER'] if s in allToRemoteServices)
    tiuNoteBlurb = f"These IFCs ended in <span class='yellowIt'>{len(tiuNotesReferencedByRole['F:FILLER']):,}</span> TIU Notes, available for reading by remote Placer VistAs (see SPQ note below)" if len(tiuNotesReferencedByRole['F:FILLER']) else "No TIU Notes were created in this Filler VistA by these IFCs"
    mu += f"<span class='yellowIt'>{fillerTTL:,}</span> consults were filled in the last 30 days of this VistA that led to at least <span class='yellowIt'>{fillerHL7TTL:,}</span> HL7 messages or <span class='yellowIt'>{fillerHL7TTL*4:,}</span> including acknowledgements. <span class='yellowIt'>{reportPercent(fillerTTLWithHL7Ex, fillerTTL)}</span> are to services with complete HL7 examples in 772/3. {tiuNoteBlurb}. The \"Have HL7 Example\" column shows the services for which this VistA still holds HL7 messages.\n\n"
    mu += tbl.md() + "\n\n" 
        
    return mu

"""
Doesn't include the TIU Note HL7
"""
def webReportIFCHL7Basic(stationNo, hl7MessageReduction, ifcConsultsByIEN):

    # ################### HL7 Transactions ####################
    
    mu = f"""## Basic IFC HL7 (772/773)
    
VistA logs HL7 messages in files 772 and 773 and purges both regularly. In this VistA, successful messages are only kept for <span class="yellowIt">{hl7MessageReduction["normalMsgRetentionDays"]}</span> days. Despite the short duration, the remaining HL7 messages in a VistA in combination with equivalent logs from other VistAs permit a full description of the __form of IFC HL7__.
    
In the following HL7 log descriptions:
    
  * The service names of completed transactions are bolded. If the work "TEST" appears then one or other of the application fields of messages is GMRC IF TEST as opposed to GMRC IF CONSULT.
  * _P_ stands for Placer and means a HL7 message is sent by a Placer VistA; _F_ denotes sending by the Filler VistA.
  * A _Full Transaction_ is one with a non error Create Message. These represent a subset of transactions in the logs as non error messages are purged more frequently than error messages.
  * Most transactions don't reference TIU Notes (TIU Note column). Those that do always have the filler sending a reference to its note. Placer note sending is limited to TeleReader IFCs - VistA's TeleReader package has extra logic. One possible grouping for IFC types (services) is to split those that result in comments from those that end in notes. _TELEDERMATOLOGY_ ends in a note while _VIRS_ and other "administrative consults don't lead to notes. The extra HL7 needed for notes is described below.
  * 201 Errors are sent back by a filler (see HL7 Event Types that end in E201) if the patient referenced in a consult has not yet been added to a filler VistA. Until the patient is added, the placer resends the consult and the filler sends back an error. This intermediate _"error until registration"_ HL7 traffic is not captured in a consult's file 123 Activities and is only seen in the 772/773 logs.
  * The table highlights where a filler is in a different timezone from a placer, something handled in VistA and reflected in HL7 timestamps. For example, in VISN 20, Boise is in Mountain Time while Spokane is in Pacific time.
  * Consults assigned to more than one local service have numbers after their service names in the Service column. Service changes lead to _FORWARD:P_ (forward to placer) HL7 messages which tell the filler about the service change.
 
"""

    if hl7MessageReduction["skippedVDIF"] + hl7MessageReduction["skippedGMRCIFC1"]:
        mu += f"__Note__: <span class='yellowIt'>{hl7MessageReduction['skippedVDIF']:,}</span> messages to and from VDIF as opposed to an end system and <span class='yellowIt'>{hl7MessageReduction['skippedGMRCIFC1']:,}</span> on a link called _GMRC IFC1_ were not analyzed. These messages involve communication enabled by the temporary _HL7 Router_ setup between a partially migrated Spokane VistA and a reader VistA. Their patterns differ from typical VistA-VistA traffic. Should this setup or form persists in fully migrated VistAs then this report would be expanded to fully describe both individual messages and their patterns.\n\n"
    
    cntDelayed = 0 # MAY ADD!
    tbl = MarkdownTable([
        ":Local Service(s)", 
        ":123 Status",
        ":Filler [Time Zone]",
        # "First Message Time", nixed so room for status
        "Time Taken",
        "Text Lines [P/F]",
        "TIU Note [P/F]",
        ":773 Event Types",
        ":123 Activities"
    ])         
    allToLocalServices = set()
    cpids = sorted(hl7MessageReduction["fullTransactionsPlaced"], key=lambda x: hl7MessageReduction["fullTransactionsPlaced"][x][0]["created"])
    cpidToShow = ""
    miCount = Counter()
    for i, cpid in enumerate(cpids):
    
        messageInfos = hl7MessageReduction["fullTransactionsPlaced"][cpid]
        miCount[len(messageInfos)] += 1
        
        # Only reason why missing is if reach back/123 cache doesn't go back
        # enough.
        try:
            localConsult = ifcConsultsByIEN[cpid.split(":")[1]]
        except:
            raise Exception(f"Can't find consult of {cpid} - probably that the message trail started too far back at {messageInfos[0]['created']}")
        consultStatus = localConsult["cprs_status"]["label"]        
        if cpidToShow == "" and consultStatus == "COMPLETE":
            cpidToShow = cpid
        
        firstMessageTimeDT = datetime.strptime(messageInfos[0]["created"], "%Y-%m-%dT%H:%M:%S")
        lastMessageTimeDT = datetime.strptime(messageInfos[-1]["created"], "%Y-%m-%dT%H:%M:%S")
                
        messageCategories = [f'{mi["messageCategory"]}{":E" + mi["errorCode"] if "errorCode" in mi else ""}' for mi in messageInfos]
        messageStatesMU = f'__{len(messageInfos)}__: {"/ ".join(messageCategories)}'
        
        sendingDNS = messageInfos[0]["sendingFacility"]
        receivingDNS = messageInfos[0]["receivingFacility"]
        
        expected123Activities = [mi["expected123Activity"] for mi in messageInfos if "expected123Activity" in mi]
        
        # Ignoring toRemoteServices for now. Come into play in 123 with 
        # previous_remote_service_name in a FORWARDED FROM
        toLocalServices = []
        for mi in messageInfos:
            # This is the remote service name and may be wrong?
            if not (mi["transmissionType"] == "O" and "toService" in mi):
                continue
            if mi["toService"] in toLocalServices:
                continue
            toLocalServices.append(mi["toService"]) # get first time only
            allToLocalServices.add(mi["toService"])
        localServicesMU = toLocalServices[0]
        if len(toLocalServices) > 1:
            localServicesMU = "<br><br>".join([f'{tls} [{j}]' for j, tls in enumerate(toLocalServices, 1)])
        if sum(1 for ms in messageCategories if re.match(r'COMPL', ms)):
            localServicesMU = f'__{localServicesMU}__'
        # GMRC IF TEST
        if "isApplicationTest" in messageInfos[0]:
            localServicesMU += "<br><br>__TEST__"
            
        commentLinesSent = sum(mi["commentsCnt"] for mi in messageInfos if "commentsCnt" in mi and mi["transmissionType"] == "O")
        commentLinesReceived = sum(mi["commentsCnt"] for mi in messageInfos if "commentsCnt" in mi and mi["transmissionType"] == "I")
        
        hasLocalTIURef = True if sum(1 for mi in messageInfos if mi["transmissionType"] == "O" and "hasTIURef" in mi) else False
        hasRemoteTIURef = True if sum(1 for mi in messageInfos if mi["transmissionType"] == "I" and "hasTIURef" in mi) else False
        tiuRefMU = f'{"Y" if hasLocalTIURef else "N"}/{"Y" if hasRemoteTIURef else "N"}'
        if tiuRefMU == "N/N":
            tiuRefMU = "&nbsp;"

        remoteTZs = [mi["tz"] for mi in messageInfos if mi["transmissionType"] == "I" and "tz" in mi]
        remoteTZ = "" if len(remoteTZs) == 0 else remoteTZs[0]
            
        receivingDNSMU = receivingDNS.split("^")[1].split(".")[0] if len(receivingDNS.split("^")) > 1 else receivingDNS 
        row = [
            localServicesMU,
            consultStatus,
            f'{receivingDNSMU}{" [" + remoteTZ + "]" if remoteTZ else ""}',
            # firstMessageTimeDT.strftime("%m/%d %H:%M:%S"), nixed so room for status in pdf
            str(lastMessageTimeDT - firstMessageTimeDT),
            f'{commentLinesSent}/{commentLinesReceived}', 
            tiuRefMU,
            messageStatesMU,
            f'__{len(expected123Activities)}__: {"/ ".join(expected123Activities)}' # expect < message categories
        ]
        tbl.addRow(row)
        
    print(f'For Placer - message cnt: {miCount}')
   
    # TODO more -- how many deal with notes vs comments ie/ TIU or not! -- feeds into copy back [also pts to custom code ala teler somewhere?]
    messageInfosFullPlacedTransactions = [mi for pci in hl7MessageReduction["fullTransactionsPlaced"] for mi in hl7MessageReduction["fullTransactionsPlaced"][pci]]
    mu += f"""The following describes the <span class="yellowIt">{len(hl7MessageReduction["fullTransactionsPlaced"])}</span> full, placed transactions in the _HL7 MESSAGE ADMINISTRATION (773)_ file of this VistA. They involve <span class="yellowIt">{len(messageInfosFullPlacedTransactions)}</span> messages, <span class="yellowIt">{sum(1 for mi in messageInfosFullPlacedTransactions if "errorCode" in mi)}</span> of which contain at least one error reply. 
               
"""
    mu += tbl.md() + "\n\n"
    
    if cpidToShow:
        messageInfos = hl7MessageReduction["fullTransactionsPlaced"][cpidToShow]
        mu += "The following is a HL7 message example - the first (NEW) message of the first transaction listed above along with its aknowledgments, the simple ACK, the APP ACK and then an ACK for that APP ACK. Though de-identified, the message follows the same format used by VistA. For testing, messages like this - with dummied up data - could be generated based on the shape and form of consults stored in any production VistA ...\n\n"
        messageInfosAcked = [messageInfo for messageInfo in messageInfos if "acks" in messageInfo]
        mu += muMessageACKAPPACK(messageInfosAcked[0])
    
    # TODO: add one sample message transaction ie/ a simple one, no errors and
    # ACKs if present ... Display Full (use full md below which enumerates all!)
        
    cntDelayed = 0 # MAY ADD!
    tbl = MarkdownTable([
        ":Remote Service(s)", 
        "123 Status", 
        ":Placer [Time Zone]", # we know the filler
        # "First Message Time", leave out so room in PDF for status
        "Time Taken",
        "Text Lines [F/P]",
        "TIU Note [F/P]",
        ":773 Event Types",
        ":123 Activities"
    ])         
    cpids = sorted(hl7MessageReduction["fullTransactionsFilled"], key=lambda x: hl7MessageReduction["fullTransactionsFilled"][x][0]["created"])
    allToRemoteServices = set()
    cpidToShow = ""
    miCount = Counter()
    for i, cpid in enumerate(cpids):
            
        messageInfos = hl7MessageReduction["fullTransactionsFilled"][cpid]
        
        miCount[len(messageInfos)] += 1
            
        fillerConsultIds = set(mi["fillerConsultId"] for mi in messageInfos if "fillerConsultId" in mi)
        # TODO: problem again with single APP ACK .. is this really a single app ack?
        if len(fillerConsultIds) != 1:
            print(json.dumps(messageInfos, indent=4))
            print("** Expected all complete filled transactions to have one and only one filler consult id")
            continue
        fillerConsultId = list(fillerConsultIds)[0]
        try:
            localConsult = ifcConsultsByIEN[fillerConsultId.split(":")[1]]
        except:
            print(json.dumps(messageInfos, indent=4))
            raise Exception(f"Can't find consult of {fillerConsultId} - probably that the message trail started too far back at {messageInfos[0]['created']}")
        consultStatus = localConsult["cprs_status"]["label"]
        if cpidToShow == "" and consultStatus == "COMPLETE":
            cpidToShow = cpid
                
        firstMessageTimeDT = datetime.strptime(messageInfos[0]["created"], "%Y-%m-%dT%H:%M:%S")
        lastMessageTimeDT = datetime.strptime(messageInfos[-1]["created"], "%Y-%m-%dT%H:%M:%S")
                
        # Given our perspective (Local is filler), we're going to flip F and P
        # in the messageCategory
        for mi in messageInfos:
            if re.search(r'\:P', mi["messageCategory"]):
                mi["messageCategory"] = re.sub(r'\:P', ':F', mi["messageCategory"])
                continue
            mi["messageCategory"] = re.sub(r'\:F', ':P', mi["messageCategory"])            
        messageCategories = [f'{mi["messageCategory"]}{":E" + mi["errorCode"] if "errorCode" in mi else ""}' for mi in messageInfos]
        messageStatesMU = f'__{len(messageInfos)}__: {"/ ".join(messageCategories)}'
        
        sendingDNS = messageInfos[0]["sendingFacility"] # Remote/Placer
        receivingDNS = messageInfos[0]["receivingFacility"] # Local/Filler

        # Shouldn't be here - work out how to get in categorizer or disambig catag
        for mi in messageInfos:
            if "expected123Activity" not in mi:
                continue
            if re.search(r'\:P', mi["expected123Activity"]):
                mi["expected123Activity"] = re.sub(r'\:P', ':F', mi["expected123Activity"])
                continue
            mi["expected123Activity"] = re.sub(r'\:F', ':P', mi["expected123Activity"])                    
        expected123Activities = [mi["expected123Activity"] for mi in messageInfos if "expected123Activity" in mi]
        
        toRemoteServices = []
        for mi in messageInfos:
            if not (mi["transmissionType"] == "I" and "toService" in mi):
                continue
            if mi["toService"] in toRemoteServices:
                continue
            toRemoteServices.append(mi["toService"]) # get first time only
            allToRemoteServices.add(mi["toService"])
        if len(toRemoteServices) == 0:
            remoteServicesMU = ""
        else:
            if len(toRemoteServices) == 1:
                remoteServicesMU = toRemoteServices[0] 
            elif len(toRemoteServices) > 1:
                remoteServicesMU = "<br><br>".join([f'{tls} [{j}]' for j, tls in enumerate(toRemoteServices, 1)])
            if sum(1 for ms in messageCategories if re.match(r'COMPL', ms)):
                remoteServicesMU = f'__{remoteServicesMU}__'
            
        commentLinesSent = sum(mi["commentsCnt"] for mi in messageInfos if "commentsCnt" in mi and mi["transmissionType"] == "O")
        commentLinesReceived = sum(mi["commentsCnt"] for mi in messageInfos if "commentsCnt" in mi and mi["transmissionType"] == "I")

        hasRemoteTIURef = True if sum(1 for mi in messageInfos if mi["transmissionType"] == "I" and "hasTIURef" in mi) else False        
        hasLocalTIURef = True if sum(1 for mi in messageInfos if mi["transmissionType"] == "O" and "hasTIURef" in mi) else False
        tiuRefMU = f'{"Y" if hasLocalTIURef else "N"}/{"Y" if hasRemoteTIURef else "N"}'
        if tiuRefMU == "N/N":
            tiuRefMU = "&nbsp;"

        remoteTZs = [mi["tz"] for mi in messageInfos if mi["transmissionType"] == "I" and "tz" in mi]
        remoteTZ = "" if len(remoteTZs) == 0 else remoteTZs[0]
            
        row = [
            remoteServicesMU,
            consultStatus,
            f'{sendingDNS.split("^")[1].split(".")[0]}{" [" + remoteTZ + "]" if remoteTZ else ""}',
            # firstMessageTimeDT.strftime("%m/%d %H:%M:%S"), PDF room for status
            str(lastMessageTimeDT - firstMessageTimeDT),
            f'{commentLinesSent}/{commentLinesReceived}', 
            tiuRefMU,
            messageStatesMU,
            f'__{len(expected123Activities)}__: {"/ ".join(expected123Activities)}' # expect < message categories
        ]
        tbl.addRow(row)
        
    print(f'For Filler - message cnt: {miCount}')
   
    # TODO more -- how many deal with notes vs comments ie/ TIU or not! -- feeds into copy back [also pts to custom code ala teler somewhere?]
    messageInfosFullFilledTransactions = [mi for pci in hl7MessageReduction["fullTransactionsFilled"] for mi in hl7MessageReduction["fullTransactionsFilled"][pci]]
    
    mu += f"""The following describes the <span class="yellowIt">{len(hl7MessageReduction["fullTransactionsFilled"])}</span> full, filled transactions in _HL7 MESSAGE ADMINISTRATION (773)_ of this VistA. They involve <span class="yellowIt">{len(messageInfosFullFilledTransactions)}</span> messages, <span class="yellowIt">{sum(1 for mi in messageInfosFullFilledTransactions if "errorCode" in mi)}</span> of which contain at least one error reply. 

"""
    mu += tbl.md() + "\n\n"
    
    if cpidToShow:
        messageInfos = hl7MessageReduction["fullTransactionsFilled"][cpidToShow]
        mu += "The following is a HL7 message example - the last message of the first transaction listed above. For testing, messages like this - with dummied up data - could be generated based on the shape and form of consults stored in any production VistA ...\n\n"
        messageInfosAcked = [messageInfo for messageInfo in messageInfos if "acks" in messageInfo]
        mu += muMessageACKAPPACK(messageInfosAcked[-1])
    
    return mu, allToLocalServices, allToRemoteServices
    
"""
Follow on to Basic HL7 - after 123 is done

Note: dump of SPQs shows VIRS as local note type and various standard types from
nursing notes to ...
"""  
def webReportSPQTIU(stationNo, hl7Config):

    spqTIUGETReduction = reduceSPQTIUREAD(stationNo, hl7Config)
    overallStats = spqTIUGETReduction["overallStats"]
    outQualMU = f'<span class="yellowIt">{reportPercent(overallStats["spqsTIUGETOUT"], overallStats["spqsTIUGET"])}</span> of which are OUTGOING (from this VistA to another)' if overallStats["spqsTIUGETOUT"] < overallStats["spqsTIUGET"] else "all of which are OUTGOING (from this VistA to another)"
    spqCount = overallStats["spqSuccessCount"] + overallStats["spqOtherCount"] + overallStats["spqErrorCount"]
        
    mu = f"""## IFC TIU Note HL7 (772/773)
    
When a completed IFC results in a TIU Note, a reference to that note instead of the note itself is sent back from the Filler VistA to a Placer VistA. This forces a doctor at the placer site to use a CPRS menu option to query the note from the Filler VistA. Every time they want to see that note, their VistA must retrieve it using a HL7 SPQ query containing the id of the note in Filler VistA.

In this system's 773 file, there are <span class='yellowIt'>{spqCount:,}</span> SPQ HL7 messages. Only <span class='yellowIt'>{reportAbsAndPercent(overallStats["spqsTIUGET"], spqCount)}</span> were for retrieving TIU Notes, {outQualMU}. 

Of note:
  * the SPQ embeds a VistA Remote Procedure Call (RPC). The identity of the doctor is sent in the SPQ too and, if not present already, the SPQ will cause the doctor to be added as a _visitor user_ in the Filler VistA. __This communication has the weakest NIST Level of security Assurance (LOA), level 1__.
  * the SPQ leads to an _immediate response_ meaning the token in the QAK segment which is used to fetch or understand a delayed response doesn't matter
  * unlike the _ORM^O01_ traffic for IFCs themselves, neither SPQs nor the TBR messages that acknowledge/respond to them lead to simple HL7 acknowledgements.  
  * the TIU Note is never cached by the Placer VistA 
  * the body of the note - from the Filler VistA's 8925 file - is serialized in RDT segments of the TBR response returned to the Placer.
  
"""
    
    spqTIUGETsByTIUIEN = spqTIUGETReduction["spqTIUGETsByTIUIEN"]
    ackedSuccesses = [tiuIEN for tiuIEN in spqTIUGETsByTIUIEN if "acks" in spqTIUGETsByTIUIEN[tiuIEN][-1] and spqTIUGETsByTIUIEN[tiuIEN][-1]["status"] != "ERROR"]
    ackedSuccessesLatest = ackedSuccesses[-1]
    
    sqlTIUGET = spqTIUGETsByTIUIEN[ackedSuccessesLatest][-1] # can have > 1 for TIU!
    sqlTIUGET["messageCategory"] = "SPQ For TIU Note"
    mu += "The following de-identified message shows a typical SPQ Query and the TBR response it leads to.\n\n"
    mu += muMessageAPPACK(sqlTIUGET)
    
    """
    # TO DUMP ALL SPQs
    for ass in ackedSuccesses:
        for sqltiuget in spqTIUGETsByTIUIEN[ass]:
            sqltiuget["messageCategory"] = "BLAH"
            print(muMessageAPPACK(sqltiuget, False))
    """
    
    return mu

"""
A complete dump of HL7 messages for each of the transactions recorded in 773. This is largely used to make the "message description section" of the summary above and to QA the extractions used to produce the summary above. ie/ NOT for wider consumption.

TODO: fix the F: for FILLER dump -- need to put F/P back to I/O for consistency
"""
def webReportHL7IFCFull(hl7MessageReduction, ifcConsultsByIEN, deidentify=True):
    
    stationNo = hl7MessageReduction["stationNo"]

    meta = metaOfVistA(stationNo)    

    mu = TOP_MD_TEMPL.format("{} IFC HL7".format(stationNo))
        
    def muMessageNTitle(messageInfo, i):
        messageTopParams = []
        if "errorCode" in messageInfo:
            messageTopParams.append("ERROR")
        if "priority" in messageInfo and messageInfo["priority"] != "IMMEDIATE":
            messageTopParams.append(messageInfo["priority"]) # DEFERRED
        if len(messageTopParams):
            messageTopParamsMU = " [{}]".format("/".join(messageTopParams))
        else:
            messageTopParamsMU = ""
        mu = f'__{i}. {"OUT" if messageInfo["transmissionType"] == "O" else "IN"}{messageTopParamsMU}__\n\n'
        return mu
        
    def muConsultContents(consult): # just its activity for now
        activities = []
        # date_time_of_actual_activity - date_time_of_action_entry
        for entry in consult["request_processing_activity"]:
            activity = entry["activity"]["label"]
            activities.append(re.sub(r'\/', ' ', activity))
        activitiesMU = "/".join(activities)
        return f'__Consult (123) Activities [{len(activities)}]__: {activitiesMU}'
    
    mu += f"## Placed Consults [{len(hl7MessageReduction['fullTransactionsPlaced'])}]\n\n"
    cpids = sorted(hl7MessageReduction["fullTransactionsPlaced"], key=lambda x: hl7MessageReduction["fullTransactionsPlaced"][x][0]["created"])
    for i, cpid in enumerate(cpids):
        messageInfos = hl7MessageReduction["fullTransactionsPlaced"][cpid]
        mu += f"### Placed Consult {cpid.split(':')[1]}\n\n"
        consult = ifcConsultsByIEN[cpid.split(":")[1]]
        mu += muConsultContents(consult) + "\n\n"
        for i, messageInfo in enumerate(messageInfos, 1):
            mu += muMessageNTitle(messageInfo, i)
            mu += muMessageACKAPPACK(messageInfo, deidentify)    

    mu += f"## Filled Consults [{len(hl7MessageReduction['fullTransactionsFilled'])}]\n\n"
    cpids = sorted(hl7MessageReduction["fullTransactionsFilled"], key=lambda x: hl7MessageReduction["fullTransactionsFilled"][x][0]["created"])
    for i, cpid in enumerate(cpids):
        messageInfos = hl7MessageReduction["fullTransactionsFilled"][cpid]
        mu += f"### Filled Consult {cpid.split(':')[1]}\n\n"
        # mu += muConsultContents(consult) + "\n\n" - can't do til got local cpid for filled (see in summary)
        for i, messageInfo in enumerate(messageInfos, 1):
            mu += muMessageNTitle(messageInfo, i)
            mu += muMessageACKAPPACK(messageInfo, deidentify)    
             
    userSiteDir = SITE_DIR_TEMPL.format(stationNo)
    print(f'Serializing ifcHL7Full Report to {userSiteDir}')
    open(f'{userSiteDir}ifcHL7Full.md', "w").write(mu) 
    
# ############ Organize and QA all the 772/773/relevant 123/HL7 Config ################

"""
[1] gather raw information and [2] QA relationships, logic (like purging) and categorize for presentation.

Note that VistA's 773/772 shows both its logic and what it parses. We also reparse in
RPC utilities.

687:
====
Reduced 1470 (773 indexed) messages to 170 consults, skipping 1 ACKs. Only 27 ha
ve a non error NEW (ie/ are full transactions we can follow), 19 placed by this
VistA, 8 filled. The first HL7 773 date is 2020-02-20T00:04:19, last is 2020-03-
25T09:01:15, first non error 2020-03-23T09:22:14
"""
def reduceIFCHL7ToConsults(stationNo, ifcHL7Consults, hl7Config): # side effect nix consults w/o + make sure all in window have messages
      
    def align773WithAppAck(entryAckedTo, appAckErrorCode="", fillerConsultId="", rejectingAppAck=False):
        
        if appAckErrorCode:
            # TODO: come back (seems that some (or all)) I's error ACKed by local
            # VistA don't have ERROR as their status but all ACKed as error by
            # remote end get that status [VISTA HL7 PARSE QUIRK?]
            if entryAckedTo["transmissionType"] == "O" and entryAckedTo["status"] != "ERROR":
                print(json.dumps(entryAckedTo, indent=4)) 
                raise Exception(f"Original 773 must be wrong - as has non error status - {entryAckedTo['status']} but APP ACK has error {appAckErrorCode}")
            if entryAckedTo["transmissionType"] == "I":
                if entryAckedTo["status"] == "ERROR":
                    raise Exception("Expect VistA Quirk that I messages ACKed as error by this VistA aren't marked as ERROR status - because 123 activity?")
                entryAckedTo["status"] = "ERROR" # override
            if "errorCode" not in entryAckedTo:
                entryAckedTo["errorCode"] = extracts["errorCode"]
            elif entryAckedTo["errorCode"] != extracts["errorCode"]:
                raise Exception("Expected parsed from message APP ACK error code to equal 773 error code when there")
            # del activity 123 as APP ACK ERROR => won't be recorded/deleted
            if "expected123Activity" in entryAckedTo: 
                del entryAckedTo["expected123Activity"] 
            return
            
        if rejectingAppAck:
            entryAckedTo["status"] = "ERROR" 
            return 
            
        # Not error
        # won't have error set in _773 if not ERROR (checked above)
        if entryAckedTo["status"] == "ERROR": 
            raise Exception("Don't expect ERROR status if no APP ACK error")
        if fillerConsultId:
            entryAckedTo["fillerConsultId"] = f'{fillerConsultId.split("^")[1]}:{fillerConsultId.split("^")[0]}'
      
    """  
    # Make sure error NEWs only follow other error NEWs and only one non error NEW
    # ... bonus id an entry as a non error NEW
    
    692 introduced situation of APP ACKed (error) an entry and another entry was
    already after it with just a plain ACK. ie/ resend happening before APP ACK even
    in. Hence search backwards in list
    """
    def postAppAckQANew(entry):
        if entry["messageCategory"].split(":")[0] != "NEW":
            return
        allConsultEntries = messagesByPlacerConsultId[entry["placerConsultId"]]
        idx = -1
        for i, ace in enumerate(allConsultEntries):
            if ace["id"] == entry["id"]:
                idx = i
                break
        if idx == -1:
            print(entry["messageId"])
            print(json.dumps(allConsultEntries, indent=4))
            raise Exception("Can't find entry in consult's list") # never happen
        if idx == 0: # none before
            return 
        oneBackEntry = allConsultEntries[idx - 1] # assuming back was app acked
        if oneBackEntry["messageCategory"].split(":")[0] != "NEW":
            print(json.dumps(allConsultEntries, indent=4))
            raise Exception("Trying to add a NEW after a non NEW")
        # Reason for OR: if ACKs lost to clean up then one back may not have em and so
        # may not have an error code (sometimes only set here). Relying on ERROR being
        # state in this case (it would be the only reason a message lingers!) [692]
        if not ("errorCode" in oneBackEntry or oneBackEntry["status"] == "ERROR"):
            print("** Warning: Trying to add a NEW after a non errored NEW - only one non errored NEW allowed - not stopping but check") # TODO: fix - hand to loosen for 663
            # print(json.dumps(oneBackEntry, indent=4))
            # print(json.dumps(entry, indent=4))
        
    gmrcHL7 = ifcHL7Consults["hl7"] # by 773 IEN 
    ifcConsultsByIEN = ifcHL7Consults["ifcConsults"]

    vistaListenerLL = hl7Config["hlo_standard_listener"]["label"] # ex/ VAWWW
    normalMsgRetentionDays = int(hl7Config["normal_msg_retention_days"])

    messagesByPlacerConsultId = defaultdict(list)    
    allDTs = [] # for time QA ie/ last one <=> cutDateTime
    skippedAcksAsNoAckTo = []
    skippedAcksAsAckToSelf = []
    skippedGMRCIFC1 = set() # special 663 - some test LL messes up TODO
    skippedVDIF = 0 # CRNRHL7SPECIAL
    skippedTSTPlacer = set() # saw in Alaska; TST placer consult id
    entriesByMessageId = {} # for ACK mapping
    for _773IEN in gmrcHL7:
            
        _77sEntry = gmrcHL7[_773IEN]        
        entry = makeBasicHL7Event(_77sEntry, "GMRC IFC SUBSC")
        _773Entry = _77sEntry["_773"]
        _772Entry = _77sEntry["_772"]
        
        # Can put reduction in with them here (ie/ not in the .md pass!)
        messageCategory, expected123Activity, extracts = categorizeAndParseIFCHL7Message(entry["message"], entry["transmissionType"], True)

        # messageId == {stationNo}{_773IEN}
        entry["messageId"] = extracts["messageId"]
        entriesByMessageId[entry["messageId"]] = entry # acks to as can ack to ack
        entry["messageCategory"] = messageCategory
        if "tiuRef" in extracts:
            entry["hasTIURef"] = True
        if "comments" in extracts:
            entry["commentsCnt"] = len(extracts["comments"])
        if "tz" in extracts:
            entry["tz"] = extracts["tz"]
        if "sendingFacility" in extracts: # VistA {SNO}^{NAME}.MED.VA.GOV but VDIF for Cerner
            entry["sendingFacility"] = extracts["sendingFacility"]
        if "receivingFacility" in extracts: # plain {SNO} from VistA but {SNO}^^DNS cerner
            entry["receivingFacility"] = extracts["receivingFacility"]
        if "security" in extracts: # VDIF/CRNR has CRNR for incoming (blank vista-vista)
            entry["security"] = extracts["security"]
        if "acceptAcknowledgementType" in extracts:
            entry["acceptAcknowledgementType"] = extracts["acceptAcknowledgementType"]
        if "applicationAcknowledgementType" in extracts:
            entry["applicationAcknowledgementType"] = extracts["applicationAcknowledgementType"]
           
        # Skipping send and receive via vdif for now
        # CRNRHL7SPECIAL
        if ("sendingFacility" in entry and re.search(r'vdif', entry["sendingFacility"])) or ("receivingFacility" in entry and re.search(r'vdif', entry["receivingFacility"])):
            skippedVDIF += 1
            del entriesByMessageId[entry["messageId"]]
            continue
            
        # HL7 Router 668
        # CRNRHL7SPECIAL            
        if entry["logicalLink"] == "GMRC IFC1":
            skippedGMRCIFC1.add(entry["messageId"])
            del entriesByMessageId[entry["messageId"]]
            continue
            
        # See ex 463:TST1234 ... error handling etc is special - just exclude
        if "placerConsultId" in extracts and re.match(r'TST', extracts["placerConsultId"].split("^")[0]):
            skippedTSTPlacer.add(entry["messageId"])
            del entriesByMessageId[entry["messageId"]]
            continue                       
        
        # GMRC IF TEST variation of application
        for p in ["sendingApplication", "receivingApplication"]:
            if p in extracts and re.search(r'TEST', extracts[p]):
                entry["isApplicationTest"] = True
       
        allDTs.append(entry["created"]) # last at end <=> cut date time (for purge)
                
        """
        ACK (simple) can ACK an APP ACK or main msg
        ... ACK to APP ACK as latter if AL|NE
        ACK APP is only for the main message and is either only ack (NE|AL) or second
        ack (AL|AL) 
        
        Usual full ACK flow (from Placer to Filler - flip for other way)
        MSG ---------- LLP -------->
            <--------- LLP --------- ACK
            <--------- LLF --------- APP ACK
        ACK ---------- LLF --------> 
        
        UNLESS have NE|AL (saw in 757) ie/ APP ACK only
        
        ie/ simple ACK back on same link even it labeled a 'listener' 
        ... above: LLP == VAPUG, LLF == VAWWW
        ... and LL's reflected in Message headers?
        """
        if re.match(r'ACK', messageCategory):            
        
            entry["ackTo"] = extracts["ackTo"]
            
            if entry["ackTo"] not in entriesByMessageId:
                skippedAcksAsNoAckTo.append(entry)
                continue
            
            entryAckedTo = entriesByMessageId[entry["ackTo"]]
                
            """
            # Special 663 - GMRC IFC1 has acks to selves and then logic
            # CRNRHL7SPECIAL part - needs more work
            if entry["logicalLink"] == "GMRC IFC1":
                del entriesByMessageId[entry["ackTo"]]
                skippedGMRCIFC1.add(entry["ackTo"])
                if entry["messageId"] in entriesByMessageId:    
                    del entriesByMessageId[entry["messageId"]]
                skippedGMRCIFC1.add(entry["messageId"])
                continue  
            """              
        
            # Consistency with ack types in the request if set
            if "acceptAcknowledgementType" in entryAckedTo and "applicationAcknowledgementType" in entryAckedTo:
                if re.match(r'ACK APP', entry["messageCategory"]):
                    if entryAckedTo["applicationAcknowledgementType"] != "AL":
                        print(json.dumps(entryAckedTo, indent=4))
                        print(json.dumps(entry, indent=4))
                        raise Exception("APP ACK but Request didn't have AL for APP ACK")
                else:
                    if entryAckedTo["acceptAcknowledgementType"] != "AL":
                        print(json.dumps(entryAckedTo, indent=4))
                        print(json.dumps(entry, indent=4))
                        raise Exception("ACK but Request didn't have AL for ACK")
        
            # ACK before
            # - can't be simple ACK
            # - if app ack, existing -1 ack can't be app ack
            # - must be on own link
            if "acks" in entryAckedTo:
            
                if not re.match(r'ACK APP', entry["messageCategory"]):
                    raise Exception("Second ACK must be app ack")
                                
                if re.match(r'ACK APP', entryAckedTo["acks"][-1]["messageCategory"]):
                    raise Exception("Last Ack in Acks was APP ACK already - can't have two")
            
                if entry["logicalLink"] == entryAckedTo["logicalLink"]:
                    raise Exception("Expected app ack after ack to go back on a different link as the message being app acknowledged")
                
                # whether error missing in _773 or not, will fill in from APP ACK
                # and QA'ing our parse with _773 VistA Parse
                # ... saw REJECT in 757
                align773WithAppAck(entryAckedTo, extracts.get("errorCode", ""), extracts.get("fillerConsultId", ""), True if re.search(r'REJECT', entry["messageCategory"]) else False)
                
                postAppAckQANew(entryAckedTo)

                entryAckedTo["acks"].append(entry) 
                
            else:
            
                # for 663, turning off for GMRC IFC1 - think it's because ACK missed
                # as refers to itself
                if entry["logicalLink"] != entryAckedTo["logicalLink"]:
                    print(entryAckedTo["logicalLink"] == "GMRC IFC1")
                    print("Should be gone", entryAckedTo["messageId"] in skippedGMRCIFC1)
                    print(entry["messageId"], entryAckedTo["messageId"])
                    print(entry["logicalLink"], entryAckedTo["logicalLink"])
                    print(json.dumps(entryAckedTo, indent=4))
                    print(json.dumps(entry, indent=4))
                    raise Exception("Expected first ack to go back on same link as the message being acknowledged")                    
    
                # 757 saw no ACK (NE|AL)
                if re.match(r'ACK APP', entry["messageCategory"]):
                    align773WithAppAck(entryAckedTo, extracts.get("errorCode", ""), extracts.get("fillerConsultId", ""), True if re.search(r'REJECT', entry["messageCategory"]) else False)                 

                # Also in 663, saw come in on novel LL, IFC1
                if entry == entryAckedTo: # only 663 - skipping (should revisit: cerner?)
                    print(json.dumps(entry, indent=4))
                    print("** Warning: entry marked to ACK itself ie/ ACK to itself - skipping")
                else:
                    entryAckedTo["acks"] = [entry]      
                
            continue
                    
        """
        # GMRC IFC1 messes up logic so just skipping
        if entry["logicalLink"] == "GMRC IFC1":
            if entry["messageId"] in entriesByMessageId:    
                del entriesByMessageId[entry["messageId"]]
            skippedGMRCIFC1.add(entry["messageId"])
            continue
        """
                    
        # beyond 773/772 ie/ what VistA's parsers produce
        if "placerConsultId" not in extracts: 
            raise Exception("Expected all but ACKs to have placer consult id from ORC") 
        # Matches unique_consult_id_ in 123 as {originatingStationNo}_{originating123IEN}
        # ... always placer consult id and this VistA could be filler role or placer role
        entry["placerConsultId"] = f'{extracts["placerConsultId"].split("^")[1]}:{extracts["placerConsultId"].split("^")[0]}'
        if "fillerConsultId" in extracts: # only after first proper APP ACK! Full with have em
            entry["fillerConsultId"] = f'{extracts["fillerConsultId"].split("^")[1]}:{extracts["fillerConsultId"].split("^")[0]}'
        if "toService" in extracts:
            entry["toService"] = extracts["toService"] 
        
        # Putting in for all - will del above if APP ACK is an error
        entry["expected123Activity"] = expected123Activity
            
        # QA LL for OUT and IN
        if entry["transmissionType"] == "O" and entry["logicalLink"] == vistaListenerLL:
            raise Exception("Expect O NOT to be on the VistA Listener Link")
        if entry["transmissionType"] == "I" and entry["logicalLink"] != vistaListenerLL:
            raise Exception("Expect I to be on the VistA listener Link")
                            
        # REM: No ACKs as those up top - embedded within entries
        messagesByPlacerConsultId[entry["placerConsultId"]].append(entry)
                
    # TODO: was bigger before - now make AL|NE etc followed 
    def isEntryAcked(entry):
        if "acks" not in entry:
            return False
        return True
    allEntries = [entry for pcId in messagesByPlacerConsultId for entry in messagesByPlacerConsultId[pcId]]
    # REM: can have purged acks - should only happen for errored entries
    entriesWOAcks = [entry for entry in allEntries if not isEntryAcked(entry)]
    entriesWOAcksNoErrors = [entry for entry in entriesWOAcks if entry["status"] != "ERROR"]
    if len(entriesWOAcksNoErrors):
        for entry in entriesWOAcksNoErrors:
            print(json.dumps(entry, indent=4))
        raise Exception("Entry lacks ACKs but is not a (lingering) error")
    # Assume if first NEW has acks then subsequent ones will too
    fullTransactionPCIds = set(pcId for pcId in messagesByPlacerConsultId if sum(1 for entry in messagesByPlacerConsultId[pcId] if isEntryAcked(entry) and entry["messageCategory"].split(":")[0] == "NEW" and entry["status"] != "ERROR"))
    fullTransactionPlacedPCIds = set(pcId for pcId in fullTransactionPCIds if re.match(stationNo, pcId))
    placedPCIdsSuppressedAsNoConsult = 0
    for pcId in list(fullTransactionPlacedPCIds):
        if pcId.split(":")[1] not in ifcConsultsByIEN:
            placedPCIdsSuppressedAsNoConsult += 1
            fullTransactionPlacedPCIds.remove(pcId)
    fullTransactionFilledPCIds = set(pcId for pcId in fullTransactionPCIds if not re.match(stationNo, pcId))
    # Extra check - if no fillerId known then shouldn't be in index of filled ie
    # no app ack with it sent so why in index of filled?
    filledPCIdsSuppressedAsNoFillerId = 0
    filledPCIdsSuppressedAsNoFillerIdFromVDIF = 0
    for pcId in list(fullTransactionFilledPCIds):
        fillerConsultIds = set(mi["fillerConsultId"] for mi in messagesByPlacerConsultId[pcId] if "fillerConsultId" in mi) # means APP ACK
        if len(fillerConsultIds) != 1: # ie/ none
            # linkIn GMRC IFC1: security is CRNR: recieving {SNO}^^DNS and not just {SNO}
            if re.search(r'vdif', messagesByPlacerConsultId[pcId][0]["sendingFacility"]):
                filledPCIdsSuppressedAsNoFillerIdFromVDIF += 1    
            elif not re.search(r'TST', messagesByPlacerConsultId[pcId][0]["placerConsultId"]):
                print(json.dumps(messagesByPlacerConsultId[pcId], indent=4))
                raise Exception(f"Expect filler ids for all incoming requests unless they are marked TST (757 only) - {pcId} - {fillerConsultIds}")
            filledPCIdsSuppressedAsNoFillerId += 1
            fullTransactionFilledPCIds.remove(pcId) # DELETE for now
        # Part of EVOLVING CERNER (see explanation up top)
        # ... if VDIF => no filler consult id expected for any (ie/ APP ACK sent)
        elif re.search(r'vdif', messagesByPlacerConsultId[pcId][0]["sendingFacility"]):
            raise Exception("Don't expect VDIF to work yet - nixing")
            
    """
    NORMALLY:
    - filler in ORC ACK ie/ app ack back out from PUG after ACK
    - linkIn is SPO
    """
                               
    # QA Time for events - first date for fully ACKed, non error ie/ full entry due
    # for purging 
    nonErrorNonACKDTs = [entry["created"] for entry in allEntries if isEntryAcked(entry) and entry["status"] != "ERROR"]
    firstNEDT = datetime.strptime(sorted(nonErrorNonACKDTs)[0], "%Y-%m-%dT%H:%M:%S")
    # <=> cut date
    lastEventDT = datetime.strptime(sorted(allDTs)[-1], "%Y-%m-%dT%H:%M:%S")
    # downgraded to warning in 692. Config says three days but seems to have 7+!
    if lastEventDT - firstNEDT > timedelta(days=normalMsgRetentionDays):
        print(f"** WARNING: Purge Date not applied: {sorted(nonErrorNonACKDTs)[0]} - {sorted(allDTs)[-1]} - {lastEventDT - firstNEDT}")
        
    # QA all consults in purge window HAVE TRANSACTIONs with NEW! (actually more may 
    # if errors start em off) ie/ not missing expected transactions.
    # ... rem: unique_consult_id_ in 123 is {originatingStationNo}_{originating123IEN}
    # and that's also the placer consult id used here.
    consultsExpectedToHaveTrans = [consultIEN for consultIEN in ifcConsultsByIEN if ifcConsultsByIEN[consultIEN]["file_entry_date"]["value"] >= sorted(nonErrorNonACKDTs)[0]]
    unexpectedMissing = set()
    discontinuedPendingConsultsNoMessages = 0
    vdifHL7RouterConsultsNoMessages = 0
    for consultIEN in consultsExpectedToHaveTrans:
        uniqueConsultId = re.sub(r'_', ":", ifcConsultsByIEN[consultIEN]["unique_consult_id_"])
        if uniqueConsultId in fullTransactionPCIds:
            continue
        # As suppressed VDIF and HL7 Router - can end up with these
        if uniqueConsultId not in messagesByPlacerConsultId:
            if ifcConsultsByIEN[consultIEN]["routing_facility"]["id"].split("-")[1] == "668":
                vdifHL7RouterConsultsNoMessages += 1
            elif ifcConsultsByIEN[consultIEN]["cprs_status"]["label"] not in ["PENDING", "DISCONTINUED"]:
                print(json.dumps(ifcConsultsByIEN[consultIEN], indent=4))
                raise Exception("Consult expected by date to have transactions/messages but none known and NOT DISCONTINUED or PENDING")
            else:
                discontinuedPendingConsultsNoMessages += 0 # 757 only
                print("** Warning: discontinued/pending consult has no 'messagesByPlacerConsultId' entry. Ok?")
        elif messagesByPlacerConsultId[uniqueConsultId][-1]["status"] != "ERROR":
            
            print(json.dumps(messagesByPlacerConsultId[uniqueConsultId], indent=4))
            raise Exception("Expect Consult w/o complete transaction to only have errors")
    
    print(f'Reduced {len(gmrcHL7)} (773 indexed) messages to {len(messagesByPlacerConsultId)} consults, skipping {len(skippedAcksAsNoAckTo)} ACKs, {discontinuedPendingConsultsNoMessages:,} discontinued/pending consults have no messages. {filledPCIdsSuppressedAsNoFillerId:,} incoming requests (fullfilled) suppressed as no fillerConsultId; {placedPCIdsSuppressedAsNoConsult:,} placed ids removed as no matching consult record. Only {len(fullTransactionPCIds)} have a non error NEW (ie/ are full transactions we can follow), {len(fullTransactionPlacedPCIds)} placed by this VistA, {len(fullTransactionFilledPCIds)} filled. The first HL7 773 date is {allDTs[0]}, last is {allDTs[-1]}, first non error {nonErrorNonACKDTs[0]}. CRNRHL7SPECIAL removals are {skippedVDIF} vdif and {len(skippedGMRCIFC1)} GMRC IFC link; skipped TST placers {len(skippedTSTPlacer)}')
            
    ifcHL7MessageReduction = {
    
        "stationNo": stationNo,
        
        "totalMessagesAvailable": len(gmrcHL7),
        # ie/ not removed as not in purge window but prior message removed (rare)
        "skippedAcksAsNoAckTo": len(skippedAcksAsNoAckTo), 
        "nonAckMessagesMatchedToConsults": len(allEntries),
        
        "skippedVDIF": skippedVDIF,
        "skippedGMRCIFC1": len(skippedGMRCIFC1),
        "skippedTSTPlacer": len(skippedTSTPlacer),
        
        "firstDate": allDTs[0],
        "lastDate": allDTs[-1],
        "firstNENADate": nonErrorNonACKDTs[0],
        "normalMsgRetentionDays": normalMsgRetentionDays,
                
        "fullTransactionsPlaced": dict((pcId, messagesByPlacerConsultId[pcId]) for pcId in fullTransactionPlacedPCIds),
        # Filled locally - by placer (ie/ remote consult id) ie/ one in NEW IN
        "fullTransactionsFilled": dict((pcId, messagesByPlacerConsultId[pcId]) for pcId in fullTransactionFilledPCIds),
        # the non error NEW gone - may only be errors or could have some non errors
        "incompleteTransactions": dict((pcId, messagesByPlacerConsultId[pcId]) for pcId in messagesByPlacerConsultId if pcId not in fullTransactionPCIds)

    }
    
    return ifcHL7MessageReduction
    
"""
SPQ - just TIU GET
"""
def reduceSPQTIUREAD(stationNo, hl7Config):
    
    spqTBRHL7ReductionInfo = reduceSPQTBRHL7(stationNo)
    overallStats = spqTBRHL7ReductionInfo["overallStats"]
    spqTBRHL7Reduction = spqTBRHL7ReductionInfo["spqEventsByRPCName"]
    
    if "TIU GET RECORD TEXT" not in spqTBRHL7Reduction:
        raise Exception("Unexpected lack of TIU GET RECORD TEXT in spqTBRHL7Reduction")
        
    # Extract the subset of SPQ TIU and index by TIU trying to retrieve
    spqTIUGETsByTIUIEN = defaultdict(list) # could ask and reask
    skipped = 0
    for event in spqTBRHL7Reduction["TIU GET RECORD TEXT"]:
        sprSeg = event["sprSeg"]
        if "priority" in event and event["priority"] != "IMMEDIATE":
            print(json.dumps(event, indent=4))
            raise Exception("Expected TIU GETs to be immediate priority (ie/ token means nothing")
        # saw a \n intervene in 692 and had to nix 
        tiuIENSearch = re.search(r'P1(\d{3})(\d+)$', re.sub(r'\n', '', sprSeg["inputParameterList"]))
        if tiuIENSearch:
            tiuIEN = re.search(r'P1(\d{3})(\d+)$', re.sub(r'\n', '', sprSeg["inputParameterList"])).group(2)
        else:
            print(f'** Warning: skipping spqTBR as P1 TIU not of \"right\" form - {sprSeg["inputParameterList"]}')
            skipped += 1
            continue # TODO: return and fix
        spqTIUGETsByTIUIEN[tiuIEN].append(event)
        # link and logical link local
        if event["transmissionType"] == "I":             
            # Lazy -- TODO: see mand, opt of  both
            link = event["link"] if "link" in event else event["logicalLink"]
            if event["logicalLink"] != hl7Config["hlo_standard_listener"]["label"]: # ex/ VAWWW
                raise Exception("SPQ I expects standard listener")
            
    overallStats["spqsTIUGET"] = len(spqTBRHL7Reduction["TIU GET RECORD TEXT"])
    overallStats["spqsTIUGETOUT"] = sum(1 for event in spqTBRHL7Reduction["TIU GET RECORD TEXT"] if event["transmissionType"] == "O") # vs IN, incoming
    overallStats["spqsTIUGETAcked"] = sum(1 for event in spqTBRHL7Reduction["TIU GET RECORD TEXT"] if "acks" in event)
    overallStats["spqsTIUGetSkipped"] = skipped
    noAckSPQTIUEvents = [event for event in spqTBRHL7Reduction["TIU GET RECORD TEXT"] if "acks" not in event]
    # Only excuse no app ack TBR == immediate document if ack must have been signaling
    # error but as it itself is not in error, it was purged before its errored cause
    if sum(1 for event in noAckSPQTIUEvents if event["status"] != "ERROR"):
        raise Exception("No ACK and not an Error!") 
    overallStats["spqsTIUGETNotAcked"] = len(noAckSPQTIUEvents)
    print(f'Total TIU Gets {overallStats["spqsTIUGET"]}')
    print(f'TIU GET has {overallStats["spqsTIUGETAcked"]} TBR to SPQ matches')
    print(f'TIU GET has {overallStats["spqsTIUGETNotAcked"]} unapp ack TBR SPQs - all in error so linger beyond their app ack')
        
    print("Serializing TMP Cache of TIUs to spqTIUGetById")
    spqTIUGETReduction = {
        "stationNo": stationNo,
        "description": "SPQs for TIUs - out and in - with matched TBR if any. Stats on SPQs in general given context.",
        "overallStats": overallStats,
        "spqTIUGETsByTIUIEN": spqTIUGETsByTIUIEN # not by _773 but by TIU IEN
    }
    
    return spqTIUGETReduction

"""
Gather all raw data for IFC HL7 together including a window of 123's so can match
and the overall HL7 config file    
- HL7 MESSAGE ADMINISTRATION (773) referencing HL7 MESSAGE TEXT (772)
- 123 Consults
"""  
def gatherRawIFCHL7NConsults(stationNo, hloSystemParameters):
    
    def ifc123InTimeWindow(stationNo, firstHL7Date, normalMsgRetentionDays): # ex/ 2020-02-20T02:04:20

        # Assuming if go back 30 times retension time then consult of any
        # retained message will be known
        # ... 10 was ok for WWW but WCI seems to be 8 days though it says its
        # 3 (see consideration for redoing gap based on actual data)
        # ... also 692 showed a long run consult going way back
        goBackDays = 30 * normalMsgRetentionDays

        ifcConsultsInTimeWindow = {}
    
        firstHL7Date = firstHL7Date.split("T")[0]
        firstHL7DateDT = datetime.strptime(firstHL7Date, "%Y-%m-%d")
        firstHL7DateDTB = firstHL7DateDT - relativedelta(days=goBackDays) 
        firstHL7DateB = datetime.strftime(firstHL7DateDTB, "%Y-%m-%d")
    
        dataLocn = f'{VISTA_DATA_BASE_DIR}{stationNo}/Data/'
        store = FMQLReplyStore(dataLocn)
        startAtReply = store.firstReplyFileOnOrAfterCreateDay("123", "file_entry_date", firstHL7DateB)
        resourceIter = FilteredResultIterator(dataLocn, "123", startAtReply=startAtReply)
        for resource in resourceIter:
            if "ifc_role" not in resource:
                continue
            if resource["file_entry_date"]["value"].split("T")[0] < firstHL7DateB:
                continue
            ifcConsultsInTimeWindow[resource["_id"].split("-")[1]] = resource
        print(f"Returning {len(ifcConsultsInTimeWindow)} starting at {firstHL7DateB} which is 14 days before {firstHL7Date}, the first HL7 date")
    
        return ifcConsultsInTimeWindow

    dataLocn = "{}{}/{}".format(VISTA_DATA_BASE_DIR, stationNo, "Data") 
    tmpLocn = "{}{}/{}".format(VISTA_DATA_BASE_DIR, stationNo, "TmpWorking") 
    
    # If already done, don't redo
    try:
        ifcHL7AndConsults = json.load(open(f'{tmpLocn}/ifcHL7Consults.json'))
    except:
        pass
    else:
        return ifcHL7AndConsults
                        
    gmrcHL7, skippedAsNotProtocolTotal, _772OrphansTotal = gatherAndQA772_773OfProtocol(stationNo, int(hloSystemParameters["normal_msg_retention_days"]), int(hloSystemParameters["bad_message_retention_days"]), "GMRC IFC SUBSC")
    firstDate = gmrcHL7[list(gmrcHL7.keys())[0]]["_773"]["date_time_entered"]["label"]
    gmrcConsultsInTimeWindow = ifc123InTimeWindow(stationNo, firstDate, int(hloSystemParameters["normal_msg_retention_days"])) # By Time
    
    # may add 870 and more later
    ifcHL7AndConsults = {
        "hl7": gmrcHL7,
        "ifcConsults": gmrcConsultsInTimeWindow
    }
    json.dump(ifcHL7AndConsults, open(f"{tmpLocn}/ifcHL7Consults.json", "w"), indent=4)
    print(f"Dumped {stationNo}'s IFC HL7 and Consults into 'ifcHL7Consults.json'")
    return ifcHL7AndConsults
        
# ################################# DRIVER #######################
               
def main():
    
    assert sys.version_info >= (3, 6)

    try:
        stationNo = sys.argv[1]
    except IndexError:
        raise SystemExit("Usage _EXE_ STATIONNO [PLOT]")

    hloSystemParameters = lookupConfig779_1(stationNo) # standard config
    hl7MessageData = gatherRawIFCHL7NConsults(stationNo, hloSystemParameters)                
    hl7MessageReduction = reduceIFCHL7ToConsults(stationNo, hl7MessageData, hloSystemParameters)
    webReportHL7IFCSummary(hl7MessageReduction, hl7MessageData["ifcConsults"], hloSystemParameters)
    webReportHL7IFCFull(hl7MessageReduction, hl7MessageData["ifcConsults"])
                    
if __name__ == "__main__":
    main()
    