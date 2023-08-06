#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys
import os
import re
import json
from collections import defaultdict, Counter
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
import shelve

from fmqlutils import VISTA_DATA_BASE_DIR
from fmqlutils.cacher.cacherUtils import FMQLReplyStore, FilteredResultIterator, metaOfVistA
from fmqlutils.reporter.reportUtils import MarkdownTable, reportPercent, reportAbsAndPercent, muBVC
from fmqlutils.typer.reduceTypeUtils import splitTypeDatas, checkDataPresent, singleValue, combineSubTypes, muBVCOfSTProp, refsOfST

from fmqlreports.webReportUtils import TOP_MD_TEMPL, SITE_DIR_TEMPL, ensureWebReportLocations, keyStats, flattenFrequencyDistribution, roundFloat, reduce4, flattenPropValues, vistasOfVISNByOne
from fmqlreports.webReportUtils import muPlotRef, makePlots, vistasOfVISN

from buildDirectory import CommonBuildDirectory

from hl7Utils import HL7TemplateMaker, makeBasicHL7Event, muMessageACKAPPACK, muMessageAPPACK, assembleMessageTextLines, gatherAndQA772_773OfProtocol, lookupConfig779_1
from webReportHL7 import reduce870
 
"""
- [ ] more on handleVACRNR ... stats
- [ ] ORWRP report ... ONC (excluding them as don't fit now - must fill in)
-----
- [ ] XUS MVI NEW PERSON GET -- #'s don't add up
- [ ] the two 531 RPCs w/o explicit handlers (and extra props)
- [ ] more build descrs
- [ ] ST CLOUD 531 6569AA -- TODO tighten ... see below check
- [ ] _BADPARSE TODO for ADD RPC ... on its P1 ... happened in 653
- [ ] 653 has no XWB BuiLd? ie/ the background
----- big
- [ ] MORE on the reports
"""  

def webReportSPQ(stationNo):

    mu = TOP_MD_TEMPL.format("{} Stored Procedure Request (SPQ/HL7)".format(stationNo))
    
    mu += "# Stored Procedure Request, a HL7 \"Backdoor\" to VistA\n\n"

    meta = metaOfVistA(stationNo)
    
    overallStats, rpcLogInfoByName = makeRPCLogInfos(stationNo)
    firstSuccessDay = list(overallStats["spqSuccessDaysCount"].keys())[0]
    lastSuccessDay = list(overallStats["spqSuccessDaysCount"].keys())[-1]
    successDays = (datetime.strptime(lastSuccessDay, "%Y-%m-%d") - datetime.strptime(firstSuccessDay, "%Y-%m-%d")).days 

    PER_VISTA_BLURB_OPEN = f"""A HL7 Stored Procedure Request (SPQ) Message ...
    
> enables an application on one system to execute a stored procedure on
> another system, which is coded to extract specific data. 

In VistA, this HL7 message type is used to immediately invoke a Remote Procedure Call (RPC) in a VistA. Some calls change VistA such as _VAFC VOA ADD PATIENT_ which adds a new Patient record. Others return data such as _TIU GET RECORD TEXT_ which retrieves the contents of a clinical note. 

VistA's RPC Interface is very extensive and some more general purpose procedures let you change and access any patient or system data. Though system logs show that only a subset of RPCs are invoked through SPQs, __any RPC could be invoked__ through this __open ended "_HL7 Backdoor_"__.
    
__VistA as Black Box Report__: this is one of a series of reports that analyzes the interfacing to and from VistA. By treating VistA as a "black box", the focus is on purpose and behavior of the system and not on internal implementation details.

The follow reports on the SPQ traffic in the HL7 logs of a copy of production VistA _{meta["name"]}_ cut on _{meta["cutDate"]}_. In this system, HL7 Logs are kept for <span class='yellowIt'>{successDays}</span> days.

"""
    mu += PER_VISTA_BLURB_OPEN
            
    mu += muRPCList(stationNo, rpcLogInfoByName)
    
    mu += muByRPCGroup(stationNo, rpcLogInfoByName)
    
    userSiteDir = SITE_DIR_TEMPL.format(stationNo)
    print(f'Serializing Report to {userSiteDir}')
    open(f'{userSiteDir}hl7SPQSummary.md', "w").write(mu)  
    
"""
Plain List
""" 
def muRPCList(stationNo, rpcLogInfoByName):

    mu = "## RPC List\n\n"
    mu += """The table below lists the Remote Procedure Calls (RPC) invoked through SPQ in this VistA (_"ALL IN"_, _"I"_) or by this VistA (_"ALL OUT"_, _"I"_), ordered from most used to least. The "RDT Count" column indicates the volume of data returned in HL7 _RDT_ segments in replies (HL7 application acknowledgements) - counts > 1 indicate data transfer and not just an acknowledgment. 
    
Finally the _Users_ column counts the number of unique users identified in calls. SPQ invocations are on behalf of users. Users not already in a VistA are added dynamically without any checks. This makes __SPQ, a NIST Level of Assurance (LOA) 1 Interface__.
    
"""
    total = sum(rpcLogInfoByName[rpcName]["count"] for rpcName in rpcLogInfoByName)
    mu += f'There are <span class="yellowIt">{total:,}</span> SPQ Entries in this VistA ...\n\n'
    tbl = MarkdownTable([":RPC Name", "\#", "I/O", "Errored", "Users", ":RDT \#s"])
    for rpcName in sorted(rpcLogInfoByName, key=lambda x: rpcLogInfoByName[x]["count"], reverse=True):
        perRPCInfo = rpcLogInfoByName[rpcName]
        userMU = str(len(perRPCInfo["userCount"]))
        if len(perRPCInfo["userCount"]) == 1:
            ssn = list(perRPCInfo["userCount"])[0]
            if ssn in ["888888888"]:
                userMU = " 1 [888888888]"
        # KEY ALL IN, ALL OUT (ex/ MPIF EDAT REMOTE)
        if perRPCInfo["countOut"] == 0:
            inOutMU = "ALL IN" # ie/ so no way to know remote
        elif perRPCInfo["countIn"] == 0:
            inOutMU = "ALL OUT"
        else:
            inOutMU = f'{perRPCInfo["countIn"]}/{perRPCInfo["countOut"]}'
        if (len(perRPCInfo["rdtCountCount"])) > 5:
            rdtCountCount = Counter()
            for i, c in enumerate(sorted(perRPCInfo["rdtCountCount"], key=lambda x: perRPCInfo["rdtCountCount"][x], reverse=True), 1):
                if i > 5:
                    rdtCountCount[f'< {lastC}'] += perRPCInfo["rdtCountCount"][c]
                else:
                    rdtCountCount[c] = perRPCInfo["rdtCountCount"][c]
                    lastC = c
        else:
            rdtCountCount = perRPCInfo["rdtCountCount"]
        rdtMU = ", ".join([f'{c} [{rdtCountCount[c]:,}]' for c in sorted(rdtCountCount, key=lambda x: rdtCountCount[x], reverse=True)])
        tbl.addRow([
            f'__{rpcName}__', 
            reportAbsAndPercent(perRPCInfo["count"], total),
            inOutMU,
            sum(perRPCInfo["errorCodeCount"][i] for i in perRPCInfo["errorCodeCount"]),
            userMU,
            rdtMU
        ])
    mu += tbl.md() + "\n\n"
    
    return mu

"""
Peer of muBy(Protocol)Group in webReportHL7
"""
def muByRPCGroup(stationNo, rpcLogInfoByName):

    tops = []
    leaves = []
    matchedRPCs = set() # check
    for rpcGId in RPC_GROUPS:
    
        gInfo = RPC_GROUPS[rpcGId]
        gInfo["id"] = rpcGId
    
        if "rpcReMatch" in gInfo:
            leaves.append(gInfo) # could be a top too!
            gInfo["rpcTransactions"] = {}
            gInfo["rpcTransactionsTotal"] = 0
            for rpcName in rpcLogInfoByName:
                if "rpcReExclude" in gInfo and re.match(gInfo["rpcReExclude"], rpcName):
                    continue
                if not re.match(gInfo["rpcReMatch"], rpcName):
                    continue
                if rpcName in matchedRPCs:
                    raise Exception(f"RPC {rpcName} matched > 1 Grouping")
                matchedRPCs.add(rpcName)
                gInfo["rpcTransactions"][rpcName] = rpcLogInfoByName[rpcName]["count"]
                gInfo["rpcTransactionsTotal"] += rpcLogInfoByName[rpcName]["count"]
                if "checkProcedure" in gInfo:
                    for event in rpcLogInfoByName[rpcName]["events"]:
                        gInfo["checkProcedure"](event) 
                    
        # consider merge up
        if "parent" in gInfo:
            pgInfo = RPC_GROUPS[gInfo["parent"]]
            if "children" not in pgInfo:
                pgInfo["children"] = []
            pgInfo["children"].append(gInfo)          
        else:
            tops.append(gInfo) 
            
    unmatchedRPCs = list(set(rpcLogInfoByName) - matchedRPCs)
    print("Unmatched RPCs", unmatchedRPCs)
    if len(unmatchedRPCs):
        # Unmatched
        umgInfo = {
            "id": "ZZUngrounded",
            "label": "ZZ RPCs",
            "description": "RPCs that haven't yet been analyzed and assigned to a category.",
            "rpcTransactions": {},
            "rpcTransactionsTotal": 0
        }
        tops.append(umgInfo)
        leaves.append(umgInfo) # for completeness
        for rpcName in unmatchedRPCs:
            umgInfo["rpcTransactions"][rpcName] = rpcLogInfoByName[rpcName]["count"]
            umgInfo["rpcTransactionsTotal"] += rpcLogInfoByName[rpcName]["count"]
                        
    def totalUp(gInfo, ttlToAdd):
        if "parent" not in gInfo:
            return
        pgInfo = RPC_GROUPS[gInfo["parent"]]
        if "rpcTransactionsTotal" not in pgInfo:
            pgInfo["rpcTransactionsTotal"] = 0          
        pgInfo["rpcTransactionsTotal"] += ttlToAdd
        totalUp(pgInfo, ttlToAdd)
    for gInfo in leaves:
        totalUp(gInfo, gInfo["rpcTransactionsTotal"])
    ttlTransactions = sum(rpcLogInfoByName[rpcName]["count"] for rpcName in rpcLogInfoByName)
    for gInfo in tops:
        print(gInfo["label"], "-" if "rpcTransactionsTotal" not in gInfo else gInfo["rpcTransactionsTotal"])
    if sum(gInfo["rpcTransactionsTotal"] for gInfo in tops) != ttlTransactions:
        print(sum(gInfo["rpcTransactionsTotal"] for gInfo in tops), ttlTransactions, sum(gInfo["rpcTransactionsTotal"] for gInfo in leaves))
        raise Exception("Bug in totalling up") # shouldn't happen as even ensured no re-entrancy problem
                
    # Protocol+Link is unique (well expected to be ... TODO: perhaps apps distinguish)
    def muRPCG(gInfo, level=0):
        if gInfo["rpcTransactionsTotal"] == 0:
            return ""
        lblPart = gInfo["label"] if "label" in gInfo else gInfo["id"]
        if level == 0:
            # JONATHAN M. WAINWRIGHT VAMC {#jonathan_m__wainwright_vamc}
            lblPart = lblPart + ' {#' + re.sub(r'[ \/]', '_', gInfo["id"]) + '}'
        headerMU = "###"
        l = level
        while l > 0:
            headerMU += "#"
            l = l - 1
        mu = f'{headerMU} {lblPart}\n\n'
        gtmu = f"This group has <span class='yellowIt'>{reportAbsAndPercent(gInfo['rpcTransactionsTotal'], ttlTransactions)}</span> transactions." # if level == 0 else ""
        if "description" in gInfo:
            mu += f'{gInfo["description"]} {gtmu}\n\n'
        else:
            mu += f'{gtmu}\n\n'
        if "children" in gInfo: 
            for cgInfo in sorted(gInfo["children"], key=lambda x: x["id"]):
                mu += muRPCG(cgInfo, level+1)
            return mu
            
        def muRemoteVPO(counter, totalIPlusO):
            vistas = set(v for v in counter if re.match(r'VA[A-Z]{3}$', v) or re.search(r'\:\d{3}[A-Z\d]{0,2}$', v)) # ie/ VAPOR or PORTLAND:648 or AMERICA LAKE:663AA
            if sum(counter[v] for v in counter if not (v in vistas or v in ["VAFHIE", "VACRNR"])):
                print(counter)
                raise Exception("Expected only VISTA | VAFHIE | [VACRNR]")
            total = sum(counter[v] for v in counter)
            totalVistA = sum(counter[v] for v in vistas) 
            totalVAFHIE = counter["VAFHIE"] if "VAFHIE" in counter else 0
            totalVACRNR = counter["VACRNR"] if "VACRNR" in counter else 0
            m = f'{total} '
            m += '[VistAs]' if (totalVAFHIE + totalVACRNR) == 0 else f'[{reportPercent(totalVistA, total)}/{reportPercent(totalVAFHIE, total) if totalVAFHIE else "-"}/{reportPercent(totalVACRNR, total) if totalVACRNR else "-"}]'
            return m 
            
        def muORWRP_REPORT_TEXT_Reports(counter):
            ms = []
            otherTtl = 0
            for i, cnt in enumerate(sorted(counter, key=lambda x: counter[x], reverse=True), 1):
                if i > 5:
                    otherTtl += counter[cnt]
                    continue
                ms.append(f'{cnt.split(":")[1] if re.search(r":", cnt) else cnt} [{counter[cnt]}]')
            ms.append(f'_Others_ [{otherTtl}]')
            return ", ".join(ms)
            
        DETAILDEFNS = [
            # ["IO", "I/O", lambda x: f'{x["I"]}/{x["O"]}'], # rely on combo
            # ", ".join([f'{i} [{x[i]}]' for i in sorted(x, key=lambda y: x[y], reverse=True)])
            ["REMOTE_V_I", "In (VistAs)", lambda x: f'{sum(x[c] for c in x):,}/{len(x):,}'],
            ["REMOTE_VP_O", "Out<br>(VistAs/VAFHIE/VACRNR)", lambda x: muRemoteVPO(x, gInfo['rpcTransactionsTotal'])],
            ["REMOTE", "Other Systems", lambda x: ", ".join([f'{i} [{x[i]}]' for i in sorted(x, key=lambda y: x[y], reverse=True)])],
            ["PATIENTS", "Patients", lambda x: len(x)],
            ["USERS_AUTO", "Users (Machine)", lambda x: ", ".join([y for y in x])],
            ["USERS", "Users", lambda x: len(x) if sum(1 for u in x if re.search(r'\[(200|776)', u)) == 0 else ", ".join([f'{i.split("[")[1][:-1]} [{x[i]}]' for i in sorted(x, key=lambda y: x[y], reverse=True)])], # TODO: some user really high and show?
            ["USERS_QUERIED", "Users Queried", lambda x: len(x)], # diff types, P etc
            ["DOCUMENTS", "Documents", lambda x: len(x)],
            ["STANDARD_TITLES", "Titles", lambda x: ", ".join([f'{st} [{x[st]}]' for st in sorted(x, key=lambda y: x[y], reverse=True)])],  
            ["DRUGS", "Drugs", lambda x: len(x)],
            ["REPORTS", "Report Types", lambda x: muORWRP_REPORT_TEXT_Reports(x)],
        ]
        colsInRPCs = set(cs for rpcName in gInfo["rpcTransactions"] for cs in rpcLogInfoByName[rpcName]["customStats"])
        cols = [":RPC"]
        cols.extend([f':{dd[1]}' if re.match(r'(REMOTE|STANDARD)', dd[0]) else dd[1] for dd in DETAILDEFNS if dd[0] in colsInRPCs])
        if "rpcDescriptions" in gInfo:
            cols.append(":Description")
        tbl = MarkdownTable(cols, includeNo=True if len(gInfo["rpcTransactions"]) > 1 else False)
        vacrnrSeen = False
        for rpcName in sorted(gInfo["rpcTransactions"], key=lambda x: gInfo["rpcTransactions"][x], reverse=True):
            logInfo = rpcLogInfoByName[rpcName]
            customStats = logInfo["customStats"]
            row = [f'__{rpcName}__']
            for dd in DETAILDEFNS:
                if dd[0] not in colsInRPCs:
                    continue
                if dd[0] not in customStats or customStats[dd[0]] == "":
                    row.append("&nbsp;")
                    continue
                row.append(dd[2](customStats[dd[0]]))
            if ":Description" in cols:
                if rpcName in gInfo["rpcDescriptions"]:
                    row.append(gInfo["rpcDescriptions"][rpcName])
                else:
                    row.append("&nbsp;")
            if "VACRNR" in customStats:
                vacrnrSeen = True
                row[0] = row[0] + "*"
            tbl.addRow(row)
                
        if vacrnrSeen:
            mu += """Note that some invocations of RPCs whose names are marked with an _*_ were sent on the _VACRNR_ (VA Cerner) connection. As Cerner cannot respond to these RPCs, an error is returned. 
            
"""
        mu += tbl.md() + "\n\n"            
        
        if "builds" in gInfo and isinstance(gInfo["builds"], dict):
            tbl = MarkdownTable([":Build", "Date Made", ":Description"], includeNo=True if len(gInfo["builds"]) > 1 else False)
            for bn in gInfo["builds"]:
                if isinstance(gInfo["builds"][bn], dict):
                    when = gInfo["builds"][bn]["when"] if "when" in gInfo["builds"][bn] else "&nbsp;"
                    descr = gInfo["builds"][bn]["description"] if "description" in gInfo["builds"][bn] else "&nbsp;"
                else:
                    when = gInfo["builds"][bn]
                    descr = ""
                tbl.addRow([f'__{bn}__', when, descr])
            mu += "Relevant Build(s) details ...\n\n"
            mu += tbl.md() + "\n\n"
            
        return mu
        
    mu = "## RPC Groups\n\n"
    tocSummTBL = MarkdownTable([":Group", "SPQ Invocations"], includeNo=False)
    for gInfo in sorted(tops, key=lambda x: x["rpcTransactionsTotal"], reverse=True): # Alpha order    
        refId = re.sub(r"[ \/]", "_", gInfo["id"])
        if gInfo["rpcTransactionsTotal"] == 0:
            continue
        tocSummTBL.addRow([
            f'__[{gInfo["label"] if "label" in gInfo else gInfo["id"]}](#{refId})__',
            reportAbsAndPercent(gInfo["rpcTransactionsTotal"], ttlTransactions)
        ])
    mu += tocSummTBL.md() + "\n\n" 
    for gInfo in sorted(tops, key=lambda x: x["label"]): # Alpha order    
        if gInfo["rpcTransactionsTotal"] == 0:
            continue
        mu += muRPCG(gInfo)
    
    return mu 
    
# ##################### SPQ DEBUG ###################

def webReportSPQDebug(stationNo):

    mu = TOP_MD_TEMPL.format("{} Stored Procedure Request (SPQ/HL7) DEBUG".format(stationNo))
    
    mu += "# Stored Procedure Request (SPQ/HL7) DEBUG\n\n"
    
    overallStats, rpcLogInfoByName = makeRPCLogInfos(stationNo)
    
    mu += "## SPQ Numbers\n\n"

    """
    overallStats:
        "skippedAsNotProtocolCount"
        "protocolCount"
        # There are lingered TBRs as no 
        "tbrNotSPQCount"
        # all SPQs have a TBR in logs I've seen except the ERRORs
        "spqSuccessCount": 
        "spqOtherCount"
        "spqErrorCount"
        "spqRemoteCount"
        "spqSuccessDaysCount"
    """        
    tbl = MarkdownTable([":Property", ":Value"])
    messagesTotal = overallStats["skippedAsNotProtocolCount"] + overallStats["protocolCount"]
    tbl.addRow(["All HL7 Messages", messagesTotal])
    tbl.addRow(["In protocol messages", reportAbsAndPercent(overallStats["protocolCount"], messagesTotal)])
    tbl.addRow(["No SPQ TBR Ack Messages (not purged yet)", reportAbsAndPercent(overallStats["tbrNotSPQCount"], overallStats["protocolCount"])])
    spqCount = overallStats["spqSuccessCount"] + overallStats["spqOtherCount"] + overallStats["spqErrorCount"]
    tbl.addRow(["SPQ Messages", reportAbsAndPercent(spqCount, overallStats["protocolCount"])])
    tbl.addRow(["Success Messages (all with TBR Acks)", reportAbsAndPercent(overallStats["spqSuccessCount"], spqCount)])
    if overallStats["spqOtherCount"]:
        tbl.addRow(["Other Messages", reportAbsAndPercent(overallStats["spqOtherCount"], spqCount)])
    tbl.addRow(["Error Messages", reportAbsAndPercent(overallStats["spqErrorCount"], spqCount)])
    tbl.addRow(["Remote (incoming SPQs)", reportPercent(overallStats["spqRemoteCount"], spqCount)])   
    # Account for number per success day - 20th - 18th + 1 ie/ include last day
    firstSuccessDay = list(overallStats["spqSuccessDaysCount"].keys())[0]
    lastSuccessDay = list(overallStats["spqSuccessDaysCount"].keys())[-1]
    successDays = (datetime.strptime(lastSuccessDay, "%Y-%m-%d") - datetime.strptime(firstSuccessDay, "%Y-%m-%d")).days 
    # Seems to undercount the boundary days as last day doesn't get going
    # but active window of first day cut out ... but ...
    successPerDay = round(overallStats["spqSuccessCount"]/successDays)
    tbl.addRow(["SPQ Success Days", f'{successDays}'])
    tbl.addRow(["SPQ Success per day", f'{successPerDay}'])
    # TODO: graphic these up
    mu += tbl.md() + "\n\n"
            
    # ######################### RPCs in Builds #############################
    
    visn20VistAs = vistasOfVISN("20")
    cbd = CommonBuildDirectory(visn20VistAs)
        
    # Builds Information (see dates, key lines etc)
    # TODO: improve dates for build order 
    mu += "## RPCs in Builds\n\nVistA software is distributed in \"KIDS Builds\". The date of releases and their contents give important background on the RPCs invoked through SPQ.\n\n"
    tbl = MarkdownTable([":RPC Name", ":Package", "Builds (Date)", ":Lines"]) 
    for rpcName in sorted(rpcLogInfoByName, key=lambda x: rpcLogInfoByName[x]["count"], reverse=True):
        bldNames = cbd.buildsWithRPC(rpcName)
        if len(bldNames) == 0:
            raise Exception(f'No builds for {rpcName}')
        bldMUList = []
        pkg = ""
        firstLines = []
        bldInfos = []
        for bldName in bldNames:
            bldInfo = cbd.lookupBuildEntriesByName(bldName)[0]
            bldInfos.append(bldInfo)
        for bldInfo in sorted(bldInfos, key=lambda x: x[3]):
            bldMU = f'{bldInfo[2]} ({bldInfo[3]})' if bldInfo[3] else bldInfo[2]
            bldMUList.append(bldMU)
            if bldInfo[4]:
                if pkg:
                    if pkg != bldInfo[4]:
                        raise Exception("Inconsistent packages for builds")
                else:
                    pkg = bldInfo[4]
            # Will parse out key lines
            if bldInfo[6]:
                lines = bldInfo[6].split("\n")
                if not (re.search(r'[rR]efer to patch', lines[0]) or re.search(r'See National Patch', lines[0])) and re.search(r' ', lines[0]) and re.search(r'[A-Za-z]', lines[0]) and lines[0] not in firstLines:
                    firstLines.append(lines[0])
        tbl.addRow([
            f'__{rpcName}__',       
            pkg,
            "<br>".join(bldMUList),
            "<br>".join(firstLines)
        ])
    mu += tbl.md() + "\n\n"
    
    # ########################### RPC by RPC ####################
    # TODO: fill in RPC details like key users or range of vistas ie/ repeat data and 
    # explain <----------- NOTE DATE AND PKG FROM BUILDs
    
    # Exs
    mu += "## Examples of all RPC Seen\n\nNote that all messages have been de-identified.\n\n"
    for rpcName in sorted(rpcLogInfoByName, key=lambda x: rpcLogInfoByName[x]["count"], reverse=True):
        perRPCInfo = rpcLogInfoByName[rpcName]
        mu += f"### {rpcName}\n\n"
        if "nonErrorExample" in perRPCInfo:
            perRPCInfo["nonErrorExample"]["messageCategory"] = "SPQ RPC" # dummy as needed
            neemu = muMessageAPPACK(perRPCInfo["nonErrorExample"])
            mu += neemu
        else:
            mu += "No Non Error Example\n\n"
        
    userSiteDir = SITE_DIR_TEMPL.format(stationNo)
    print(f'Serializing Report to {userSiteDir}')
    open(f'{userSiteDir}hl7SPQSummaryDebug.md', "w").write(mu)  
    
# ########### Generate Background (could just do fixed) #########

"""
SPQ Intro Backgrounder - will probably make this a fixed report
"""
def webReportSPQBackground():

    mu = TOP_MD_TEMPL.format("{} Stored Procedure Request (SPQ/HL7) Background".format("Common"))
    
    # ######################### INTRO ##################
    
    INTRO = """A HL7 Stored Procedure Request (SPQ) Message ...
    
> enables an application on one system to execute a stored procedure on
> another system, which is coded to extract specific data. 

In VistA, this HL7 message type is used to immediately invoke a Remote Procedure Call (RPC) in a VistA. Some calls change VistA such as _VAFC VOA ADD PATIENT_ which adds a new Patient record. Others return data like _TIU GET RECORD TEXT_ which retrieves the contents of a clinical note. 

VistA's RPC Interface is very extensive and some more general purpose procedures let you change and access any data in a system. Though system logs show that only a subset of RPCs are invoked through SPQs, __any RPC could be invoked__ through this __open ended "_HL7 Backdoor_"__.
    
"""

    mu += INTRO
    
    mu = """__Cerner Notes/Questions:__
    
  1. Peer to Peer data transfers - VistA to VistA or VistA to FHIE - how will Cerner source and sink equivalent data transfers after Hospitals are migrated if at all?
  2. Will the MPI sync with Cerner using a different mechanism?
  3. How will unmigrated generate reports (_ORWRP_REPORT_TEXT_) for facilities migrated to Cerner?  
  4. What will happen to logs in VistA marked by Directives for permanent retention?
  5. Interfacility Consults (IFC) in VistA end with an RPC call for the document containing the consult's result. For consults that arise in Cerner, that will no longer happen. But what will happen for consults sent to Cerner from VistA? Will the current "ask with an RPC" flow be emulated?
    
"""
    
    # ######################### Key Protocol Blurb ###########
    
    visn20VistAs = vistasOfVISN("20")
    cbd = CommonBuildDirectory(visn20VistAs)
    
    BLURB_PROTOCOL = """In VistA, a Protocol is a “method for accomplishing orders”. SPQ Interactions go through the _XWB RPC SUBSCRIBER_ Protocol which is
    
> used to facilitate invocation of Remote Procedure Calls on a remote server.  The RPC Broker uses Vista HL7 as the vehicle to pass RPC name and parameters from local server to remote server.  On the return path, Vista HL7 is also used to send results from the remote server back to the local server.
>
> This particular protocol represents the receiving system and as such information is used to generate the response HL7 message header(MSH segment) from this perspective.

Key protocol attributes ...

Property | Value
--- | ---
Message Type (Request) | SPQ
Event Type (Request) | R08
Message Type (Response/Ack) | TBR
HL7 Version | 2.3.1
Receiving Facility Required | No
Sending Facility Required | No
Processing Entry Point | _D RPCRECV^XWB2HL7B_

This invocation of (any) RPC in one message and its one protocol breaks the normal VistA paradigm of a link having one or more protocols, one per message type and a message type having a very specific purpose.
    
"""
    mu += BLURB_PROTOCOL

    bldNames = cbd.buildsWithProtocol("XWB RPC SUBSCRIBER")
    if len(bldNames) > 1:
        raise Exception(f"Expect at most one build for 'XWB RPC SUBSCRIBER' but {bldNames}")        
    if len(bldNames) == 1:  
        bldInfo = cbd.lookupBuildEntriesByName(bldNames[0])[0]
        escBldName = re.sub(r'\*', '\*', bldNames[0])
    
        # TODO: what about these deferred and other calls?
        mu += f"""The protocol was distributed in Build {escBldName} from {bldInfo[3].split("-")[0]} for package {bldInfo[4]}. The build is in ...
    
> support of the CPRS Remote Data Views project. The RPC Broker is used to facilitate invocation of Remote Procedure calls on a remote server.

The build lists expected protocols and application parameters but also a list of 'RPCs for invoking RPCs', entities that don't appear to be called anymore.

```text
To facilitate the running of  server to server  RPCs, new RPCs are sent
out in this patch.  The documentation on how to use these RPCs can be
found on Forum's DBA menu. Please reference the following Integration
Agreements:
 
 #3032 Direct RPCs - controlled subscription
 #3031 Remote RPCs - controlled subscription
 #3033 Deferred RPCs - supported
 
New Remote Procedure entries: 
 1. XWB REMOTE RPC 
 2. XWB REMOTE STATUS CHECK 
 3. XWB REMOTE GETDATA 
 4. XWB REMOTE CLEAR
 5. XWB DEFERRED CLEAR
 6. XWB DEFERRED CLEARALL
 7. XWB DEFERRED RPC 
 8. XWB DEFERRED GETDATA 
 9. XWB DEFERRED STATUS 
 10. XWB DIRECT RPC 
 
New Protocol entries: 
 1. XWB RPC EVENT 
 2. XWB RPC SUBSCRIBER 
 
New HL7 Application Parameter entries: 
 1. XWB RECEIVER 
 2. XWB SENDER 
```

"""
    else:
        mu += """There is __NO__ build with the protocol _\"XWB RPC SUBSCRIBER\"_ in this system's file 9.6
        
"""

    """
    TODO add EVENT to SUBSCRIBER
    
    XWB RPC EVENT is for the response process
        
    http://localhost:9100/query?fmql=DESCRIBE%20101-2943&format=HTML
    response processing routine: RETURN^XWB2HL7
    references subscriber
    http://localhost:9100/query?fmql=DESCRIBE%20101-2942&format=HTML
    processing routine D RPCRECV^XWB2HL7B
    
    both receive = request (subscribe) and response process
    """
    
    
    # ##################### ESSO and USERS ################
    # TODO: more on users and their form in the system
    
    BLURB_ESSO_ID = """## User Identification and Validation

The field _"XWBESSO"_ sent in the SPQ's SPR segment identifies the user invoking the RPC. It has the following properties ...

Property | Example
--- | ---
Social Security Number | 111223333 
Name | JONES,BOB J
Name of Clinic | CLEVELAND VAMC
Station Number of Clinic | 541
IEN in User File of Sender | 99999
Phone | 999-555-1212
- | blank in this VistA's logs
Network User Name | VHAXXXJONESB

  * If a user doesn't already exist in the receiving VistA's file 200, a new _"Visitor User"_ entry is created as a result of the SPQ request.
  * The receiving VistA does not check the validity of the user or the users permission to perform the RPC. Hence this is __NIST LOA 1__.
  * "Machine Users" like _PSUSER, APPLICATION PROXY_ have simple synthesized social security numbers and unlike real users don't have network user names.

"""
    mu += BLURB_ESSO_ID
    
    commonSiteDir = SITE_DIR_TEMPL.format("Common")
    print(f'Serializing Report to {commonSiteDir}')
    open(f'{commonSiteDir}hl7SPQBackground.md', "w").write(mu) 
    
# ################## RPC Meta and Groupers ############################
    
RPC_GROUPS = {

    "Patient Demographics": {
    
        "label": "Patient Demographics",
        
        "contains": ["DateOfDeath", "Facility and MPI Views", "VAFC_REMOTE_PDAT", "VOA", "VAFCTFU", "Patient Send"]
    
    },
    
    "DateOfDeath": {
    
        "parent": "Patient Demographics",
                
        "label": "Deceased Validation",
        
        "description": """The RPC _MPIF DOD ACTIVITY CHECK_ is called __from the AAC__ to search through various packages: FEE BASIS, OUTPATIENT PHARMACY, PCE  PATIENT CARE ENCOUNTER, REGISTRAION and SCHEDULING, to find any activity that might indicate that a patient is not actually deceased. The validity of the reported Date of Death is confirmed if no activity is found.""",
        
        "__comment": "Check on Demographics - question of Cerner doing this?",
        
        "package": "MPIF - MASTER PATIENT INDEX VISTA", # from Build
        
        "buildDates": ["7/26/2016"],
 
        "rpcReMatch": "MPIF DOD ACTIVITY CHECK",
        
        # 8994: availability PUBLIC
        # 
        # Most answer is RDT^0 but one has
        #   RDT^1^{\d+}^Appointment Found
        "rpcDescriptions": {
        
            "MPIF DOD ACTIVITY CHECK": "called by the MPI to look for activity of the given patient. It will search multiple packages to verify there has been no activity since a reported date of death as a conformation. ... Takes Patient Id (DFN) and Reported Date of Death"
        
        },
        
        "seeAlso": [
            "https://foia-vista.worldvista.org/Patches_By_Application/MPIF-MASTER%20PATIENT%20INDEX%20FILE/MPIF-1_SEQ-61_PAT-64.TXT"
            
        ]
        
    },
    
    "Facility and MPI Views": {
    
        "parent": "Patient Demographics",
    
        "label": "MPI Primary View",
            
        "description": """Sent by users in individual VistAs __to Austin__. Build(s) for _MPIF EDAT REMOTE_ say it was part of the \"Master Patient Index (MPI) Identity Hub Project for the Healthcare Identity Management (HC IdM) team\" which moved patient identity coalesion to commercial identity management software.

_Open Question_: this RPC seems to belong ONLY to a custom \"VistA\" in Austin that manages Patient Demographic records across the VA.
        
""",
        
        "buildDates": ["2009-10-28"], # only checked MPIF...; TODO check RG
    
        # 8994: availability PUBLIC
        # ... add ALLINALLOUT: inOutCategory: ["ALLOUT"] # MPIVA
        # ? 
        "rpcReMatch": "(MPIF EDAT REMOTE|RG PRIMARY VIEW FROM MPI)",
        
        "rpcDescriptions": {
        
            "MPIF EDAT REMOTE": "MPI returns a tabbed text report showing Austin's primary view of a Patient's demographics and the views of known treating facilities.",
            
            "RG PRIMARY VIEW FROM MPI": "return the MPI Patient Data Inquiry [MPI DATA MGT PDAT MPI] (PDAT) report for a requested ICN"
        
        },
        
        "seeAlso": [        
            "https://foia-vista.worldvista.org/Patches_By_Application/MPIF-MASTER%20PATIENT%20INDEX%20FILE/MPIF-1_SEQ-48_PAT-52.TXT"
        
        ]

    },
    
    "VOA": { 
    
        "parent": "Patient Demographics",
                    
        "label": "Patient Addition",
        
        "description": """The Veteran On-Line Application (VOA) project is a collaborative effort by the MyHealtheVet veteran web-portal, the National Enrollment Service (ESR), Person Services Identity Management (PSIM), the Master Patient Index (MPI), and the VistA Patient Information Management System (PIMS) application. The VOA-enabled process flow has:
  * veteran completing web-based application
  * ESR and PSIM taking the data
  * record created in MPI and ICN allocated
  * ESR vetting to determine Enrollment Status
  * RPC will be called to add the patient to the Preferred Facility's VistA database.
        
Patient demographics (DOB, SSN, ICN ...) are passed in and the patient's local identifier (in file 2 of VistA) is returned. Only __invoked from Austin__ from a machine user with SSN _888888888_, called _PSUSER,APPLICAITON PROXY_.

""",

        "TODO": "Both Builds for the one RPC - Parse complex Patient Argument",
    
        "buildDates": ["2010-02-02", "2014-08-18"],
        
        "rpcReMatch": "VAFC VOA",
        
        "rpcsWrite": ["VAFC VOA ADD PATIENT"],
        
        "rpcDescription": {
        
            # 8994: availability RESTRICTED
            # VOA == VETERAN ON-LINE APPLICATION
            "VAFC VOA ADD PATIENT": "allows the remote creation of a VistA PATIENT (#2) record at the Preferred Facility for the Veteran On-Line Application (VOA) project. The one RDT in the reply has the IEN of the new Patient Record."
            
        },
    
        "seeAlso": [      
            "https://foia-vista.worldvista.org/Patches_By_Application/DG-REGISTRATION/DG-5P3_SEQ-726_PAT-800.TXT",
                   "https://foia-vista.worldvista.org/Patches_By_Application/DG-REGISTRATION/DG-5P3_SEQ-784_PAT-876.TXT"
        ]
    
    },
    
    # 8994: availability PUBLIC
    #
    # TODO: look at all these other systems queried?
    # 
    # In addition to individual VistAs, returned info on patient demos from ...
    # - RDT^AUSTIN INFORMATION T  200                        
    # - RDT^AUSTIN MHV            200MH
    # - RDT^AUSTIN PSIM           200PS                         
    # - RDT^DEPARTMENT OF DEFENS  200DOD                     
    # - RDT^ENROLLMENT SYSTEM RE  200ESR                     
    # - RDT^MULTICARE             200NWS                     
    # - RDT^VA PROVISIONING SYST  200PROV                    
    # - RDT^VA VETS360            200VETS                    
    # - RDT^VBA BRLS              200BRLS                    
    # - RDT^VBA CORP              200CORP                    
    # - RDT^VETERANS ID CARD SYS  742V1 
    # 
    # If SSN wrong => get RDT^-1^Invalid SSN passed into RPC
    # ie/ RPC error means three part but actual document goes in RDT^blah blah etc. 
    #
    "VAFC_REMOTE_PDAT": { # Consider into MPIF group - all IN so prob MPI (TODO: see user!)
    
        "parent": "Patient Demographics",
    
        "label": "MPI/PD Data Inquiry",
        
        # TBD: need to expand on use of LOCAL GETCORRES ... first seen in 692 5/21
        "description": """These RPCs are invoked __from remote systems__. PDAT returns demographics including a patient's treating facilities in a tab delimited rpeort; AUDIT details who made changes to the patient's demographics/ids in a text table. Patients are identified by _ICN_, _DFN_ (local VistA Id) or _SSN_ and the AUDIT RPC also sends a date range. They are invoked by either Birmingham (521) or \"MPI\" (200) users. 521 Users identify with either SSN or ICN; MPI Users use DFN.""",
        
        "__comment": "More - what app does this?; AUDIT report has reference to DVBA CAPRI GUI (so is that the App?); see MPIF A24 HL7 BG Task shown as one changer!",
        
        "rpcReMatch": "VAFC (REMOTE|LOCAL)",

        "rpcDescriptions": { # all in ... but from who?

            "VAFC REMOTE PDAT": "return the text Patient MPI/PD Data Inquiry report. In addition to individual VistAs, data comes from Austin systems including Enrollment, MHV, VETS360 and more.",
            
            # 8994: availability PUBLIC
            "VAFC REMOTE AUDIT": "return a Patient audit report (changes made to a Patient's demographics/identifiers in a date range) from a remote site", # What Audit? TODO
    
            "VAFC LOCAL GETCORRESPONDINGIDS": "return list of treating facilities where the patient has been seen" # may be new build but didn't look up - 692 only
        },
        
        "buildDates": ["2001-12-19"],
        
        # No see also as can't find DG*5.3*414
        
    },
    
    "VAFCTFU": {
    
        "parent": "Patient Demographics",
    
        "label": "Convert ICN to DFN",
    
        "rpcReMatch": "VAFCTFU CONVERT ICN TO DFN",
        
        # VIA added "APP PROXY USE" prop to RPCs as VIA uses that
        "builds": {
            "DG*5.3*261": "2000-05-08", 
            "DG*5.3*477": "2003-08-15", 
            "DG*5.3*900": "2014-09-10"
        } # has treating facility list - 391.91 too

    },
    
    "Patient Send": { # 531
    
        "parent": "Patient Demographics",
    
        "label": "ICN Assignement",
        
        "rpcReMatch": "MPIF REMOTE SPI",
        
        "rpcDescriptions": { 
        
            # 8994: no details on availability etc. - READ
            "MPIF REMOTE SPI": "Allows the remote sending of a specific patient at a specific site to the MPI for ICN assignment. The patient is found based upon social security number." # but used from MPI to site
        
        }
    
    },
    
    "Users": {
    
        "label": "Users",
    
        "contains": ["CardData", "User Management"]
    
    },
    
    "CardData":  { 
    
        "parent": "Users",
            
        "label": "VHIC/CAC CARD DATA to MPI",
    
        "description": """Allow __Veteran Health Information Card (VHIC)__ and the Department of Defense's (DoD) __Common Access Card (CAC)__ swipe and scan information to be temporarily stored on VistA, until retrieved __from the Master Patient Index (MPI) system in Austin__:
  * allow the MPI system to retrieve the locally stored VHIC/CAC data
  * MPI will then purge all of the retrieved VHIC/CAC information in the local VistA system using the RPC MPIF PURGE VHIC/CAC CARD DATA
  
""",
        
        "__comment": "Category of 'BULK DOWNLOAD'; Input ONLY + AUSTIN (200) only but it is an individual from Austin ie/ not just anyone",
        
        "package": "MPIF - MASTER PATIENT INDEX VISTA", # from Build
        
        "buildDates": ["6/6/2016"],
 
        "rpcReMatch": "MPIF(.*)VHIC",
        
        # 8994: no details on availability etc
        # READ -- other (purge is cleanup)
        "rpcDescriptions": {
        
            "MPIF GET VHIC/CAC CARD DATA": "look up all VHIC/CAC swipe/scan activity at the site for all days prior to today", 
            
            "MPIF PURGE VHIC/CAC CARD DATA": "purge data used to track VHIC/CAC card usage for all prior dates"
        
        },
        
        "seeAlso": [
            "https://foia-vista.worldvista.org/Patches_By_Application/MPIF-MASTER%20PATIENT%20INDEX%20FILE/MPIF-1_SEQ-59_PAT-62.TXT",
            
            "https://foia-vista.worldvista.org/Patches_By_Application/MPIF-MASTER%20PATIENT%20INDEX%20FILE/MPIF-1_SEQ-61_PAT-64.TXT"
            
        ],
        
        "TODO": "Expect to see both RPCs as incoming and want 8994 about them; ie/ expect in from MPI. Also re-inforce, user set (who is the user?) and show NO ARGS"
 
    },
    
    "User Management": {
    
        "parent": "Users",
                
        "label": "User Management",
        
        "description": """These RPCs retrieve or update a user's record (file 200) in a VistA. 
        
The most frequent users of _NEW PERSON GET_ are the AUSTIN INFORMATION TECH CTR (200) and the OFFICE OF INFORMATION SRV CNTR (776). Their use seems to involve the Provider Profile Management System (PPMS) / Provider Integration Engine (PIE).
        
""",

        "__comment": """The builds with these RPCs stated they were part of the Provider Profile Management System (PPMS) / Provider Integration Engine (PIE) updates for Mission Act that the Master Veteran Index (MVI) team has been requested to implement.""",

        "rpcReMatch": "XUS",
        
        "rpcDescriptions": {
        
            # 8994: availability AGREEMENT app proxy allowed -- READ
            "XUS MVI NEW PERSON GET": "Retrieve data (by DUZ, SECID, NPI or SSN) from the Vista New Person File (200). The RDT segments in the TBR acknowledgement each serialize part of the file 200 entry.", 
            
            # 8994: availability AGREEMENT app proxy allowed -- WRITE
            "XUS MVI NEW PERSON UPDATE": "Update an entry (by DUZ) in the VistA New Person File (200)"
        
        },

        "seeAlso": [
            "https://foia-vista.worldvista.org/Patches_By_Application/XU-KERNEL/XU-8_SEQ-551_PAT-711.txt",
            "https://foia-vista.worldvista.org/Patches_By_Application/XU-KERNEL/XU-8_SEQ-540_PAT-691.txt"
        ]
        
    },
        
    "DGBT": {
    
        "label": "Beneficiary Travel",
        
        "buildDates": ["2013-02-03", "2019-07-17"],

        "seeAlso": [
            "https://foia-vista.worldvista.org/Patches_By_Application/DGBT-BENEFICIARY%20TRAVEL/DGBT-1_SEQ-22_PAT-20.TXT",
            
            "https://foia-vista.worldvista.org/Patches_By_Application/DGBT-BENEFICIARY%20TRAVEL/DGBT-1_SEQ-37_PAT-35.txt"
            
        ],
        
        # 8994: availability PUBLIC / READ
        "rpcReMatch": "DGBT CLAIM DEDUCTIBLE PAID",
    
        "rpcDescriptions": { # ?"What is the one line booleans or counts?"

            "DGBT CLAIM DEDUCTIBLE PAID": "used by Beneficiary Travel Package to retrieve travel claim information about any travel claims for patient ... will return the number of claims and amount of deductible paid by a patient during the current month"
                
        },
        
        "TODO": "Seem to be all VistA unlike MPIF and mixed I/O"
        
    },
    
    "IB": {
    
        "label": "Integrated Billing",
        
        "description": """Integrated Billing uses _SPQ_ to synchronize and query copay and insurance information between VistAs and between VistAs and the FHIE.
        
""",
        
        "contains": ["IBCN", "IBECEA", "IBARXM"]
        
    },

    "IBCN": {
    
        "parent": "IB",
    
        "label": "Insurance Query",
                
        "rpcReMatch": "IBCN",
        
        "builds": {
            "IB*2.0*214": "2003-06-06"
        }, # from so far back - can't get
        
        # 8994: availability PUBLIC, suppress rdv user setup TRUE -- READ
        # RDT^-1^No insurance on file if nothing to return but if data then
        # have the RDT^..^ with data. This is structured and not text.
        "rpcDescriptions": {
        
            "IBCN INSURANCE QUERY TASK": "a remote query on the insurance information. The file _INSURANCE REMOTE QUERY RESULTS (355.34)_ logs query data and VHA Directive 10-93-142 states it should not be modified"
        
        }
            
    },
    
    "IBECEA": { # TODO: break this one does to CRUD stuff!
    
        "parent": "IB",
    
        "label": "OCC Segregated Billing",
        
        "description": """The Office of Community Care (OCC) ... enhanced VistA Integrated Billing (IB), Accounts Receivable (AR), and Fee Basis (FB) ... to allow segregating all billing and collection activities for Non-Department of Veterans Affairs (VA) Care Third Party Insurance carriers' reimbursement. ... to increase timeliness and collections of billable Non-Veterans Affairs (VA) care services""",
        
        "rpcReMatch": "IBECEA",
        
        "rpcDescriptions": { # Restricted Access RPC
        
            "IBECEA COPAY SYNCH": "perform actions Create, Read, Update, Delete (CRUD) to track urgent care copays for a Veteran across all VA facilities the individual has been treated at. File _IB UC VISIT TRACKING (351.82)_ is updated by this RPC and per VHA Directive 6402, this file should not be modified or deleted."
            
        },
        
        "builds": {
            "IB*2*663": {"when": "2020-01-21", "description": "goal of this enhancement is to increase timeliness and collections of billable Non-Veterans Affairs (VA) care services."},
            "IB*2*671": {"when": "2020-03-10", "description": "update to _IB*2*663_"}
        }, # NEWish so not FOIA 
        
        "seeAlso": [       "https://foia-vista.worldvista.org/Patches_By_Application/IB-INTEGRATED%20BILLING/IB-2_SEQ-603_PAT-663.txt",
        
            "https://foia-vista.worldvista.org/Patches_By_Application/IB-INTEGRATED%20BILLING/IB-2_SEQ-604_PAT-671.txt",
            "https://www.va.gov/vdl/documents/Financial_Admin/Integrated_Billing_(IB)/ib_2_0_p663_ig.pdf"        

        ]
        
    },
    
    "IBARXM": {
    
        "parent": "IB",
    
        "label": "Pharmacy Copay",
        
        "rpcReMatch": "IBARXM",
        
        "rpcDescriptions": {
        
            # 8994: availability RESTRICTED, suppress rdv user setup -- WRITE
            "IBARXM TRANS DATA": "receive outpatient medication transaction data from a remote system. The data is stored in the file _IB COPAY TRANSACTIONS (354.71)_.",
                     
            # Restricted Access is set in 8994 -- READ
            # "Suppress User" seems to refer to not allowing a user 
            # to see their own information.
            # ... 354.71 format for reply
            "IBARXM QUERY SUPPRESS USER": "query only the information for pharmacy co-payment billing that has happened for the given month/year",
         
            "IBARXM QUERY ONLY": "same description and purpose as \"IBARXM QUERY SUPPRESS USER\"",
            
            "IBARXM TRANS BILL": "" # only saw in 653 6/21
            
        },
        
        "builds": {
            "IB*2.0*150": "2001-05-31", 
            "IB*2.0*178": "2002-05-20"
        }
    
    },
    
    "Patient Medical Record": {
    
        "label": "Patient Medical Record",
        
        "contains": ["Medical Results", "OR", "TIU"]
    
    },
    
    # "Saw an ESSO BOISE into BOISE ie/ a local app of some kind?"
    "Medical Results": { # Only 531
    
        "parent": "Patient Medical Record",
    
        "label": "Medical Results",
        
        "rpcReMatch": "ORQQCN GET MED RESULT DETAILS",
        
        # 8994: no details on availability etc
        "rpcDescriptions": {
            "ORQQCN GET MED RESULT DETAILS": "Detailed display of medicine results. Reads from file _GENERALIZED PROCEDURE CONSULT (699.5)_."
        }
    
    },
    
    "OR": {
    
        "parent": "Patient Medical Record",
    
        "label": "Order Reports",
        
        "description": """These Order Report RPCs are invoked to and from other VistAs (peer to peer) or to (never from) the Federal Heath Information Exchange (FHIE).""",
        
        "builds": {
            "ORDER ENTRY/RESULTS REPORTING 3.0": {"when": "1997-12-17", "description": "General-purpose release that includes all RPCs shown here"}, 
            "OR*3.0*10": {"when": "2000-09-07", "description": "Rerelease of RPCs"},
            "OR*3.0*392": {"when": "2014-03-20", "description": "Adds access to these RPCs for VistA Integration Adapter (VIA)"}
        },
                
        "rpcReMatch": "ORW",
        
        # ALL READ (no need to say
        "rpcDescriptions": { # RP/LR/LRR all in same two builds
        
            # 8994: availability SUBSCRIPTION, app proxy allowed TRUE
            "ORWRP REPORT TEXT": "retrieves the report text for a report selected on the Report tab. Arguments include patient identifier and report identifiers",
            
            # 8994: availability SUBSCRIPTION
            "ORWLR CUMULATIVE REPORT": "returns an up to date laboratory cumulative report for a given patient",
            
            # Nothing in 8994
            "ORWLRR INTERIM": "Interim Report RPC - all tests by date"
        
        },
        
        "seeAlso": [
        
            "https://foia-vista.worldvista.org/Patches_By_Application/OR-ORDER%20ENTRY_RESULTS%20REPORTING/OR-3_SEQ-341_PAT-392.TXT" # with VIA, APP PROXY USER
        
        ]
    
    },
    
    # A specific range of notes?
    "TIU": {
    
        "parent": "Patient Medical Record",
    
        "label": "Text Notes (TIU) For IFCs",
        
        "description": """Used to retrieve a note created in another VistA as a result of an Inter-facility Consult (IFC).
        
""",
                
        # Another READ RPC (ie/ not write)
        # 8994: availability SUBSCRIPTION, app proxy allowed TRUE
        "rpcReMatch": "TIU GET RECORD TEXT",
        
        "builds": {
            "TEXT INTEGRATION UTILITIES 1.0": "1997-06-20",
            "TIU*1.0*283": "2014-03-20" # was this the VIA change?
        }
            
    }
    
}
    
"""
XUS MVI NEW PERSON (GET|UPDATE)

USER DEMO/USE REPORT or UPDATE

GET | READ | ALL IN | AUSTIN (MACHINE), 776 (REAL)
UPDATE | WRITE | ALL IN | ...

Invoked remotely - by Austin or Office of Information Services

GET: Pass in DUZ (file 200) or SECID or ... and get back contents of 200, delimited by ^'s
UPDATE: see a complicated arg, P1(0)->P1(6) with details of 200 to update/or put in? ie/ if new is P1(0) start with 200;IEN vs pre-existing?

"""
def checkXUS_MVI_NEW_PERSON(rpcName, event, userInfo, customStats): # GET or UPDATE
        
    if rpcName in ["XUS MVI NEW PERSON GET", "XUS MVI NEW PERSON UPDATE"]:
        if not (
            event["transmissionType"] == "I" 
            # userInfo[2] in ["AUSTIN INFORMATION TECH CTR", "OFFICE OF INFORMATION SRV CNTR", "MPI"] and 
            # userInfo[3] in ["200", "200M", "776"] # 200M from White City, saw 534 in Charleston
            # if 200 => "PSUSER,APPLICATION PROXY" ie/ 88888888
            # saw SECID P2 passed in from 776
        ):
            print(userInfo)
            raise Exception(f'Unexpected User/Transmission of {rpcName}') 
                        
    # AAC or Office - IN
    customStats["REMOTE"][f'{userInfo[2]}:{userInfo[3]}'] += 1   
    
    customStats["USERS"][f'{userInfo[1]} [{userInfo[3]}:{userInfo[0]}]'] += 1
    
    # UPDATE -- P1(6) edit many in one argument
    if rpcName == "XUS MVI NEW PERSON GET":
        for p in ["P1", "P2", "P3", "P4"]:
            # P1 is IEN of 200
            if event["sprSeg"]["_inputParameterList"][p]:
                customStats["USERS_QUERIED"][f'{p}:{event["sprSeg"]["_inputParameterList"][p]}'] += 1
                break
            
    customStats["USERS"][f'{userInfo[1]} [{userInfo[3]}:{userInfo[0]}]'] += 1
        
"""
MPIF GET VHIC/CAC CARD DATA", "MPIF PURGE VHIC/CAC CARD DATA

USER DEMO/USE REPORT or UPDATE

GET | READ | ALL IN | AUSTIN (real)
PURGE | WRITE | ALL IN | AUSTIN (real)

No args needed - show scans of card (TODO: what exact format?) 

Log retrieval and then purge after retrieval - one-two punch; all from Austin.

Purge may have one RDT - "PURGE SUCCESSFUL"
"""
def checkMPIF_GETPURGE_VHIC(rpcName, event, userInfo, customStats):

    if not (
        event["transmissionType"] == "I" and
        userInfo[2] in ["AUSTIN INFORMATION TECH CTR"] and
        userInfo[3] in ["200"] # real person though
        # and no P's
    ):
        print(userInfo)
        raise Exception(f'Unexpected User/Transmission of {rpcName}') 
        
    # All AAC
    customStats["USERS"][f'{userInfo[1]} [{userInfo[3]}:{userInfo[0]}]'] += 1

    customStats["REMOTE"][f'{userInfo[2]}:{userInfo[3]}'] += 1   
                
"""
MPIF DOD ACTIVITY CHECK

PATIENT DEMO REPORT OR UPDATE

READ | ALL IN | AUSTIN x 2, real people

See response comment ala DOD,{date of death} OR plain 0 (alive?) back to Patient Id (P1)
"""
def checkMPIF_DOD_ACTIVITY_CHECK(rpcName, event, userInfo, customStats):

    if not (
        event["transmissionType"] == "I" and
        userInfo[2] in ["MPI", "AUSTIN INFORMATION TECH CTR"] and 
        userInfo[3] in ["200M", "200"] # 687 only 200M but 757 200 
    ):
        print(userInfo)
        raise Exception(f'Unexpected User/Transmission of {rpcName}')
        
    customStats["REMOTE"][f'{userInfo[2]}:{userInfo[3]}'] += 1    
            
    customStats["PATIENTS"][event["sprSeg"]["_inputParameterList"]["P1"]] += 1

    customStats["USERS"][f'{userInfo[1]} [{userInfo[3]}:{userInfo[0]}]'] += 1
    
"""
MPIF EDAT REMOTE - OUT, on MPIVA

PATIENT DEMO REPORT OR UPDATE

READ | ALL OUT | MPIVA (ie/ to AUSTIN) by real users

[cerner case as all out => ok]

Tab delimited text report on the demographics of a Patient (id'ed by ICN in P1) back from Austin showing what various sites/treating facilities say about the patient. Invoked locally.

Phrases like "PRIMARY VIEW DATA" and then individual treating facility views.

Note: the built with this is in FOIA BUT the code isn't. Presumably the code is in a special VistA in VAEC?
"""     
def checkMPIF_EDAT_REMOTE(rpcName, event, userInfo, customStats):
    
    if not (
        event["transmissionType"] == "O" and
        event["logicalLink"] == "MPIVA"
    ):
        print(userInfo)
        raise Exception(f'Unexpected User/Transmission of {rpcName}')   
    
    # Must use LL as user is outgoing ie/ local user
    customStats["REMOTE"][event["logicalLink"]] += 1
    
    # First short part of ICN
    customStats["PATIENTS"][event["sprSeg"]["_inputParameterList"]["P1"]] += 1
        
    customStats["USERS"][f'{userInfo[1]} [{userInfo[3]}:{userInfo[0]}]'] += 1
    
"""
VAFC REMOTE (PDAT|AUDIT)

PDAT, AUDIT | READ | ALL IN | AAC, Birmingham 

- PDAT is demographics and treating facilities too
- AUDIT is who changed the record (it appears) ie/ text report on logs

[TODO: must see logs behind it; who is concerned?]

return reports on a patient id'ed by ICN|SSN|DFN to remote systems (I only) and 
are only invoked by MPI staff (not machines but real) and Birmingham staff
"""
def checkVAFC_REMOTE(rpcName, event, userInfo, customStats): # PDAT and AUDIT

    """
    Removed (for 663) 200M/521 fix as say other in 663.
        # REM: 200M => 2 is "MPI"
        # ... Note: MPI uses DFN, 521/Birmingham uses SSN or ICN. Saw
        # some error reported back for SSN (invalid SSN) but some SSNs worked
        # userInfo[3] in ["521", "200M"] # only Birmingham and AAC
    """
    if not (
        event["transmissionType"] == "I" # and
    ):
        # Could do:
        # "_inputParameterList"]["P1"] -- DFN or SSN or ICN (ie/ count
        # ??? does an incoming ICN TO DFN come and give this?
        print(userInfo)
        print(json.dumps(event, indent=4))
        raise Exception(f'Unexpected User/Transmission of {rpcName}') 
        
    # MPI or Birm IN
    customStats["REMOTE"][f'{userInfo[2]}:{userInfo[3]}'] += 1
        
    pTypeSearch = re.search(r'(ICN|DFN|SSN)', event["sprSeg"]["_inputParameterList"]["P1"])
    if not pTypeSearch:
        raise Exception(f'Only expect IDs ICN\SSN\DFN in {rpcName} but {event["sprSeg"]["_inputParameterList"]["P1"]}')
    # May ignore    
    customStats["PATIENT_ID_TYPE"][pTypeSearch.group(1)] += 1
    
    # This could be wrong ie/ patient one time as SSN, another as ICN etc but
    # no way to know
    customStats["PATIENTS"][event["sprSeg"]["_inputParameterList"]["P1"]] += 1
    
    customStats["USERS"][f'{userInfo[1]} [{userInfo[3]}:{userInfo[0]}]'] += 1
    
def checkVAFC_LOCAL(rpcName, event, userInfo, customStats):
    if not (
        event["transmissionType"] == "I"
    ):
        # Could do:
        # "_inputParameterList"]["P1"] -- DFN or SSN or ICN (ie/ count
        # ??? does an incoming ICN TO DFN come and give this?
        print(userInfo)
        print(json.dumps(event, indent=4))
        raise Exception(f'Unexpected User/Transmission of {rpcName}') 

    # MPI or Birm IN
    customStats["REMOTE"][f'{userInfo[2]}:{userInfo[3]}'] += 1   
    
    pTypeSearch = re.search(r'(USDVA)', event["sprSeg"]["_inputParameterList"]["P1"])
    if not pTypeSearch:
        raise Exception(f'Only expect IDs USDVA in {rpcName} but {event["sprSeg"]["_inputParameterList"]["P1"]}')
    # May ignore    
    customStats["PATIENT_ID_TYPE"][pTypeSearch.group(1)] += 1
    
    # This could be wrong ie/ patient one time as SSN, another as ICN etc but
    # no way to know
    customStats["PATIENTS"][event["sprSeg"]["_inputParameterList"]["P1"]] += 1
    
    customStats["USERS"][f'{userInfo[1]} [{userInfo[3]}:{userInfo[0]}]'] += 1      
    
"""
VAFC VOA ADD PATIENT

PATIENT DEMO REPORT OR UPDATE

WRITE | ALL IN | Austin (Machine User)

Patient demographic values passed in - DOB, ICN ... ; DFN returned

Note: rpcUtils, ensured not de-identified
"""
def checkVAFC_VOA_ADD_PATIENT(rpcName, event, userInfo, customStats):

    """
    Removing hard code as see a 200M in 653
        
    userInfo[0] == "888888888" and
    userInfo[1] == "PSUSER,APPLICATION PROXY" and
    userInfo[2] == "AUSTIN INFORMATION TECH CTR" and 
    userInfo[3] == "200" # 200M would have been MPI
    # and 12722 as IEN in slot 4
    """                    
    if not (
        event["transmissionType"] == "I" 
    ):
        print(userInfo)
        print(json.dumps(event, indent=4))
        raise Exception(f'Unexpected User/Transmission of {rpcName}')   
                
    # IN
    customStats["REMOTE"][f'{userInfo[2]}:{userInfo[3]}'] += 1     
        
    # Even though know there is one
    customStats["USERS"][f'{userInfo[1]} [{userInfo[3]}:{userInfo[0]}]'] += 1
        
    # TODO: can't handle
    if "_BADPPARSE" in event["sprSeg"]["_inputParameterList"]:
        return 
        
    # Only one P1 - with args for filling in Patient - DOB, NAME, GENDER etc.
    # 009P1(\"DOB\")...(\"FULLICN\") ... 
    if not re.search(r'(DOB|NAME|FULLICN|GENDER)', event["sprSeg"]["_inputParameterList"]["P1"]): # there's more ...
        raise Exception(f'Expect P1 in {rpcName} to have patient details but {event["sprSeg"]["_inputParameterList"]["P1"]}')  
        
    # TODO: parse P1 so know individual patients
    patientSearch = re.search(r'P1\(\"FULLICN\"\)\d{3}([^P+])', event["sprSeg"]["_inputParameterList"]["P1"])
    if not patientSearch:
        raise Exception("Can't parse PATIENT ICN")
    customStats["PATIENTS"][patientSearch.group(1)] += 1
    
"""
Converts both ways - count patients BUT ALSO VACRNR - enforce doesn't work
"""
def checkVAFCTFU_CONVERT_ICN_TO_DFN(rpcName, event, userInfo, customStats):

    checkRPCVistAPlus(rpcName, event, userInfo, customStats, crnrOutAllowed=True)

    customStats["PATIENTS"][event["sprSeg"]["_inputParameterList"]["P1"]] += 1

    if "acks" in event:
        ack = event["acks"][0]
        if "message" in ack:
            rdts = [seg for seg in ack["message"] if seg.split("^")[0] == "RDT"]
            if len(rdts) != 1:
                raise Exception("Expected one and only one RDT")
            # Report not currently available
            reply = rdts[0].split("^")[1] 
            if re.match(r'\d+$', reply):
                reply = "DUZID"
                if event["logicalLink"] == "VACRNR":
                    raise Exception("Don't expect VACRNR to reply properly")
            customStats["REPLY"][reply] += 1
    else:
        customStats["REPLY"][f'ERROR:{event["errorCode"]}'] += 1
        
"""
This remote procedure call will return the MPI Patient Data Inquiry [MPI DATA MGT PDAT MPI] (PDAT) report for a requested ICN.
"""
def checkRG_PRIMARY_VIEW_FROM_MPI(rpcName, event, userInfo, customStats):
    
    if not (
        event["transmissionType"] == "O" and
        event["logicalLink"] == "MPIVA"
    ):
        print(json.dumps(event, indent=4))
        raise Exception(f'Expect {rpcName} to be OUTGOING to MPIVA')
        
    customStats["PATIENTS"][event["sprSeg"]["_inputParameterList"]["P1"]] += 1
    
    customStats["USERS"][f'{userInfo[1]} [{userInfo[3]}:{userInfo[0]}]'] += 1
    
"""
Should be mixed ie/ IO and VISTA both ways -- want to see args/data

PATIENT INSURANCE (ie/ PATIENT Data)

READ | I/O VISTAs | Real Users

Arguments:
- ICN (P1) and Date (P2)
Return:
- just 0's in one RDF or
- #'s ala 2^0 ... but what do they mean in the one RDT?
"""
def checkDGBT_CLAIM_DEDUCTIBLE_PAID(rpcName, event, userInfo, customStats):
        
    checkRPCVistAPlus(rpcName, event, userInfo, customStats, crnrOutAllowed=False)
    
    customStats["PATIENTS"][event["sprSeg"]["_inputParameterList"]["P1"]] += 1
    
"""
PATIENT (as passes ICN)

suppress user => user not supplied inside RPC (as now XWB!); not a USER RPC

Invoke:
- Called 12 or more times per patient for current year ie/ P2 is 3210100 ...

Reply:
- Application failed to return any data OR IBY
... prompts other calls?
"""
def checkIBARXM_QUERY_SUPPRESS_USER(rpcName, event, userInfo, customStats):

    checkRPCVistAPlus(rpcName, event, userInfo, customStats, crnrOutAllowed=False)

    customStats["PATIENTS"][event["sprSeg"]["_inputParameterList"]["P1"]] += 1
    customStats["P2DATES"][event["sprSeg"]["_inputParameterList"]["P2"]] += 1
    
    """
    Removed as 757 has way back to 3110... and full year of 321 (not sure why) as 311 not
    for all of them.
    
    if len(customStats["P2DATES"]) > 12:
        print(customStats["P2DATES"])
        raise Exception("QUERY SUPPRESS USER has > 12 P2 dates in the logs")
    """

"""
PATIENT

pass ICN P1
RDT's ^ info in reply with words like "MEDICARE" OR "no insurance on file"
"""
def checkIBCN_INSURANCE_QUERY_TASK(rpcName, event, userInfo, customStats):

    checkRPCVistAPlus(rpcName, event, userInfo, customStats, crnrOutAllowed=False)

    customStats["PATIENTS"][event["sprSeg"]["_inputParameterList"]["P1"]] += 1

"""
PATIENT 

Write
ICN P1
Details P2 inc 52 ref, seems like drug name too ...
Response if works: one RDT with what looks like an IEN (52 on remote?)
"""
def checkIBARXM_TRANS_DATA(rpcName, event, userInfo, customStats):
    
    checkRPCVistAPlus(rpcName, event, userInfo, customStats, crnrOutAllowed=False)

    customStats["PATIENTS"][event["sprSeg"]["_inputParameterList"]["P1"]] += 1
    if "_P2UNC" in event["sprSeg"]["_inputParameterList"]:
        customStats["DRUGS"][event["sprSeg"]["_inputParameterList"]["_P2UNC"][8]] += 1
    # Bad Parse P2 as well -- seem to be data
    else:
        customStats["DRUGS"]["__BADPARSE"] += 1
        
def checkIBARXM_TRANS_BILL(rpcName, event, userInfo, customStats):
    """
    TODO: parse the p2 - one ex in 653 6/21 and let through
    """
    checkRPCVistAPlus(rpcName, event, userInfo, customStats, crnrOutAllowed=False)

    customStats["PATIENTS"][event["sprSeg"]["_inputParameterList"]["P1"]] += 1
        
"""
PATIENT
I or O
P1-P8
"""
def checkIBECEA_COPAY_SYNCH(rpcName, event, userInfo, customStats):

    checkRPCVistAPlus(rpcName, event, userInfo, customStats, crnrOutAllowed=False)

    customStats["PATIENTS"][event["sprSeg"]["_inputParameterList"]["P1"]] += 1  

"""
PATIENT (LABS)

P1 seems to be ICN (small part) but it's not echo'ed in report

4 Arguments
- IEN? ;ICN small?
- 366?
- Date end day today
- Date one year back

Return Lab Report/ Human Readable Table/Tabbed, different labs and locations
"""
def checkORWLR_CUMULATIVE_REPORT(rpcName, event, userInfo, customStats):

    checkRPCVistAPlus(rpcName, event, userInfo, customStats, crnrOutAllowed=True)

    customStats["PATIENTS"][event["sprSeg"]["_inputParameterList"]["P1"]] += 1
    
"""
P1-P7 - 6, 7 is date range, 1 seems to be Patient IEN;ICN Short, 2 is notes
to ask summary of.

Returns structure (^ ...) in RDTs if there is data.
"""
def checkORWRP_REPORT_TEXT(rpcName, event, userInfo, customStats):
    
    checkRPCVistAPlus(rpcName, event, userInfo, customStats, crnrOutAllowed=True)

    customStats["PATIENTS"][event["sprSeg"]["_inputParameterList"]["P1"]] += 1

    customStats["REPORTS"][event["sprSeg"]["_inputParameterList"]["P2"].split(";")[0]] += 1
    
"""
PATIENT (LABS)

P1 is the IEN?;ICN short combo
P2, P3 are dates

Response: No Data Found | Tabbed Text Report on Labs
"""
def checkORWLRR_INTERIM(rpcName, event, userInfo, customStats):
    
    checkRPCVistAPlus(rpcName, event, userInfo, customStats, crnrOutAllowed=True)

    customStats["PATIENTS"][event["sprSeg"]["_inputParameterList"]["P1"]] += 1
   
""" 
PATIENT
One Argument - a document IEN (not a patient)
Probably part of IFC

Note CAN'T KNOW PATIENT as just get TIU DOC ID
"""
def checkTIU_GET_RECORD_TEXT(rpcName, event, userInfo, customStats):
    
    # CRNR IFC sync in HL7 fully - no need for the pull
    # ... had to allow CRNR as 663 has a TIU GET RECORD TEXT sent to it!
    checkRPCVistAPlus(rpcName, event, userInfo, customStats, crnrOutAllowed=True)

    if "acks" in event:
        ack = event["acks"][0]
        if "message" in ack:
            rdts = [seg for seg in ack["message"] if seg.split("^")[0] == "RDT"]
            ltrdts = [rdt for rdt in rdts if re.search(r'LOCAL TITLE\:', rdt)]
            if len(ltrdts):
                # Take first - as other could be embedded (saw in 757)
                lt = re.sub(r' +$', '', re.search(r'LOCAL TITLE\: (.+)', ltrdts[0]).group(1))
                customStats["LOCAL_TITLES"][lt]
            strdts = [rdt for rdt in rdts if re.search(r'STANDARD TITLE\:', rdt)]
            if len(strdts):
                st = re.sub(r' +$', '', re.search(r'STANDARD TITLE\: (.+)', strdts[0]).group(1))
                customStats["STANDARD_TITLES"][st] += 1
    
    customStats["DOCUMENTS"][
    f'{event["logicalLink"]}:{event["sprSeg"]["_inputParameterList"]["P1"]}'] += 1
    
# VACRNR -- see 4 and see if any IN --- want no users from there 
    
"""
General purpose check for RPCs that I/O between VistAs or VistA and VAFHIE or VACRNR
"""
def checkRPCVistAPlus(rpcName, event, userInfo, customStats, crnrOutAllowed=False):

    """
    Don't Expect VACRNR to 'work'
    ... and universal check below enforces no incoming
    """
    def handleVACRNR(event, crnrOutAllowed):
    
        # VIRS referral received in Spokane CERNER EHRM ... Results will result in JLV
        # ... seen in 663 (from 668)
        # Provider Note or 687 saw Prodiatry Outpatient Note
        MULTI_RDT_STRING_EXPECTED = "EHRM TITLE:"
    
        if not crnrOutAllowed:
            raise Exception(f"Don't expect dispatch of {rpcName} to Cerner")
        
        if event["status"] == "ERROR":
            customStats["VACRNR"][f'ERROR:{event["errorCode"]}'] += 1
            return
    
        if "acks" not in event:
            raise Exception("Not Error for VACRNR - where's the ACK")
        ack = event["acks"][0]
        rdts = [seg for seg in ack["message"] if seg.split("^")[0] == "RDT"]
        if len(rdts) != 1:
            if not sum(1 for rdt in rdts if re.search(MULTI_RDT_STRING_EXPECTED, rdt)):
                print(json.dumps(event, indent=4))
                raise Exception("Expected one and only one RDT in VACRNR ACK")
            customStats["VACRNR"]["REPLY:EHRM_NOTE_RECEIVED"] += 1
            return
        # Report not currently available
        reply = rdts[0].split("^")[1] 
        if reply != "Report not currently available":
            raise Exception("Not error to VACRNR but expected it to be Report not available") # ICN to and REPORT RPCs
        customStats["VACRNR"]["REPLY:REPORT_NOT_CURRENTLY_AVAILABLE"] += 1

    if event["transmissionType"] == "O":
        # see the CRNR
        if not re.match(r'VA([A-Z]{3}|FHIE|CRNR)$', event["logicalLink"]):
            raise Exception(f'Unexpected other side (not a VistA) for {rpcName} - {event["logicalLink"]}')
        if not (re.match(r'VA[A-Z]+$', event["logicalLink"]) or event["logicalLink"] in ["VAFHIE", "VACRNR"]):
            raise Exception(f'Expected OUT from I/O RPCs to be just to VistAs or VAFHIE or VACRNR but {event["logicalLink"]}')
        customStats["REMOTE_VP_O"][event["logicalLink"]] += 1
        if event["logicalLink"] == "VACRNR": # OUT (see never IN in check below)
            handleVACRNR(event, crnrOutAllowed)
    else: # as user is real - "200", "776", "200M"
        if not (re.match(r'\d{3}[A-Z\d]{0,2}$', userInfo[3]) or userInfo[3] in ["6569AA"]): # allowing BIRMINGHAM VAMC (521) even though a special elsewhere
            # May not be precise enough
            raise Exception(f"** WARNING: only expect INCOMING from VistA station Number but {userInfo[2]}:{userInfo[3]}") # ST CLOUD 531 6569AA -- TODO tighten
        customStats["REMOTE_V_I"][f'{userInfo[2]}:{userInfo[3]}'] += 1
    
    customStats["USERS"][f'{userInfo[1]} [{userInfo[3]}:{userInfo[0]}]'] += 1
    customStats["IO"][event["transmissionType"]] += 1
    
# Overall - may move into the general ABOUT
XWB_BUILDS_DESCR = {

    "protocol": "XWB RPC SUBSCRIBER", 
    
    "build": "XWB*1.1*12", # from 2000, remote data views setup (but then others came in?)

    "__comment": """Aside on Build: newer build XULM LOCK DICTIONARY (8993) [TODO: walk all build components and get the pieces ... and fill em in? ie/ redo Build Directory]"""
}
    
# ######################## Reduction of RPCs ##################################
    
"""
Do per RPC Infos based on Logs ie/ their form and use
"""
def makeRPCLogInfos(stationNo):

    rpcLogInfoByName = {}
    
    spqTBRHL7Reduction = reduceSPQTBRHL7(stationNo)
    spqEventsByRPCName = spqTBRHL7Reduction["spqEventsByRPCName"]
    hl7TemplateMaker = HL7TemplateMaker(False)
    inLL = "" # derive the one and only inbound LL ex/ VAWWW for 687
    for rpcName in spqEventsByRPCName:
                        
        perRPCInfo = {
            "count": 0,
            "countIn": 0,
            "countOut": 0,
            "errorCodeCount": Counter(),
            "rdtCountCount": Counter(),
            "userCount": Counter(),
            
            "customStats": defaultdict(lambda: Counter())
        }
        rpcLogInfoByName[rpcName] = perRPCInfo
        
        for event in spqEventsByRPCName[rpcName]:
                            
            if "priority" in event and event["priority"] != "IMMEDIATE":
                raise Exception("Expected all SPQs to be immediate")           
               
            perRPCInfo["count"] += 1
                
            sprSegINP = event["sprSeg"]["_inputParameterList"] 
            # defn will fix pcount - make sure consistent (as dev a defn, 
            # will see error first time through)
            thisPCount = sum(1 for p in sprSegINP if re.match(r'P\d+(\(\d+\))?$', p))
                
            userInfo = sprSegINP["_XWBESSOUNC"]
            perRPCInfo["userCount"][userInfo[0]] += 1 # SSN and it is mandatory
            
            if event["transmissionType"] == "I":
                perRPCInfo["countIn"] += 1
                if inLL == "":
                    inLL = event["logicalLink"]
                elif inLL != event["logicalLink"]:
                    raise Exception("Inconsistent In LL")
                # ie/ IN From a Cerner user: SNO
                # ... enforcing ERROR or no reply for OUT to Cerner in RPC specials
                if userInfo[3] == "200CRNR": 
                    raise Exception("Don't EXPECT any incoming from Cerner")
            else:
                perRPCInfo["countOut"] += 1
            
            """
            Checks by RPC (bound the expected too) and custom stats
            """
            if re.match(r'VAFC REMOTE', rpcName):
                checkVAFC_REMOTE(rpcName, event, userInfo, perRPCInfo["customStats"])
            elif re.match(r'VAFC LOCAL', rpcName):
                checkVAFC_LOCAL(rpcName, event, userInfo, perRPCInfo["customStats"])
            elif re.match(r'XUS MVI NEW PERSON', rpcName):
                checkXUS_MVI_NEW_PERSON(rpcName, event, userInfo, perRPCInfo["customStats"])
            elif re.match(r'MPIF (GET|PURGE) VHIC', rpcName):
                checkMPIF_GETPURGE_VHIC(rpcName, event, userInfo, perRPCInfo["customStats"])
            elif re.match(r'MPIF DOD ACTIVITY', rpcName): 
                checkMPIF_DOD_ACTIVITY_CHECK(rpcName, event, userInfo, perRPCInfo["customStats"])            
            elif re.match(r'VAFC VOA ADD PATIENT', rpcName):
                checkVAFC_VOA_ADD_PATIENT(rpcName, event, userInfo, perRPCInfo["customStats"])
            elif re.match(r'MPIF EDAT REMOTE', rpcName):
                checkMPIF_EDAT_REMOTE(rpcName, event, userInfo, perRPCInfo["customStats"])
            elif re.match(r'DGBT CLAIM DEDUCTIBLE PAID', rpcName):
                checkDGBT_CLAIM_DEDUCTIBLE_PAID(rpcName, event, userInfo, perRPCInfo["customStats"])
            elif re.match(r'IBARXM QUERY SUPPRESS USER', rpcName):
                checkIBARXM_QUERY_SUPPRESS_USER(rpcName, event, userInfo, perRPCInfo["customStats"])
            elif re.match(r'IBCN INSURANCE QUERY TASK', rpcName):
                checkIBCN_INSURANCE_QUERY_TASK(rpcName, event, userInfo, perRPCInfo["customStats"])
            elif re.match(r'IBARXM TRANS DATA', rpcName):
                checkIBARXM_TRANS_DATA(rpcName, event, userInfo, perRPCInfo["customStats"])
            elif re.match(r'IBARXM TRANS BILL', rpcName):
                checkIBARXM_TRANS_BILL(rpcName, event, userInfo, perRPCInfo["customStats"])
            elif re.match(r'IBECEA COPAY SYNCH', rpcName):
                checkIBECEA_COPAY_SYNCH(rpcName, event, userInfo, perRPCInfo["customStats"])
            elif re.match(r'ORWLR CUMULATIVE REPORT', rpcName):
                checkORWLR_CUMULATIVE_REPORT(rpcName, event, userInfo, perRPCInfo["customStats"])
            elif re.match(r'ORWRP REPORT TEXT', rpcName):
                checkORWRP_REPORT_TEXT(rpcName, event, userInfo, perRPCInfo["customStats"])
            elif re.match(r'ORWLRR INTERIM', rpcName):
                checkORWLRR_INTERIM(rpcName, event, userInfo, perRPCInfo["customStats"])
            elif re.match(r'TIU GET RECORD TEXT', rpcName):
                checkTIU_GET_RECORD_TEXT(rpcName, event, userInfo, perRPCInfo["customStats"])
            elif re.match(r'VAFCTFU CONVERT ICN TO DFN', rpcName):
                checkVAFCTFU_CONVERT_ICN_TO_DFN(rpcName, event, userInfo, perRPCInfo["customStats"])
            elif re.match(r'RG PRIMARY VIEW FROM MPI', rpcName):
                checkRG_PRIMARY_VIEW_FROM_MPI(rpcName, event, userInfo, perRPCInfo["customStats"])                
            elif rpcName not in ["ORQQCN GET MED RESULT DETAILS", "MPIF REMOTE SPI"]:
                raise Exception(f"Unexpected RPC {rpcName}")
                
            """
            −	RPC: VAFC LOCAL GETCORRESPONDINIGIDS returns Treating Facility information
            VAFC LOCAL GETCORRESPONDINGSIDS
            """
                
            if event["status"] == "ERROR":
                perRPCInfo["errorCodeCount"][event["errorCode"]] += 1
                if "acks" in event:
                    print(json.dumps(event, indent=4))
                    raise Exception("Don't expect 'acks' in event of ERROR but what made the error? - TODO: lookup that MSA!")
                continue  
                
            if "acks" not in event:
                raise Exception("Acks missing from event") # won't happen - see below
                                
            if len(event["acks"]) != 1: # may not be true!
                raise Exception("Expect at most one ACK")
            ackInfo = event["acks"][0]
            psegmentsAck = hl7TemplateMaker.parseMessage(ackInfo["message"]) 
            
            # TODO: add check for RDT has > 1 argument ie/ ^1^... if > 1 of them
            # but if for document then no third argument.
            rdtsAck = [psegment for psegment in psegmentsAck if psegment["segmentType"] == "RDT"]
            perRPCInfo["rdtCountCount"][len(rdtsAck)] += 1  
            
            if "nonErrorExample" not in perRPCInfo or len(rdtsAck) > perRPCInfo["nonErrorExample"]["_rdtCount"]:
                perRPCInfo["nonErrorExample"] = event
                event["_messageCategory"] = "SPQ Query"
                event["_rdtCount"] = len(rdtsAck)
    
    return spqTBRHL7Reduction["overallStats"], rpcLogInfoByName

def reduceSPQTBRHL7(stationNo):

    tmpLocn = "{}{}/{}".format(VISTA_DATA_BASE_DIR, stationNo, "TmpWorking")
    
    try:
        spqTBRHL7Reduction = json.load(open(f'{tmpLocn}/spqTBRHL7Reduction.json'))
    except:
        pass
    else:
        return spqTBRHL7Reduction
    
    hloSystemParameters = lookupConfig779_1(stationNo)
    spq_tbr_772_773, skippedAsNotProtocolTotal, _772OrphansTotal = gatherAndQA772_773OfProtocol(stationNo, int(hloSystemParameters["normal_msg_retention_days"]), int(hloSystemParameters["bad_message_retention_days"]), "XWB RPC SUBSCRIBER", [])
    
    hl7TemplateMaker = HL7TemplateMaker(False)
    
    spqSuccessCount = 0
    spqErrorCount = 0
    tbrNoSPQEvents = []
    spqEventById = {}
    spqSuccessDaysCount = Counter()
        
    """
    Note no simple ACK in this case. Only APP ACK. And it is a TBR. If an
    error then RDT'less (still no examples). For the TIU Message we want, there
    is no delayed request and hence no OK TBR (w/o RDT) and the query token
    is meaningless.
    
    See XWB2HL7B REMOTERPC for more (ie/ APP ACK, RDT, error and could
    delve into tokens were that needed later)
    """
    for _773IEN in spq_tbr_772_773:
    
        # going to group em into spqEventById
        event = makeBasicHL7Event(spq_tbr_772_773[_773IEN], "XWB RPC SUBSCRIBER")
        _773 = spq_tbr_772_773[_773IEN]["_773"]
        _772 = spq_tbr_772_773[_773IEN]["_772"]
        
        psegments = hl7TemplateMaker.parseMessage(event["message"]) 

        mt = event["messageType"]
        # message = ":".join(messageLines)
                
        if re.search('SPQ', mt):
            spqEventById[event["messageId"]] = event
            event["sprSeg"] = psegments[1] # for line parse below
            sprSegInfo = hl7TemplateMaker.parseSPR(event["sprSeg"]["_raw"])
            event["rpcName"] = sprSegInfo["_inputParameterList"]["RPC"]
            if event["status"] == "ERROR":
                spqErrorCount += 1
            else:
                spqSuccessCount += 1
                spqSuccessDaysCount[event["created"].split("T")[0]] += 1
            continue
            
        if not re.search(r'TBR', mt):
            raise Exception("Only expect TBR at this stage")
            
        # REM: only subset have _ackTo773IEN as many SPQs purged!
        if "acknowledgeTo" not in event:
            raise Exception("Assumed Protocol reducer recorded ack to message for all TBRs")
         
        if event["status"] == "ERROR":
            print("ERROR TBR", json.dumps(psegments, indent=4))
            raise Exception("Didn't expect error TBR ie/ APP ACK as error")
            
        # TBD: what if lack of priority == deferred -- see > 1 TBR per
        if "priority" in event and event["priority"] != "IMMEDIATE":
            raise Exception("Expected only IMMEDIATE priority") # in 687
            
        """
        ie/ WWW
        <------- VAWWW (with non www stationNo Id)
        ----O--- same non stationNo Id TBR APP ACKed
        """
        if event["transmissionType"] == "O:OUTGOING" and re.match(stationNo, event["acknowledgeTo"]):
            raise Exception("Expect ACK outgoing to be to non local/remote message id")

        # Should be rare - fell into window where came in just after purge cut off
        # while its SPQ was purged.
        if event["acknowledgeTo"] not in spqEventById:
            tbrNoSPQEvents.append(event)
            continue
            
        """
        Ignoring QAK for now
        
        # "QAK"_HL("FS")_XWB2QTAG_HL("FS")_$S($G(HLERR)]"":"AE",1:"OK") (in XWB2HL7B)
        # ... see above. Appears not important for me as immediate!
        qakSegment = [psegment for psegment in psegments if psegment["segmentType"] == "QAK"][0]
        queryTag = qakSegment["queryTag"]
        queryTagBase = queryTag.split("_")[0] # ie/ < 0, 1, 2 ... (why these?)
        """
            
        # Never expect to TBR ACK twice - "acks" plural for compatibility with ORM
        if "acks" in spqEventById[event["acknowledgeTo"]]:
            print(json.dumps(psegments, indent=4))
            raise Exception("> 1 TBR in response")        
        """
        TMP Exception to show new information
        
        # spq773["error_message"] == "Write Error" too

        TODO: PHASE 2 -  MUMPS shows an RDT'less ACK would
        be sent with an error code. But no examples. 
        
        Probably because though there are ERROR SPQs, their TBR ACK ERROR are 
        not themselves errors and so were purged. Just unlucky that no 
        error SPQs in final days of clone.  
        """
        if spqEventById[event["acknowledgeTo"]]["status"] == "ERROR":
            raise Exception("Hadn't seen TBR ACK ERROR before for write error SPQ (but wanted to!) - seems like TBRs signalling errors aren't stored") # ie/ if main is ERROR then would expect RDTless TBR with Error code in MSA
             
        # Only ever one but using "acks" for backward compatibility with other 
        # interactions
        spqEventById[event["acknowledgeTo"]]["acks"] = [event] # an app ack!
        
    noAcks = [id for id in spqEventById if "acks" not in spqEventById[id]]
    for id in noAcks:
        del spqEventById[id]
        
    overallStats = {
        "skippedAsNotProtocolCount": skippedAsNotProtocolTotal, # out of scope
        "protocolCount": len(spq_tbr_772_773),
        # There are lingered TBRs as no 
        "tbrNotSPQCount": len(tbrNoSPQEvents),
        # ignoring lingering _772's reported in the protocol reduction
        "spqNoAckCount": len(noAcks), # rare 663 only - was suppressed

        # all SPQs have a TBR in logs I've seen except the ERRORs
        "spqSuccessCount": sum(1 for id in spqEventById if re.match(r'SUCCESS', spqEventById[id]["status"])),
        "spqOtherCount": sum(1 for id in spqEventById if not re.match(r'(SUCCESS|ERROR)', spqEventById[id]["status"])),
        "spqErrorCount": sum(1 for id in spqEventById if spqEventById[id]["status"] == "ERROR"),
        "spqRemoteCount": sum(1 for id in spqEventById if not re.match(stationNo, id)),
        
        "spqSuccessDaysCount": spqSuccessDaysCount
    }
    print(f'Skipped as not protocol: {overallStats["skippedAsNotProtocolCount"]:,}')
    print(f'Of protocol: {overallStats["protocolCount"]:,}')
    print(f'TBR, no SPQ (as not purged): {overallStats["tbrNotSPQCount"]:,}')    
    print(f'SPQ no ACK (663 only so far): {overallStats["spqNoAckCount"]:,}')
    print(f'SPQ Success: {overallStats["spqSuccessCount"]:,}')
    print(f'SPQ Other: {overallStats["spqOtherCount"]:,}')
    print(f'SPQ Error: {overallStats["spqErrorCount"]:,}')
    # See protocol dump's dates. Will see all for days outside purge days
    # ... probably won't report as not significant
                
    print("Serializing TMP Cache of SPQ TBRs reduced")
    spqEventsByRPCName = defaultdict(list)
    for id in spqEventById:
        event = spqEventById[id]
        spqEventsByRPCName[event["rpcName"]].append(event)
    spqTBRHL7Reduction = {
        "stationNo": stationNo,
        "description": "SPQs with matched TBRs",
        "overallStats": overallStats,
        "spqEventsByRPCName": spqEventsByRPCName
    }
        
    json.dump(spqTBRHL7Reduction, open(f'{tmpLocn}/spqTBRHL7Reduction.json', 'w'), indent=4)
    
    return spqTBRHL7Reduction
    
# ##################### Cerner LL and Institution ####################
    
"""
Institution and Logical Link for Cerner

For LL: VACRNR
- tcp_ip_address 10.247.62.26
- dns_domain hc-vdif-ent-a.va.gov

For 4: CERNER
- parent is AUSTIN INFORMATION TECH CTR
- station_number 200CRNR
- official_va_name CERNER
- facility_type VAMC
- location_timezone CENTRAL[3]

For reports - just to check 
"""
def dumpCernerIandL(stationNo):
    # Cerner has stationNo, 200CRNR
    from fmqlreports.webReportUtils import reduce4
    _4s = reduce4(stationNo)
    for _4Id in _4s:
        _4 = _4s[_4Id]
        print(_4["label"])
        if _4["label"] == "CERNER":
            cerner4 = _4
            break
    print(json.dumps(cerner4, indent=4))
    from webReportHL7 import reduce870
    _870s = reduce870(stationNo)
    for _870Id in _870s:
        _870 = _870s[_870Id]
        if _870["label"] == "VACRNR":
            cernerLL = _870
            break
    print(json.dumps(cernerLL, indent=4))
    
"""
For ORWRP REPORT TEXT 
- references from 101.24 ... higher levels are national (>=IEN 1000)
[Prelim to webReport on this report text ... note the fhie ref]
  - use rpc to break down/gather
- dump the SPQ exs

Interesting:
- 668 remote only for ORWRP_REPORT_TEXT and ORQQPX IMMUNE LIST (and only 1 of them)
- note that ORWLR CUMULATIVE REPORT and ORWLRR INTERIM (both only in local) both appear in SPQ report
  - seems like all CUM and INT are remote too (ie/ though LOCAL setup, call remote)
- strange: 172 entries for SPO and WWW; 175 for COS and even the locals overlap

ie/ want to tie [1] report defn to [2] invoked report AND tie invocation to treatment facility list entry for patient?

CPRS uses RPCs to control screen:
    RPC_NAME: ORWRP COLUMN HEADERS
    RPC_TAG: GETCOL
    RPC_ROUTINE: ORWRP
    RPC_RETURN_VALUE_TYPE: ARRAY
    RPC_DESCRIPTION: 
        Get list of Column headers for a ListView type report from file 101.24.
<---- what does it use to get the active 101.24's?

TODO: Build + Oncology not filled in

    From: https://foia-vista.worldvista.org/Patches_By_Application/OR-ORDER%20ENTRY_RESULTS%20REPORTING/OR-3_SEQ-351_PAT-312.TXT
    > This patch adds a new Pharmacy report to the Clinical Reports on the
    > Reports Tab in CPRS (Computerized Patient Record System)
    > 
    > The All Medications report supports Remote Data Views (RDV) from remote
    > Facilities.
    > 
    > also be used by the VistaWeb application to create the same report
    > in VistaWeb <---- so VistAWeb -- JLV?
    >
    > This patch re-exports entries with internal numbers greater than 999
    > and entries 3 (ORRP AP ALL) and 24 (ORL ANATOMIC PATHOLOGY)
    > from the OE/RR Reports file (#101.24).
    
    Note in FOIA: http://localhost:9100/query?fmql=DESCRIBE%20101_24-1004&format=HTML ... DISCHARGE SUMMARIES is the first (beyond 3, 23, 24)
    
    TODO -- compare the 101.24 files across VistAs ... see if same ids
    ---- will do table of the Standard (> 999 + other checks)
"""

def webReportORWRP_REPORT_TEXT(stationNo, enforceTFL=False):

    # TMP HERE: will move off to TFL report - only QA in here
    def reduceTFLByPatient(stationNo):
        """
        Keeping all and not just remote 'institution' so could report
        on source of TFL data (assigning_authority, source_id)
        
        TODO from typer report:
        - institution spread see biggies are central systems vs "actually treating facilities"? Are these filtered out by type before HL7?
          (MEDTRONIC is in at .02% => > VistAs! but also these are institutions)
        - see # per patient spread ie/ 100 patients have 50 entries etc
        - patient id as "Patient Internal Id" etc etc
        ---
        source_id is 90%
        ---
        - date_last_treated only 21% => many entries just central records?
        - adt_... reason -- nearly the same # => last treated from HL7
        ---
        - signed roi is 2% (probably a sub class of inserts)
        
        From Examples here:
        - see Institution of "Walgreens Pharmacies", "VETS 360", ... with NO
        HL7 field
        - if Portland etc => PI:Patient Internal Identifier (IEN) in source id and HL7 and     
        last treated => could subset! source_type PI, assigning auth USVHA (that's also
        used by Card System so not enough to isolate VistAs)
        - if outside hospital then like others nationals (no HL7 or date) and
        the assigning_authority OID must be that hospital's id!
        - VA PROVISIOING SYSTEM uses ICN + USDVA (assigning) + PN:Person number as source 
        type. No HL7 or date.
        - Veteran ID Card system seems to be IEN in it, no HL7, no date => it is a Vista?
        - Ditto for VBA BRLS
        - National Cemetary ... USNCA .. so 
        """
        tmpWorkingDir = f'{VISTA_DATA_BASE_DIR}{stationNo}/TmpWorking/'
        tflFL = f'{tmpWorkingDir}all391_91ByPIEN.db'
        if os.path.isfile(tflFL):
            print(f'Returning pre-made 391.91 Reduction')
            return shelve.open(tflFL, flag='r')
        print("391.91 not yet reduced - reducing ...")    
        dataLocn = f'{VISTA_DATA_BASE_DIR}{stationNo}/Data/'
        resourceIter = FilteredResultIterator(dataLocn, "391_91")
        byPatientIEN = shelve.open(tflFL, writeback=True)
        for resource in resourceIter:
            if "patient" not in resource:
                continue # 10 in 687 lack
            patientIEN = str(resource["patient"]["id"].split("-")[1])
            if patientIEN not in byPatientIEN:
                byPatientIEN[patientIEN] = [resource]
                continue
            byPatientIEN[patientIEN].append(resource)
        byPatientIEN.close()
        print("Flushing 391.91 reduction and returning")
        return shelve.open(tflFL, flag='r')
        
    """
    TODO: improve more context ie/ of x, ...
    """
    def mu101_24WORWRP_REPORT_TEXTRemote(stationNo):
    
        # FIRST UP - The Report Types available for ORWRP REPORT TEXT
        dataLocn = f'{VISTA_DATA_BASE_DIR}{stationNo}/Data/'
        resourceIter = FilteredResultIterator(dataLocn, "101_24")
        reportTypeById = {}
        tbl = MarkdownTable([
            ":Name",
            ":Heading",
            ":ID",
            "National or Local", # IEN Based
            "Tab",
            "FHIE?"
        ])
        for i, resource in enumerate(resourceIter, 1):
            if "rpc" not in resource:
                continue
            """
            Id form is
        
                {tab.split(":")[0]}:{id__02}:{heading | descriptive text.upper()}
    
            Note: that "R": is the default so won't appear in the P2 of the messages
            """
            tabNId = f'{resource["tab"].split(":")[0]}:{resource["id__02"]}'
            if tabNId in reportTypeById:
                print(json.dumps(reportTypeById[tabNId], indent=4))
                print(json.dumps(resource, indent=4))
                raise Exception("Did not expect report type to be in twice - overlapping id n tab's ie/ expected unique id in any given tab") 
            ienInt = int(resource["_id"].split("-")[1])
            # I Y>999!(Y=3)!(Y=23)!(Y=24)
            localOrNational = "NATIONAL" if ienInt > 999 or ienInt in [3, 23, 24] else "LOCAL"
            resource["local_or_national"] = localOrNational
            if resource["rpc"]["label"] != "ORWRP REPORT TEXT":
                continue
            if "remote" not in resource:
                if "fhie_data" in resource:
                    raise Exception("Why FHIE when not remote")
                continue # only want go remote
            reportTypeById[tabNId] = resource
            row = [
                resource["name"],
                resource["heading"],
                tabNId,
                f'{localOrNational} [{ienInt}]',
                resource["tab"].split(":")[1],
                "YES" if "fhie_data" in resource else "&nbsp;"
            ]
            tbl.addRow(row)
            # print(json.dumps(resource, indent=4))
        mu = f'Of <span class="yellowIt">{i}</span> report types defined in _101.24_, <span class="yellowIt">{len(reportTypeById):,}</span> involve the RPC _ORWRP REPORT TEXT_ dispatched to other VistAs and VAFHIE using HL7/SPQ ...\n\n'
        mu += tbl.md() + "\n\n"
        return mu, reportTypeById
        
    mu = TOP_MD_TEMPL.format("{} SPQ Reports (ORWRP REPORT TEXT)".format(stationNo))
    
    mu += "# Reports with _ORWRP REPORT TEXT_\n\n"
    
    mu += """Physicians select _Patient \"Rollup\" Reports_ in various places in _CPRS_, but mainly in the _Reports Tab_. 
  * Report types are defined in VistA file _101.24_ 
  * Per patient reports are built by VistA using invocations of the RPC _ORWRP REPORT TEXT_ sent to other VistAs and VAFHIE 
  * The remote sources of patient data is specified in the _Treating Facility List_, file _391.91_. 
  * The RPC calls are made using the SPQ/HL7 mechanism.
    
"""

    mu += """__Potential Cerner Migration Issue:__ as VistAs move to Cerner, more and more  HL7/SPQ-carried _ORWRP REPORT TEXT_ calls will not be fulfilled. This means the reports invoked by Physicians in unmigrated centers will increasingly be incomplete. 
    
  * From Columbus - whose Treating Facility List has VACRNR - Cerner responds to requests with _"Report not currently available"_. Perhaps this message should be more specific and explicit warn doctors that there _may be_ information in Cerner but it wasn't returned
  * These "report fetches" could be supported by Cerner with a Proxy Service that processes HL7/SPQs and calls Cerner for appropriate patient data using FHIR or an equivalent mechanism. This would leave __CPRS reporting unaffected by migration__
  
"""

    meta = metaOfVistA(stationNo)                                        
    mu += "The following describes the report types and specific report creation in a copy of _{}_ VistA cut on {}.\n\n".format(meta["name"], meta["cutDate"])  

    tmu, reportTypeById = mu101_24WORWRP_REPORT_TEXTRemote(stationNo) # add usage so comes second
    mu += tmu
    
    # SECOND - invocation of the reports - OUT (ie/ sent out to others)
    # TODO: the one "LOCAL" ... is it really "LOCAL" across the VistAs
    spqTBRHL7Reduction = reduceSPQTBRHL7(stationNo)
    spqEventsByRPCName = spqTBRHL7Reduction["spqEventsByRPCName"]
    if "ORWRP REPORT TEXT" not in spqEventsByRPCName:
        return
    errorCnt = 0
    inCnt = 0
    byPatientP1 = Counter()
    patientICNs = set()
    patientIENs = set()
    reportTypePatientLinks = defaultdict(lambda: defaultdict(lambda: Counter()))
    reportTypeCounts = Counter()
    firstTime = ""
    lastTime = ""
    vaCRNRReportNA = 0
    vaCRNRsNonSuccess = 0
    # Gathering and Enforcing
    for spqEvent in spqEventsByRPCName["ORWRP REPORT TEXT"]:
        if spqEvent["status"] == "ERROR":
            errorCnt += 1
            continue
        if spqEvent["transmissionType"] == "I":
            inCnt += 1
            continue
        lastUpdate = spqEvent["lastUpdate"]
        if firstTime == "" or lastUpdate < firstTime:
            firstTime = lastUpdate
        if lastTime == "" or lastTime < lastUpdate:
            lastTime = lastUpdate
        ll = spqEvent["logicalLink"]
        if ll == "VACRNR":
            if spqEvent["status"] == "SUCCESSFULLY COMPLETED":
                rdts = [seg for seg in spqEvent["acks"][0]["message"] if re.match(r'RDT', seg)]
                if not (len(rdts) == 1 and rdts[0] == "RDT^Report not currently available"):
                    raise Exception("Success VACRNR not just report not available")
                vaCRNRReportNA += 1
            else:
                vaCRNRsNonSuccess += 1
        sprSegINP = spqEvent["sprSeg"]["_inputParameterList"]
        p1 = sprSegINP["P1"]
        byPatientP1[p1] += 1 # multiple per - one to each site in TFL?
        patientIEN = p1.split(";")[0]
        patientIENs.add(patientIEN)
        if len(p1.split(";")) > 1:
            patientICNs.add(p1.split(";")[1])            
        p2 = sprSegINP["P2"]
        p2First = p2.split(";")[0]
        if sprSegINP["P3"]: # ONCOLOGY
            if sprSegINP["P3"] != "0" and not (len(p2First.split(":")) == 1 and p2First == "1"): # !=0 added for BOI TODO
                print(json.dumps(spqEvent, indent=4))
                raise Exception("Only expect P3 set for Report Type 1 which we can find in types")
            continue
        if len(p2First.split(":")) not in [2, 3]:
            print(p2First, json.dumps(spqEvent, indent=4))
            raise Exception("Expected [Tab]:ID:Name as P2 now")
        if len(p2First.split(":")) == 3:
            if p2First.split(":")[0] == "R":
                print(json.dumps(spqEvent, indent=4))
                raise Exception("Expect R to be defaulted")
            reportTypeId = f'{p2First.split(":")[0]}:{p2First.split(":")[1]}'
            heading = p2First.split(":")[2]
        else: # 2
            reportTypeId = f'R:{p2First.split(":")[0]}'
            heading = p2First.split(":")[1]
        if reportTypeId not in reportTypeById: # TODO: be neater
            if reportTypeId.split(":")[0] == "R":
                if re.sub(r'^R', 'L', reportTypeId) not in reportTypeById:
                    print(json.dumps(spqEvent, indent=4))
                    raise Exception(f'Unknown report type id: {reportTypeId}')
                else:
                    reportTypeId = re.sub(r'^R', 'L', reportTypeId) # 757 needed this
        reportTypePatientLinks[reportTypeId][patientIEN][ll] += 1
        reportTypeCounts[reportTypeId] += 1
        reportType = reportTypeById[reportTypeId]
        """
        if reportType["local_or_national"] != "NATIONAL":
            print(reportType)
            raise Exception("Don't expect non nationals to send out")
        """
        itsHeading = reportType["heading"]
        itsHeading = re.sub(r'\&', '\\\\T\\\\', itsHeading) # escape & to \T\
        if itsHeading.upper() != heading:
            print(f'** WARNING: Unexpected Heading value in P3 for type: {heading} vs expected {itsHeading}') # only 757 - seems extra after \
    if len(patientIENs) != len(byPatientP1): # doing IENs and not ICN as see one in 757 w/o ICN
        raise Exception("Expected P1 to be IEN;ICN and so equal # ICN")
    hl7DaysGap = (datetime.strptime(lastTime, "%Y-%m-%dT%H:%M:%S") - datetime.strptime(firstTime, "%Y-%m-%dT%H:%M:%S")).days + 1 
          
    tbl = MarkdownTable([":Heading", ":ID", "#", "Patient #", "Local or National", "# Links [Patients]"])  
    lls = set(ll for rt in reportTypePatientLinks for p in reportTypePatientLinks[rt] for ll in reportTypePatientLinks[rt][p])
    ps = set(p for rt in reportTypePatientLinks for p in reportTypePatientLinks[rt])
    # Only doing Outbound as inbound is "bitty" ie/ other sites assembling
    for rt in sorted(reportTypePatientLinks, key=lambda x: reportTypeCounts[x], reverse=True):
        reportType = reportTypeById[rt]
        itsHeading = reportType["heading"]
        lCountPatientCount = Counter()
        for p in reportTypePatientLinks[rt]:
            lCountPatientCount[len(reportTypePatientLinks[rt][p])] += 1
        lCountPatientCountMU = ", ".join([
            f'{cnt} [{lCountPatientCount[cnt]}]' for cnt in lCountPatientCount
        ])
        tbl.addRow([
            f'__{itsHeading}__',
            rt,  
            reportTypeCounts[rt],
            len(reportTypePatientLinks[rt]),
            reportType["local_or_national"],
            lCountPatientCountMU
        ])
    mu += f'In the last {hl7DaysGap} full days of this VistA copy (full HL7 logs are only kept for this number of days), _ORWRP REPORT TEXT_ was sent out to <span class="yellowIt">{len(lls)}</span> VistAs and VAFHIE for <span class="yellowIt">{len(reportTypePatientLinks)}</span> report types about <span class="yellowIt">{len(ps)}</span> patients ...\n\n'  
    mu += tbl.md() + "\n\n"
    
    """
    3. ENFORCE/QA: the Treatment Facility List (391.91) for the Patients - patientICNs or 
    patientIENs
    
    VAFHIE == AUSTIN INFORMATION TECH CTR - 6112
    
    VAPTH is 870 for PITS... 646 Instit
    VALOM ... 605
    
    Outside Hospitals (UC Davis etc) has 4's and parent facility of AUSTIN (6112)
    """
    # FULL GUY WITH MANY REPORTs to 4 LL's to look at including FHIE ...
    # ... 7228413
    #         if re.match(r'7228413', p1):
    def enforce391_91(stationNo):
    
        _870s = reduce870(stationNo)
        _870LabelByIIEN = {}
        for _870Id in _870s:
            _870 = _870s[_870Id]
            if "institution" not in _870s[_870Id]:
                continue
            _870LabelByIIEN[_870["institution"]["id"].split("-")[1]] = _870["label"]
        institByIEN = reduce4(stationNo)
            
        _391_91ByPIEN = reduceTFLByPatient(stationNo)
        patientRTLinks = defaultdict(lambda: defaultdict(lambda: Counter()))
        for rt in reportTypePatientLinks:
            for p in reportTypePatientLinks[rt]:
                for ll in reportTypePatientLinks[rt][p]:
                    patientRTLinks[p][rt][ll] += reportTypePatientLinks[rt][p][ll]
        institIENsW870 = set()
        institIENsNo870 = set() 
        for patientIEN in patientIENs:
            patientIEN = str(patientIEN)
            if patientIEN not in _391_91ByPIEN:
                raise Exception("Unexpected - patient with TFL directed HL7 not in TFL")
            print(f'Patient {patientIEN} - {len(_391_91ByPIEN[patientIEN])}')
            print(f'\t{", ".join(list(set(r["institution"]["label"] + ":" + r["institution"]["id"] for r in _391_91ByPIEN[patientIEN])))}')
            # print(json.dumps(_391_91ByPIEN[patientIEN], indent=4))
            for r in _391_91ByPIEN[patientIEN]:
                institIEN = r["institution"]["id"].split("-")[1]
                if institIEN in _870LabelByIIEN:
                    institIENsW870.add(institIEN)
                    # if _870LabelByIIEN[institIEN] in 
                    # patientRTLinks[patientIEN]

                    institMU = f'{institByIEN[institIEN]["label"]} [{institByIEN[institIEN]["station_number"]}]'
                    print(f'\t\tInstit: {institMU}, Link {_870LabelByIIEN[institIEN]}')
                else:   
                    institIENsNo870.add(institIEN)
    if enforceTFL: # too slow for 663
        try:
            enforce391_91(stationNo)
        except Exception as e:
            print(f"** Failed enforce 391.91: {e}")
                
    """
    4. An example - patient w R:OR_PN and > 1 VistA or a table of top five patients
    + Report Types, VistAs/VAFHIE (as confirmed in TFF)
    """
    lls = set(ll for rt in reportTypePatientLinks for p in reportTypePatientLinks[rt] for ll in reportTypePatientLinks[rt][p])
    reportPatientTypeLinks = defaultdict(lambda: defaultdict(lambda: Counter()))
    patientCounts = Counter()
    tbl = MarkdownTable(["Patient Id", "#", ":Remote Systems", ":Report Types"])
    for rt in reportTypePatientLinks:
        for p in reportTypePatientLinks[rt]:
            for ll in reportTypePatientLinks[rt][p]:
                reportPatientTypeLinks[p][rt][ll] = reportTypePatientLinks[rt][p][ll]
                patientCounts[p] += reportTypePatientLinks[rt][p][ll]
    for i, p in enumerate(sorted(patientCounts, key=lambda x: patientCounts[x], reverse=True), 1):
        if i == 6:
            break
        tbl.addRow([
            f'__{p}__',
            f'{patientCounts[p]:,}',
            re.sub(r'(VACRNR|VAFHIE)', '__\\1__', ", ".join(sorted(list(set(ll for rt in reportPatientTypeLinks[p] for ll in reportPatientTypeLinks[p][rt]))))),
            ", ".join(sorted(list(set(rt for rt in reportPatientTypeLinks[p]))))
        ])
    mu += f"The top five patients (out of <span class='yellowIt'>{len(patientCounts)}</span>) have the following remote systems with data and had the following reports invoked for them ..." + "\n\n"
    mu += tbl.md() + "\n\n"

    """
    4.1 VACRNR Note
    """
    if vaCRNRReportNA:
        mu += """Note that this VistA does dispatch to __VACRNR__, Cerner. Cerner does reply to the queries with (the non specific) ...
        
> Report not currently available

"""
    
    """
    5. Builds filling that report defn file
    
    BUILDs ... must lookup by file ... FILE/OE_RR REPORT ... ie/ file == 101.24 and is replace or not I Y>999!(Y=3)!(Y=23)!(Y=24) <---- otherwise will just be code
    """
    
    """
    6. Inbound - perhaps just MU count up above
    # + need a screen shot ie show the use ... ie/ TFL + SPQ produces integrated
    # reports on medications, ... irrespective of what VistA/Facility treated
    # the patient [note: get the typical date range for each call too]
    """
    
    # print(mu)
    
    userSiteDir = SITE_DIR_TEMPL.format(stationNo)
    print(f'Serializing Report to {userSiteDir}')
    open(f'{userSiteDir}hl7SPQ_ORWRP_REPORT_TEXTSummary.md', "w").write(mu)  
            
# ################################# DRIVER #######################
               
def main():
    
    assert sys.version_info >= (3, 6)

    try:
        stationNo = sys.argv[1]
    except IndexError:
        raise SystemExit("Usage _EXE_ STATIONNO [PLOT]")
    
    webReportSPQ(stationNo)
    
    # webReportSPQDebug(stationNo)
    
    # webReportSPQBackground()

    webReportORWRP_REPORT_TEXT(stationNo)
                    
if __name__ == "__main__":
    main()
    
