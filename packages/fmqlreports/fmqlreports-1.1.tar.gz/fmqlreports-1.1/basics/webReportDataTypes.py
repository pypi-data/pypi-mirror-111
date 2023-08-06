#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys
import os
import re
import json
from collections import defaultdict
from datetime import datetime
import numpy

from fmqlutils import VISTA_DATA_BASE_DIR
from fmqlutils.cacher.cacherUtils import SCHEMA_LOCN_TEMPL, metaOfVistA
from fmqlutils.reporter.reportUtils import MarkdownTable, reportPercent, reportAbsAndPercent

from fmqlreports.webReportUtils import ensureWebReportLocations, SITE_DIR_TEMPL, TOP_MD_TEMPL, keyStats

from buildDirectory import CommonBuildDirectory

"""
TODO:
- Go back to Dates etc missing
  = Back to 687: redo types for date + fill in remaining types
    - ** No ByValueCount for cmr_information/acq_date of 687008
      ** No ByValueCount for cmr_information/repl_date of 687008
      and stopped lists ...
      ie/ how to bypass that in typer
- Builds (and other ways for context ... could also be other files in same range that aren't exclusive?)
- ZZ push off as know ZZ and suggest others should be?
- other way to group station / class III files
- highlight Exclusive Files that need looking at <---- how to do automatically
- consider FILES in other systems but originated here ie/ 663 files elsewhere

Overview of Exclusive File Types in a VistA

Reporting based on:
- base type info used for other type reports
- add extra not in base from schema info
- reduction of all available data (_all) from running typer
    
"""
def webReportDataTypesExclusive(stationNo, typeInfoById=None):

    meta = metaOfVistA(stationNo) # want for MU
    cutYear = meta["cutDate"].split("-")[0] # want for Date QA
       
    # ############################# Assemble Data ###############################   
    
    print("Assembling data for Exclusive Type Report ...")
    
    if typeInfoById == None:
        typeInfoById = expectedTypeCounts(stationNo)
    if "categories" not in typeInfoById[list(typeInfoById)[0]]:
        if not categorizeTypes(typeInfoById, stationNo):
            raise Exception("Can't categorize types as Exclusive or otherwise. Exiting")
    exclusiveTypeInfos = [typeInfoById[typId] for typId in typeInfoById if "EXCLUSIVE" in typeInfoById[typId]["categories"]]
    
    def findDateValuesInReduction(red, tid="", predpath=[]): 
        if tid == "":
            tid = red["_id"]
        dateInfosByTopPred = defaultdict(list)
        stopped = False
        for pred in red:
            if re.match(r'_', pred):
                continue
            fred = red[pred]
            tpredpath = predpath[:]
            tpredpath.append(pred)
            tpred = ":".join(tpredpath)
            if re.match(r'DATE', fred["type"]):
                info = {"tpred": tpred, "count": fred["count"]}
                if "byValueCount" in fred:
                    info["years"] = [dt.split("-")[0] for dt in fred["byValueCount"]]
                elif "invalidCount" in fred:
                    print(f'\t\t** {tid} - {tpred} date reduction missing - all {fred["invalidCount"]} invalid')                    
                else:
                    print(f'\t\t** {tid} - {tpred} date reduction missing (all not noted to be invalid)')
                dateInfosByTopPred[tpred.split(":")[0]].append(info)
                continue 
            if fred["type"] == "LIST":
                if "cstopped" in fred:
                    maxElementsMU = f' - Max els {fred["maxElements"]}' if "maxElements" in fred else ""
                    print(f'\t\t** {tid} - {tpred} STOPPED LIST{maxElementsMU} - redo typer (finding dates)')
                    stopped = True
                    continue
                lDateInfos, lstopped = findDateValuesInReduction(fred["reduction"], tid, tpredpath)
                if lstopped:
                    stopped = True
                for d in lDateInfos:
                    for e in lDateInfos[d]:
                        dateInfosByTopPred[d].append(e)
        return dateInfosByTopPred, stopped  
    def findPointerPredsInReduction(red, rangeTypes, tid="", predpath=[]): 
        if tid == "":
            tid = red["_id"]
        pterInfosByTopPred = defaultdict(list)
        stopped = False
        for pred in red:
            if re.match(r'_', pred):
                continue
            fred = red[pred]
            tpredpath = predpath[:]
            tpredpath.append(pred)
            tpred = ":".join(tpredpath)
            if fred["type"] == "POINTER":
                if len(set(rangeTypes).intersection(set(fred["rangeTypes"]))) == 0:
                    continue
                pterInfosByTopPred[tpred.split(":")[0]].append({"tpred": tpred, "count": fred["count"], "rangeCount": len(fred["byValueCount"]) if "byValueCount" in fred else fred["rangeCount"]})
                continue
            if fred["type"] == "LIST":
                if "cstopped" in fred:
                    maxElementsMU = f' - Max els {fred["maxElements"]}' if "maxElements" in fred else ""
                    print(f'\t\t** {tid} - {tpred} STOPPED LIST{maxElementsMU} - redo typer (finding {"/".join(rangeTypes)})')
                    stopped = True
                    continue
                lptrInfos, lstopped = findPointerPredsInReduction(fred["reduction"], rangeTypes, tid, tpredpath)
                if lstopped:
                    stopped = True
                for p in lptrInfos:
                    for e in lptrInfos[p]:
                        pterInfosByTopPred[p].append(e)
        return pterInfosByTopPred, stopped
        
    """
    Add to type information:
    - field infos and description from schema
    - usage information from _all reduction
    """
    exclusiveTypeInfosReduced = []
    exclusiveTypeInfosNotReducedAsZero = []
    exclusiveTypeInfosNotReducedNotConfirmedZero = []
    typsDateRedVCSuppressed = set()
    typsCSTOPPED = set()
    buildInfosByType = assembleBuildsByType(stationNo, [typInfo["id"] for typInfo in exclusiveTypeInfos])
    try:
        trackFilesCached = json.load(open(f'{VISTA_DATA_BASE_DIR}{stationNo}/Logs/trackFilesCached.json'))
    except:
        zeroFiles = []
    else:
        zeroFiles = trackFilesCached["zeros"]
    # sort makes report of completeness easier
    for typInfo in sorted(exclusiveTypeInfos, key=lambda x: x["count"], reverse=True):
        typId = re.sub(r'\.', '_', typInfo["id"])
        schema = loadSchema(stationNo, typId)
        typInfo["location"] = schema["location"]
        if "description" in schema:
            typInfo["description"] = schema["description"]
        typInfo["fieldInfosByPred"] = dict((fi["pred"], fi) for fi in schema["fields"])
        if typId in zeroFiles:
            typInfo["countReduction"] = 0
            typInfo["countSchema"] = typInfo["count"]
            del typInfo["count"]
            exclusiveTypeInfosNotReducedAsZero.append(typInfo)
            continue
        _all, _subReds = loadReductions(stationNo, typId)
        if _all:
            typInfo["countReduction"] = _all["_total"]
            typInfo["countSchema"] = typInfo["count"]
            del typInfo["count"]
            dateRedsByTPred, dstopped = findDateValuesInReduction(_all)
            if dstopped:
                typsCSTOPPED.add(typId)
            if len(dateRedsByTPred):
                allYRs = sorted([yr for diy in [di for dig in dateRedsByTPred.values() for di in dig if "years" in di] for yr in diy["years"] if yr <= cutYear])
                if len(allYRs):
                    typInfo["firstYear"] = allYRs[0]
                    typInfo["lastYear"] = allYRs[-1]
                if sum(1 for dig in dateRedsByTPred.values() for di in dig if "years" not in di):
                    typsDateRedVCSuppressed.add(typId)
            patientRedsByTPred, pstopped = findPointerPredsInReduction(_all, ["2"])
            userRedsByTPred, ustopped = findPointerPredsInReduction(_all, ["200"])
            typInfo["fieldInfosUsedByPred"] = {}
            for aprop in _all:
                if re.match(r'_', aprop):
                    continue
                if aprop not in typInfo["fieldInfosByPred"]:
                    raise Exception(f"Reduction has prop not in Schema Defn: {aprop}")
                apropInfo = _all[aprop]
                # having "reduction" = use
                fieldInfo = typInfo["fieldInfosByPred"][aprop]
                fieldInfo["reduction"] = apropInfo
                typInfo["fieldInfosUsedByPred"][aprop] = fieldInfo
                del typInfo["fieldInfosByPred"][aprop]
                # pointer reduction for LIST too!
                if aprop in patientRedsByTPred:
                    fieldInfo["patientPointerReduction"] = patientRedsByTPred[aprop]
                if aprop in userRedsByTPred: # could be user + patient red for list
                    fieldInfo["userPointerReduction"] = userRedsByTPred[aprop]  
                if aprop in dateRedsByTPred:
                    fieldInfo["dateReduction"] = dateRedsByTPred[aprop]            
            typInfo["fieldInfosUnusedByPred"] = typInfo["fieldInfosByPred"]
            del typInfo["fieldInfosByPred"]
            exclusiveTypeInfosReduced.append(typInfo)
        else: # not confirmed 0 (ie/ no data => not reduced or just lazy!)
            exclusiveTypeInfosNotReducedNotConfirmedZero.append(typInfo)           
            
    print(f"""Finish Exclusive Type Data Assembly: {len(exclusiveTypeInfosReduced)} reduced""")
    # Missing Data or missing Type (or both maybe - only check types and ZERO file above)
    if len(exclusiveTypeInfosNotReducedNotConfirmedZero):
        print(f"""
Issue with Caching:
    
  * {sum(1 for ti in exclusiveTypeInfosNotReducedNotConfirmedZero if ti["count"] > 0):,} types with FM Count > 0 are missing reduction (PROBABLY HAVE DATA/Not in Zero files) 
    * {"/".join([ti["id"] for ti in exclusiveTypeInfosNotReducedNotConfirmedZero if ti["count"] > 0])}
  * {sum(1 for ti in exclusiveTypeInfosNotReducedNotConfirmedZero if ti["count"] == 0):,} types with FM Count == 0 (MUST CONFIRM/ Not in Zero files). 
    * {"/".join([ti["id"] for ti in exclusiveTypeInfosNotReducedNotConfirmedZero if ti["count"] == 0])}  
    
Overall cache or just type: {", ".join(sorted([ti["id"] for ti in exclusiveTypeInfosNotReducedNotConfirmedZero]))}
  
""")
    if len(typsDateRedVCSuppressed) or len(typsCSTOPPED):
        print(f"""
Issue with typing (date values, list stopped):
  
  * {len(typsDateRedVCSuppressed):,} - {", ".join(sorted(list(typsDateRedVCSuppressed)))} - have a ValueCount date red suppressed 
  * {len(typsCSTOPPED):,} - {", ".join(sorted(list(typsCSTOPPED)))} - have a list cstopped
  
both mean redo typer with different explicit limits.

""")
            
    # ################################## MU ####################################
                    
    def muReducedType(cutYear, typInfo, buildInfosByType):
        if "countReduction" not in typInfo:
            raise Exception("Only for Reduced Types")            
        refId = "X" + re.sub(r'\.', '_', typInfo["id"])
        mu = f'## {typInfo["label"]} ' + ' {#' + refId + '}' + '\n\n'
        if "description" in typInfo:
            mu += "\n> "
            mu += "\n> ".join(typInfo["description"].split("\n")) + "\n\n"
        if typInfo["id"] in buildInfosByType:
            bmu = ", ".join([f'__{bi[2]}__' + (f' ({bi[3]})' if bi[3] else "") for bi in buildInfosByType[typInfo["id"]]])
            mu += f'The file appears in the following builds: {bmu}.' + "\n\n"
        cols = [":Property", ":Description", "Use", "Type"] if sum(1 for p in typInfo["fieldInfosUsedByPred"] if "description" in typInfo["fieldInfosUsedByPred"][p]) else [":Property", "Use", "Type"]
        if sum(1 for pred in typInfo["fieldInfosUsedByPred"] if "patientPointerReduction" in typInfo["fieldInfosUsedByPred"][pred] or "userPointerReduction" in typInfo["fieldInfosUsedByPred"][pred] or "dateReduction" in typInfo["fieldInfosUsedByPred"][pred]):
            cols.append(":Key Values")
        tbl = MarkdownTable(cols, includeNo=False)
        for pred in sorted(typInfo["fieldInfosUsedByPred"], key=lambda x: typInfo["fieldInfosUsedByPred"][x]["reduction"]["count"], reverse=True):
            fieldInfo = typInfo["fieldInfosUsedByPred"][pred]
            ftypMU = fieldInfo["reduction"]["type"]
            if "rangeTypes" in fieldInfo["reduction"]:
                ftypMU = f'{ftypMU} [{"/".join(fieldInfo["reduction"]["rangeTypes"])}]'
            row = [
                f'__{pred}__',
            ]
            if ":Description" in cols:
                row.append(" ".join(fieldInfo["description"].split("\n")) if "description" in fieldInfo else "&nbsp;")
            row.extend([
                reportAbsAndPercent(fieldInfo["reduction"]["count"], typInfo["countReduction"]),
                ftypMU
            ])
            if ":Key Values" in cols:
                valmus = ""
                if "patientPointerReduction" in fieldInfo:
                    valmus += "<br>".join([f'{pr["tpred"]} [P/{pr["count"]}/{pr["rangeCount"]}]' for pr in fieldInfo["patientPointerReduction"]])
                if "userPointerReduction" in fieldInfo:
                    if len(valmus):
                        valmus += "<br><br>"
                    valmus += "<br>".join([f'{pr["tpred"]} [U/{pr["count"]}/{pr["rangeCount"]}]' for pr in fieldInfo["userPointerReduction"]])
                if "dateReduction" in fieldInfo:
                    if len(valmus):
                        valmus += "<br><br>"
                    valmus += "<br>".join([f'{pr["tpred"]} [D/{pr["count"]}]' for pr in fieldInfo["dateReduction"]])
                row.append(valmus)
            tbl.addRow(row)
        mu += f"This type has <span class='yellowIt'>{typInfo['countReduction']:,}</span> records in this system."
        if not re.match(stationNo, typInfo["id"]) and len(typInfo["id"]) >= 6:
            mu += f" Its identifier, _{typInfo['id']}_,  does not start with this system's station number, _{stationNo}_, meaning it __appeared first in another system outside VISN 20__."
        else:
            mu += f" Its identifier is _{typInfo['id']}_."  
        if "firstYear" in typInfo:
            mu += f' It contains date property(s), _{typInfo["firstYear"]}_ is the first year, _{typInfo["lastYear"]}_ is the last.'
        if len(typInfo["fieldInfosUnusedByPred"]) == 0:
            mu += " Every property of this type is used in at least one record.\n\n"
        else:
            mu += f" Out of <span class='yellowIt'>{(len(typInfo['fieldInfosUsedByPred']) + len(typInfo['fieldInfosUnusedByPred'])):,}</span> properties of this type, <span class='yellowIt'>{len(typInfo['fieldInfosUsedByPred']):,}</span> are used." + "\n\n"
        mu += tbl.md() + "\n\n"
        return mu
                
    title = "{} Data Types Exclusive".format(stationNo)
    mu = TOP_MD_TEMPL.format("Data Types Exclusive", title)
    
    # Triple of 
    mu += f"""# Exclusive Types

__{meta.get("name", "VistA")} [{stationNo}]__ was cut on _{meta["cutDate"]}_ and reports <span class='yellowIt'>{len(typeInfoById):,}</span> types of data (\"File Types\"). <span class='yellowIt'>{len(exclusiveTypeInfos):,}</span> are _exclusive_ to the system, meaning they appear in no other VISN 20 VistA. Of these, <span class='yellowIt'>{len(exclusiveTypeInfosReduced):,}</span> are confirmed to have data and are detailed below.

"""

    # Still 
    if len(exclusiveTypeInfosNotReducedNotConfirmedZero):
        mu += f"""__Note__: <span class='yellowIt'>{len(exclusiveTypeInfosNotReducedNotConfirmedZero):,}</span> of the exclusive types have no yet been analyzed.
        
"""
        print(f'** During Reporting, see {len(exclusiveTypeInfosNotReducedNotConfirmedZero):,} lacks types and were not confirmed as data: {", ".join(t["id"] for t in exclusiveTypeInfosNotReducedNotConfirmedZero)}')            

    def tblExclusiveTypeReducedSet(exclusiveTypeInfosReduced, typIds, showYears=True):
        cols = [":Exclusive Type", "Count"]
        if showYears:
            cols.extend(["First Year", "Last Year"])
        tocTBL = MarkdownTable(cols)
        for typInfo in sorted(exclusiveTypeInfosReduced, key=lambda x: x["countReduction"], reverse=True):
            if typInfo["id"] not in typIds:
                continue
            refId = "X" + re.sub(r'\.', '_', typInfo["id"])
            cntMU = f'{typInfo["countReduction"]:,}'
            if typInfo["countReduction"] != typInfo["countSchema"]:
                # could be 0 in schema but have a count
                cntMU = f'__{typInfo["countReduction"]:,} [Actual] / {typInfo["countSchema"]:,} [FileMan]__'
            labelMU = typInfo["label"] if not re.match(stationNo, typInfo["id"]) else f'__{typInfo["label"]}__'
            row = [
                f'[{labelMU}](#{refId}) [{typInfo["id"]}]',
                cntMU
            ]
            if showYears:
                row.extend([
                    typInfo["firstYear"] if "firstYear" in typInfo else "&nbsp;",
                    typInfo["lastYear"] if "lastYear" in typInfo else "&nbsp;"
                ])
            tocTBL.addRow(row)
        return tocTBL
        
    thisYR = int(datetime.strftime(datetime.now(), "%Y"))
    thisYRLessTwo = thisYR - 2
    lastTwoYearTypes = set(typInfo["id"] for typInfo in exclusiveTypeInfosReduced if "lastYear" in typInfo and int(typInfo["lastYear"]) > thisYRLessTwo)
    if len(lastTwoYearTypes):
        mu += f"<span class='yellowIt'>{len(lastTwoYearTypes):,}</span> exclusive types latest entries fall in the last two years. These types may __feature in system migration__ ..." + "\n\n"
        tocTBL = tblExclusiveTypeReducedSet(exclusiveTypeInfosReduced, lastTwoYearTypes)
        mu += tocTBL.md() + "\n\n"
    priorToLastTwoYearTypes = set(typInfo["id"] for typInfo in exclusiveTypeInfosReduced if "lastYear" in typInfo and int(typInfo["lastYear"]) <= thisYRLessTwo)
    if len(priorToLastTwoYearTypes):
        mu += f"<span class='yellowIt'>{len(priorToLastTwoYearTypes):,}</span> exclusive types latest entries are from two or more years ago. These types probably won't feature in system migration ..." + "\n\n"
        tocTBL = tblExclusiveTypeReducedSet(exclusiveTypeInfosReduced, priorToLastTwoYearTypes)
        mu += tocTBL.md() + "\n\n"
    noLastYearTypes = set(typInfo["id"] for typInfo in exclusiveTypeInfosReduced if "lastYear" not in typInfo)
    if len(noLastYearTypes):
        mu += f"<span class='yellowIt'>{len(noLastYearTypes):,}</span> exclusive types lack date properties which means we don't know if the file was used recently or not ..." + "\n\n"
        tocTBL = tblExclusiveTypeReducedSet(exclusiveTypeInfosReduced, noLastYearTypes, False)
        mu += tocTBL.md() + "\n\n"

    if len(exclusiveTypeInfosReduced):
        tmu = ""
        for typInfo in sorted(exclusiveTypeInfosReduced, key=lambda x: x["countReduction"], reverse=True):
            tmu += muReducedType(cutYear, typInfo, buildInfosByType)
        mu += tmu
                
    userSiteDir = SITE_DIR_TEMPL.format(stationNo)
    open(userSiteDir + "dataTypesExclusive.md", "w").write(mu)
    
    print(f"** Finally if needed, fmqlcacher todo in _{stationNo}ExclCacher.sh")
    cachermu = ""
    for ti in exclusiveTypeInfosNotReducedNotConfirmedZero: # will include zero's
        tid = re.sub(r'\.', '_', ti['id'])
        cachermu += f"fmqlcacher configs/SYS.json {tid}" + "\n"
    open(f'_{stationNo}ExclCacher.sh', "w").write(cachermu)
    
"""
Basic overview of Data available in system (suits a PDF/ all is for Web)
"""
def webReportDataTypesSummary(stationNo, typeInfoById=None):
       
    if typeInfoById == None:
        typeInfoById = expectedTypeCounts(stationNo)
    noRecords = sum(typeInfoById[typId]["count"] for typId in typeInfoById)

    title = "{} Data Types Summary".format(stationNo)
    mu = TOP_MD_TEMPL.format("Data Types Summary", title)
        
    mu += muIntroduction(stationNo, typeInfoById)
    
    mu += "The top 15 types are a mixture of patient record and system log and configuration data ...\n\n"
    
    top15 = set()
    tbl = MarkdownTable(["Rank", ":Type", "Records", "Share"], includeNo=False)
    for i, typId in enumerate(sorted(typeInfoById, key=lambda x: typeInfoById[x]["count"], reverse=True), 1):
        top15.add(typId)
        fid = re.sub(r'\_', '.', typId)
        cntMU = typeInfoById[typId]["count"] if typeInfoById[typId]["count"] != -1 else "UNTRACKED"
        percMU = reportPercent(typeInfoById[typId]["count"], noRecords) if typeInfoById[typId]["count"] > 0 else ""
        tbl.addRow([typeInfoById[typId]["rank"], "__{}__ ({})".format(typeInfoById[typId]["label"], fid), cntMU, percMU])
        if i == 15:
            break
    mu += tbl.md() + "\n\n"
    
    # In case not in the top 15
    OTHER_SIGNIFICANT_FILES = set([
        "3_081",
        "2", # PATIENT
        "9_4", # PACKAGE
        "44", # HOSPITAL LOCATION
        "200", # NEW PERSON
        "409_84", # SDEC APPOINTMENT
        "627_8", # DIAGNOSTIC RESULTS - MENTAL HEALTH 
        "631", # H... Patient
        "665", # Prosthetic Patient
        "790", # WV Patient
        "2005", # IMAGE
        "8925", # TIU DOCUMENT
        "8925_1", # TIU DOCUMENT DEFINITION
        "8994", # REMOTE PROCEDURE
    ])
        
    mu += "Other less populated but significant files include ...\n\n"
    
    tbl = MarkdownTable(["Rank", ":Type", "Records", "Share"], includeNo=False)
    for i, typId in enumerate(sorted(typeInfoById, key=lambda x: typeInfoById[x]["count"], reverse=True), 1):
        if typId not in OTHER_SIGNIFICANT_FILES:
            continue
        if typId in top15:
            continue
        fid = re.sub(r'\_', '.', typId)
        cntMU = typeInfoById[typId]["count"] if typeInfoById[typId]["count"] != -1 else "UNTRACKED"
        percMU = reportPercent(typeInfoById[typId]["count"], noRecords) if typeInfoById[typId]["count"] > 0 else ""
        tbl.addRow([typeInfoById[typId]["rank"], "__{}__ ({})".format(typeInfoById[typId]["label"], fid), cntMU, percMU])
    mu += tbl.md() + "\n\n"
    
    userSiteDir = SITE_DIR_TEMPL.format(stationNo)
    open(userSiteDir + "dataTypesSummary.md", "w").write(mu)

"""
Full enumeration of available data (web suitable - summary suits a PDF)
"""    
def webReportDataTypesAll(stationNo, typeInfoById=None):

    if typeInfoById == None:
        typeInfoById = expectedTypeCounts(stationNo)
    noRecords = sum(typeInfoById[typId]["count"] for typId in typeInfoById)
        
    title = "{} Data Types".format(stationNo)
    mu = TOP_MD_TEMPL.format("Data Types", title)
    
    mu += muIntroduction(stationNo, typeInfoById)
                                    
    def muFileGroup(typeInfos, highlightNameIfTrue=None):
        def reverseLetters(lbl):
            org = "*&0123456789abcdefghijklmnopqrstuvwxyz()/"
            repl = "zz9876543210zyxwvutsrqponmlkjihgfedcba)(/"
            rlbl = ""
            lbl = re.sub(r'\s', '', lbl)
            for let in lbl:
                try:
                    idx = org.index(let.lower())
                except:
                    print(f'No mapping for {let} - {lbl}')
                    raise
                rlbl += repl[idx].upper()
            return rlbl
        currentPercentile = -1
        mu = ""
        tbl = None
        firstZeroSeen = False
        firstUntrackedSeen = False
        typIds = []
        recordCNT = 0
        i = 0
        for typeInfo in sorted([ti for ti in typeInfos if ti["count"] > 0], key=lambda x: f'{x["count"]:012}{reverseLetters(x["label"][0:1].upper())}', reverse=True):
            i += 1
            typIds.append(re.sub(r'\.', '_', typeInfo["id"]))
            percMU = ""
            if typeInfo["count"] > 0:
                perc = reportPercent(typeInfo["count"], noRecords)
                if perc != "0.0%":
                    percMU = perc 
            sizePercentile = typeInfo["sizePercentile"] if "sizePercentile" in typeInfo else ""
            if sizePercentile != currentPercentile:
                currentPercentile = sizePercentile
                if tbl:
                    mu += tbl.md() + "\n\n"
                mu += "{} Percentile ...\n\n".format(currentPercentile) if currentPercentile else "Remainder (other than empty or untracked) ...\n\n"
                cols = ["\#", ":Type", "Records"]
                if percMU:
                    cols.append("Share")
                tbl = MarkdownTable(cols, includeNo=False)
            rcnt = typeInfo["count"]
            recordCNT += rcnt
            lbl = re.sub(r'\s+$', '', typeInfo["label"])
            row = [
                i,
                "{} ({})".format(f"__{lbl}__" if not highlightTest or highlightTest(typeInfo) else lbl, typeInfo["id"]),
                rcnt
            ]
            if "Share" in cols:
                row.append(percMU)
            tbl.addRow(row)
        if tbl:
            mu += tbl.md() + "\n\n"
        # 0's
        zeroTIs = sorted([typeInfo for typeInfo in typeInfos if typeInfo["count"] == 0], key=lambda x: reverseLetters(x["label"][0:2].upper()))
        if len(zeroTIs):
            cols = ["\#", ":Type", "Populated Elsewhere"]
            mu += """The following files are marked empty in this VistA. The list below indicates if any other VistAs have records in their equivalents.
                    
"""
            tbl = MarkdownTable(cols, includeNo=False)
            for typeInfo in sorted(zeroTIs, key=lambda x: x["label"][0:2].upper()):
                i += 1
                typIds.append(re.sub(r'\.', '_', typeInfo["id"]))
                lbl = re.sub(r'\s+$', '', typeInfo["label"])
                tbl.addRow([
                    i, 
                    "__{}__ ({})".format(lbl, typeInfo["id"]),
                    "YES" if "NOTEMPTY_0" in typeInfo["categories"] else ""
                ])
            mu += tbl.md() + "\n\n"
        # untracked
        untrackedTIs = sorted([typeInfo for typeInfo in typeInfos if typeInfo["count"] == -1], key=lambda x: reverseLetters(x["label"][0:2].upper()))
        if len(untrackedTIs):
            cols = ["\#", ":Type", "Tracked Elsewhere"]
            mu += """This VistA doesn't proper track the record count of the following files. The list below notes if such files ARE tracked properly in other VistAs.
                    
"""
            tbl = MarkdownTable(cols, includeNo=False) 
            for typeInfo in sorted(untrackedTIs, key=lambda x: x["label"][0:2].upper()):
                i += 1 
                typIds.append(re.sub(r'\.', '_', typeInfo["id"]))
                lbl = re.sub(r'\s+$', '', typeInfo["label"])
                tbl.addRow([
                    i, 
                    "__{}__ ({})".format(lbl, typeInfo["id"]),
                    "YES" if "UNTRACKED:NOT_ELSEWHERE" in typeInfo["subcategories"] else ""
                ])
            mu += tbl.md() + "\n\n"
        return mu, typIds, recordCNT

    mu += """Files break down between __[Core](#core)__ files - those present in every production VistA, __[Exclusive](#exclusive)__ files - those only in this VistA and __[Other](#other)__ files - those in this VistA and some but not all others.
    
"""
    
    categorizeTypes(typeInfoById, stationNo)
    typIdsSeen = set()
    for catag, catagHeader, blurb, highlightTest in [
            ["CORE", "Core Files", "These files are present in every production VistA system.", None], 
            ["EXCLUSIVE", "Exclusive Files", f"These files are only present in this and no other VistA. They may represent functionality exclusive to this VistA. The names of files  from this VistA's local namespace, _{stationNo}_, are in bold.", lambda x: "EXCLUSIVE:NOT_THIS_STATION" not in x["subcategories"]],
            ["OTHER", "Other Files", "Unlike _Core files_, while these files appear in other VistAs, they do not appear in all other VistAs.", None]
        ]:
        if catag == "OTHER":
            typeInfos = [typeInfoById[typId] for typId in typeInfoById if typId not in typIdsSeen]
        else:
            typeInfos = [typeInfoById[typId] for typId in typeInfoById if catag in typeInfoById[typId]["categories"]]
        fgmu, typIds, recordCNT = muFileGroup(typeInfos, highlightTest)
        typIdsSeen |= set(typIds)
        catagIdRef = "{#" + catag.lower() + "}"
        mu += f"""## {catagHeader} {catagIdRef}
        
{blurb} 

These files represent <span class="yellowIt">{reportAbsAndPercent(len(typIds), len(typeInfoById))}</span> of the system's files and <span class="yellowIt">{reportAbsAndPercent(recordCNT, noRecords)}</span> of its records.
        
"""
        mu += fgmu
    
    userSiteDir = SITE_DIR_TEMPL.format(stationNo)
    open(userSiteDir + "dataTypes.md", "w").write(mu)
    
"""
Basic summary shared by ALL and Summary reports
"""
def muIntroduction(stationNo, typeInfoById):

    noEmptyTypes = sum(1 for typId in typeInfoById if typeInfoById[typId]["count"] == 0)
    # untrack is -1
    noUntrackedTypes = sum(1 for typId in typeInfoById if typeInfoById[typId]["count"] == -1)
    noRecords = sum(typeInfoById[typId]["count"] for typId in typeInfoById)
    
    cnts = [typeInfoById[typId]["count"] for typId in typeInfoById if typeInfoById[typId]["count"] > 1]
    singletonCnts = sum(1 for typId in typeInfoById if typeInfoById[typId]["count"] == 1)
    kstats = keyStats(cnts)
    median = int(round(kstats["median"]))
    recordCntBiggest = sorted(cnts, reverse=True)[0]
    
    # 'fails' gracefully on meta and perhaps run BEFORE any but schema exist
    meta = metaOfVistA(stationNo)
    mu = "__{} [{}]__ was cut on _{}_ and reports <span class='yellowIt'>{:,}</span> types of data (\"File Types\"), <span class='yellowIt'>{}</span> of which are singletons (have only one record), <span class='yellowIt'>{}</span> are empty and <span class='yellowIt'>{:,}</span> are _untracked_ (have bad counts). The system has a total of <span class='yellowIt'>{:,}</span> records. While the biggest type has <span class='yellowIt'>{:,}</span> records, the median number of records for types with more than one record is a lowly <span class='yellowIt'>{:,}</span>.\n\n".format(
        meta.get("name", "VistA"), 
        stationNo, 
        meta["cutDate"],
        len(typeInfoById), 
        reportAbsAndPercent(singletonCnts, len(typeInfoById)), 
        reportAbsAndPercent(noEmptyTypes, len(typeInfoById)), 
        noUntrackedTypes, 
        noRecords, 
        recordCntBiggest, 
        median
    )
    
    return mu
    
"""
Utility that using SELECT TYPES to rank files by count and give them
a size percentile

TODO: if full and SO for types then may add date summary ie/ first entry etc
"""
def expectedTypeCounts(stationNo):
    try:
        selectTypes = json.load(open(SCHEMA_LOCN_TEMPL.format(stationNo) + "SELECT_TYPES.json"))
    except:
        raise Exception("Can't load SELECT_TYPE.json from {}".format(SCHEMA_LOCN_TEMPL.format(stationNo)))
    expectedCountByType = {}
    ranks = set()
    cnts = []
    for result in selectTypes["results"]:
        if "parent" in result:
            continue
        typ = re.sub(r'\.', '_', result["number"])
        if "count" not in result:
            cnt = 0
        elif re.search(r'\-', result["count"]):
            cnt = -1
        else:
            cnt = int(result["count"]) 
            cnts.append(cnt)
        if cnt not in ranks:
            ranks.add(cnt)
        expectedCountByType[typ] = {"label": result["name"], "count": cnt}
    ranks = sorted(list(ranks), reverse=True)
    percentileThress = []
    for ptile in range(90, 0, -10):
        thres = numpy.percentile(cnts, ptile)
        percentileThress.append((int(thres), ptile))
    for typ in expectedCountByType:
        if expectedCountByType[typ]["count"] == -1: # no rank given
            continue
        expectedCountByType[typ]["rank"] = ranks.index(expectedCountByType[typ]["count"]) + 1
        if expectedCountByType[typ]["count"] == 0:
            continue
        for percThres in percentileThress:
            if expectedCountByType[typ]["count"] >= percThres[0]:
                expectedCountByType[typ]["sizePercentile"] = percThres[1]
                break
    return expectedCountByType
    
def categorizeTypes(typeInfoById, stationNo=""): # sno for EXCLUSIVE:NOT_THIS_STATION

    commonTmpDir = f'{VISTA_DATA_BASE_DIR}Common/TmpWorking/'
    try:
        vistaFileCategorization = json.load(open(f"{commonTmpDir}vistaFileSummary.json"))
    except:
        print("Exiting: can't load common vista file summary for categorization (common ...)")
        return False
    
    for typId in sorted(typeInfoById, key=lambda x: typeInfoById[x]["count"], reverse=True):
        
        typeInfo = typeInfoById[typId]
        typeInfo["id"] = re.sub(r'_', '.', typId)
        typeInfo["label"] = re.sub(r'^\s+', '', re.sub(r'\s+$', '', typeInfo["label"]))
        if len(typeInfo["label"]) == 0:
            raise Exception("Can't have empty label")
        typeInfo["categories"] = []
        typeInfo["subcategories"] = []
            
        if typeInfo["id"] in vistaFileCategorization["core"]:
            typeInfo["categories"].append("CORE")
        elif typeInfo["id"] in vistaFileCategorization["exclusive"]:
            typeInfo["categories"].append("EXCLUSIVE")
            if stationNo and not re.match(stationNo, typeInfo["id"]):
                typeInfo["subcategories"].append("EXCLUSIVE:NOT_THIS_STATION")
                    
        if typeInfo["id"] not in vistaFileCategorization["empty"] and typeInfo["count"] == 0: # ie/ can show empties separate and indicate not always
            typeInfo["categories"].append("NOTEMPTY_0") # 0 here
                
        if typeInfo["count"] == -1:
            typeInfo["categories"].append("UNTRACKED")
            if typeInfo["id"] not in vistaFileCategorization["invalidCounts"]:
                typeInfo["subcategories"].append("UNTRACKED:NOT_ELSEWHERE")
                    
        if typeInfo["count"] == 1:
            typeInfo["categories"].append("SINGLETON")
            if typeInfo["id"] not in vistaFileCategorization["singletons"]:
                typeInfo["subcategories"].append("SINGLETON:NOT_ELSEWHERE")
                
    return True
                
def loadSchema(stationNo, typId):

    stationDir = f'{VISTA_DATA_BASE_DIR}{stationNo}'
    schemaDir = f'{stationDir}/Schema'
    if not os.path.isdir(schemaDir):
        raise Exception(f"Schema of {stationNo} not available")
    _typId = re.sub(r'\.', '_', typId)
    schemaFile = SCHEMA_LOCN_TEMPL.format(stationNo) + f"SCHEMA_{_typId}.json"
    try:
        schema = json.load(open(schemaFile))
    except:
        print(f"** No Schema known for {typId}")
    else:
        return schema
    return None
    
def loadReductions(stationNo, typId):

    stationDir = f'{VISTA_DATA_BASE_DIR}{stationNo}'
    redDir = f'{stationDir}/Typer/Reductions'
    if not os.path.isdir(redDir):
        return None, []
    redFile = f'{redDir}/{typId}Reduction.json'
    try:
        reds = json.load(open(redFile))
    except:
        pass
    else:
        _all = [red for red in reds if "_subTypeId" not in red][0]
        _subReds = [red for red in reds if "_subTypeId" in red]
        return _all, _subReds
    return None, []
    
def assembleBuildsByType(stationNo, fls):
    cbd = CommonBuildDirectory([stationNo])
    buildInfosByType = defaultdict(list)
    for fl in fls:
        buildNames = cbd.buildsWithFile(fl)
        if not len(buildNames):
            continue
        for bldName in buildNames:
            bldInfo = cbd.lookupBuildEntriesByName(bldName)[0]
            buildInfosByType[fl].append(bldInfo)
    return buildInfosByType
    
# ################################# DRIVER #######################
               
def main():

    assert sys.version_info >= (3, 6)
    
    try:
        stationNo = sys.argv[1]
    except IndexError:
        raise SystemExit("Usage _EXE_ STATIONNO")
                
    ensureWebReportLocations(stationNo)

    webReportDataTypesSummary(stationNo)
                 
    webReportDataTypesAll(stationNo)
    
    webReportDataTypesExclusive(stationNo)
    
if __name__ == "__main__":
    main()
