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

from fmqlreports.webReportUtils import TOP_MD_TEMPL, SITE_DIR_TEMPL, ensureWebReportLocations, keyStats, flattenFrequencyDistribution, roundFloat, reduce4, flattenPropValues, vistasOfVISN, vistasOfVISNByOne
from fmqlreports.webReportUtils import muPlotRef, makePlots 

from hl7Utils import HL7TemplateMaker, makeBasicHL7Event 
            
"""
GOAL: sufficient report to allow the recreation of a Black Box "VistA" that sends and receives appropriate messages/activity. Sub example LIFT SPQ out.
- base components (protocols, links, apps, files, workcodes, locations, doc types, consult types clear)
  ... may call for subset of consults, docs, 2.98 entries etc
  (i/e nothing that stays in the system - everything that comes in and out of VistA to peer systems)
- message types clear
- subsystems (CCRA ...) clear

Background note in general:
- REGION 1 ... Sacramento. NTP is there. Other region 1 is denver. Then Region 2/3 is Philly 

Reflection/TODO (alot not seen): Cerner Charts
- Enrollment Application System (EAS) ... see ESR IP in AAC again <-------------- get more on this
- IB/ Vitria AAC too 
- find the XML in HL7 (saw ex ... find it again as ref in Cerner Revenue)
- more on Med Instruments
- Acustaf Application (NUASTAFF)
- Remote Order Entry System (ROES) ... <--- is in Cerner diagrams

Files to Consider ie/ all HL7 subsystem accounted for and reported on
<-------- nice for [1] auto behavior + [2] other sites like Austin
- 1. VDEF http://localhost:9100/schema#577 event descr etc ... HL7 ... DO THESE events appear in generic logs? [ie/ context report] ... says 2.4
- 2. RAD NUC http://localhost:9100/schema#79_7 ... Exception for HL7 defn
- 3. ADT/HL7 PIVOT (391_71) -- [687 6M+ ... ie/ big log!]
- 4. PCMM HL7 ERROR CODE (404_472) ... "the Austin Automation Center (AAC) will report when processing PCMM HL7 Transmissions"
- 5. Instrument HL7 http://localhost:9100/schema#690_7
- 6. http://localhost:9100/schema#770 "This file contains parameters associated with non-DHCP applications from whom the DHCP system can accept HL7 transmissions. This is the main file that sites must edit before they can begin receiving HL7 transmissions from another system." <------ key config file? <------ see what's in WWW ...
- 7. http://localhost:9100/schema#771 "This file contains a list of Vista applications that are capable of sending and receiving HL7 transmissions." ... which one is IFC?
- 8. Monitor job http://localhost:9100/schema#776 ... and what are they doing?
----- 687 Logs ... shows more HL7 logging
- 10. CM HL7 DATA (8973_1) ... holds daily statistics for CM [687: 3,755]
- 11. DSII RX-Framework HL7 Tracker (19665_9) [687:2,619,625]
- 12. DSID HL7 TRACKING (19630_13) [687: 447K]
- 13. DSID HL7 TRACKING (19633) [687: 143K]
- 14: ADT/HL7 TRANSMISSION (39_4) [687: 47K]
- 15: PRF HL7 EVENT (26_21) [687: 46K]
- 16: PRF HL7 QUERY LOG (26_19) [687: 34K]
- 17: PRF HL7 TRANSMISSION LOG (26_17) [687: 4K]
- 18: CM HL7 DATA (8973_1) [687: 3K]
- 19: DES/HL7 TRANSMISSION (228_25) [687: 2.9K]
- 20: HL7 Message Exceptions File (79_3) [687: 1K]
...

HL7 BG Note
-----------
In HL7 versions 2.2 and above, Enhanced Mode differentiates between commit
accept acks and application acks ... For Enhanced mode acknowledgements with full two-phase commit, over TCP/IP, the COMMIT ACK should always be immediate and over the current connection. The application acknowledgement should always be deferred, and performed as a separate transaction. This means that the application ack is always deferred and the final "commit" is optional. ... For dynamically addressed messages over TCP/IP where original mode is used, returning application acknowledgements is not a problem, because the response is returned over the open TCP/IP channel.

A future patch will support HL7 V. 2.3-style message headers, where all the
information needed to address a response to a message is contained in that
message's header (rather than in the advance interface setup). ... (other than using original mode) If the sender is a VISTA facility, and if that facility's institution number is in the original message's facility field, use the dynamic addressing features
released in patch HL*1.6*14 to resolve the proper logical link and dynamically
address the response. 

MLLP very simple ... The TCP/IP implementation in patch HL7*1.6*19 encapsulates HL7 messages using Minimal Lower Layer Protocol (MLLP), rather than Hybrid Lower Layer
Protocol (HLLP). MLLP is a very simple protocol, and can be used because the
TCP/IP channel itself provides most services needed for error-free transmission of
messages
""" 
def webReportHL7(stationNo, transactions, transactionInfo):

    startTime = datetime.now()
    print(f"Generating HL7 Summary for {stationNo}")
                                    
    meta = metaOfVistA(stationNo)
     
    mu = TOP_MD_TEMPL.format("{} HL7 Messaging".format(stationNo))
             
    mu += "# HL7 Messaging of {} [{}]\n\n".format(meta["name"], stationNo)
    
    mu += "This is a summary of the HL7 messaging of a copy of _{}_ VistA cut on {}. It is one of a series of reports that focuses on the interaction of VistA with peer systems - specifically it treats VistA as a \"black box\" with distinct subsystems that are the source and sink for HL7 messages sent to or received from peer systems.\n\n".format(meta["name"], meta["cutDate"])
    
    # TMP fix - older transactions copies lack some counts
    if "totalTransactionsIncoming" not in transactionInfo:
        tmpEnsureTransactionInfoComplete(stationNo, transactions, transactionInfo)
    
    mu += f'''Most VistAs log sufficient messages to allow a full account of their HL7 messaging. This system keeps <span class="yellowIt">{transactionInfo['purgeTimeGap']}</span> days of complete _HL7 Transactions_ (dispatched or received messages and their responses if any), <span class="yellowIt">{transactionInfo["totalTransactions"]:,}</span> in all, <span class="yellowIt">{reportAbsAndPercent(transactionInfo["totalTransactionsIncoming"], transactionInfo["totalTransactions"])}</span> of which are incoming (marked with _I_ below), <span class="yellowIt">{reportAbsAndPercent(transactionInfo["totalTransactionsOutgoing"], transactionInfo["totalTransactions"])}</span> are outgoing (marked with _O_ below). 
    
In VistA, messages are dispatched or received by a \"Protocol\" on a \"Link\", a connection between systems. A _Protocol_ is a

> method for accomplishing orders
        
'''

    mu += muByGroup(transactions, transactionInfo)
    
    # Background
    mu += muBackgroundMessageLogs(transactions, transactionInfo)

    print(f'Done making report - took {datetime.now() - startTime}')
            
    userSiteDir = SITE_DIR_TEMPL.format(stationNo)
    print(f'Serializing Report to {userSiteDir}')
    open(f'{userSiteDir}hl7Summary.md', "w").write(mu) 

"""
Debug/ meta - in its raw form - behind the report

TODO: add in long builds table with dependencies
"""
def webReportHL7Debug(stationNo, transactions, transactionInfo):

    startTime = datetime.now()
    print(f"Generating HL7 Debug for {stationNo}")

    mu = TOP_MD_TEMPL.format("{} HL7 Messaging DEBUG".format(stationNo))

    mu += "Background meta - in all its gory details for the manually construction (static defn of groups) HL7 report\n\n"

    standardListener = transactionInfo["standardListener"]
    llInfoById = transactionInfo["llInfoById"]
    protocolInfoById = reduce101SE(stationNo)
    
    llsSeen = set() # not including standard listener
    llsNSListenerSeen = set()
    protocolsSeen = set()
    for transId in transactions:
        for i, resource in enumerate(transactions[transId]):
            protocolsSeen.add(resource["subscriber_protocol"]["label"])
            ll = resource["logical_link"]["label"]
            if ll != standardListener:
                llsSeen.add(ll)
                if i == 0 and resource["transmission_type"] == "I:INCOMING":
                    llsNSListenerSeen.add(ll) 

    mu += "# Logical Links Seen\n\n"
    tblObj = tblLinkSet(llsSeen, llInfoById, llsNSListenerSeen)
    mu += tblObj.md() + "\n\n"

    # TODO: consider pulling up the Server ie/ dispatcher to this event protocol
    # ... and others on same server => COMMON FAN OUT!
    # TODO: perhaps dump sending app etc here too ... see if fixed for protocol
    mu += "# Protocols Seen\n\n"
    tbl = MarkdownTable([":Protocol", ":Description", "Link", "Sending App", "Receiving App"])
    for pr in sorted(list(protocolsSeen)):
        prInfo = protocolInfoById[pr]
        if "description" in prInfo:
            descr = '<br>'.join(prInfo['description'].split('\n'))
        else:
            descr = "&nbsp;"
        tbl.addRow([
            f"__{pr}__",
            descr,
            prInfo["logical_link"]["label"] if "logical_link" in prInfo else "&nbsp;",
            prInfo["sending_application"]["label"] if "sending_application" in prInfo else "&nbsp;",
            prInfo["receiving_application"]["label"] if "receiving_application" in prInfo else "&nbsp;"            
        ])
    mu += tbl.md() + "\n\n"

    mu += muHLOConfig(transactionInfo["_779_1"])

    print(f'Done making report - took {datetime.now() - startTime}')

    userSiteDir = SITE_DIR_TEMPL.format(stationNo)
    print(f'Serializing Report to {userSiteDir}')
    open(f'{userSiteDir}hl7SummaryDEBUG.md', "w").write(mu) 
    
"""
Group/Subsystem definitions - fixed in Version 1. May move to auto group (on sending application?) in Version 2. But for now, reg exp on protocol and break down with link (as can have > 1 link per protocol) to static descriptions.

Note sources other than build such as Monograph: https://www.va.gov/VA_Monograph_2019.pdf

Other Notes:
- Monograph has TIU but TIU below is spread ie/ Notes across functional areas

TODO/SEE: from TeleHealth/Other Cerner:
- IFAN (sic) so no stop codes
- From TeleHealth (saw Medtronic -- mentioned below) but not ....
  - VCM (Virtual Care Manager) ... "MVP integration" ... staff tool for providers/schedulers to manage virtual care tools use to deliver care. ... video visits, digital therapies, patient generated data ... IronBow (sic)
  - CapSure VistA Live - GlobalMed ... store and forward VistA, DICOM ...
  - Account Sign-Up Service
  - Home TeleHealth Cognosante ... through remote device conn API on CareAwareCloud for patient enrollments and device integ for vitals, glucose and weight ...
  - IFC ... CAMM7, CAMM Appliance, Compass Router ... imaging stations, cameras
"""
PROTOCOL_SUBSYSTEMS = { # Read/Write, VistA or National VA (VBA or ?) or Other

    "ARHCATHL": { # 531 only
    
        "label": "Caresuite PICIS",
        
        "protocolReMatch": "ARHCATHL",
      
        "_comment": "Only build lacks description and protocol lack descriptions. TODO: chase down Caresuite. Fit in with other PICIS."
        
    },  

    "BCMA": {
    
        "label": "Bar Code Medication Administration (BCMA)",
        
        "description": "Bar Code Medication Administration (BCMA) software provides a realtime, point-of- care solution for validating the administration of Unit Dose (UD) and Intravenous (IV) medications to inpatients and outpatients in Veterans Administration Medical Centers (VAMCs).""",
        
        "namespace": "PSB",
        
        "isVistAPackage": True, # 1999
        
        "inMonograph": True, 
        
        "protocolReMatch": "PSB BC" # May need to split
        
    },

    "CCRA HSRM": {
    
        "label": "Community Care Appointments (HSRM to VistA)", 
    
        "parent": "CCRA",
        
        "description": """VA and non-VA care coordination staff make, cancel and mark as no-show __Community Care Referral appointments__ for Veterans in HSRM. This data is then automatically pushed into non-count clinics in the  home VistA of those Veterans using the following Scheduling Information Unsolicited (SIU) messages.""",
        
        "_comments": [
        
            "CCRA-NAK: see if the CCRA-NAK logical link exists in the system. If not, it asks for the Health Connect Server IP Address and Port number, then creates the logical link in the VistA system. This link is required to receive consult updates from HSRM to VistA. This link is also used by the SD*5.3*707 scheduling patch, which may or may not be installed previously. <------ shared Consult Update and Schedule In setup: >PLEASE ENTER THE HEALTHCONNECT SERVER IP ADDRESS"
            
        ], 
        
        "protocolReMatch": "CCRA HSRM",

        "protocolDescriptions": {
            "CCRA HSRM SIU-S12 CLIENT": "new appointment",
            "CCRA HSRM SIU-S15 CLIENT": "appointment cancellation",
            "CCRA HSRM SIU-S26 CLIENT": "patient did not show up for an appointment"
        }
    },
    
    "DG HOME": {
    
        "parent": "TELEHEALTH",
    
        "protocolReMatch": "DG HOME TELEHEALTH",
        
        "description": """From VistA to Home TeleHealth vendor systems via AITC's VIE Server or HealthConnect. A04 is activation; A03 is de-activation. Other communications to and from the vendor systems don't involve VistA. TeleHealth does lead to two other types of HL7 to (TIU) and from (Order) VistA. The TIU interaction shares the TIUHL7 outgoing connection used for other note synchronizations; the Order ...""",
        
        "__comment": """
    
The Home Telehealth application is in support of the Care Coordination Program that involves the use of Home Telehealth technologies ... The care coordinator serves as a bridge between the primary care team and the patient.

Non-institutionalized Care (NIC) - The goal of this care is to assist patients
at risk for requiring residential care to better manage a serious disease
process, stay in their home, and avoid institutionalization. This care is
specifically funded by Congress <--- note funding

The Care Coordinator uses a VistA menu to initiate the sign up process. The basic objective of the sign up process is to either create and activate a patient in a vendor system or activate an existing patient in the vendor system. The Care Coordinator selects the patient from the list of VistA registered patients and selects the Home Telehealth vendor server from the approved list. The VistA system obtains a national identifier, if one has not already been obtained. [ie/ VistA will have list of TeleHealth Vendors!]

TO VISTA: The Home Telehealth vendor server transfers selected patient status information to VistA. The information is placed into a template for a text note that is stored in the VistA patient record. The status information is placed in a standard VA progress note for distribution to appropriate individuals. The data is sent in an HL7 message documented in chapter nine of the HL7 2.4 standard. ... There are two types of progress notes. One is the report of an “out-of-bounds” observation and the second is a “Summary of Episode” 87 progress report. The Home Telehealth vendor server generates the data used by VistA to build a draft note and identifies the note title. After VistA builds the draft, it is queued for signature by the care coordinator. [ie/ LISTEN and then should see notes and id care coordinators] ...  Summary of Episode progress note template each
month after the signup/activation of a patient. A Summary of Episode note is to be created for each patient every month; the patient should receive just one note per month except (perhaps) for the last month that the patient is in the program. The note is generated at midnight and covers the period that ends at midnight [AS MONTHLY ... do I have?] ... The observation function uses the Medical Document Management (MDM) Message as documented in chapter 9 of the HL7 standard. The event code is T02. .... seems on TIUHL7    
        
""", 
    
        "protocols": [
            "DG HOME TELEHEALTH ADT-A03 CLIENT", 
            "DG HOME TELEHEALTH ADT-A04 CLIENT"
        ],
        
        "note": "Medtronic of DG HT CC link -- one of the TeleHealth projects; also 226 must be AAC",
        
        "seeAlsos": [
            "https://www.vendorportal.ecms.va.gov/FBODocumentServer/DocumentServer.aspx?DocumentId=2404010&FileName=VA791-15-R-0020-028.pdf",
            "https://www.va.gov/vdl/documents/Clinical/CPRS-Text_Integration_Utility_(TIU)/tiuhl7.pdf" # if tie in HL7 (MDM/T02 -- there are others)
        ]
    },
    
    "CCRA": {
    
        "parent": "REM CONS", # May be too broad as CCRA beyond Consults?

        "label": "Community Care Consults (HSRM)",
        
        "__comment": "Likely to persist as works, Cerner equivalent not there (yet) and so not a high priority for migration",
        
        "description": "_HealthShare Referral Manager (HSRM)_ is an enterprise-wide system in support of community care used by facility community care staff to manage referrals ('CCRA Referrals') and authorizations for Veterans receiving care in the community.",

        "type": "GROUP OF GROUP",
                
        "contains": ["GMRC CCRA", "TIU CCRA", "CCRA HSRM"] 
    
    },
    
    # TO REDO -- downplay DSS and bring out all separately
    "DSS": {
    
        "label": "DSS Inc. VistA Integrations",
        
        "__comment": "See long list under '2.103. DSS Inc. Commercial-off-the-Shelf (COTS) VistA Integrations' in Monograph. Not all have HL7 (obviously).",
        
        "inMonograph": True,
        
        "_todo": "[1] parse msgs for relevant below to see subordinate systems",
        
        "_todoNS": """... 'The VA's Database Administrator (DBA) has assigned the VEJD, DSI namespaces and the Fileman file range 19600-19629.' ie/ follow up and see if all DSS in that range""",
        
        "__seeToo": "DSS VitalsLink - https://www.oit.va.gov/Services/TRM/ToolPage.aspx?tid=11265 -  allows Philips SureSigns vitals monitors to transfer patient vitals data via Health Level 7 (HL7)",
        
        "contains": ["DSIIB", "DSID", "DSIH", "DSIW"]
        
    },
    
    "DSIIB": {
    
        "parent": "DSS",
    
        "label": "Rx-Framework",
        
        "description": "DSS Rx-Framework is an interface that allows __pharmaceutical vendors and their machines__ to interface with Veterans Health Information Systems and Technology Architecture (VistA).",

        "protocolReMatch": "DSIIB",
        
        "_todo": "[1] what pharma in particular? (MUST PARSE MSGs); [2] RDE_O01 communicates the pharmacy or treatment application’s encoding of the pharmacy/treatment order - gets a lot less than <=> DSID ... difference? [3] 692 but not 687 etc. Why difference?",
        
        "trmURL": "https://www.oit.va.gov/Services/TRM/ToolPage.aspx?tid=7563"
    
    },
    
    "DSID": {

        "parent": "DSS",
    
        "label": "Theradoc Interface",
        
        "description": "DSS VistA Gateway for __TheraDoc__",
        
        "_todo": "[1] why the stage and client dups? ;[2] https://www.theradoc.com/ - seems to be private CDS product - potentially turn into a separate item as just because it's DSS is not a real category!; [3] old report (see 'LAB Results Link' to go with DSID_LAB -- ditto for BCMA ie/ link tie in",
    
        "protocolReMatch": "DSID",
        
        "trmURL": "https://www.oit.va.gov/Services/TRM/ToolPage.aspx?tid=8153"
        
    },
    
    "DSIH": { # TODO: expand out on DataBridge PICIS use and what vendors ... see msgs?
    
        "parent": "DSS",
    
        "label": "DataBridge",
        
        "description": "DSS Clinical Information System (CIS)-DataBridge is a software interface solution that filters patient data information from Veterans Health Information Systems and Technology Architecture (VistA) and Clinical Patient Record System (CPRS) to a commercial __Intensive Care Unit (ICU)/Anesthesia__ record keeping (ARK) system.",
        
        "_todo": "See Build lines like 'DSIHD is the DataBridge Sub Build for the Picis products' -- but Picis seems to be a particular vendor. Get to bottom of that and see if particular products mentions -- MUST PARSE MSG; 757, 531 only?",
        
        "protocolReMatch": "DSIH",
        
        "trmURL": "https://www.oit.va.gov/Services/TRM/ToolPage.aspx?tid=8969"
    
    },
    
    "DSIW": { # There are many RPCs in a relevant build
    
        "parent": "DSS",
    
        "label": "Watchdogs",
        
        "_comment": "VEJD WATCH DOG CLIENT goes out in DSS RPC Builds",
        
        "protocolReMatch": "(VEJD WATCH DOG CLIENT|DSIW WATCH DOG CLIENT)"
        
    },
    
    "EAS": { # See PIMS doc and if need to roll in along with MPI/PD?; NO BUILDs have the protoocols etc - had to widen to see and (TODO) haven't yet examined those wider builds
    
        "label": "Enrollment Application System (EAS)",
        
        "description": """The Enrollment Application System (EAS) package supports the mandate for collection of Long Term Care (LTC) copayments, as required by Public Law 106-117. In addition to the LTC functionality, the EAS package provides support for Health Level 7 (HL7) for processing of HL7 messages between VistA, the enterprise Enrollment System (ES) and data matching with the Internal Revenue Service (IRS) / Social Security Administration (SSA).""",
        
        "_todo": "'Enrollment System (ES) 5.2.4 is the replacement system for the decommissioned product known as HEC (Health Eligibility Center, Atlanta) Legacy' -- how does this fit in? New plan?",
        
        "namespace": "EAS",
        
        "isVistAPackage": True, 
        
        "inMonograph": True,
        
        "protocolReMatch": "EAS", # ESR etc -- may subset
        
        "seeAlso": [
            "https://www.va.gov/vdl/application.asp?appid=183",
            
            "https://www.va.gov/vdl/application.asp?appid=143",
            "https://www.va.gov/vdl/documents/HealtheVet/VA_Enrollment_System/es_5_13_ug.pdf"
        ],
        
        "otherComments": [
        
            "The release of the ESR 3.0 project marked a significant event in the HealtheVet (HeV) space. ESR 3.0.1 is comprised of a major change to the HECMS, an online business application for the HEC in Atlanta, GA. (ESR 3.10 Installation Guide)",
            
            "The Enrollment System (ES) assists Veterans to enroll for VA healthcare benefits and is the core application that feeds other VA systems with Enrollment and Eligibility (E&E) data. (ES 5.1 Release Notes)",
            
            "Enrollment System Redesign, Health Eligibility Case Management System (HECMS), now known as the Enrollment System (ES)",
            
            "ES is the HealtheVet replacement system for the product known as HEC Legacy. It is both a re-host of HEC Legacy and in some instances (use cases/features), a reengineering. ES allows staff at the HEC to work more efficiently and determine patient eligibility in a timelier manner",
            
            "HEC: Health Eligibility Center, Atlanta Georga",
            
            "On January 23, 2002, President Bush signed into law Public Law 107-135, The Department of Veterans Affairs Health Care Programs Enhancement Act of 2001. Section 202 of this Act requires the implementation of HUD indices to determine geographic income thresholds in support of more discrete means testing.",
            
            "The Income Verification Match (IVM) module is designed to extract patient-reported Means Test data and transmit it to the Health Eligibility Center (HEC) located in Atlanta, Georgia.  IVM allows Veterans Health Administration (VHA) to accurately assess a patient’s eligibility for health care when the eligibility criteria is income-based."
            
        ]
        
    },
    
    "ECME": { # TODO: see all refs to Vitria, WebMD and claims process
    
        "label": "Electronic Claims Management Engine (ECME)", 
        
        "description": """The Electronic Claims Management Engine (ECME) package provides the ability to create and distribute electronic Outpatient Pharmacy claims to insurance companies on behalf of VHA Pharmacy prescription beneficiaries in a real-time environment.
        
Claims are in HIPPA Compliant (NCPDP V.5.1) format and sent to the Vitria server at the FSC at the AAC. Vitria then forwards these claims to WebMD for processing.  
      
""",
        
        "namespace": "BPS",
        
        "filesComment": "9002313.02 - BPS Claims ... report on these; there's 9002313.03 BPS Responses ... and more.",
        
        "otherBuildContentsComment": "Note the Options 19 and Reports and their link to Files. ie/ Files for specific reports; has security keys too. ... Vitria Interface Engine (IEN) BusinessWare product ... TODO/QUESTION -- Vitria again ala IB",
        
        "protocolDescriptions": {
        
            "BPSJ PAYER RESPONSE": "Payer Sheet Input"
            
        },
        
        "isVistAPackage": False, # in FOIA but maybe in VistA?
        
        "inMonograph": True,
                
        "protocolReMatch": "BPS",
        
        "_todo": "One of (four) financial areas I was asked about in dec; see comments in a VICs issue (https://github.com/vistadataproject/RPCDefinitionToolkit/issues/6)"
        
    },
    
    "FHVC": {
    
        "label": "Dietetics",
        
        "description": "Region 1 (R1) Dietetics COTS interface.",
        
        "protocolReMatch": "R1FHVC",
        
        "filesComment": "100100.0021 etc",
        
        "namespace": "FH",
        
        "isVistAPackage": True,
        
        "_note": "'COMPUTRITION' is receivingFacility in 531 and 687 and ...; see acronym ASIH in Build comment; lot's of ADT HL7 in Build but don't see use of them ie/ A08 etc.; note the link doesn't set an IP!"
        
    },
    
    "GMRC CCRA": {
    
        "parent": "CCRA",
        
        "label": "Community Care Consults (VistA to HSRM)",
        
        "description": "Non-VA Community Care consults sent from VistA to HSRM.",
        
        "protocolReMatch": "GMRC CCRA",
        
        "_comment": "Does REF == Referral?",
        
        "systems": ["HSRM"], # see acronym defn below
            
        "protocolDescriptions": {
            "GMRC CCRA REF-I12 CLIENT": "New Referral",
            "GMRC CCRA REF-I13 CLIENT": "Change to a Referral",
            "GMRC CCRA REF-I14 CLIENT": "Cancel a Referral" # Same as HCP equivalents ie/ only 123 type chosen differs?
        }
        
    },

    "GMRC HCP": { # Is this financial? Same REF-... but different contents?
    
        "label": "Non-VA Consults (HCPS)",
        
        "description": """Non-VA Consults sent from VistA to the __Healthcare Claims Processing System (HCPS)__ in Austin.""",
    
        "parent": "REM CONS",
        
        "protocolReMatch": "GMRC HCP",
        
        "protocolDescriptions": {
            "GMRC HCP REF-I12 CLIENT": "New Referral",
            "GMRC HCP REF-I13 CLIENT": "Change to a Referral",
            "GMRC HCP RRI-I13 CLIENT": "Change to a Referral (Acknowledgement)" # Listen
        }
        
    },

    "GMRC IFC": {
    
        "parent": "REM CONS",
        
        "label": "Inter-Facility Consults",
        
        "description": "Consults ordered in other VistAs. Includes clinical and administrative orders and telereading.",
        
        "protocolReMatch": "GMRC IFC",
        
        "seeAlso": [
            "https://www.va.gov/vdl/documents/Clinical/CPRS-Consult_Request_Tracking/constm.pdf"   
        ]
        
    },
    
    "IB": { # Any tie to PIMS and what more?
    
        "label": "Integrated Billing (IB)",
        
        "description": """The Integrated Billing (IB) software provides all the features necessary to create first party (patient) and third party (insurance carriers/Medicare) bills. 
        
eIIV and IIV stand for the electronic Insurance Identification and Verification project.
        
""",
        
        "namespace": "IB",
        
        "fileComment": "2.312 sub type on insurance in Patient(2); 36 is Insurance Company; 350.9 is Site Parameters for IB; 355.33; 365 (IIV Response -- so log to look at?) ... and there are X12's",
        
        "buildComment": "The NIF Protocol pulls in a NIF Build - separate path ... Vitria too ala ECME!",
        
        "isVistAPackage": True,
        
        "protocolDescriptions": {
        
            "IBCNE EIV ID REQUEST": "EICD Identification Request for insurance",
        
            "IBCNE IIV MFN OUT": "MFN enroll",
            "IBCNE IIV VER REQUEST": "Insurance Verification for a specified patient",
            "IBCNE IIV TABLE": "MFN table updates",
            
            "IB NIF QUERY SUBSCRIPTIONS": "National Insurance File (NIF) is owned by the Financial Services Center (FSC), part of Health Plan Identifier (HPID) Project."
        
        },
        
        "inMonograph": True,
        
        "protocolReMatch": "(IBCNE|IB NIF)",
        
        "_todo": "One of financial set I was asked about in DEC"
    
    },
    
    "IFCAP": { # Basic Build is 2001; ACC Report Build in 2006.
    
        "label": "Integrated Funds Distribution Control Point Activity, Accounting And Procurement (IFCAP)",
        
        "description": "Most communications is GIP communicating with purchased/rented Supply Stations. A later patch added support for reporting VistA procurement information to the FPDS system at AAC.",
                
        "protocolReMatch": "PRC",
        # "protocolReExclude": "(PRCM|PRCZ|PRCP|PRCA|PRCC|PRCN|PRCK)", nixed exclude
        # mshLocalApplication > 1 - reflected in some links and links matter
        
        "isVistAPackage": True,
        
        "linksSent": True, # and the IP is not changed!
        
        "vistaNamespace": "PRC", # for ref - off 9.4 entry for IFCAP which has excludes too for PRCM etc. PRCA is AR's namespace, a separate package!
        
        "inMonograph": False, # NOT GIVEN OWN PLACE though mentioned
        
        # Builds has many files -- 445, 410.1 (fields) ...; AAC build has 420s.
        
        "protocolDescriptions": {
                
            # From Build
            "PRC_IFCAP_01_SU_AAC": "Send IFCAP procurement detail (PO Detail) to AAC"
        
            # Not putting in PRCP SU QOH REQ as doesn't seem to fit (accepts ACKs).
        },
        
        # Note Explicit Listener Links in Builds are not now shown (see md below). Must
        # fix this.
        "linkDescriptions": {
        
            # DEBUG hl7 report - should see descr for this from LL defn
            "PRCPSSPYXS": "Its IP is set in an IFCAP Build and so is uniform across all VistAs.",
            "PRCPSSOMNI": "Unlike _PRCPSSOMNI_, the IP set for this in the IFCAP Build is reset in individual VistAs."
            
        },
        
        "_todo": """Integrated Funds Distribution Control Point Activity, Accounting And Procurement (IFCAP) ... The Integrated Fund Distribution Control Point Accounting & Procurement (IFCAP) system) is an interface with FMS ... Par Excellence Supply Stations?

PRC_IFCAP_01_SU_AAC": "IFCAP Report to Austin    

PRCP SU INV UPDATE ... many PRCP...'s ... break down all PRC_IFCAP_... may in own subtable and the PRCP may be separate table.   

Sub ns's: PRCI, ... etc etc so expect many?

Note Accounts Receivable (AR) is separate package in VistA with PRCA (superset!) of IFCAP's namespace. Must distinguish.

""",

        "_todo2": "One of financial set I was asked about in DEC"
        
    },
    
    "LA7": {
    
        "label": "Automated Lab Instruments",
        
        "namespace": "LA",
        
        "isVistAPackage": True, # 2005 - Monograph says LA belongs to LA UI
                        
        "_todo": "See POC, UI ... break in 62.1, 62.48 etc",
        
        "contains": ["LA7POC", "LA7UI", "LA7V"]
    
    },
    
    "LA7POC": {
    
        "parent": "LA7",
    
        "label": "Laboratory Point of Care (POC) Interface",
    
        "description": "POC devices are interfaced with HL7 to VistA with POC vendor's server located within the VA Medical Center. VistA accepts their laboratory test results for which there is no pre-existing VistA laboratory order - it creates an order as part of result processing and storage. It also allows POC devices with appropriate support to subscribe to patient information (HL7 ADT) from VistA (\"POCA Interface\"). VistA can be configured to support up to five separate vendor’s Point of Care systems, _LAPOC1[A]_ to _LAPOC5[A]_.",
    
        "background": """Note the description is from the 'interface type' field of 62.48:
        
  * two users: LRLAB,POC and 
  * Messages to the POC system are transmitted via a logical link LA7POCx for lab result acknowledgments and LA7POCxA for transmission of VistA ADT HL7 messages (hence POC and POCA)
  * In 770: LA7POC{1-5} and LA7LAB (for reception)
  * Auto instrument file, 62.4 has LA7POC{1-5} too. It has 60 maps too (it appears ie/ from POC to 60)
  * See comment in one: ADT -Point Of Care Interface for RALs network using VLAN_81_ROCHE_POC5 pointing to cos-palms-555 using VISTA POC Interface LA7POC1 and LA7POC1A. ie/ specialized
  
support for Laboratory Point of Care (POC) interfaces ... Laboratory Electronic Data Interchange (LEDI) ... of POC test results in the VistA Laboratory Package ... [AND] the ability of POC interfaces to subscribe to VistA HL7 ADT messages for patient demographics and location information is provided as needed
""",

        "_subSysMsgNote": """
    
687 see: Clinitex Status and Roche GTS (two systems?)    
        
""",

        "protocolReMatch": "LA7POC",

        "seeAlso": [
            "https://www.va.gov/vdl/documents/Clinical/Lab-Point_of_Care/lab_poc_iug.pdf"
        ],

        "_todo": "[1] MESSAGING inside shows actual POC server? or [2] (lab specific) see 62.4 etc maps ie/ the order population configuration",
        
    },
    
    "LA7UI": {
    
        "parent": "LA7",
    
        "label": "Laboratory Universal Interface (UI)",
        
        "description": "For processing laboratory automated instrument data via a Generic Instrument Manager (GIM) - for the transmission of laboratory test results from clinical analyzers to the VistA system. The GIM is a locally procured commercial device that controls communications between the Laboratory instruments and VistA. The VistA system downloads work lists through the GIM to the various instruments, and the instruments upload results to VistA through the GIM, eliminating the need for Laboratory developers to write a new interface for each different instrument. VistA can interface with multiple Generic Instrument Managers (GIMs).",
        
        "inMonograph": True, # says UI owns "LA" but VistA say instruments as a whole do
        
        "protocolReMatch": "LA7UI",

        "background": """
        
            * The new Lab Universal Interface Setup [LA7 UI SETUP] option allows sites to configure Lab Universal Interface entries (LAUI*) in the LA7 MESSAGE PARAMETER file (#62.48), and corresponding entries in the AUTO INSTRUMENT file (#62.4), which use the Lab Universal Interface. It also allows editing of fields pertaining to Laboratory UI only. This option is located on ‘Lab Universal Interface Menu [LA7 MAIN MENU] menu
            * Vendors of the GIM devices have been notified of VistA’s enhanced capabilities. The three primary vendors are: Data Innovations, Dade, Dawning Technologies

the Lab Universal Interface (UI) ... sites to interface their automated testing devices ... HL LOGICAL LINK ... each has ten entries with name LA7UI{\d} ... allows the site to inteface with multiple generic instrument managers ... 10 event drivers of this form ... NEW OPTION [LA7 UI SETUP] ... Allows configuring Lab Universal Interface entries

""",

        "_todo": "can we see the GIM vendor in the messages?"
    
    },
    
    "LA7V": {
    
        "parent": "LA7",
    
        "label": "Laboratory Electronic Data Interchange (LEDI)",
        
        "description": "Orders can be sent to other VAs (VistAs), DoD and Commercial Reference Laboratories. This includes placing new orders, cancellation of existing orders, discontinuation, holding, etc. ORM messages can originate also with a placer, filler, or an interested third party. The order dispatch (ORM) protocols are named _LA7 Send Order to {ID}_ and result receipt (ORU) protocols are named _LA7V Process Results from {ID}_ where _ID_ is station number for VistAs and DMIS ID for DoD sites.",
        
        "protocolReMatch": "LA7V",
        
        "background": """
        
  * at least one VISN uses a single VISN-wide laboratory system, obviating the need for LEDI within the VISN laboratories, and only uses LEDI to create the shipping manifest.
  * There are approximately ten special reference laboratories that serve many VA labs
  * The VA Decision Support System (DSS) contains aggregate laboratory test volume for 2002 through 2007.

""",
    
        "_todo": "[1] what is LA7VLCA/692 - third party?, [2] break out 4's for DoD - TCP/IP ADDRESS: 10.224.129.80 AAC Vitria? -- see in old report first -- 4's have agency code field if DoD ie/ AF etc and DMIS ID (Select the logical link created for the DoD facility (LA7Vnnnn) where nnnn is the 4-digit DMIS ID of the DoD facility) [3] LAB SHIPPING CONFIGURATION file (#62.9) contains the test information to process orders received from the DoD facility. ----> refs to 4's [4]  Updating LAB AUTO INSTRUMENT file (#62.4) for HOST Lab TRIPLER ARMY MEDICAL CENTER.",
        
        "seeAlso": [
                    "https://www.va.gov/vdl/documents/Clinical/Lab-Electr_Data_Intrchg_(LEDI)/lab_ledi_iii_imp_ug.pdf",
                    
            "https://www.va.gov/vdl/documents/Clinical/Lab-Electr_Data_Intrchg_(LEDI)/lab_ledi_iv_install_guide.pdf",
            
            "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3041428/"

        ]    
    },
    
    "MAG CPACS": { # 757 only
    
        "label": "Commercial PACS from VistA Imaging",
    
        "description": "Send VistA patient demographic changes to PACS using ADT A08 and/or ADT A47 messaging",
        
        "protocolReMatch": "MAG CPACS",
        
        "fileComment": "2006.1 imaging site parameters get a new field 3.01, PACS HL7 INTERFACE ACTIVE",
        
        "buildComment": "Note that MAG CPACS link's IP is set in the Build. Both Builds are identified are national"
    
    },
    
    "MC": {
        
        "label": "Medical Instruments",
    
        "__comment": """MC is Medical Package?""",
        
        "seeAlso": [
            "https://www.va.gov/vdl/documents/Clinical/Medicine/mc_2_3tm.pdf",
            "https://www.va.gov/vdl/documents/Clinical/ClinProc/clinproc1_impg.pdf"
        ],
        
        "contains": ["MUSE", "MCAR"]
    
    },
    
    "MCAR": {
    
        "parent": "MC",
    
        "label": "Clinical Instruments",
        
        "protocolReMatch": "MCAR",
    
        "protocolDescriptions": {
            "MCAR Device Client": "Return data to VistA from Clinical Instruments",
            "MCAR ORM CLIENT": "Send orders from VistA to Clinical Instruments"
        },
        
        "extractSenderReceiver": True,
        
        "_todo": "See if can work out instruments from HL7 message parse",
        
        "todo757": "757 links in old report show details: MCAR ENDO1 - BKR created new MCAR ENDO1 link for new Endosoft Endovault software implementation + MCA XCEL - EXCELERA INTERFACE 7/2016 ... all are used by MCAR ORM CLIENT ie/ one Client P and many links (or can protocols have shared labels -- throws me?)",

        "todo531": "531: MCAR MGS: BreezeConnect link for new PFT machine 1.16.14",

        "todoRead": ["https://www.va.gov/vdl/documents/Clinical/ClinProc/md_1_p6_impg.docx", "https://www.va.gov/vdl/documents/Clinical/ClinProc/md_1_p21_tm.docx"]
        
    },
    
    "MUSE": {
    
        "parent": "MC",
    
        "label": "GE MUSE Cardiology Information System",
        
        "protocolReMatch": "GE-Muse"
    
    },
    
    "MHV": {
      
        "label": "My HealtheVet",
        
        "description": """My HealtheVet (MHV) (www.myhealth.va.gov) is VA’s Personal Health Record (PHR) online portal.""",
        
        "namespace": "MHV",
        
        "isVistAPackage": True,
        
        "inMonograph": True,
        
        "protocolReMatch": "MHV"
                
    },
    
    "MPI/PD": { # MPI and CLINICAL INFO RESOURCE NETWORK are packages 
    
        "label": "Master Patient Index/Patient Demographics (MPI/PD)",
    
        "type": "GROUP OF GROUP",
        
        "TODO": """More on Treating facility list and 'The treating facility list is a list of systems that know a specific Integration Control Number (ICN). The list can contain systems that are not VAMC like FHIE or HDR.' ie/ not just sync VistAs but sync FHIE or HDR too
        
391.91: If SOURCE ID is from the Master Patient Index, the value is the Integration Control Number (ICN). If SOURCE ID is from the Department of Defense (DoD), the value is the Electronic Data Interchange Personal Identifier (EDIPI), which is their equivalent of an ICN. In the future, SOURCE ID may come from other sources due to additional initiatives.
... want to see HDR etc => do type reduction on this ... see institutions
... Federal Health Information Exchange [FHIE], HomeTeleHealth, Person Service Identity
Management [PSIM], Health Data Repository [HDR] ... does HomeTeleHealth show separately?
""",
        "TODO2": "Tie to PIMS: https://www.va.gov/vdl/documents/Clinical/Scheduling/pimstm.pdf",
        
        "description": "Master Patient Index/Patient Demographics (MPI/PD) in VistA sends patient data to and receives data from the Master Patient Index in Austin. This triggeed traffic uses the _MPIVA_ link. HL7 protocol names fall into three buckets each with their own namespace, MPI, RG and VAF. The variety is a product of history as different approaches to Patient Demographic synchronization were taken and changed.",
        
        "background": """References to three name spaces used by reporter on 773/2 for this entity: RG, MPIF, VAFC: 
            
> utility searches the HL7 MESSAGE TEXT file (#772) for a selected date range. Each HL7 message in the date range is examined. If the RELATED EVENT PROTOCOL field contains the MPI/PD protocols (e.g., "VAF","RG", or "MPI") data is compiled into the ^XTMP("RGMT","HL" array 

See 

> Master Patient Index (MPI) enhancements are being distributed in three VistA namespaces: DG, RG and MPIF. (MPIF*1*62)

and

> To prevent legacy systems ending up as Treating Facilities, RG* and MPIF* patches should NOT be installed on legacy systems

""",
        
        "contains": ["RG", "MPI", "VAF"]
        
    },

    "MPI": {

        "parent": "MPI/PD",
        
        "label": "Master Patient Index (MPI) Synchronization",
        
        "description": "The Master Veteran Index (MVI) database (formerly known as the Master Patient Index [MPI]) is the primary vehicle for assigning and maintaining unique patient identifiers.""",
        
        "namespace": "MPIF",
        
        "isVistAPackage": True, # MASTER PATIENT INDEX VISTA - 2005
        
        "inMonograph": True,
        
        "background": """
        
  * In the Phase III Enhancements project, [a] a new 2.4 messaging structure was implemented for the MPI/PD. [b] To reduce the amount of facility-to-facility messaging, the MPI Austin is now the source for update messages rather than the CMOR. For those message types that require CMOR action, the CMOR will update the MPI, and the MPI will distribute updates to the appropriate facilities. 
  * Package in 9.4 is Master Patient Index VistA with prefix MPIF
  
""",

        "TODO": "Why the A28 vs an RG equivalent on Registration",
                
        "protocolReMatch": "MPIF",
    
        "protocolDescriptions": {
        
            "MPIF ADT-A24 CLIENT": "Link patient information message. Results in the addition of the associated/treating facility for an ICN OR the update of the data associated with the associated/treating facility",
            
            "MPIF ADT-A28 CLIENT": "Add new patient message. The MPI will in-turn broadcast out an ADT-A24 (link patient information) message",
            
            "MPIF ADT-A31 CLIENT": "Update patient information) message"
        },
        
        "seeAlsos": [
        "https://www.va.gov/vdl/documents/Infrastructure/Master_Patient_Index_(MPI)/rg1_0_um.pdf",
        "https://www.va.gov/vdl/documents/Infrastructure/Master_Patient_Index_(MPI)/rg1_0_tm.pdf"
        ]
        
    },
    
    "PRF": {

        "label": "Patient Record Flag Synchronization",
        
        "description": """Patient record flags are
used to alert VHA medical staff and employees of patients whose behavior, medical status, or characteristics may pose a threat either to their safety, the safety of other patients or employees, or which may otherwise compromise the delivery of quality safe health care.

Patient record flags are divided into Category I (national) and Category II (local)
flags. Category I flags are nationally approved and distributed by VHA nationally released
software for implementation by all facilities. Category I flags are shared across all known treating facilities for the patient utilizing VistA HL7 messaging, and can only changed or deactivated by the owning facility.
        
When a national Patient Record Flag (PRF) assignment occurs or is edited in VistA or a new patient is registered, messages are sent to other VistAs with the same patient. The other VistAs are recorded in the Treatment Facility List (391.91) file (synchronized separately).""",
        
        "namespace": "DGPF",
        
        "inMonograph": True,
        
        "protocolReMatch": "DGPF PRF",
        
        "protocols": [
            "DGPF PRF ORF/R04 SUBSC", "DGPF PRF ORU/R01 SUBSC", 
            "DGPF PRF QBP/Q11 SUBSC", "DGPF PRF RSP/K11 SUBSC" # only 757 has transfers
        ],
        
        "seeAlsos": [
            "https://www.va.gov/vdl/documents/Clinical/Patient_Record_Flags/prfhl7is.pdf" # patch DG*5.3*425
        ]
        
    },
    
    "PSO": {
    
        "label": "Outpatient Pharmacy",
        
        "description": """Outpatient Pharmacy provides a method for managing the medications given to Veterans who have visited a clinic or who have received prescriptions upon discharge from the hospital.""",
        
        "namespace": "PSO",
        
        "isVistAPackage": True, 
        
        "inMonograph": True,
        
        "protocolReMatch": "PSO (EXT|REMOTE)",
        
        "protocols": ["PSO EXT CLIENT", "PSO REMOTE RX QBP-Q13 ESUBS", "PSO REMOTE RX RDS-O13 ESUBS"],
        
        "linkDescriptions": {
        
            "PSO DISP": "This is the Pharmacy Optifill link. This link sends PHR data to the Vitrea servers. The Vitrea servers then forward the data to the Optifill server located in the Outpatient Pharmacy."
        
        },
        
        "seeAlso": [
        "https://www.va.gov/vdl/documents/Clinical/Pharm-Outpatient_Pharmacy/pso_7_tm_r0218.pdf",
        "https://foia-vista.worldvista.org/Patches_By_Application/PSO-OUTPATIENT%20PHARMACY/PSO-7_SEQ-439_PAT-534.txt",
        
            "https://github.com/department-of-veterans-affairs/vets-api/search?q=VIERS" # ie/ in vets-api
        
        ]
        
    },
        
    "R1NUASTAFF": {
    
        "label": "Acustaf Application",
        
        "description": "Labor-management Solution.",
        
        "protocolReMatch": "R1NUASTAFF",
        
        "background": """

Routines R1NUASB and R1NUASC, File 100100.006, and option R1NUASB have
been added to address the HR data. 

HR data will be gathered to a host file then sftp'd to Acustaf.

ACUSTAF will pull data from Veterans Health Information Systems and Technology Architecture (VistA); Decision Support System (DSS); VA Nursing Outcomes Database (VANOD); and Office of Nursing Service (ONS) to create strategic plans based on retrievable and accurate data. The system shall accommodate today s increasing staffing challenges by using 21st century technology.

""",

        "filesComment": "100100.006 == R1 ACUSTAF HR",

        "_comment": "Build Ambig is that DGRU pull ins will bring in this area's builds as this one registers with DGRU Server protocols and mention them. So be careful with fan out from this one and DGRU being too aggressive - no easy fix. Need to EXCLUDE.",

        "seeAlso": [
        
            "https://www.fedhealthit.com/2019/07/va-intent-to-sole-source-acustaf-software-application/",
            
            "https://www.acustaf.com/" # Labor Management
            
        ]             
        
    },
    
    "R2WL": {
    
        "label": "Welch Allyn CONNEX Vitals Server",
                        
        "protocolReMatch": "R2WL",
        
        "linksSent": True, # links sent in builds BUT IP sent is reset!!! (TODO)
        
        "__buildComment": """Looked at Builds and protocols (which have descrs) but all obvious stuff like 'Subscriber protoocol to transmit A01 ADT message to Welsh Allyn CONNEX COTS System' and really inside implementation stuff that doesn't talk to the HL7 i/f or the server's nature. 
        
        Logical Links and Application Parameters ARE sent/fixed in Builds (one build).
        
        Note that 687 has the Builds/Setup for this BUT no example messages and its 100215 is empty. But 653 has messages and data there. 692 has 100215 but no messages.
        
        Initial build had a description that there was an initial CSV export of VistA users and the never seen R2WL SINGLE PATIENT A08 ADT; second build added the protocols seen in various systems. The second build setup the protocols we see and the links.
        
        Second says R2WL ADT protocols come from VAFC ADT protocols (so TODO: client reg with VAFC ADT generic protocols?). Also [1] adds qualifier 120.85 cross ref (ie/ vitals stuff!) and [2] R2WL VITALS PARAMETER file 100215. 531 has both. 757 neither (so VISN 20 specific?)
        
        File 100215 has [a] default user [b] default location (44) <---- TODO
        
        There's a third build for R2WL that patches but doesn't give protocols or links or ... so it won't come in a lookup. However it would show a debug reset.

""",
        
        "protocolDescriptions": {
        
            "R2WL A08-OP": "A08 Outpatient ADT messages", # as opposed to plain
        
            "R2WL CONNECT CLIENT": "Inbound ORU messages" # only inbound (but not telling much)
            
        }
        
    },
    
    "RAI/MDS": {
    
        "label": "Resident Assessment Instrument / Minimum Data Set (RAI/MDS)",
        
        "description": "Used in Medicare Title 18 skilled nursing facilities and Medicaid Title 19 nursing facilities",
        
        "protocolReMatch": "DGRU\-RAI",
        
        "filesComment": "Seems to send 2 and ... ie/ regular files, again? In builds TODO - 40.8 does have RAI Subscription Number; 42 has RAI field too.",
                
        "_comment": "Build Ambig is that DGRU pull ins will bring in NUA's builds as they register protocols with DGRU Server protocols and mention them. So be careful with DGRU and being too aggressive (make it match explicitly)",
    
    },
    
    "RA": {
    
        "label": "Radiology/Nuclear Medicine",
        
        "description": """Rad/Nuc Med also has the ability to broadcast messages to outside sources. These messages are typically consumed by vendor PACS Systems, VistA Imaging, and Voice Recognition (VR) dictation systems. Rad/Nuc Med broadcasts messages when exams are registered, edited, cancelled or deleted, and reported
or released.

Vendor systems and other applications send Observational Results Unsolicited (ORU) messages back to VistA.

""",

        "_todoDump101": """See subscribers for events ... Eight event driver protocols (RA REG, RA REG 2.3, RA EXAMINED, RA EXAMINED 2.3, RA
CANCEL, RA CANCEL 2.3, RA RPT and RA RPT 2.3) were exported with VistA Rad/Nuc Med and
subsequent patches ... six example subscribers (SEE 101 setup in VISTA .... TODO) ie/ subscribers are VistA specific

Two protocols will be required for Radiology to receive reports from a COTS product. An ORU message type subscriber protocol, and an event-driver. Three event driver protocols (RA VOICE TCP SERVER RPT, RA TALKLINK TCP SERVER RPT and
RA PSCRIBE TCP SERVER RPT) were exported with VistA Rad/Nuc Med and subsequent patches
""",
                        
        "_todo": """[1] follow up on meta files - 'The Diagnostic Code sent to VistA must be one of a predefined set in the VistA Rad/Nuc Med's Diagnostic Codes file (#78.3)' [2] note the ORM/ORU pairings and some have TCP report""",
        
        "_todoMoreBreaks": """
  
Issues:
- RA-MTX (757): PRIMORDIAL RADMETRIX SERVER (PHILIPS PACS)
""",
        
        "contains": ["R1RAAA", "RACARESCAPE", "RANTP", "RASCIMAGE", "RAPSCRIBE", "RATALK", "RAPINESTAR", "RAOTHER"],
        
        "protocolReMatchRemainder": "RA" # not applied yet so need RAOTHER
        
    },
    
    "RACARESCAPE": {
    
        "parent": "RA",
        
        "label": "CARESCAPE",
        
        "protocolReMatch": "RA CARES",
        
        "_todo": "RA CARES24 ORM: RA-CARES24 Link (Care Scape 2.4 for Radiology) - RA-CARES24 Care Scape 2.4 for Radiology --- GE Product ... BUT lookups seem to have it as a monitor, not a voice server even if its protocols listen to the broadcast (many subscribers) of the RA VOICE app in VistA"

    
    },
    
    "RAMTX": {
    
        "parent": "RA",
        
        "label": "Primordial Radmetrix",

        "protocolReMatch": "RA MTX", # 757 only
        
        "_todo": """See messages 
        
        # Protocol Descr RA MTX ORU
## Link RA-MTX
	PRIMORDIAL RADMETRIX SERVER (PHILIPS PACS) ie/ for the Philips PACs?
## Protocol RA MTX ORU
	ORU Protocol for MTX Primordial
	
	    In seeAlso, seems to be reporting dashboard
	    
RadMetrix will receive data from multiple sources and integrate with the Merge PACS to provide a single view of imaging and operational data for actionable decision making, enhancing productivity and workflow.

Royal Philips Electronics announced that its iSite PACS are now available with optional communications tools from Primordial LLC, offering customers communications tools from Primordial LLC specially designed to foster process efficiencies and increase collaboration within radiology departments using iSite.
""",
        
        "seeAlso": ["https://www.radiologybusiness.com/topics/imaging-informatics/primordial-design-and-merge-healthcare-partner-provide-enhanced-business"]
    
    },
    
    "RANTP": {
    
        "parent": "RA",
        
        "label": "National TeleRadiology (NTP)",
        
        "description": """National Teleradiology Program (NTP) reading center is established in California and staffed by VHA radiologists. VA medical centers may contract with the NTP to provide daytime or after-hours interpretation of imaging studies. Its central Teleradiology PACS archive (24 TB) is located in the VA Region 1 data center in Sacramento""",
        
        "protocolReMatch": "RA NTP",
        
        "_note": "PACS Version 2 == PV2", 
        
        "_todo": "Probably a voice server too: 'a COTS voice recognition unit'; 'The v2.4 report message is triggered when National Teleradiology (NTP) releases a study back to the local facility for interpretation. This ‘Release Study’ message will always follow a NTP ‘Released/Unverified (preliminary)’ message.'",
            
    },
    
    "RAOTHER": {
    
        "parent": "RA",
        
        "label": "RA Other",
        
        "protocolReMatch": "RA (?!(CARES|MTX|NTP|SCIMAGE|TALK|PS))",
        
        "_todo": "Replace with fallback ie/ all other RA and no need for explicit exclude RE"
    
    },
    
    "RAPINESTAR": { # 757 only
    
        "parent": "RA",
        
        "label": "Pinestar",
        
        "protocolReMatch": "R3RANM\-PINESTAR"
        
    },
    
    "RASCIMAGE": {
    
        "parent": "RA",
        
        "label": "ScImage",
        
        "protocolReMatch": "RA SCIMAGE",
        
        "_todo": "See the .doc - seems to be in NTP so may move there; seems to be used in NTP",
        
        "seeAlso": ["https://www.va.gov/vdl/documents/Clinical/Radiology_Nuclear_Med/ra5_0rn_p78.doc", "https://scimage.com/"]
        
    },
    
    "RAPSCRIBE": {
    
        "parent": "RA",
    
        "label": "PowerScribe",
        
        "description": "Voice Recognition reporting tool",
        
        "protocolReMatch": "(R1RA|RA) (PSCR|PS360)",
        
        "_todo": "Is R1 for PSCRIBE some centralized version?"
        
    }, 
    
    "RATALK": {
    
        "parent": "RA",
        
        "label": "TalkLink",
        
        "description": "TalkStation is a Voice Recognition reporting tool from Agfa (TalkTechnology)",
        
        "protocolReMatch": "(RA TALK|R1RAAA)",
        
        "seeAlso": ["https://www.diagnosticimaging.com/view/agfa-invests-future-voice-talk-technology-purchase"],
        
        "_aboutMessages": """
        
  * Apps are RA-VOICE-SERVER
  * link is R1RAAA-AGFA
  
""",

        "_about": """As with other Voice (PSCRIBE, SCIMAGE, NTPV2 ...), there are are range of pre-canned RA server protocols for relevant happenings in VistA and these Agra Subscribers are added to them if the Agfa systems are used in a VistA."""

    },
    
    "REM CONS": {
    
        "type": "GROUP OF GROUP",
        
        "label": "Outside Consults",
        
        "description": "Consults that take place outside the facilities managed by this VistA. These include consults at other VA facilities and Community Care consults.",
        
        "note": "Consult Tracking package in Monograph with NS GMRC",
        
        "isVistAPackage": True, # as GMRC
        
        "inMonograph": True, # as GMRC
        
        "contains": ["CCRA", "GMRC HCP", "GMRC IFC"]
        
    },
    
    "RG": {
    
        "parent": "MPI/PD",
        
        "label": "Patient Registration Synchronization",
        
        "protocolReMatch": "RG",
        
        "background": """

  * Clinical Information Resource Network (CIRN) was later broken down to MPI and HDR. Due to its beginnings, you will still notice references to CIRN. This includes application names like RG CIRN in RGMT DEFERRED QRY CLIENT and 
  * RG is 2.4 and listens to 2.3 (VAFC) registration messages ie/ so indirection to MPIF x 2    
        
""",
        
        "protocolDescriptions": {
        
            "RG ADT-A01 2.4 CLIENT": "Admission data to the MPI to support the synchronization of the patients date last treated and/or event reason. May result in the broadcast of a MFN-M05 to other VistAs by the MPI",
            
            "RG ADT-A03 2.4 CLIENT": "Discharge and clinic checkout data to the MPI to support the synchronization of the patients date last treated and/or event reason. May result in the broadcast of a MFN-M05 to other VistAs by the MPI",
            
            "RG ADT-A04 2.4 CLIENT": "Patient has been registered via the Register a Patient option [DG REGISTER A PATIENT]. It does not indicate that the person actually had a treatment session",
            
            "RG ADT-A08 2.4 CLIENT": "Updates to specific patient demographic data. Sent by a batch job that monitors edit events in the ADT/HL7 PIVOT file (#391.71)",
            
            "RGMT DEFERRED QRY CLIENT": "" # need blurbs - can't find - listen only from MPI!
        }
    
    },
    
    "ROES": {
    
        "label": "Remote Order Entry System (ROES)",
        
        "description": """ The Remote Order Entry System (ROES) is the front-end of the Denver Acquisition & Logistics Center (DALC) supply chain/order fulfillment production system. ROES is used by Department of Veterans Affairs (VA) clinicians to place orders for certain types of medical products (hearing aids, prosthetic items, aids for
the visually impaired and assistive devices) and services that are maintained under contract by the DDC.
        
Support for TIU Note input into VistA is a general mechanism first used by the Resident Assessment Instrument/Minimum Data Set (RAI/MDS) application by AccuMed Software. Besides ROES, other projects interested in the interface are the Precision Data Solutions Transcription Service software, and the VA Home Telehealth software (CCRA). The HL7 used to come from VIE but now comes from HC.""",
    
        "protocolReMatch": "TIUHL7 ROES",
    
        "protocolDescriptions": {
        
            "TIUHL7 ROES-PN ORDER MDM SUB": "Medical Records/Information Management - notification of the creation of a document with the accompanying content."
        
        },
        
        "inMonograph": True,
        
        "_todo": "Is this the Prosthetics ref in the Cerner diags ie/ HL7 into VDIF?",
        
        "seeAlso": "https://www.va.gov/vdl/documents/Clinical/CPRS-Text_Integration_Utility_(TIU)/tiuhl7.pdf"
    
    },
    
    "ROR": {
    
        "label": "Clinical Case Registries (CCR)",
        
        "description": "The Clinical Case Registries (CCR) application collects data on the population of veterans with certain clinical conditions.",
        
        "namespace": "ROR",
        
        "inMonograph": True,
        
        "isVistAPackage": True,
        
        "protocolReMatch": "ROR",
    
        "_todo": "HEP-C, HIV; Note that the other end is ROR AAC => AAC!"
        
    },
    
    "SPQ BACKDOOR": {
    
        "label": "SPQ Backdoor",
      
        "description": "Invoke any Remote Procedure Call (RPC) in VistA through a HL7 \"backdoor\". It is used for Billing, Orders, Pharmacy Co-Pays and MPI Integration. For details on this _backdoor_, see the detailed _hl7SPQSummary_ report.",
      
        "protocolReMatch": "XWB RPC SUBSCRIBER"
        
    },
    
    "TELEHEALTH": {
    
        "label": "Telehealth",
        
        "description": "Scheduling and Consults for Tele-Health - other \"Outside\" consults are detailed in _Outside Consults_.",
        
        "note": "TeleHealth is in Monograph with NS's, DGHT and WEBI. But not reflected here",
                
        "contains": ["DG HOME", "TIUHL7", "TMP"],
        
        "_todo": "Other Telehealth potentially is ORDER out (ORM) ... medical order function identifies the device, the observations, the measurement limits, the dialogs used during the observation process, and the progress note templates that are used to report on the patient progress"
    },
    
    "TMP": {
    
        "parent": "TELEHEALTH",
    
        "label": "Telehealth Management Platform (TMP)",
        
        "description": """The Telehealth Management Program (TMP) integrates with Veterans Health Information Systems and Technology Architecture (VistA) to schedule, cancel or update appointments in support of Telehealth services provided by the VA.
        
""",
        
        "protocolReMatch": "(SD TMP|TMP |SD IFS)",
        
        "protocols": [
            "SD TMP SIU-S12 CLIENT", 
            "SD TMP S15 CLIENT SUBSCRIBER", 
            "TMP QBP-Q13 Subscriber", 
            "SD TMP RECEIVE INTRAFACILITY", 
            "SD TMP RECEIVE CANCEL INTRA", 
            "SD IFS SUBSCRIBER",
            "TMP RTB-K13 Subscriber" # only seen in Build, not VistAs
        ],
        
        "_comment": """the Add User To VistA seems to proxy through the MVI ie/ MVI does it? ie/ related traffic?
        
YET MORE SCHEDULING! ie/ CCCP and internal and ...
  
TMP (Microsoft Dynamics 365 Online) <---- MICROSOFT TIE IN

•	The TMP messaging system includes the TMP application, a HealthConnect Ensemble Production and VistA. The HealthConnect Ensemble Production is maintained by the VA’s HealthShare Team. TMP doesn’t have a direct HL7 interface. TMP uses JavaScript Option Notation format (JSON) to exchange messages. However, VistA is not capable of receiving JSON messages directly. VistA relies on the HL7 messaging to do the translation and communication with TMP
•	TMP deploys an InterSystems HealthConnect Ensemble production (HC) that acts as a message transformation and routing system. TMP sends a JSON message to the TMP HC server. HC transforms the JSON to the appropriate HL7 message structure and routes the message to the correct VistA system. VistA responds by sending the appropriate HL7 message to HC where HC transforms the HL7 message to JSON and posts the response on the TMP Rest End Point. 

The Telehealth Management Platform continues this tradition of excellence by simplifying and standardizing telehealth business processes, including for scheduling appointments, telehealth administration, and managing resources.
  * VistA Integration: Appointments that are scheduled or canceled in the Telehealth Management Platform are automatically updated in VistA. Schedulers are no longer required to enter appointments into VistA after scheduling in the Telehealth Management Platform.
  * Resource Databases: Resource data (e.g. facility, site, group, components, users, teams, etc.) can be used to prepopulate required fields (such as for scheduling an appointment).
  * Robust Reporting <------- ie/ here are the reports!
  * Proxy Add to VistA:  Unregistered Veterans who are scheduled through the Telehealth Management Platform will automatically be proxy registered into the distant VistA station <------------ SEE THIS
  * Two types of appt:
    * Clinic-Based scheduling is used to coordinate resources for an appointment between two VA Facilities. 
    * VA Video Connect scheduling is used to coordinate resources for an appointment between a VA Facility and a Veteran’s home. 
        
""",
        
        "seeAlsos": [
            "https://www.va.gov/vdl/application.asp?appid=231", 
            "https://www.va.gov/vdl/documents/Clinical/Telehealth_Management_Platform/telehealthmanagementplatform_tmp_vistatechnicalmanual.docx",
            "https://www.healthcareitnews.com/news/microsoft-cloud-healthcare-touts-telehealth-remote-team-collaboration", # MS push and google's too to follow up
            "https://www.g2xchange.com/statics/rfi-va-telehealth-management-platform-enhancements/", # see rollout
            "https://foia-vista.worldvista.org/Patches_By_Application/SD-SCHEDULING/SD-5p3_SEQ-588_PAT-704.txt"
            
        ]
        
        # May be better as olinkReMatch": "SD TMP"
    
    },
    
    "TIUHL7": {
    
        "label": "Telehealth Progress Note Intake",
    
        "parent": "TELEHEALTH",
        
        "description": "Uses the general-purpose TIU Note Acceptance process to take in TIU Progress Notes from a variety of vendors",
        
        "protocolReMatch": "TIUHL7 ROCHE",
    
        # can't protocol RE and gets MHV too then!
            
        # Shouldn't be TIUHL7 ROES-PN ORDER MDM SUB as that is another user!
        # Shouldn't be MHVSM MDM-T02 Subscriber as that is another user!
        "protocols": ["TIUHL7 ROCHE MDM SUBSCRIBER"] # ROCHE in 757
    },
    
    "TIU CCRA": { # doc sync - expanding GMRC defn (as pkg is TIU)
        
        "parent": "CCRA",
        
        "label": "Community Care Progress Notes (VistA to HSRM)",
        
        "protocolReMatch": "TIU CCRA",
        
        "description": "VistA supports a set of community-care specific, standard progress note titles. Writing a note with one of these titles in VistA triggers an Original document notification and content (MDM-T02) message to HSRM.", 
        
        "_comment": """
        
 the following CCRA Progress Note Titles that are used to file a 
historical Progress Notes
 from CPRS:
      1   COMMUNITY CARE - PATIENT LETTER       TITLE  
      Std Title: NONVA PROGRESS NOTE
     2   COMMUNITY CARE- ADMINISTRATIVE REQUEST       TITLE  
      Std Title: ADMINISTRATIVE NOTE
     3   COMMUNITY CARE-COORDINATION NOTE       TITLE  
      Std Title: NONVA PROGRESS NOTE
     4   COMMUNITY CARE-HOSPITAL NOTIFICATION NOTE       TITLE  
      Std Title: PRIMARY CARE ADMINISTRATIVE NOTE
      
""",
        
        "protocols": [
            "TIU CCRA-HSRM MDM-T02 CLIENT"
        ]
    
    },
    
    "VAF": { # 772 report in VistA pulls all VAF
        
        "parent": "MPI/PD",
        
        "protocolReMatch": "VAF",
        
        "TODO": "v2.3 HL7? Most taken over - via protocol proxying by RG but why these left? As MFN in incoming sync? Or just isolate and continue to expose Listens here?",
        
        "protocolDescriptions": {
        
            "VAFC MFN-M05 CLIENT": "treating facility update message. The HL7 standard has this message updating \"healthcare patient locations, such as nursing units, rooms, beds, clinics, exam rooms\" but VistA/MPI uses it specifically for facility/VistA synchronization", 
            
            "VAFC ADR-A19 CLIENT": "process in a patient query and  respond with a ADR-A19 patient response.  The process will be used to help re-synchronize the MPI with the associated systems that know an ICN"
        }
    
    },
    
    "VBECS": {
    
        "label": "VistA Blood Establishment Computer Software (VBECS)",
        
        "description": """The VistA Blood Establishment Computer Software (VBECS) shall facilitate ongoing compliance with Food and Drug Administration (FDA) standards for 
medical devices.""",
        
        "protocolReMatch": "(VBEC|OR OMG CLIENT)",
        "__noteOnMatch": "OR OMG CLIENT is from OR*3.0*212, a patch that implements the interface between CPRS and VBECS' and the OR OMG SERVER says it 'is triggered whenever an order for a Blood Bank component class or diagnostic test is created in CPRS'. The patch is from 2008 - VBECS, the package (9.4) was distributed in 2009!",
        
        "namespace": "VBEC",
        
        "isVistAPackage": True,
        
        "isMonograph": True,
        
        "seeAlso": [
                "https://vaausdarapp41.aac.dva.va.gov/ee/request/folder/e/123502/c/56/nt/-1?id=1578"
        ],
        
        "_todo": "Note the VBECS 9.4 entry with a blurb that this introduces VBECS."
    
    },
    
    "VDEF": {
    
        "label": "VistA Data Extraction Framework (VDEF)",
        
        "description": """VistA Data Extraction Framework (VDEF) is a VistA package that uses hard-coded M routines to create and deliver Health Level 7 (HL7) messages - it's a framework for extracting VistA data into HL7.""",
        
        "namespace": "VDEF",
        
        "isVistAPackage": True, # see from 2005?
        
        "inMonograph": True,
        
        # Has to explicitly add LA7 LAB RESULTS TO HDR (SUB)
        "protocolReMatch": "([A-Z]+ VDEF|LA7 LAB RESULTS TO HDR \(SUB\)|GMRV ORU R01 VITALS HR)",
        
        "package": "VDEF", # this or connection list is better
        
        "links": ["VDEFVIE1", "VDEFVIE2", "VDEFVIE3", "VDEFVIE4"],
        
        "_todo": "see debug versions VDEFVIE1-4 and variation of messages -- mainly ORU^R01 but RDE~O... for PSO"
        
    },
    
    "VFAL": { # 653 only - one build doesn't have good description - TODO
    
        "label": "Logicare",
        
        "protocolReMatch": "VFAL"
    
    },
    
    "XUMF": {
    
        "label": "Master File Server (MFS)",
        
        "description": """The Master File Server allows VA FileMan Master Files to be maintained""",
        
        "protocolReMatch": "XUMF",
        
        "protocolDescription": {
        
            "XUMF MD5 HANDLER": "Master File Query messages from the VETS service",
            
            "XUMF 04 MFK": "Master File Notifications for the Institution File"
            
        },
        
        "fileComment": "MASTER FILE PARAMETERS distributed with the build",
        
        "_todo": "Seems to be related to MFN ... Master File Notification ... MUST CHECK OUT THIS SYNC (sync 4, sync? ...)"
            
    }

}

"""
Based on Categorical Hierarchy, matching transactions - done manually based on the above (for now). May move to group by sendingApplication or ... and auto populate descriptions later. For now, MANUAL ABOVE (version 1!)

TODO: move to 'subsystem' ie/ so can eventually have a block diagram of black box VistA with its subsystems (each with a minimum of K IO) ie/ those parts of VistA that source or sink HL7!
"""
def muByGroup(transactions, transactionInfo, debug=False):

    linkLabelsByServiceType = transactionInfo["linkLabelsByServiceType"]
    standardListener = transactionInfo["standardListener"]
    llInfoById = transactionInfo["llInfoById"]
    
    def getFirstOResource(transaction):
        if transaction[0]["transmission_type"] == "O:OUTGOING": # always want first out
            resource = transaction[0]
        else: # is there a resource with a link other than first link!
            ilink = transaction[0]["logical_link"]["label"]
            olinkResources = [r for r in transaction if r["logical_link"]["label"] != ilink]
            if len(olinkResources) == 0:
                return None  
            resource = olinkResources[0] # first out
        return resource
    """
    TODO: issue for IFCAP etc where ILINK not standard -- should do O:I as
    qualifier (or combine em). PRCP SU INV UPDATE (IFCAP) should have own incoming.
    """
    def getTransactionOLink(transaction, standardListener, reduceVISTAs=True):
    	# Bonus check
        links = set(resource["logical_link"]["label"] for resource in transaction)
        if len(links) > 2:
            raise Exception("Transaction can have at most 2 links - one out, one in")
        resource = getFirstOResource(transaction)
        if not resource:
            return ""
        ll = resource["logical_link"]["label"]
        # 531 had PENDINGs and there OLink set to standard listener (temporarily?)
        # TODO: CONSIDER Nixing olinks
        if ll == standardListener and resource["status"]["label"] != "PENDING TRANSMISSION":
            print(json.dumps(transaction, indent=4))
            print()
            print(json.dumps(resource, indent=4))
            raise Exception("Never expect outgoing to VistA's own Standard Listener unless PENDING")
        if reduceVISTAs and re.match(r'VA[A-Z]{3}$', ll):
            ll = "VISTA"
        return ll
    # TODO: version 2 - move msh parse data into reduction 773/772 below
    def getLocalRemote(fresource):
        exclFACRE = '(^\d+$|\^|DNS|VAMC|^DSS$)'
        hl7TemplateMaker = HL7TemplateMaker(False)
        mshInfo = hl7TemplateMaker.parseMSH(fresource["msh"])
        if mshInfo == None:
            return "", ""
        if fresource["transmission_type"] == "O:OUTGOING":                
            local = mshInfo["sendingApplication"] if "sendingApplication" in mshInfo else ""
            remote = mshInfo["receivingApplication"] if "receivingApplication" in mshInfo else ""
            # Want facility if not just a station no or DNS or VAMC name or ...
            if "receivingFacility" in mshInfo and not re.search(exclFACRE, mshInfo["receivingFacility"]):
                remote = f'{remote}/{mshInfo["receivingFacility"]}'            
        else: # incoming
            remote = mshInfo["sendingApplication"] if "sendingApplication" in mshInfo else ""
            # Want facility if not just a station no or DNS or VAMC name or DSS
            if "sendingFacility" in mshInfo and not re.search(exclFACRE, mshInfo["sendingFacility"]):
                remote = f'{remote}/{mshInfo["sendingFacility"]}'
            local = mshInfo["receivingApplication"] if "receivingApplication" in mshInfo else ""        
        return local, remote 
        
    """
    TODO: suggestion breakdown by SENDAPP:[SENDFAC]/RECVAPP:[RECVFAC] both for:
    - 2 msg Listener only => don't know link and may breakdown! 
    - situation of one link, one protocol and various senders! (R1NUASTAFF PROTOCOL)
    ie/ if local and remote are multiples => extra break criteria ... V2
    """
    protocolsTransactions = Counter()
    protocolsTransactionsLC = defaultdict(lambda: Counter())
    protocolsTransactionsListenNonStandard = defaultdict(lambda: Counter())
    protocolsMsgCount = defaultdict(lambda: Counter())
    protocolsMessageTypes = defaultdict(set)
    protocolsLocalApps = defaultdict(lambda: Counter())
    protocolsRemoteApps = defaultdict(lambda: Counter())
    protocolsTransactionsOLL = defaultdict(lambda: Counter()) 
    protocolsBHS = set()
    startTimeTR = datetime.now()
    print("Start tranversing transactions to count by protocol")
    for i, transId in enumerate(transactions, 1):
        if i % 50000 == 0:
            print(f"\tTraversed 50K more to {i}")
        fresource = transactions[transId][0] # ie/ just request 
        sp = fresource["subscriber_protocol"]["label"]
        spl = sp # if no link then spl == sp
        olink = getTransactionOLink(transactions[transId], standardListener)
        if olink:
            protocolsTransactionsOLL[sp][olink] += 1
            spl = f'{sp}:{olink}' # will combine and then nix link if only one in set ie/ # sps == # sp:ols
        protocolsTransactions[spl] += 1
        # Protocol/Link combo should be unique but if listener only (don't know link)
        # or just?, perhaps > 1 APP combos for the combo. Allowing for that.
        local, remote = getLocalRemote(fresource)
        if local:
            protocolsLocalApps[spl][local] += 1
        if remote:  
            protocolsRemoteApps[spl][remote] += 1            
        protocolsMsgCount[spl][len(transactions[transId])] += 1
        if "_message_type" in fresource: # not BHS
            mt = f'{fresource["_message_type"]} [{fresource["_version_id"]}]' if "_version_id" in fresource else fresource["_message_type"]
            protocolsMessageTypes[spl].add(mt)
        if fresource["transmission_type"] == "I:INCOMING":
            protocolsTransactionsLC[spl]["LISTENER"] += 1
            if fresource["logical_link"]["label"] != standardListener:
                protocolsTransactionsListenNonStandard[
                spl][fresource["logical_link"]["label"]] += 1
        else:
            protocolsTransactionsLC[spl]["CLIENT"] += 1                        
        if "_is_bhs" in fresource:
            protocolsBHS.add(spl)
        elif spl in protocolsBHS:
            raise Exception("Inconsistent BHS/MSH for protocol") 
    print(f'... finished tranversing transactions - break by protocol - in {datetime.now() - startTimeTR}')

    tops = []
    leaves = []
    matchedProtocols = set() # check
    protocolsTransactionsOnlyP = set(prtm.split(":")[0] for prtm in protocolsTransactions)
    for pgId in PROTOCOL_SUBSYSTEMS:
    
        gInfo = PROTOCOL_SUBSYSTEMS[pgId]
        gInfo["id"] = pgId
    
        if "protocolReMatch" in gInfo:
            leaves.append(gInfo) # could be a top too!
            gInfo["protocolTransactions"] = {}
            gInfo["protocolTransactionsTotal"] = 0
            for sp in protocolsTransactions:
                if "protocolReExclude" in gInfo and re.match(gInfo["protocolReExclude"], sp):
                    continue
                if re.match(gInfo["protocolReMatch"], sp):
                    if sp in matchedProtocols:
                        raise Exception(f"Protocol {sp} matched > 1 Grouping")
                    matchedProtocols.add(sp)
                    gInfo["protocolTransactions"][sp] = protocolsTransactions[sp]
                    gInfo["protocolTransactionsTotal"] += protocolsTransactions[sp]
                    
        # consider merge up
        if "parent" in gInfo:
            pgInfo = PROTOCOL_SUBSYSTEMS[gInfo["parent"]]
            if "children" not in pgInfo:
                pgInfo["children"] = []
            pgInfo["children"].append(gInfo)       
            # Reentrancy issue with static hierarchy so if call this mu twice
            # will recalc. Avoid that.
            if "protocolTransactionsTotal" in pgInfo:
                del pgInfo["protocolTransactionsTotal"]         
        else:
            tops.append(gInfo) 
            
    # Unmatched
    umgInfo = {
        "id": "ZZUngrounded",
        "label": "ZZ Protocols",
        "description": "Protocols that haven't yet been analyzed and assigned to a category.",
        "protocolTransactions": {},
        "protocolTransactionsTotal": 0
    }
    tops.append(umgInfo)
    leaves.append(umgInfo) # for completeness
    for pr in list(set(protocolsTransactions) - matchedProtocols):
        umgInfo["protocolTransactions"][pr] = protocolsTransactions[pr]
        umgInfo["protocolTransactionsTotal"] += protocolsTransactions[pr]
            
    def totalUp(gInfo, ttlToAdd):
        if "parent" not in gInfo:
            return
        pgInfo = PROTOCOL_SUBSYSTEMS[gInfo["parent"]]
        if "protocolTransactionsTotal" not in pgInfo:
            pgInfo["protocolTransactionsTotal"] = 0          
        pgInfo["protocolTransactionsTotal"] += ttlToAdd
        totalUp(pgInfo, ttlToAdd)
    for gInfo in leaves:
        totalUp(gInfo, gInfo["protocolTransactionsTotal"])
    ttlTransactions = sum(protocolsTransactions[sp] for sp in protocolsTransactions)
    if sum(gInfo["protocolTransactionsTotal"] for gInfo in tops) != ttlTransactions:
        print(sum(gInfo["protocolTransactionsTotal"] for gInfo in tops), ttlTransactions, sum(gInfo["protocolTransactionsTotal"] for gInfo in leaves))
        raise Exception("Bug in totalling up") # shouldn't happen as even ensured no re-entrancy problem
                 
    # Protocol+Link is unique (well expected to be ... TODO: perhaps apps distinguish)
    def muProtocolLinkSet(gInfo, level=0):
        try:
            if gInfo["protocolTransactionsTotal"] == 0:
                return ""
        except:
            print(json.dumps(gInfo, indent=4))
            raise
        lblPart = gInfo["label"] if "label" in gInfo else gInfo["id"]
        if level == 0:
            # JONATHAN M. WAINWRIGHT VAMC {#jonathan_m__wainwright_vamc}
            lblPart = lblPart + ' {#' + re.sub(r'[ \/]', '_', gInfo["id"]) + '}'
        headerMU = "##"
        l = level
        while l > 0:
            headerMU += "#"
            l = l - 1
        mu = f'{headerMU} {lblPart}\n\n'
        gtmu = f"This group has <span class='yellowIt'>{reportAbsAndPercent(gInfo['protocolTransactionsTotal'], ttlTransactions)}</span> transactions." if level == 0 else ""
        if "description" in gInfo:
            mu += f'{gInfo["description"]} {gtmu}\n\n'
        else:
            mu += f'{gtmu}\n\n'
        if "children" in gInfo: 
            for cgInfo in sorted(gInfo["children"], key=lambda x: x["id"]):
                mu += muProtocolLinkSet(cgInfo, level+1)
            return mu
        cols = [":VistA Protocol", ":Link", ":Message Type(s)", ":Transactions (O/I)", "Per", "Local", "Remote"]
        if "protocolDescriptions" in gInfo:
            cols.append(":Description")
        tbl = MarkdownTable(cols, includeNo=True if len(gInfo["protocolTransactions"]) > 1 else False)
        for prl in sorted(gInfo["protocolTransactions"], key=lambda x: gInfo["protocolTransactions"][x], reverse=True):
            if len(protocolsTransactionsLC[prl]) == 1:
                cl = list(protocolsTransactionsLC[prl])[0]
                dir = "I" if cl == "LISTENER" else "O"
                if len(gInfo["protocolTransactions"]) == 1:
                    ttlMU = f'{gInfo["protocolTransactionsTotal"]} [{dir}]'
                else:
                    ttlMU = f'{reportAbsAndPercent(protocolsTransactionsLC[prl][cl], gInfo["protocolTransactionsTotal"])} [{dir}]'
            else:
                ttlMU = f'{reportAbsAndPercent(gInfo["protocolTransactions"][prl], gInfo["protocolTransactionsTotal"])}<br>{reportPercent(protocolsTransactionsLC[prl]["CLIENT"], gInfo["protocolTransactions"][prl])}/{reportPercent(protocolsTransactionsLC[prl]["LISTENER"], gInfo["protocolTransactions"][prl])}'
            pmcMU = list(protocolsMsgCount[prl])[0] if len(protocolsMsgCount[prl]) == 1 else "/".join([f"{cntType} [{protocolsMsgCount[prl][cntType]}]" for cntType in sorted(protocolsMsgCount[prl], key=lambda x: protocolsMsgCount[prl][x], reverse=True)])
            ll = prl.split(":")[1] if re.search(r':', prl) else ""
            if ll == "VISTA":
                ll = "Other VistA"
            row = [
                f'__{re.sub("_", " ", prl.split(":")[0])}__', 
                re.sub(r'_', ' ', ll) if ll else "&nbsp;",
                "/ ".join(sorted(list(protocolsMessageTypes[prl]))) if prl in protocolsMessageTypes else "-", # BHS
                ttlMU,
                pmcMU,
                muBVC(protocolsLocalApps[prl]) if prl in protocolsLocalApps else "&nbsp;",
                muBVC(protocolsRemoteApps[prl]) if prl in protocolsRemoteApps else "&nbsp;" 
            ]
            if ":Description" in cols: 
                row.append("&nbsp;" if not (prl.split(":")[0] in gInfo["protocolDescriptions"] and gInfo["protocolDescriptions"][prl.split(":")[0]]) else gInfo["protocolDescriptions"][prl.split(":")[0]])
            tbl.addRow(row)
        mu += tbl.md() + "\n\n"
        lls = set(prl.split(":")[1] for prl in gInfo["protocolTransactions"] if re.search(r'\:', prl) and prl.split(":")[1] != "VISTA")
        if len(lls): # if all listen => none
            tblObj = tblLinkSet(lls, llInfoById, linkDescriptions=gInfo["linkDescriptions"] if "linkDescriptions" in gInfo else None)
            if tblObj: # ie/ links have more than a name
                mu += "This group uses the following non VistA links ...\n\n"
                mu += tblObj.md() + "\n\n"
        return mu
        
    mu = "# Functional Groupings\n\n"
    tocSummTBL = MarkdownTable([":Group", "Transactions"])
    for gInfo in sorted(tops, key=lambda x: x["protocolTransactionsTotal"], reverse=True): # Alpha order    
        refId = re.sub(r"[ \/]", "_", gInfo["id"])
        if gInfo["protocolTransactionsTotal"] == 0:
            continue
        tocSummTBL.addRow([
            f'__[{gInfo["label"] if "label" in gInfo else gInfo["id"]}](#{refId})__',
            reportAbsAndPercent(gInfo["protocolTransactionsTotal"], ttlTransactions)
        ])
    mu += tocSummTBL.md() + "\n\n" 
    for gInfo in sorted(tops, key=lambda x: x["label"]): # Alpha order    
        if gInfo["protocolTransactionsTotal"] == 0:
            continue
        mu += muProtocolLinkSet(gInfo)
    
    return mu
    
def tblLinkSet(linkSet, llInfoById, llsNSListenerSeen=None, linkDescriptions=None):
    rows = []
    colMap = {
        "link": ":Link",
        "description": ":Description",
        "mailman_domain": "Domain MailMan",
        "dns_domain": "Domain DNS",
        "institution": "Institution",
        "tcp_ip_address": "IP Address"
    }
    propsInRows = set(["link"])
    for ll in sorted(list(linkSet)):
        linkInfo = llInfoById[ll]
        llLabel = f'__{ll}__'
        if llsNSListenerSeen and ll in llsNSListenerSeen:
            llLabel = f'{re.sub("_", " ", ll)} [LISTENER]'
        row = {"link": llLabel}
        rows.append(row)
        if linkDescriptions and ll in linkDescriptions:
            row["description"] = linkDescriptions[ll]
        for prop in colMap:
            if prop == "link":
                continue
            if prop in linkInfo:
                propsInRows.add(prop)
                if isinstance(linkInfo[prop], dict):
                    row[prop] = linkInfo[prop]["label"]
                else:
                    if prop == "tcp_ip_address" and re.match(r'10\.(224|226|245|247)\.', linkInfo[prop]):
                        row[prop] = f'__{linkInfo["tcp_ip_address"]}__ [AAC]'
                        continue
                    if prop == "description":
                        descr = "<br>".join(linkInfo[prop].split("\n"))
                        if "description" in row:
                            row["description"] = f'{descr}<br>{row["description"]}'
                        else:
                            row["description"] = descr
                        continue
                    row[prop] = linkInfo[prop]
    colMap = dict((col, colMap[col]) for col in colMap if col in propsInRows)
    if len(colMap) == 1: # LL only
        return None
    tbl = MarkdownTable(list(colMap.values()), includeNo=True if len(rows) > 1 else False)
    for row in rows:
        nrow = []
        for col in colMap:
            if col in row:
                nrow.append(row[col])
            else:
                nrow.append("&nbsp;")
        tbl.addRow(nrow)
    return tbl

"""
Background 1: about source data
"""
def muBackgroundMessageLogs(transactions, info):

    mu = "## HL7 Log Data behind this Report\n\n"    
            
    mu += f'''VistA logs full, representative HL7 traffic for between 3 and 8 days depending on how it's configured - this system keeps successful messages or messages waiting for responses for <span class="yellowIt">{info["purgeTimeGap"]}</span> days.
    
Some aspects of logging depend on the packages sending or receiving the HL7 messages and packages are not consistent. For example, Community Care (CCRA) sends messages asking for application acknowledgement but only uses HL7 acknowledgements - this means success messages never get beyond the _AWAITING APPLICATION ACKNOWLEDGEMENT_ state. These differences demand nuance from the HL7 log Extractor which assembled the data behind this report.

'''
    mu += f'The following gives how many messages are in this system and how many are relevant for analysis ...\n\n'
    
    tbl = MarkdownTable([":Property", "Value"], includeNo=False)
    tbl.addRow(["Total Messages", f'{info["totalMsgs"]:,}'])
    suppressed = sum(info["suppressedWhy"][sw] for sw in info["suppressedWhy"])
    relevant = info["totalMsgs"] - suppressed
    tbl.addRow(["Relevant Messages", f'{reportAbsAndPercent(relevant, info["totalMsgs"])}'])
    tbl.addRow(["Suppressed Messages", f'{reportAbsAndPercent(suppressed, info["totalMsgs"])}'])
    mu += tbl.md() + "\n\n"
    
    mu += "Messages are suppressed for a variety of reasons ...\n\n"
    tbl = MarkdownTable([":Property", "Value"], includeNo=False)
    for sw in sorted(info["suppressedWhy"], key=lambda x: info["suppressedWhy"][x], reverse=True):
        tbl.addRow([re.sub("_", " ", sw), info["suppressedWhy"][sw]])
    mu += tbl.md() + "\n\n"

    # REM: last entry in tran's entered or the status update time of the first trans
    # sets the date of the transaction for purge window purposes. Possible that entry
    # of first member of trans is outside window but last update is within it
    mu += f"Relevant Messages are gathered into <span class='yellowIt'>{info['totalTransactions']:,}</span> transactions. The following shows the count per day where day is the last time a transaction was updated ...\n\n"
    dayCounter = Counter()
    statusCounterByDay = defaultdict(lambda: Counter())
    for tid in transactions:
        fresource = transactions[tid][0]
        ttime = fresource["status_update_date_time"]["value"] if "status_update_date_time" in fresource else fresource["date_time_entered"]["label"]
        day = ttime.split("T")[0]
        status = fresource["status"]["label"]
        statusCounterByDay[day][status] += 1
        dayCounter[day] += 1
    tbl = MarkdownTable([":Day", "Count", ":Status'"], includeNo=False)
    for day in sorted(dayCounter):
        dayDT = datetime.strptime(day, "%Y-%m-%d")
        dayMU = f'__{day}__ [{dayDT.strftime("%A")}]'
        tbl.addRow([dayMU, dayCounter[day], muBVC(statusCounterByDay[day])])
    mu += tbl.md() + "\n\n"
        
    return mu
    
"""
Want basic config setup.

Config
- 779_1: HLO SYSTEM PARAMETERS http://localhost:9100/rambler#779_1-1 (Singleton in 687)... seems to have "bad message retention days" and "normal message retension days" ... see in all + domain name

TODO MAYBE:
- 771: HL7 APPLICATION PARAMETER, referenced from 773 receiving or sending application
  but no info beyond ref in 773's! SO may leave to dynamic message setup UNTIL make own
  META static definition of these "applications" 
  <--------- of real interest: Austin vs other VistAs etc. May get from logical link. See
  link expansion below. Do links give indication of Austin vs?
  
TODO: HL7 message/meta setup 

773's fast_purge_dt_tm (__time_to_fast_purge ie/ gap!)
"""
def muHLOConfig(hloSystemParameters):
    
    mu = """# The HLO Settings
    
The basic operation of HL7 is configured in a single entry in file 779.1. 

Note the values for normal and bad message retention. These settings decide how long the system keeps logs of successful and errored messages. In general, VistA does not keep messages for long but the logs have enough messages to allow a full account of the HL7 messaging of a system.

"""
    
    tbl = MarkdownTable([":Property", "Value"])
    for prop in hloSystemParameters:
        if prop in ["_id", "type", "label"]:
            continue
        val = hloSystemParameters[prop]
        if isinstance(val, dict):
            val = f'{val["label"]} [{val["id"]}]'
        elif re.match(r'[A-Z\d]\:', val):
            val = val.split(":")[1]
        tbl.addRow([
            "__{}__".format(re.sub(r'\_', ' ', prop)) if re.search(r'retention', prop) else re.sub(r'\_', ' ', prop),
            val
        ]) 
    mu += tbl.md() + "\n\n"
    
    return mu
    
# ########################## Reduce 773 Transaction Info #######################
        
"""
Two pass - useable transactions (HL7-level) out of 773 and 772
"""
def reduce773Transactions(stationNo): 

    tmpLocn = f'{VISTA_DATA_BASE_DIR}{stationNo}/TmpWorking/'
    sredFile = f'{tmpLocn}_773TransactionRed.db'
    metaFile = f'{tmpLocn}_773RedMeta.json'
    if os.path.isfile(sredFile):
        print("Loading premade 773 Reduction (small JSON + .db) from \"{}\"".format(sredFile))
        stransactions = shelve.open(sredFile, flag='r')
        meta = json.load(open(metaFile))
        print("... loaded")
        return stransactions, meta
        
    print("Must create reduction from scratch")
    startTime = datetime.now()
            
    _779_1 = reduce779_1(stationNo)
    HLOSTANDARDLISTENER = _779_1["hlo_standard_listener"]["label"]
    linkLabelsByServiceType = defaultdict(list)
    llInfoByIEN = reduce870(stationNo)
    for ien in llInfoByIEN:
        llInfo = llInfoByIEN[ien]
        if "tcp_ip_service_type" not in llInfo:
            continue                 
        linkLabelsByServiceType[llInfo["tcp_ip_service_type"]].append(llInfo["label"])
        
    # GOAL - redo hl7Utils for a 773 with correct 772 pieces and fixes
        
    """
    Cache note:
    
    One
    - message text by 772IEN
    - ctrlId, MSA by IEN
    """
        
    dataLocn = f'{VISTA_DATA_BASE_DIR}{stationNo}/Data/'
    resourceIter = FilteredResultIterator(dataLocn, "772")
    hl7TemplateMaker = HL7TemplateMaker(False)
    msaBy772IEN = {}
    ipt772TextRedFile = f'{tmpLocn}ipt772TextRed.db' # ipt = in process tmp
    messageTextBy772IEN = shelve.open(ipt772TextRedFile)
    _772IENs = set() # for full orphan catch
    _772SkippedAsNoMessageText = set()
    timeFor50Start = datetime.now()
    for i, resource in enumerate(resourceIter, 1):
        if i % 50000 == 0:
            after50Time = datetime.now() # want to see if slows
            print(f"Traversed 50K more 772's to {i} in {after50Time - timeFor50Start}")
            timeFor50Start = after50Time
        _772IEN = resource["_id"].split("-")[1]
        _772IENs.add(_772IEN)
        if "message_text" not in resource:
            _772SkippedAsNoMessageText.add(_772IEN)
            continue
        messageTextBy772IEN[_772IEN] = resource["message_text"] # for here, not st
        msaSegments = [seg for seg in re.split(r'\n+', resource["message_text"]) if re.match(r'MSA[^A-Z\d]', seg)]
        if len(msaSegments):
            hl7TemplateMaker = HL7TemplateMaker(False) # reset splitters
            msgCtrlIdLocals = set()
            ackCodes = set()
            for msaSegment in msaSegments:  
                try:
                    msaInfo = hl7TemplateMaker.parseMSA(msaSegments[0])
                except:
                    print(msaSegments)
                    raise
                # Saw MSAs ie/ > 1 and a set of 'errors' sent back with - breaks 
                msgCtrlIdLocal = msaInfo["msgCtrlIdLocal"].split("-")[0]
                msgCtrlIdLocals.add(msgCtrlIdLocal)
                ackCodes.add(msaInfo["ackCode"])
            msaBy772IEN[_772IEN] = {
                "msgCtrlIdLocal": list(msgCtrlIdLocals)[0],
                "ackCode": list(ackCodes)[0]
            }
    print(f"PASS 772 Gather Complete in {datetime.now() - startTime}: {len(msaBy772IEN)} out of {i} were MSAs, {i - (len(_772SkippedAsNoMessageText) + len(msaBy772IEN))} not MSAs and {len(_772SkippedAsNoMessageText)} were skipped as no message text")
        
    """
    # Equivalent to "enhanced 773" pass where 773 gets [1] MSA
    # and [2] correct message type
    
    ie/ st of [a] #_msa, [b] status, [c] transmission_type,
    [d] logical_link where a is introduced in an E walk (clears
    up issue of 'missing acknowledgement_to' and _message_type 
    (which clears up app ack resetting message_type/event_type)
    is also present for calculation (and could be added to split)
    """
    dataLocn = f'{VISTA_DATA_BASE_DIR}{stationNo}/Data/'
    resourceIter = FilteredResultIterator(dataLocn, "773")
    hl7TemplateMaker = HL7TemplateMaker(False) 
    messageIdsSeen = set()
    # messageIdsSuppressedForStatus = {}
    _772IENW773 = set()
    msaToSourceMap = {}
    suppressedWhy = Counter()
    allSPsSeen = Counter() # For QAs
    sredFileIPT = f'{tmpLocn}ipt773TransactionRed.db'
    transactions = shelve.open(sredFileIPT)   
                    
    _773Total = 0 # For QA at end
                
    def suppressResource(phase, resource, why):
        suppressedWhy[f'{phase}:{why}'] += 1
        resource["_suppressed"] = why
        """
        # REMAINS unresolved ... why one TMP type totally removed
        if "subscriber_protocol" in resource and re.match(r'(RGMT|SD TMP)', resource["subscriber_protocol"]["label"]):
            print(json.dumps(resource, indent=4))
            print(why)
            print()
        """
        
    # Avoid WriteBack in Shelve (slow - too much memory) though does
    # lead to growing Shelve which needs to be rewritten.
    def addToResourcesList(transactions, messageId, resource):
        temp = transactions[messageId]
        temp.append(resource)
        transactions[messageId] = temp
                       
    # Pass 1 773 - [1] corrupt resources suppressed [2] Make Transactions w/MSA correlate
    # ... note: simple layer 5 transaction - complex, application level transactions are 
    # not assembled as they depend on beyond-messaging, transaction ids in 
    # specific segments (layer 7 stuff) ex/ NTE segments for IFCs is a level above.
    startTimePass1 = datetime.now()
    timeFor50Start = startTimePass1
        
    for i, resource in enumerate(resourceIter, 1):
        
        if sum(1 for prop in resource if re.match(r'hlp', prop)):
            json.dumps(resource, indent=4)
            raise Exception("Didn't expect any hlp properties - facility unused") 
    
        _773Total += 1
        
        if i % 50000 == 0:
            after50Time = datetime.now() # want to see if slows
            print(f"Traversed 50K more 773's to {i} in {after50Time - timeFor50Start}")
            timeFor50Start = after50Time
    
        # Want a unified record - MSA is better than any ACK!
        _772IEN = resource["date_time_entered"]["id"].split("-")[1]
        if _772IEN not in messageTextBy772IEN:
            suppressResource("1", resource, "772_NO_MESSAGE_TEXT")
            continue
        resource["_message_text"] = messageTextBy772IEN[_772IEN]
        _772IENW773.add(_772IEN) # for orphans and subset of orphans with MSA!
    
        if "msh" not in resource: # st reduction could be ignored
            suppressResource("1", resource, "MISSING_MSH")
            continue
        if re.match(r'MSH', resource["msh"]):
            mshInfo = hl7TemplateMaker.parseMSH(resource["msh"]) # auto resets separators
            # Issue that 773's actual message_type, event_type overridden by app acks
            # in the "one response" case. Got to put it back for st!
            resource["_message_type"] = mshInfo["messageType"]
            if "versionId" in mshInfo:
                resource["_version_id"] = mshInfo["versionId"]
            if resource["message_id"] != mshInfo["messageCtrlId"]:
                # Saw ONLY in 531 -- put back Exception here when tightening up
                suppressResource("1", resource, "MHS_NO_CTRLID_OR_MISMATCH")
                continue
            resource["_sending_application"] = mshInfo["sendingApplication"]
            resource["_receiving_application"] = mshInfo["receivingApplication"]
        elif re.match(r'BHS', resource["msh"]):
            bhsInfo = hl7TemplateMaker.parseBHS(resource["msh"]) 
            if resource["message_id"] != bhsInfo["ctrlId"]:
                suppressResource("1", resource, "BHS_NO_CTRLID_OR_MISMATCH")
                continue
            resource["_is_bhs"] = True
            resource["_sending_application"] = bhsInfo["sendingApplication"]
            resource["_receiving_application"] = bhsInfo["receivingApplication"]   
        else: # seems blank or just sentences ... may enforce/distinguish
            suppressResource("1", resource, "MSH_NOT_MSH_OTHER")
            continue                
        messageId = resource["message_id"]
        messageIdsSeen.add(messageId)
        
        if "status" not in resource: # would be st on own
            suppressResource("1", resource, "NO_STATUS")
            continue
            
        if "logical_link" not in resource: # would be in st on own
            if not re.search(r'\u0000', resource["msh"]):
                print("NO LL", json.dumps(resource, indent=4))
                raise Exception("Non rubblish msh ie/ not just \u0000's but still no LL")
            suppressResource("1", resource, "MISSING_LL_U0000MSH")
            continue
                    
        # Case where error is "Event Protocol Not Found" - very special (just want to
        # record it so putting early in suppression chain)
        if "subscriber_protocol" not in resource:
            if (
                resource["status"]["label"] == "ERROR" and
                resource["transmission_type"] == "I:INCOMING" and 
                "acknowledgement_to" not in resource
            ):
                sreason = "MISSING_PROTOCOL_ERRORASCANTFIND"
            else:
                sreason = "MISSING_PROTOCOL_OTHER"
            suppressResource("1", resource, sreason)
            continue   
            
        allSPsSeen[resource["subscriber_protocol"]["label"]] += 1     
                            
        """
        # Allow SUCCESS | ERROR | AWAITING | PENDING 
        # THRU (awaiting as CCRA treats differently, see RA-SERVER with PENDING)
        if not re.match(r'(SUCCESS|AWAITING|ERROR|PENDING)', resource["status"]["label"]):
            suppressResource("1", resource, f"EXCLUDE_STATUS_{re.sub(r' ', '_', resource['status']['label'])}")
            messageIdsSuppressedForStatus[messageId] = resource["status"]["label"]
            continue       
        """     
            
        # NOTE: must come AFTER suppress PENDING_TRANSMISSION as they mess things up
        if _772IEN in msaBy772IEN:
            msaInfo = msaBy772IEN[_772IEN]
            resource["_msa_to"] = msaInfo["msgCtrlIdLocal"] # message id
            resource["_msa_ack_code"] = msaInfo["ackCode"] # for error etc
        elif "acknowledgement_to" in resource: # 773 QA
            print(json.dumps(resource, indent=4))
            raise Exception("Acknowledgement To in 773 but 772 lacks an MSA")
                                                                    
        """
        Tie in MSA for success, awaiting, error
        
        Note: exception is MSA for unexpected states 
        """    
        if "_msa_to" not in resource:
            if messageId in transactions:
                # Can be error with dup (resource['error_type']['label']) [687]
                # but 757 has a lab dup that isn't in error
                print(f"Adding extra non MSA trans: {resource['error_type']['label'] if 'error_type' in resource else 'NOT ERROR'}") # TODO: lot's of warnings in ANC
                addToResourcesList(transactions, messageId, resource)
            else:
                transactions[messageId] = [resource]
        else:
            msaTo = resource["_msa_to"] # QA'ed above that this exists
            if msaTo in transactions:
                addToResourcesList(transactions, msaTo, resource)
                msaToSourceMap[messageId] = msaTo # in cases of ACK to ACK
            elif msaTo in msaToSourceMap:
                if resource["_msa_ack_code"][-1] != "A":
                    raise Exception(f'Expect ACK to APP ACK to always be success but {resource["_msa_ack_code"]}')
                reqTo = msaToSourceMap[msaTo]
                addToResourcesList(transactions, reqTo, resource)
            elif msaTo in messageIdsSeen:
                suppressResource("1", resource, "MSA_TO_SUPPRESSED_TRANSACTION") 
            else:
                suppressResource("1", resource, "MSA_WITHOUT_TRANSACTION")
                
    messageTextBy772IEN.close()
                                
    print(f"PASS 1 COMPLETE (took {datetime.now() - startTimePass1}) - [1] corruption suppress, [2] Transactions from MSA correlation: suppressed {sum(suppressedWhy[sw] for sw in suppressedWhy)} resources out of {i}, leaving {len(transactions)} transactions")
    spsOfTrans = set(transactions[tid][0]["subscriber_protocol"]["label"] for tid in transactions)
    if len(set(allSPsSeen) - spsOfTrans):
        print(f"\t** Warning post PASS 1: protocols {dict((sp, allSPsSeen[sp]) for sp in (set(allSPsSeen) - spsOfTrans))} have been completely suppressed")
                        
    """
    Pass 2 - only keeping transactions in the NORMAL MESSAGE PURGE WINDOW
    
    Note on the "NORMAL MESSAGE PURGE WINDOW"
    -----------------------------------------
    Normal Message Threshold Time <=> after this will have successes
    and errors and others in REPRESENTATIVE PROPORTIONS. It is the time of the 
    oldest transaction with fast_purge_dt_tm set. Use the status update date time as 
    opposed to date time entered as purge uses status update time.
    
    Would expect 779.1 to always set this window (ie/ normal msg retention days) but it
    doesn't. Two examples:
    - 757 and 692 have 7 day period which means [1] HLO bad message is applied to good
    messages too and there is no error/other lingering beyond the success persistence 
    - 687 is 3 which means [1] it follows HLO normal and [2] it will have errors'n'others
    around for 4 days longer than successes. As these will scew the success-error 
    proportions, we will suppress these transactions too 
    
    dont_purge vs fast_purge:
    -------------------------
      * never together
      * if transaction in window and SUCCESS and not fast_purge => dont_purge == 0
      * may be set to 1 if before window ie/ reason for NON ERRORs to linger
    ... don't just key off "must have fast_purge" as still want in-window dont_purge
    as some protocols/packages may be using that.
    """
    # Doing after as because of edits, order of trans may not reflect threshold time
    firstTTime = sorted(list(set((transactions[tid][0]["status_update_date_time"]["value"] if "status_update_date_time" in transactions[tid][0] else transactions[tid][0]["date_time_entered"]["label"]) for tid in transactions if "fast_purge_dt_tm" in transactions[tid][0] and transactions[tid][0]["status"]["label"] == "SUCCESSFULLY COMPLETED")))[0]
    startTimePass2 = datetime.now()
    print(f"Pass 2 Setup - First Threshold Time: {firstTTime}")
    ttimesInT = set()
    purgeTimeGaps = set()
    for tid in transactions.keys(): 
                            
        # First time of transaction window is first status|entry time where purge set
        ttime = transactions[tid][0]["status_update_date_time"]["value"] if "status_update_date_time" in  transactions[tid][0] else transactions[tid][0]["date_time_entered"]["label"]
                        
        if ttime < firstTTime:
            if "fast_purge_dt_tm" in transactions[tid][0]:
                print(json.dumps(transactions[tid], indent=4))
                raise Exception("Kept transactions shouldn't have fast purge set")
            if "dont_purge" in transactions[tid][0]:
                reason = f'TOO_EARLY_DONT_PURGE_{transactions[tid][0]["dont_purge"].split(":")[0]}'
            else: # Mainly ERROR
                if re.match(r'SUCCESS', transactions[tid][0]["status"]["label"]):
                    raise Exception("Kept transactions shouldn't be status SUCCESS unless dont_purge set (either 0 or 1)")
                reason = f'TOO_EARLY_{re.sub(r" ", "_", transactions[tid][0]["status"]["label"])}'
            for resource in transactions[tid]:
                suppressResource("2", resource, reason)
            sp = transactions[tid][0]["subscriber_protocol"]["label"]
            del transactions[tid]
            continue
            
        # A/C for lack of fast_purge in in-window transactions - SUCCESS uses dont_purge
        # in a few cases. And then some other status' may have neither
        if "fast_purge_dt_tm" not in transactions[tid][0]:
            if re.match(r'SUCCESS', transactions[tid][0]["status"]["label"]) and "dont_purge" not in transactions[tid][0]:
                raise Exception("Expect dont_purge (set to 0) for successful in-window transactions w/o fast_purge set ie/ alt use by package")
        else:
            purgeTimeGaps.add(
                datetime.strptime(transactions[tid][0]["fast_purge_dt_tm"]["value"], "%Y-%m-%dT%H:%M:%S").date() - datetime.strptime(ttime, "%Y-%m-%dT%H:%M:%S").date()
            )
    
        ttimesInT.add(ttime)
              
        """
        # Final Transactions accepted must follow rules ...  
        if (transactions[tid][0]["transmission_type"] == "I:INCOMING" and transactions[tid][0]["logical_link"]["label"] in linkLabelsByServiceType["C:CLIENT (SENDER)"]) or (transactions[tid][0]["transmission_type"] != "O:OUTGOING" and transactions[tid][0]["logical_link"]["label"] not in linkLabelsByServiceType["C:CLIENT (SENDER)"]):
            print(json.dumps(transactions[tid], indent=4))
            raise Exception("Transaction out on LISTENER or in on CLIENT")
        """
        
    lastTTime = sorted(list(ttimesInT))[-1]
    purgeTimeGap = sorted(list(purgeTimeGaps), reverse=True)[0].days
        
    print(f"... PASS 2 COMPLETE (took {datetime.now() - startTimePass2}) - Nixed [1] dont_purge sets [2] One-off Onlies, [3] Before Threshold Start for Purge Time - {firstTTime}/{purgeTimeGap} - transactions: suppressed {sum(suppressedWhy[sw] for sw in suppressedWhy if re.match('2', sw))} more resources, leaving  {len(transactions)} transactions")
    spsOfTrans = set(transactions[tid][0]["subscriber_protocol"]["label"] for tid in transactions)
    if len(set(allSPsSeen) - spsOfTrans):
        print(f"\t** Warning post PASS 2: protocols {dict((sp, allSPsSeen[sp]) for sp in (set(allSPsSeen) - spsOfTrans))} have been completely suppressed")
    
    # Catch bugs
    totalMsgs = sum(suppressedWhy[w] for w in suppressedWhy)
    totalMsgs += sum(len(transactions[tid]) for tid in transactions)
    if totalMsgs != _773Total:
        raise Exception(f"** Not accounting for all in suppress # and transaction resources: {totalMsgs} vs {_773Total}")
        
    # ############################ Pass Three Transactions Clean up ##################

    # Serialize finally to cut size down. (25->15G for 663)
    print("Pass Three - final small as possible reserialization of Transactions and cleanup IPT (in process tmp) shelve")
    
    # linkLabelsByServiceType = transactionInfo["linkLabelsByServiceType"]
    
    startTimeReserialization = datetime.now()
    transactionsFinal = shelve.open(sredFile)
    timeFor50Start = startTimeReserialization
    totalTransactions = 0
    totalTransactionsIncoming = 0
    totalTransactionsOutgoing = 0
    for i, tid in enumerate(transactions.keys(), 1):
        totalTransactions += 1
        if i % 50000 == 0:
            after50Time = datetime.now() # want to see if slows
            print(f"\tTraversed 50K more transactions to {i} in {after50Time - timeFor50Start}")
            timeFor50Start = after50Time
        transactionsFinal[tid] = transactions[tid]   
        if transactions[tid][0]["logical_link"]["label"] not in linkLabelsByServiceType["C:CLIENT (SENDER)"]:
            totalTransactionsIncoming += 1
            continue
        totalTransactionsOutgoing += 1 
    transactions.close()

    print(f"... Pass Three Complete: reserialization and deletion completed in {datetime.now() - startTimeReserialization}")
    
    # ######################### Final Flush ########################
    
    llInfoById = dict((llInfoByIEN[ien]["label"], llInfoByIEN[ien]) for ien in llInfoByIEN)
    
    meta = {
    
        "stationNo": stationNo,
        "standardListener": HLOSTANDARDLISTENER,
        
        "totalMsgs": totalMsgs,
        "totalTransactions": totalTransactions,
        "totalTransactionsIncoming": totalTransactionsIncoming,
        "totalTransactionsOutgoing": totalTransactionsOutgoing,
        "suppressedWhy": suppressedWhy, # the other set, count for why suppressed

        "firstTTime": firstTTime,   
        "lastTTime": lastTTime, # note literally may be > purgeTimeGap days ie/ part of day
        "purgeTimeGap": purgeTimeGap,

        "orphan772Count": len(_772IENs - _772IENW773),
        "_779_1": _779_1,

        "llInfoById": llInfoById,
        "linkLabelsByServiceType": linkLabelsByServiceType # may change to just calc
    }
    json.dump(meta, open(metaFile, "w"), indent=4)

    print(f"Final Flushing {meta['totalTransactions']} 773 Transactions with {meta['totalMsgs']} messages")
    transactionsFinal.close()
    print("... flushed")
    
    print("Final step - delete two IPT shelves")
    os.remove(sredFileIPT)
    print(f'\tRemoved {sredFileIPT}')
    os.remove(ipt772TextRedFile)
    print(f'\tRemoved {ipt772TextRedFile}')
    
    print(f"Total Build and Flush in {datetime.now() - startTime}")
        
    return shelve.open(sredFile, flag='r'), meta
    
"""
Along with Reduction, interpret 101 and interplay with 773:
- LL may not be in Protocol as can use protocol (ex/ XWB...) with many?
- From Quote, the simple ACK is taken care of in the underlying comms
    > The HL7 package generates and processes Enhanced mode Commit Accepts internally.
- Subscriber Protocol for incoming is looked up with a cross reference embedded in 101. These references allow one or more of application or message type or event type to be missing (presuming moves from strictest to less strict).
  > ^DD(101,770.1,1,1,"%D",1,0)="This cross reference is used to look up the protocol related to an incoming "
    ^DD(101,770.1,1,1,"%D",2,0)="message at the time the incoming message is received.      This cross reference"
    ^DD(101,770.1,1,1,"%D",3,0)="is composed of values from the Server Application, Message Type, Event"
    ^DD(101,770.1,1,1,"%D",4,0)="Type and Version ID fields. This cross reference works in conjunction with"
    ^DD(101,770.1,1,1,"%D",5,0)="the AHL1A, AHL1B and AHL1C cross references."
- Note that from GMRC EX (GMRC IFC SUBSC), see it has ORR 002 set for it but Event Driver would also be setup by this cross ref ie/ Lookup for both SENDING and RECEIVING?
- The App Ack is processed by the 'processing_routine' in the subscriber protocol picked ...
    > executed on the receiving system. It defines the routine used to process the original inbound message in a transaction and to GENERATE and APPLICATION response/ACK back to the sending system using the entry point, GENACK^HLMA1.
  Note that the Subscriber Protocol's processing routine (eventually) may send back an
  App Ack! Ex for GMRC ...
    > D APPACK^GMRCIAC2(GMRCDA,"AA") ;send app. ACK and unlock record
ie/ 773 doesn't route. The 773 just records what subscriber gets the message.
- For Event Driver, a Driver's 'response_processing_routine' ...
    > executed on the sending system when an Acknowledgement or Query response is received. The message ID of the original message is always contained within the response. This is used to identify the location of the original message and the corresponding event point protocol.
    
Here's my problem: 
- can't find line up from Subscriber to Event Driver
- ie/ event driver processing is for the APP ACK on the Sending System (ORRIN!)
- subscriber processing is in Receiving system for taking in first message
<------ why link ED (SEND SYS?) and SUB (RECEIVE SYS) unless some way subs (intended for Receiver independently) become linked designationors in Sender for the ED ie/ the Message Type etc in the Subscriber(s) of an ED must be 
(no .11 new Crosses in it for 101)

"""

def reduce101SE(stationNo):
    
    tmpLocn = f'{VISTA_DATA_BASE_DIR}{stationNo}/TmpWorking/'
    _101RedFile = f'{tmpLocn}_101SERed.json'
    try:
        _101Red = json.load(open(_101RedFile))
    except:
        pass
    else:
        return _101Red

    dataLocn = f'{VISTA_DATA_BASE_DIR}{stationNo}/Data/'
    _101ByLabel = {} # doing label as BuildDirectory keeps labels
    _101EDsByLL = defaultdict(list) # > 1 possible. As sending.
    _101SsByLL = defaultdict(list) # Many possible, even per ED.
    _101sWithDescriptions = set()
    _101sWithPackages = set()
    allSubscribers = set()
    allEventDrivers = set()
    eventDriversDisabled = set()
    eventDriversThatLackSendingApplication = set()
    eventDriversThatSend = set()
    eventDriversThatSendAck = set()
    eventDriversWithNoLL = set()
    eventDriversWRespMTNNoTransM = set()
    allSubscribers = set()
    subscribersDisabled = set()
    subscribersThatResp = set()
    subscribersThatRespAck = set()
    subscribersWTransMNNoRespMT = set() # corrupt
    subscribersThatLackReceivingApplication = set()
    subscribersWithTransactionMessageType = set()
    subscribersWithNoLL = set()
    _101EDsBySs = defaultdict(set) # Label to Label - expect more Subs than EDs
    resourceIter = FilteredResultIterator(dataLocn, "101")
    for i, resource in enumerate(resourceIter, 1):
        # ien = resource["_id"].split("-")[1]
        if not ("type_4" in resource and resource["type_4"] in ["S:subscriber", "E:event driver"]):
            continue
        _101ByLabel[resource["label"]] = resource
        if "description" in resource:
            _101sWithDescriptions.add(resource["label"])
        if "package" in resource:
            _101sWithPackages.add(resource["label"])
        """
        TODO: 
        1. DONE get the Philips 101's
        a. RA MTX ORM or ORU
           > ORM Protocol for MTX - Primordial
           ...
           > ORU Protocol for MTX - Primordial
           with a creator BAXTER,CHRIS T
           Subscriber, ACK and Q for processing
        2. walk subscribers of ED and index subs by ED ... ensure
        once ED per sub and ...
           ... get any Event Driver for RA MTX ORM, RA MTX ORU
        3. ------> see if no build => creator! ie/ move above
        
        ... still unsure of the LL to Subscriber, ED though maybe if
        App Ack => LL and IN QUEUE differ?
        """
        if resource["type_4"] == "E:event driver":
            allEventDrivers.add(resource["label"])
            if "disable" in resource:
                eventDriversDisabled.add(resource["label"])
            if "subscribers" in resource:
                for subInfo in resource["subscribers"]:
                    subLabel = subInfo["subscribers"]["label"]
                    _101EDsBySs[subLabel].add(resource["label"])
            # leaving receiving_application optional
            if "sending_application" not in resource:
                eventDriversThatLackSendingApplication.add(resource["label"])
            # Where to dispatch to (unless local?)
            if "logical_link" not in resource:
                eventDriversWithNoLL.add(resource["label"])
            if "transaction_message_type" in resource:
                eventDriversThatSend.add(resource["label"])
                if resource["transaction_message_type"]["label"] == "ACK":
                    eventDriversThatSendAck.add(resource["label"])
            # May have redundant response_message_type but corrupt if only one there!
            # ... not in 757 but 1 equivalent corruption for subscriber in 757           
            if "response_message_type" in resource and "transaction_message_type" not in resource:
                eventDriversWRespMTNNoTransM.add(resource["label"])
            # TODO: w/ accept_ack_code, application_ack_type ... may enforce for 
            # subscriber ie/ not ACK if application_ack_type? or if both NE, why 
            # subscriber?
        else:
            allSubscribers.add(resource["label"])
            if "disable" in resource:
                subscribersDisabled.add(resource["label"])
            if "transaction_message_type" in resource:
                subscribersWithTransactionMessageType.add(resource["label"])
            # corruption - invalid          
            if "transaction_message_type" in resource and "response_message_type" not in resource:
                subscribersWTransMNNoRespMT.add(resource["label"])
            if "response_message_type" in resource:
                subscribersThatResp.add(resource["label"])                 
                if resource["response_message_type"]["label"] == "ACK":
                    subscribersThatRespAck.add(resource["label"]) 
            # leaving sending_application optional
            if "receiving_application" not in resource:
                subscribersThatLackReceivingApplication.add(resource["label"])
            # ?: to what end?
            if "logical_link" not in resource:
                subscribersWithNoLL.add(resource["label"])      
        
    """
    Note that LL isn't mandatory in 101's as perhaps reused across many LLs?
    """
    print()                  
    print("101 for Event Driver and Subscriber")
    print(f"\t{len(_101ByLabel)} 101s - (2/3) w/descriptions {len(_101sWithDescriptions)} - w/packages {len(_101sWithPackages)}")
    # Few (3 in 757) EDs have ACK as the transaction_message_type
    print(f"\t{len(allEventDrivers)} Event Drivers - disabled {len(eventDriversDisabled)} - (most have) with subscriber(s) {len(set(e for s in _101EDsBySs for e in _101EDsBySs[s]))} - (nearly all) have transaction message {len(eventDriversThatSend)} - (few) with transaction message ACK {len(eventDriversThatSendAck)} - (corrupt) w/o transaction message but with response message *{len(eventDriversWRespMTNNoTransM)}* - (most have) lack Sending Application {len(eventDriversThatLackSendingApplication)} - (most have) lack LL {len(eventDriversWithNoLL)}")
    # Half or so of the Subscribers have ACK as their response message
    print(f"\t{len(allSubscribers)} Subscribers - disabled {len(subscribersDisabled)} -  (most have) known Event Driver(s) {len(_101EDsBySs)} - (few) w > 1 driver {sum(1 for s in _101EDsBySs if len(_101EDsBySs[s]) > 1)} - (nearly all) with response message {len(subscribersThatResp)} - (half) with response message ACK {len(subscribersThatRespAck)} - (corrupt) w/o response message but w transaction_message_type *{len(subscribersWTransMNNoRespMT)}* - with transaction_message_type {len(subscribersWithTransactionMessageType)} - (few) lack Receiving Application {len(subscribersThatLackReceivingApplication)} - (half) lack LL {len(subscribersWithNoLL)}")
    print()
    
    """
    QA ACKs:
    - if "accept_ack_code" set in ED of an ACKing Subscriber then expect value to be AL
    ... not forcing it to be set as see some where not and so presuming taken to mean
    could be AL.
    
    Tried to enforce if ACK in subscriber => must have AL if accept_ack_code set in 
    Event Driver but that doesn't hold. 

    for subrLabel in subscribersThatRespAck:
        if subrLabel not in _101EDsBySs: # No ED so skip
            continue
        edLabel = list(_101EDsBySs[subrLabel])[0]
        ed = _101ByLabel[edLabel]
        if "accept_ack_code" in ed and ed["accept_ack_code"]["label"] != "AL":
            print(json.dumps(ed, indent=4))
            raise Exception(f"For Subscriber with ACK {subrLabel} - expected its Event Driver to have value AL for accept_ack_code if set")
    """
        
    json.dump(_101ByLabel, open(_101RedFile, "w"), indent=4)
    return _101ByLabel
    
"""
- tcp_ip_service_type (Client => out; other two are listeners)
- description (most don't have but may be interesting)
- mailman_domain
- dns_domain
- institution (not all links) and only one per instit! ex/ VAPUG etc
- tcp/ip service type
- tcp_ip_address (what is not client?)

NEW: are all LL's of tcp_ip_service_type CLIENT (SENDER) if that is set?

TODO: more on in_queue and 870
"""
def reduce870(stationNo):

    tmpLocn = f'{VISTA_DATA_BASE_DIR}{stationNo}/TmpWorking/'
    _870RedFile = f'{tmpLocn}_870Red.json'
    try:
        _870Red = json.load(open(_870RedFile))
    except:
        pass
    else:
        return _870Red

    dataLocn = f'{VISTA_DATA_BASE_DIR}{stationNo}/Data/'
    _870ById = {}
    resourceIter = FilteredResultIterator(dataLocn, "870")
    for i, resource in enumerate(resourceIter, 1):
        entry = {"ien": resource["_id"].split("-")[1], "label": resource["label"]}
        # tcp_ip_service_type is key differentiator
        # ... want llp_type == "TCP"
        # ... persistent absent or False
        for prop in ["description", "mailman_domain", "dns_domain", "institution", "tcp_ip_service_type", "tcp_ip_address", "llp_type", "persistent"]:
            if prop not in resource:
                continue
            entry[prop] = resource[prop]
        _870ById[entry["ien"]] = entry
    json.dump(_870ById, open(_870RedFile, "w"), indent=4)
    return _870ById
    
def reduce8994(stationNo):

    tmpLocn = f'{VISTA_DATA_BASE_DIR}{stationNo}/TmpWorking/'
    _8994RedFile = f'{tmpLocn}_8994Red.json'
    try:
        _8994Red = json.load(open(_8994RedFile))
    except:
        pass
    else:
        return _8994Red

    dataLocn = f'{VISTA_DATA_BASE_DIR}{stationNo}/Data/'
    _8994ByName = {}
    resourceIter = FilteredResultIterator(dataLocn, "8994")
    for i, resource in enumerate(resourceIter, 1):
        _8994ByName[resource["label"]] = resource
    json.dump(_8994ByName, open(_8994RedFile, "w"), indent=4)
    return _8994ByName
    
def reduce779_1(stationNo):

    dataLocn = "{}{}/{}".format(VISTA_DATA_BASE_DIR, stationNo, "Data") 
    fmqlReplyStore = FMQLReplyStore(dataLocn)
    hloSystemParametersReply = fmqlReplyStore.lastReplyOfType("779_1")
    if not hloSystemParametersReply:
        raise Exception("Expected HLO System Parameters 779_1 to have been cached but missing")
    if len(hloSystemParametersReply["results"]) != 1:
        raise Exception("Expected one and only one result in 779_1")
    hloSystemParameters = hloSystemParametersReply["results"][0]
    return hloSystemParameters
    
# ############################# QA / Examine #################

"""
Expect to see receivingFacility to hold receiving instrument (Pentax, Xcelera) and to have distinct links for each
"""
def lookinsideMCAR_ORM_CLIENT(transactions):
    SP = "MCAR ORM CLIENT"
    hl7TemplateMaker = HL7TemplateMaker(False)
    cnt = Counter()
    for tid in transactions:
        ts = transactions[tid]
        fresource = ts[0]
        if fresource["subscriber_protocol"]["label"] != SP:
            continue
        if fresource["transmission_type"] != "O:OUTGOING":
            raise Exception("Only expect MCAR ORM CLIENT to be OUTGOING")
        ll = fresource["logical_link"]["label"]
        mshInfo = hl7TemplateMaker.parseMSH(fresource["msh"])
        rf = mshInfo["receivingFacility"] if "receivingFacility" in mshInfo else "NOT_SPEC"
        cnt[f'{ll}/{rf}'] += 1
    print(cnt)     

"""
Example individual transactions (as QA Happens)
"""
def examineTransactions(transactions, protocolLabels): 

    """
    For examination to improve reporting
    
    > examineTransactions({SNO}, {LINKLABEL})
    """
    receivingFacilityCount = Counter()
    for tid in transactions:
        ts = transactions[tid]
        fresource = ts[0]
        if fresource["subscriber_protocol"]["label"] in protocolLabels:
            if "msh" in fresource:
                hl7TemplateMaker = HL7TemplateMaker(False)
                mshInfo = hl7TemplateMaker.parseMSH(fresource["msh"])
                for field in ["sendingApplication", "sendingFacility", "receivingApplication", "receivingFacility"]:
                    if field in mshInfo:
                        print(f"\t{field}: {mshInfo[field]}")
                        if field == "receivingFacility":
                            receivingFacilityCount[mshInfo[field]] += 1
                print()
            print(json.dumps(ts[0], indent=4))
            print()
    print(receivingFacilityCount)
    # MCAR PENT as link => receiving facility goes there.
    
def examineSome101s(stationNo):

    """
    See subscribers for events ... Eight event driver protocols (RA REG, RA REG 2.3, RA     
    EXAMINED, RA EXAMINED 2.3, RA
    CANCEL, RA CANCEL 2.3, RA RPT and RA RPT 2.3) were exported with VistA Rad/Nuc Med and
    subsequent patches ... six example subscribers (SEE 101 setup in VISTA .... TODO) ie/     
    subscribers are VistA specific

    Two protocols will be required for Radiology to receive reports from a COTS product.     
    An ORU message type subscriber protocol, and an event-driver. Three event driver 
    protocols (RA VOICE TCP SERVER RPT, RA TALKLINK TCP SERVER RPT and
    RA PSCRIBE TCP SERVER RPT) were exported with VistA Rad/Nuc Med and subsequent patches
    """
    _101ByLabel = reduce101SE(stationNo)
    for lbl in _101ByLabel:
        if re.match(r'RA', lbl) or re.search(r' LCA$', lbl):
            print(lbl, json.dumps(_101ByLabel[lbl], indent=4))
            print()
            
"""
Issue: older db's didn't have these totals - must fill in if missing

if "totalTransactionsIncoming" not in transactionInfo:
    tmpEnsureTransactionInfoComplete(stationNo, transactions, transactionInfo)
    
TODO: move protocol counts in here to avoid redoing that again and again too.
"""
def tmpEnsureTransactionInfoComplete(stationNo, transactions, transactionInfo):
    
    linkLabelsByServiceType = transactionInfo["linkLabelsByServiceType"]
    totalTransactions = 0
    totalTransactionsIncoming = 0
    totalTransactionsOutgoing = 0
    print("Missing Meta Info - must total incoming and outgoing ...")
    startTimeTotalling = datetime.now()
    for i, t in enumerate(transactions, 1):
        totalTransactions += 1
        if i % 50000 == 0:
            print(f'Another 50K to {i}')
        if transactions[t][0]["logical_link"]["label"] not in linkLabelsByServiceType["C:CLIENT (SENDER)"]:
            totalTransactionsIncoming += 1
            continue
        totalTransactionsOutgoing += 1
    print(f"... done totaling in {datetime.now() - startTimeTotalling}")
    transactionInfo["totalTransactionsIncoming"] = totalTransactionsIncoming
    transactionInfo["totalTransactionsOutgoing"] = totalTransactionsOutgoing
    print("Reserializing meta for the next time ...")
    tmpLocn = f'{VISTA_DATA_BASE_DIR}{stationNo}/TmpWorking/'
    metaFile = f'{tmpLocn}_773RedMeta.json'
    json.dump(transactionInfo, open(metaFile, "w"), indent=4)
    print(f'Totals: {transactionInfo["totalTransactions"]}/{transactionInfo["totalTransactionsIncoming"]} I/{transactionInfo["totalTransactionsOutgoing"]} O')
    
# ################################# DRIVER #######################
               
def main():
    
    assert sys.version_info >= (3, 6)

    try:
        stationNo = sys.argv[1]
    except IndexError:
        raise SystemExit("Usage _EXE_ STATIONNO [PLOT]")
                
    # ... TIUHL7 ROCHE MDM SUBSCRIBER
    # dumpRawBuild9_6s(stationNo, ["SD*5.3*704", "SD*5.3*650", "OR*3.0*496"], ["databridge", "medtronic", "roche"])
    # return

    transactions, transactionInfo = reduce773Transactions(stationNo)
        
    # GE-Muse-ADT-A08-Client
    # examineTransactions(transactions, ["R1NUASTAFF PROTOCOL"]) # "GMRCCCRA" ... "PSO DISP"
    # lookinsideMCAR_ORM_CLIENT(transactions)
    # examineSome101s(stationNo)
    # return
        
    # Version for Report and then all the gory details/debug meta to leverage
    webReportHL7(stationNo, transactions, transactionInfo)
    webReportHL7Debug(stationNo, transactions, transactionInfo)
                        
if __name__ == "__main__":
    main()
    