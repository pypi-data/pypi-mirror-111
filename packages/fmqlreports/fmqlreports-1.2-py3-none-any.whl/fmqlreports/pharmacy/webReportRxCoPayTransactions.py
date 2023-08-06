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
from fmqlutils.typer.reduceTypeUtils import splitTypeDatas, checkDataPresent, singleValue, combineSubTypes, muBVCOfSTProp, makeTypeTSCSVByDay

from fmqlreports.webReportUtils import muPlotRef, makePlots 
from fmqlreports.webReportUtils import TOP_MD_TEMPL, SITE_DIR_TEMPL, ensureWebReportLocations, keyStats, flattenFrequencyDistribution, roundFloat, reduce200, reduce4, flattenPropValues, vistasOfVISNByOne

"""
NEXT TODO OBS:
- ? ST. LOUIS MO VAMC-JC DIVISION [657] + 
- Boise and its leaps in July remotes and before that locals (ie/ more patients?) ... Patient Dir
  - Same leap seen in ROS, WCO too at that time ... WHY? Patient DIR tells?
  - SPO is like ROS in its earliest ones 
  ... see far more children for the later ones ... a big uptick in children?
      [or what I count as children? ... needs work]
- PUG (and lessor POR) shows more remotes than local => bigger system receives more as its patients are spread outside vs small site with patients of others which sends things out to others.

NEXT TODO:
(... plus neaten/remove need for makeTypeTSCSV ...)
- in ... do Instits (ie/ Sankey prep)
- POSTMASTER as user for remote and NEVER for local
- brief_description ---- parse out DRUG -- ex/ 599...A-ASPIRIN 8-3 ... do only some go to St L?
- patients: out | in | both (with #'s)
- refine to ONLY do Completes => put into csv take too (ie/ put in TS filter too)
--------- Examine + YR1[E] stuff
- QA # right for out (analysis)
CHANGE: #transmission_record => can then see if patients elsewhere
ST Red Changes suggested:
- #action_type for child
- #transmission_record => can then isolate patients that are local only
- [YRE] formally check child (ie parent_transaction not self)
"""

"""
> individual transactions for outpatient medication copayments
...
> transactions in this file will be used to store detailed information about a patient's rx copayments, including amounts billed and not billed (hence: 
...
> should be transactions stored in this file for both this facility and other treating facilities through out the VA system

Four Status' with a flow to transmit and then completed
- P:PENDING TRANSMISSION
- C:COMPLETE
    or
- Y:CANCELLED PENDING TRANSMISSION
- X:CANCELLED COMPLETE

=> distinguish local (sent out, only) and remote
=> give #'s for pending, cancelled ... but stick to completes

Related: 350 with many of the same fields and it refers to 354_71 with ib_copay_transaction_number. It (350) is referenced from 354_71 with ib_action_pointer and shows 350's .01 is {SNO}IEN ie/ no gaps of SNO and the IEN.
"""
def webReportRxCoPayTransactions(stationNo, imageDir="Images"):

    homeVisnVistAs = vistasOfVISNByOne(stationNo)

    allThere, details = checkDataPresent(stationNo, [

        {"fileType": "354_71", "check": "YR1"}
        
    ])
    if not allThere:
        raise Exception("Some required data is missing - {}".format(details))
        
    meta = metaOfVistA(stationNo)
    vistaName = meta["name"]
    cutDay = meta["cutDate"]

    plotData = {}

    mu = TOP_MD_TEMPL.format("{} Copay Transactions".format(stationNo))
    mu += f"""# Copay Transactions 
    
The following reports on the most recent year of copay transactions (file _354.71_) from a clone of VistA {vistaName} [{stationNo}] cut on {cutDay}.
    
"""

    type354_71YR1, sts354_71YR1 = splitTypeDatas(stationNo, "354_71", reductionLabel="YR1", expectSubTypeProperties=["status", "institution"])
    inSTsByInstit = defaultdict(list)
    localSTs = []
    institIENOfHome = f'{stationNo}' if "isSNODefaultInstitutionIEN" in meta else meta["defaultInstitutionIEN"]
    for st in sts354_71YR1:
        try:
            instit = singleValue(st, "institution")
        except:
            print(f'No ST - just dropping these {st["_total"]}')
            continue
        if instit.split("4-")[1][:-1] == institIENOfHome:
            homeInstit = instit
            localSTs.append(st)
            continue
        inSTsByInstit[instit].append(st)
            
    """
    TODO: 
    - Do split of Outgoing/Local (sent out/ stays local) and Incoming
    - Consider relative Patient #'s [we could categorize the site on prop patients?]
    """
    totalLocal = sum(st["_total"] for st in localSTs)
    totalIn = sum(st["_total"] for instit in inSTsByInstit for st in inSTsByInstit[instit])
    total = totalLocal + totalIn
    
    plotData["transactionTypes"] = {
        "title": "Transaction Types",
        "plotName": "rxCoPayTransactionTypes",
        "plotMethod": "plotCategoryBH",
        "rows": [
            "types"
        ],
        "columns": [
            "local",
            "remote"
        ],
        "data": [
            [
                totalLocal,
                totalIn
            ]
        ]
    }
    blurb = "Of <span class='yellowIt'>{:,}</span> transactions, <span class='yellowIt'>{}</span> were created locally (\"Local Transactions\") while <span class='yellowIt'>{}</span> were received from <span class='yellowIt'>{:,}</span> other sites (\"Remote Transactions\").\n\n".format(
        total,
        reportAbsAndPercent(totalLocal, total),
        reportAbsAndPercent(totalIn, total),
        len(inSTsByInstit)
    )
    mu += "{}\n\n{}\n\n".format(
        blurb,
        muPlotRef(plotData["transactionTypes"], imageDir)
    )
    
    # TODO PATIENTs: from remote, local only, local sent out but not remote, remote/local
    # ... for COMPLETED
    
    # ############################### Locals ##############################
    
    sortedLocalSTs = sorted(localSTs, key=lambda x: x["_total"], reverse=True)
    blurb = """Over this period, Local Transactions were made for <span class='yellowIt'>{:,}</span> patients by <span class='yellowIt'>{:,}</span> users. The <span class='yellowIt'>{:,}</span> status' of these transactions in the system are {}.
    
""".format(        
        len(set(patientId for st in sortedLocalSTs for patientId in st["patient"]["byValueCount"])),
        len(set(userRef for st in sortedLocalSTs for userRef in st["user_adding_entry"]["byValueCount"])),
        
        len(localSTs),
        ", ".join(
            [f'{singleValue(st, "status").split(":")[1]} [<span class="yellowIt">{reportPercent(st["_total"], totalLocal)}</span>]' for st in sortedLocalSTs]
        )
    )
    # Could add later: 
    # - action_type == PSO RX etc <---- if not present => child
    # - co payment tier == 1/2/3
    # - ib action pointer (all but POR => account exists if billed amount > 0
    localSTComplete = sortedLocalSTs[0]   
    plotData["percsLocalCompleted"] = {
        "title": "{:,} Completed Local Transactions".format(localSTComplete["_total"]),
        "plotName": "rxCoPayLocalCompletedAttributes", 
        "plotMethod": "plotIsHasBH",
        "specs": {
            "__entityName": "Completed Local Transactions",
            "__total": localSTComplete["_total"],
            "Sent to other sites": localSTComplete["transmission_record"]["count"],
            # means ST forced to keep billed_amount. Only got bigger for 663 
            "No Bill": localSTComplete["billed_amount"]["byValueCount"]["0"],
            # higher for June on and increase in #'s ... some change?
            "Child Transactions": localSTComplete["_total"] - localSTComplete["action_type"]["count"]
        }
    }
    mu += "{}\n\n{}\n\n".format(
        blurb,
        muPlotRef(plotData["percsLocalCompleted"], imageDir)
    )    
    
    transmissionBVC = localSTComplete["transmission_record"]["reduction"]["transmission_facility"]["byValueCount"]
    transmissionBVCSNO = dict((instit.split("4-")[1][:-1], transmissionBVC[instit]) for instit in transmissionBVC)
    institBySNO = dict((instit.split("4-")[1][:-1], instit.split(" [")[0]) for instit in transmissionBVC)
    mu += f'''Complete Local transactions are sent to <span class='yellowIt'>{len(institBySNO):,}</span> other sites including {sum(1 for sno in institBySNO if sno in homeVisnVistAs):,} VISN 20 sites. The top ten sites receiving transaction data are (VISN 20 sites are in bold) ...
    
'''
    receivingSitesSorted = sorted(transmissionBVCSNO, key=lambda x: transmissionBVCSNO[x], reverse=True)
    tbl = MarkdownTable([":Remote Site", "Completed Transactions Sent (1 Year)"])
    for i, rinstitSNO in enumerate(receivingSitesSorted, 1):
        if i > 10:
            break
        institMU = "{} [{}]".format(institBySNO[rinstitSNO], rinstitSNO)
        tbl.addRow([
            "__{}__".format(institMU) if rinstitSNO in homeVisnVistAs else institMU,
            reportAbsAndPercent(transmissionBVCSNO[rinstitSNO], localSTComplete["_total"])
        ]) 
    mu += tbl.md() + "\n\n"
        
    # ####################### DETAILS FROM REMOTE ########################
    
    # TODO - do the institutions and % VISN 20
    
    # ####################### Time Series ################## (merge)
    
    # REM: want more on medians + max + min per weekday
    tsPlotData, tsmu = muTimeSeries(stationNo, cutDay)
    mu += tsmu
    plotData.update(tsPlotData)
    
    # ####################### Serialize ####################

    plotDir = f'{VISTA_DATA_BASE_DIR}{stationNo}/TmpWorking/'
    print(f'Serializing vizData to {plotDir}')
    json.dump(plotData, open(f'{plotDir}plotDataRxCoPay.json', "w"), indent=4)
    
    userSiteDir = SITE_DIR_TEMPL.format(stationNo)
    print("Serializing Rx CoPay Report to {}".format(userSiteDir))
    open(userSiteDir + "rxCoPayTransactions.md", "w").write(mu)
    
def muTimeSeries(stationNo, cutDay, imageDir="Images"):

    PLOT_PREFIX = f'rxCoPay'
    plotData = {}
        
    cutDayDT = datetime.strptime(cutDay, "%Y-%m-%d")
    
    mu = ""
    
    print(f'Making CSV dates for TS with 18 months back from cut day, {cutDay}')
    class Splitter:
        def __init__(self, stationNo):
            self.__stationNo = stationNo
        def split(self, resource):
            if "institution" not in resource:
                print(f'** Warning: missing "institution" from resource {resource["_id"]} - skipping')
                return "" # suppress
            institSNO = resource["institution"]["id"].split("-")[1]
            colId = "Local" if institSNO == self.__stationNo else "Remote"
            return colId
    createdByDayCSV = makeTypeTSCSVByDay(stationNo, "354_71", "date_entry_added", upToDay=cutDay, timeBack={"months": 18}, splitter=Splitter(stationNo))
    colNameById = dict((colId, colId) for colId in createdByDayCSV[0].split(",")[1:])
    
    # Three months back
    cutDayBefore = createdByDayCSV[-1].split(",")[0] # last full day
    threeMonthsBackDayDT = cutDayDT - relativedelta(months=3)
    threeMonthsBackDay = datetime.strftime(threeMonthsBackDayDT, "%Y-%m-%d")
    plotData["tsDailies"] = {
        "title": "Transactions",
        "plotName": f'{PLOT_PREFIX}',
        "plotMethod": "plotDailies",
        "dfcsv": createdByDayCSV,
        "kargs": {
            "colNameById": colNameById,
            "start": threeMonthsBackDay,
            "end": cutDayBefore 
        }
    }
    blurb = f'Daily Addition - from {threeMonthsBackDay} to {cutDayBefore} - shows the expected regular weekday levels with dips at weekends and holidays. The legend gives the minimum, median and maximum number of transactions per day ...'
    mu += "{}\n\n{}\n\n".format(
        blurb, 
        muPlotRef(
            plotData["tsDailies"],
            imageDir
        )
    )
        
    # No ts365RollingMean unless do CSV for all years
    
    # TODO: may change to "end" and "timeBack" ala utility => easier to QA inside
    # graph and no duplication logic
    cutDayMonthBeforeDT = datetime.strptime(cutDay, "%Y-%m-%d") - relativedelta(months=1)
    cutMonthBefore = datetime.strftime(cutDayMonthBeforeDT, "%Y-%m")
    cutDay13MonthsBeforeDT = datetime.strptime(cutDay, "%Y-%m-%d") - relativedelta(months=13)
    cutMonthBeforeYearBack = datetime.strftime(cutDay13MonthsBeforeDT, "%Y-%m")
    plotData["tsMonthlyResamples"] = {
        "title": "Transactions for last year - Resampled Monthly",
        "plotName": f'{PLOT_PREFIX}',
        "plotMethod": "plotMonthlyResamples",
        "dfcsv": createdByDayCSV,
        "kargs": {
            "colNameById": colNameById,
            "start": cutMonthBeforeYearBack,
            "end": cutMonthBefore # want full months
        }
    }
    # TODO: median + weekday/ weekend on all three -- median per weekday/ max/ min?
    blurb = f'Resample by month from {cutMonthBeforeYearBack} to {cutMonthBefore} ...'
    mu += "{}\n\n{}\n\n".format(
        blurb,
        muPlotRef(
            plotData["tsMonthlyResamples"],
            imageDir
        )
    )
    
    return plotData, mu
    
# ####################### (TMP) Utility to Work out shape for YRXE reduction #############
    
"""
Manually examine a year plus 

OUTSTANDING TODO:
- must do patient is in patient dir based on IEN
- what is the transaction_number? -- can't see source
- 52 -- is it remote 52 (resulting_from) for incoming and local for outgoing
- parent transaction means? 
  - SEE where same as entry itself (ie/ always set, set to self? => must see where not equal). ... [YR1E]
  - where does this trans 687... come from?
Big Questions: from explicit?

Conclusions:

# Distinct Categories
#
# - OUTGOING (instit is home sno; account ref if billed_amount !=0; copayment_tier nearly always present for it and not outgoing)
#   no POSTMASTER
#
# - INCOMING (instit isn't home sno; no account ref; no copayment_tier ever) 
#   POSTMASTER dominates but not exclusive
#   + why child ones too? + is 52 ref to remote sys?
#
# Status range of four: COMPLETE/PENDING - CANCELLED PENDING, CANCEL COMPLETE
#

As get older, some mandatories become optional

REPORTS (SPO and PUG missing - some problem)

SPO
---
Iterating 354_71 starting with 354_71-5323322.zip - date 2019-01-01
** Warning: Expect brief description to be some ? id + short name of drug + "-cnt units" but RX COPAYMENT

Last entry date: 2020-04-20T10:51:24
** Warning: 1 are missing institution - skipped
Outgoing 264,168 - updated 3,698 - child 6,925 - account missing though bill !=0 0

Incoming 233,164 - updated 5,013 - child 7,106 - institutions 129

WCO
---
Iterating 354_71 starting with 354_71-3141840.zip - date 2019-01-01
** Warning: unexpected - POSTMASTER not enterer of incoming from WHITE CITY VA MEDICAL CENTER

Last entry date: 2020-08-01T01:42:00
Outgoing 160,096 - updated 2,018 - child 19,893 - account missing though bill !=0 0

Incoming 208,747 - updated 5,230 - child 20,241 - institutions 129

BOI
---
Iterating 354_71 starting with 354_71-5178248.zip - date 2019-01-01
** Warning: unexpected - POSTMASTER not enterer of incoming from BOISE VA MEDICAL CENTER
** Warning: Expect brief description to be some ? id + short name of drug + "-cnt units" but RX COPAYMENT
** Warning: Expect brief description to be some ? id + short name of drug + "-cnt units" but RX COPAYMENT

Last entry date: 2020-08-01T02:54:30
** Warning: 3 are missing institution - skipped
** Warning: 31 are missing patient - skipped
Outgoing 372,319 - updated 7,067 - child 27,221 - account missing though bill !=0 0

Incoming 504,483 - updated 11,175 - child 22,261 - institutions 129

POR [it has the NO BILL ISSUE and even a slightly out of order entry date!]
---
Iterating 354_71 starting with 354_71-18627474.zip - date 2019-01-01
** Warning: Billed 152, Totals 24, non billed -176, don't add up
** Warning: Billed 312, Totals 24, non billed -336, don't add up
** Warning: Expect brief description to be some ? id + short name of drug + "-cnt units" but RX COPAYMENT
** Warning: unexpected - POSTMASTER not enterer of incoming from PORTLAND VA MEDICAL CENTER
** Warning: unexpected - POSTMASTER not enterer of incoming from PORTLAND VA MEDICAL CENTER
** Warning: unexpected - POSTMASTER not enterer of incoming from PORTLAND VA MEDICAL CENTER
** Warning: Expect brief description to be some ? id + short name of drug + "-cnt units" but RX COPAYMENT
** Warning: Expect brief description to be some ? id + short name of drug + "-cnt units" but RX COPAYMENT
** Warning: Expect brief description to be some ? id + short name of drug + "-cnt units" but RX COPAYMENT
** Warning: Expect brief description to be some ? id + short name of drug + "-cnt units" but RX COPAYMENT

Last entry date: 2020-03-25T04:10:07
** Warning: 1 are missing institution - skipped
Outgoing 622,938 - updated 8,124 - child 16,400 - account missing though bill !=0 599,919

Incoming 808,965 - updated 18,122 - child 30,027 - institutions 129

WWW
---
Iterating 354_71 starting with 354_71-3135480.zip - date 2019-01-01

Last entry date: 2020-03-25T09:02:47
** Warning: 99 are missing patient - skipped
Outgoing 100,446 - updated 733 - child 1,180 - account missing though bill !=0 0

Incoming 124,327 - updated 3,431 - child 5,521 - institutions 127

ROS
---
Iterating 354_71 starting with 354_71-6099243.zip - date 2019-01-01

Last entry date: 2020-08-02T01:26:19
Outgoing 280,774 - updated 4,585 - child 27,727 - account missing though bill !=0 0

Incoming 369,904 - updated 7,881 - child 37,286 - institutions 129


"""
def examineAYearPlus(stationNo):

    dataLocn = "{}{}/Data/".format(VISTA_DATA_BASE_DIR, stationNo)   
    store = FMQLReplyStore(dataLocn)
    startAt = "2019-01-01"
    startAtReply = store.firstReplyFileOnOrAfterCreateDay("354_71", "date_entry_added", startAt)
    print(f'Iterating 354_71 starting with {startAtReply} - date {startAt}')
    resourceIter = FilteredResultIterator(dataLocn, "354_71", startAtReply=startAtReply)
        
    # INCOMING (19): 18 MAND, 1 OPT
    MAND_INCOMING_PROPS = set([
        "_id", "label", "type", 
        "transaction_number", # TODO: named for source (668-####) or always 687-####
        "patient", 
        "trans_effective_date", 
        "status", 
        "resulting_from", # is the 52 or 52 multiple in source system or copied locally?
        "units", # see tie in to brief_description
        "total_charge", # = abs(billed amount) + nonbillable_amount
        "brief_description", # \d{10+}-ALPHANUM-{#UNITs from units}? 
        "billed_amount", 
        "institution", # MARKER that != 4-{SNO}
        "user_adding_entry", # NEARLY always POSTMASTER but a few exceptions
        "date_entry_added", 
        "user_last_updating", # isUpdated count
        "date_last_updated" 
    ])
    OPT_INCOMING_PROPS = set([
        "parent_transaction_entry", # can't see pattern (ie/ not cause is not child AND not cause isUpdated etc. Just assume is not child and has no children.
        
        "nonbillable_amount" # really rare - saw in old incoming (was this a 'call back in time' as patient newly added to a VistA and no such data in old sys?
    ])
    # OUTGOING (24): 19 MAND
    MAND_OUTGOING_PROPS = set([
        "_id", "label", "type", 
        "transaction_number", 
        "trans_effective_date", 
        "status", 
        "resulting_from", # always a local 52?
        "units", # same tie in to brief_description as INCOMING
        "total_charge", # same form/enforce as INCOMING
        "brief_description", # same form/enforce as INCOMING
        "parent_transaction_entry", # always self if parent and if parent then action_type always set; never set for children (see below)
        "billed_amount", # bug where - for child so using abs (seems to not effect INCOMING)
        "institution", # always home station ie/ MARKER
        "user_adding_entry", # NEVER POST MASTER
        "date_entry_added", 
        "user_last_updating", # TODO: when != date_entry_added ie/ what updates?
        "date_last_updated" 
    ])
    OPT_OUTGOING_PROPS = set([
        "patient", # has to be BUG but happens ie/ exclude
        "ib_action_pointer", # to 350 and most have it (items that were billed) - means "billed_amount" == 0 as no 350 ie/ MARKER (# FOLLOW UP)
        "action_type", # action used to create and outgoing only and always 'PSO [N]SC RX COPAY NEW' or UPDATE - service and not service connected; never the update or cancel 350_1 options. Key is always set for top level entries; NEVER set for child entries (parent ref != self) ie/ MARKER so can drop parent if set (# FOLLOW UP)
        "transmission_record", # make sense if user only local ie/ a marker for Patient being only treated locally. Note both parents and children have it.
        "cancellation_reason", # only set if status is CANCELLED
        
        "copayment_tier", # Nearly mand for locals and not in incoming (so marker of outgoing). Not connected to 'action_type' setting. 1, 2 or 3; only not for OOOLD Portland one ie/ parent was way back -- is there some catchup if a patient suddenly goes elsewhere? 
        
        "nonbillable_amount" # saw in older in POR so not always
    ])
    
    institutionMissing = 0
    patientMissing = 0
    dateEntryAddedMissing = 0

    notProcessing = True
    lastEntryDate = ""
    
    noIncoming = 0
    noIncomingUpdated = 0
    noIncomingChild = 0
    incomingInstitutions = Counter()
    accountMissingOutgoing = 0
    noOutgoing = 0
    noOutgoingUpdated = 0
    noOutgoingChild = 0

    for i, resource in enumerate(resourceIter):
    
        if "date_entry_added" not in resource:
            dateEntryAddedMissing += 1
            continue
    
        if resource["date_entry_added"]["value"] < startAt and notProcessing:
            continue # a/c for out of order too
        notProcessing = False
        # Allowing wiggle room as POR had one  that was a minute off
        if lastEntryDate != "" and lastEntryDate.split("T")[0] > resource["date_entry_added"]["value"].split("T")[0]:    
            raise Exception(f'Entry Dates out of Order - {lastEntryDate} - {resource["date_entry_added"]["value"]}')
        lastEntryDate = resource["date_entry_added"]["value"]
    
        if "institution" not in resource:
            institutionMissing += 1
            continue # CRAP
            
        isChild = False
        if "parent_transaction_entry" in resource: # mand outgoing but not inc
            parentIEN = resource["parent_transaction_entry"]["id"].split("-")[1]
            if parentIEN != resource["_id"].split("-")[1]:
                isChild = True
            
        if "patient" not in resource:
            patientMissing += 1
            continue # CRAP - only WWW
    
        # saw in POR for old (effective date) incoming
        nonBillableAmount = 0 if "nonbillable_amount" not in resource else abs(int(resource["nonbillable_amount"]))
    
        # Abs as see - for billed_amount though total is always +
        # usually billed_amount is - but 
        if int(resource["total_charge"]) != abs(int(resource["billed_amount"])) + abs(nonBillableAmount):
            print(f'** Warning: Billed {resource["billed_amount"]}, Totals {resource["total_charge"]}, non billed {resource["nonbillable_amount"]}, don\'t add up')
            
        if resource["brief_description"].split("-")[-1] != resource["units"]:
            print(f'** Warning: Expect brief description to be some ? id + short name of drug + "-cnt units" but {resource["brief_description"]}')
            
        isUpdated = True if resource["date_last_updated"]["value"] != resource["date_entry_added"]["value"] else False
                
        # ################### Incoming #########################
                
        if not re.search(r'\-{}'.format(stationNo), resource["institution"]["id"]):
        
            if not ((set(resource.keys()) - OPT_INCOMING_PROPS) == MAND_INCOMING_PROPS):
                print(json.dumps(resource, indent=4))
                raise Exception("Expected incoming props to be exact")
        
            noIncoming += 1
            if isUpdated:
                noIncomingUpdated += 1
            if isChild:
                noIncomingChild += 1
            incomingInstitutions[resource["institution"]["label"]] += 1
                                                               
            continue
            
        # ################### Outgoing/Local ######################
        
        noOutgoing += 1
        if isUpdated:
            noOutgoingUpdated += 1
        if isChild:
            noOutgoingChild += 1
                        
        if len(MAND_OUTGOING_PROPS - set(resource.keys())) != 0:
            print(MAND_OUTGOING_PROPS - set(resource.keys()))
            print(json.dumps(resource, indent=4))
            raise Exception("Outgoing: missing mandatory property(s)")
            
        if "cancellation_reason" in resource:
            # 687 always true but perhaps a pending for others?
            if not re.search(r'CANCELLED', resource["status"]):
                print(json.dumps(resource, indent=4))
                raise Exception("Don't expect 'cancellation_reason' if status isn't CANCELLED")
                                        
        """
        If action_type specified then means:
        - parent_transaction == self
        - must be NSC or SC NEW (WWW)
        - POR has updates too
        and if missing => child transaction
        """ 
        if "action_type" in resource:
            if resource["action_type"]["label"] not in ["PSO SC RX COPAY NEW", "PSO NSC RX COPAY NEW", "PSO NSC RX COPAY UPDATE", "PSO SC RX COPAY UPDATE"]:
                print(json.dumps(resource, indent=4))
                raise Exception("if action_type specified for OUTGOING then except PSO [N]SC RX COPAY NEW")
        elif isChild == False:
            print(json.dumps(resource, indent=4))
            raise Exception("If no action_type (MARKER) then expect to be child transaction - parentIEN != self IEN") 
                
        # VAST MAJORITY ARE but there are exceptions
        if re.search(r'POSTMASTER', resource["user_adding_entry"]["label"]):
            print(f'** Warning: unexpected - POSTMASTER not enterer of incoming from {resource["institution"]["label"]}')
        
        """
        If ib_action_pointer specified (ie/ pointer to account) then must be a billed
        amount and if no billed amount => no account pointed to
        
        Note: account (350) doesn't arise for incoming co pays
        
        ... always true for WWW but not for POR
        """
        if "ib_action_pointer" not in resource:
            if resource["billed_amount"] != "0":
                accountMissingOutgoing += 1
        else:
            if resource["billed_amount"] == "0":
                print(json.dumps(resource, indent=4))
                raise Exception("Expect NO 350/Account to be pointed to if billed amount == 0 for OUTGOING")
            if resource["ib_action_pointer"]["label"] != f'{stationNo}{resource["ib_action_pointer"]["id"].split("-")[1]}':
                raise Exception("Expected account - ib_action_pointer - to be labeled with {SNO}{itsIEN} but " + resource["ib_action_pointer"]["label"])
    
    print()
    print(f'Last entry date: {lastEntryDate}')
    if dateEntryAddedMissing:
        print(f'** Warning: {dateEntryAddedMissing} are missing dateEntryAdded and were skipped') # PUG
    if institutionMissing:
        print(f'** Warning: {institutionMissing} are missing institution - skipped')           
    if patientMissing:
        print(f'** Warning: {patientMissing} are missing patient - skipped')
    print(f'Outgoing {noOutgoing:,} - updated {noOutgoingUpdated:,} - child {noOutgoingChild:,} - account missing though bill !=0 {accountMissingOutgoing:,}')
    print()
    print(f'Incoming {noIncoming:,} - updated {noIncomingUpdated:,} - child {noIncomingChild:,} - institutions {len(incomingInstitutions)}')
    print()
        
# ################################# DRIVER #######################
               
def main():

    assert sys.version_info >= (3, 6)

    try:
        stationNo = sys.argv[1]
    except IndexError:
        raise SystemExit("Usage _EXE_ STATIONNO")
        
    if len(sys.argv) > 2:
        if sys.argv[2] == "PLOT":
            makePlots(stationNo, "RxCoPay")
            return
        raise Exception("Only extra argument allowed is 'PLOT'")

    # ... as see shape
    # examineAYearPlus(stationNo)
    # return

    webReportRxCoPayTransactions(stationNo)
        
if __name__ == "__main__":
    main()
