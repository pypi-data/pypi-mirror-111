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

from fmqlreports.webReportUtils import TOP_MD_TEMPL, SITE_DIR_TEMPL, ensureWebReportLocations, keyStats, flattenFrequencyDistribution, roundFloat, reduce2, reduce4, reduce44, flattenPropValues, vistasOfVISNByOne
from fmqlreports.webReportUtils import muPlotRef, makePlots, vistasOfVISN

from buildDirectory import CommonBuildDirectory

from hl7Utils import HL7TemplateMaker, makeBasicHL7Event, muMessageACKAPPACK, muMessageAPPACK, assembleMessageTextLines, gatherAndQA772_773OfProtocol, lookupConfig779_1
from webReportHL7 import reduce870

"""
Treating Facility File (391.91)

TODO more:
- Warning: some 200XXX's seem to treat? Follow up OR AT LEAST REPORT IN TABLE
    print(f"** Warning: don't expect 'date_last_treated' from anything but VistA (and? Spinal Chord Clinics?) but {institInfo['label']}/{sno}")
- 742V1 ... 741 ... etc --- why these in the "Other Systems" ie/ not a VistA so what is it? [VETERANS ID CARD SYSTEM ... is it there as updates id in Patient records?] ... also sync Cerner now?
- Spinal Care (why so distinct -- any reach out now? What will happen to them?)
- why so many Epic?
- effect of the non VistA, non Cerner entries ie/ 200-based entries on fan out. ie/ why are they in there?
- ASSEMBLE all HIEs across systems ie/ OUTSIDE HOSPITAL + HIE directory (fits with SPQ's used too)
- Update description as clearly doesn't have treatment in Central systems ie/ id updaters (to note if patient updated or not?) ie/ more a log of Patient updates.
- Range of Institutions very similar (400ish) irrespective system size (PUG vs WWW)
----
- date_last_treated is a YEAR! (ie/ not full date)
- cemetary to dth?
- Medtronic etc
- adt_ (A3, A2, A1) and date_last_treated and multiple entries per instit -- why and effect?
- identifier_status: A:Active, H:Merged
- tie into # patients in a system w/o ANY entry here? ie/ should be one?
  ... 85784 in www but 85692 here (so nearly <=>) <-- verify/count completely
- DOES AUSTIN grab this data? If so, with what? SPQs? ie/ shouldn't it be totally centralized? 

MU

<div style="width: 100%">
<div style="width: 35%; float: right">
This report reflects the contents of a copy of _White City_ VistA cut on 2020-08-01.
</div>
<div style="width: 65%">
The _Treating Facility List_, file 391.91 holds

> a list of institutions where the patient has had treatment

</div>
</div>

"""
def webReportTRF(stationNo):

    type391_91, sts391_91s = splitTypeDatas(stationNo, "391_91", expectSubTypeProperties=["institution", "#patient"]) # may add identifier_status (merged|active)
        
    # Prepass - clean out unwanted STs:
    # - no instit
    # - no patient
    # and embed Instit Info 
    institByIEN = reduce4(stationNo)
    excludeSTTotal = 0
    sts391_91Propers = []
    totalWInP = 0
    patientCount = Counter()
    patientInstitCount = defaultdict(lambda: Counter())
    patientsThisVistA = set()
    institSNOsSeen = set() # for QA
    for st in sts391_91s:
        if "institution" not in st:
            excludeSTTotal += st["_total"]
            continue
        if "patient" not in st: # separate
            excludeSTTotal += st["_total"]
            continue
        # silly - not needed as subtype #patient/instit and two presence checks means ...
        if not (st["patient"]["count"] == st["_total"] and st["institution"]["count"] == st["_total"]):
            
            raise Exception("Expected Mandatory Patient and Institution for all considered ST's")
            
        totalWInP += st["_total"]
             
        institRef = singleValue(st, "institution")
        institInfo = institByIEN[re.search(r'\[4\-(\d+)\]', institRef).group(1)]
        if "station_number" not in institInfo:
            print(json.dumps(st, indent=4))
            print(json.dumps(institInfo, indent=4))
            raise Exception("No station number in instit record for TRF source")
        sno = institInfo["station_number"]
        if sno in institSNOsSeen:
            raise Exception("Shared SNOs!") # as breakdown is per instit => unique
        institSNOsSeen.add(sno)
        st["__institInfo"] = institInfo
        
        for ptId in st["patient"]["byValueCount"]:
            patientCount[ptId] += st["patient"]["byValueCount"][ptId]
            patientInstitCount[ptId][sno] = st["patient"]["byValueCount"][ptId]
        
        sts391_91Propers.append(st)
        
        if sno == stationNo:
            patientsThisVistA = set(st["patient"]["byValueCount"].keys())
        
    # Note Excludes BUT - issue that not counting the patient in patient report if no
    # record from home VistA BUT will still show up in sts and do not break down st by
    # patient. Small discrepency and at least top totals for patients align with the
    # number of entries for the home VistA in the VistA report and so won't cause
    # a double-take. Don't exclude from overall entry total ('totalWInP' as may be 
    # below in some st with cnt for that patient  
    # TODO - may hone more if bigger problem
    if excludeSTTotal:
        print(f"** Warning: excluded {excludeSTTotal} entries as either missing I or P")
    for ptid in list(patientCount.keys()):
        if ptid not in patientsThisVistA:
            print(f"** Warning: not counting patient {ptid} as no record for this ({stationNo}) VistA.") # Only seen in 531
            del patientCount[ptid]
            del patientInstitCount[ptid]
        
    mu = TOP_MD_TEMPL.format("{} Treating Facility List".format(stationNo))
    
    meta = metaOfVistA(stationNo)

    mu += "# Treating Facility List {} [{}]\n\n".format(meta["name"], stationNo)
    
    mu += f"""The following describes the Treating Facility List of _{meta["name"]}_ VistA cut on {meta["cutDate"]}. The _Treating Facility List_, file 391.91 holds 

> a list of institutions where the patient has had treatment

This file drives a VistA's reach out to other systems when it needs to assemble a complete record of a patient's care. This file also records if a patient's identifiers and other information in a VistA were updated by a variety of VA systems. 

This VistA's _Treating Facility List_ has <span class="yellowIt">{type391_91["_total"]:,}</span> entries, <span class="yellowIt">{excludeSTTotal}</span> of which are invalid (lack 'institution' or 'patient'). The valid entries come from <span class="yellowIt">{len(institSNOsSeen):,}</span> institutions and are about <span class="yellowIt">{len(patientCount):,}</span> patients.
    
"""

    """
    Basic Patient 
    
    TODO: could do # VistAs per patient too ie/ focus there + VACRNR
    """
    cntInstitPerPatient = Counter()
    thresholds = [5, 10, 15, 20, 50, 100, 500]
    for ptid in patientInstitCount:
        thresMU = f'> {thresholds[len(thresholds)-1]}'
        for i, thres in enumerate(thresholds):
            if len(patientInstitCount[ptid]) <= thres:
                fthres = thres
                if i == 0:
                    thresMU = f'1-{thres}'
                else:
                    thresMU = f'{thresholds[i-1]}-{thres}'
                break
        cntInstitPerPatient[thresMU] += 1
    tbl = MarkdownTable([":Number Institutions", "Patient Count"], includeNo=False)
    for cnt in sorted(cntInstitPerPatient, key=lambda x: cntInstitPerPatient[x], reverse=True):
        tbl.addRow([cnt, reportAbsAndPercent(cntInstitPerPatient[cnt], len(patientInstitCount))])
    mu += "The following shows the number of institutions per patient ...\n\n"
    mu += tbl.md() + "\n\n"
    
    # ################### Break in Five ###################

    vistaSTs = []
    cernerST = None
    sciSTs = []
    oidAssignedSTs = []
    vaDoDInternalSTs = []
    institSNOByOID = {} # for QA
    vistaAllUSVHA = True
    for st in sorted(sts391_91Propers, key=lambda x: x["_total"], reverse=True):

        institInfo = st["__institInfo"]
        sno = institInfo["station_number"]

        if sno not in ["200", "741", "742"] and re.match(r'[3-7][\d]{2}$', sno):
            if not (
                len(st["assigning_authority"]["byValueCount"]) == 1 and 
                singleValue(st, "assigning_authority") == "USVHA"
            ):
                vistaAllUSVHA = False
            if "date_last_treated" not in st:
                print(json.dumps(st, indent=4))
                raise Exception("Expect VistA STs to have 'date_last_treated' even if not 100%")
            # Mainly true but not alreadys
            if sno != institInfo["ien"]:
                print(f'** Warning - Instit IEN for a VistA != SNO - {institInfo["label"]}/{sno}/{institInfo["ien"]}')
            if len(vistaSTs) == 0 and sno != stationNo: 
                raise Exception("Expected top VistA to be the system itself!")
            vistaSTs.append(st)
            continue
            
        if sno == "200CRNR":
            cernerST = st
            continue

        # The Spinal Clinics
        if re.match(r'[^2][\d]{2}SCI$', sno):
            if not (
                len(st["assigning_authority"]["byValueCount"]) == 1 and 
                singleValue(st, "assigning_authority") == "USVHA"
            ):
                raise Exception("SCI centers should only have USVHA as assigning authority")
            sciSTs.append(st)
            continue
            
        if "date_last_treated" in st:
            print(f"** Warning: don't expect 'date_last_treated' from anything but VistA (and? Spinal Chord Clinics?) but {institInfo['label']}/{sno}")
            
        if not re.match(r'(101|200|741|742)', sno): # all of 741 and subs and 742 too
            print(json.dumps(institInfo, indent=4))
            raise Exception(f"By now only expect 101 (central office), 200 or 741* 742* sno's but {sno}")

        # TMP handling no assigning_authority for 200NIN
        if "assigning_authority" in st and sum(1 for aa in st["assigning_authority"]["byValueCount"] if re.search(r'\.', aa)):
            if sum(1 for v in st["source_id_type"]["byValueCount"] if re.search(r'National unique individual identifier', v)) != len(st["source_id_type"]["byValueCount"]):
                raise Exception("OID bearing Facility to be National unique individual identifier")  
            if not (
                "facility_type" in institInfo and
                re.match(r'OTHER', institInfo["facility_type"])
            ):
                print(json.dumps(institInfo, indent=4))
                raise Exception("OID bearing Facility not given facility type OTHER")
            if "isNational" not in institInfo:
                print(json.dumps(institInfo, indent=4))
                raise Exception("OID bearing Facility not marked as National")
            # If set then ...
            if ("parent_facility" in institInfo and 
                not re.match(r'AUSTIN', institInfo["parent_facility"]["label"])):
                print(json.dumps(institInfo, indent=4))
                raise Exception("OID bearing Facility doesn't have austin parent, set to another")         
            oidAssignedSTs.append(st)
            aaOIDs = set(aa for aa in st["assigning_authority"]["byValueCount"] if re.search(r'\.', aa))
            epicAAOIDs = set(aa for aa in aaOIDs if re.match(r'1\.2\.840\.114350\.', aa))
            if set(aa for aa in epicAAOIDs if re.match(r'1\.2\.840\.114350\.1\.13\.\d+\.2\.7\.3\.688884\.100', aa)) != epicAAOIDs:
                    raise Exception("Non EPIC formula for OID") # if true => can extract epic company id
            for oid in aaOIDs:
                if oid in institSNOByOID:
                    if institSNOByOID[oid] != sno:
                        raise Exception("Two SNOs for one OID!")
                else:
                    institSNOByOID[oid] = sno            
            continue

        if "assigning_authority" in st and sum(1 for v in st["assigning_authority"]["byValueCount"] if re.match(r'US[A-Z]{3}$', v)) != len(st["assigning_authority"]["byValueCount"]):
            raise Exception("Expected only USDOD etc for assigning authority of non OID, non ... remaining")
            
        if not re.match(r'200', sno):
            if not (
                sno == "101" or
                ("parent_facility" in institInfo and
                institInfo["parent_facility"]["label"] in ["HEALTH ADMINISTRATION CENTER", "HEALTH ELIGIBILITY CENTER"]) or 
                re.match(r'HEALTH (ADMINISTRATION|ELIGIBILITY) CENTER', institInfo["label"])
            ): # 741 and around
                print(json.dumps(institInfo, indent=4))
                raise Exception(f"Non 200 sno {sno} - Only HEALTH ADMINISTRATION|ELIGIBILITY CENTER Instits put into Internal VA and DoD set")

        vaDoDInternalSTs.append(st)
    
    mu += "Entries in the Treating Facility List can be broken into __[1] VistAs, [2] Cerner, [3] Spinal Chord Injury Centers, [4] VA or DoD Centralized Systems and [5] Third Party Health-care Providers__.\n\n"

    mu += "## VistAs\n\n"
    totalVistAs = sum(st["_total"] for st in vistaSTs)
    if vistaAllUSVHA:
        vistaAllUSVHAMU = ". These entries have a _\"source id type\"_ of _Patient internal identifier_ with _\"assigning authority\"_ of _USVHA_"
    else:
        vistaAllUSVHAMU = ""
    mu += f"""VistAs account for <span class='yellowIt'>{reportAbsAndPercent(totalVistAs, totalWInP)}</span> of the entries. Every patient in the Treating Facility List has an entry for this VistA ({stationNo}) and as a result, it accounts for the highest percentage of VistA entries{vistaAllUSVHAMU} ...
    
"""
    cols = [":VistA", "Station Number", "Count", "Patients", "Treated Date Set"]
    if not vistaAllUSVHA:
        cols.append(":Assigning Authority")
    tbl = MarkdownTable(cols)
    vistaInstitutions = []
    for st in sorted(vistaSTs, key=lambda x: x["_total"], reverse=True):
        institInfo = st["__institInfo"]
        dltSetMU = reportPercent(st["date_last_treated"]["count"], st["_total"])
        row = [
            f'__{institInfo["label"]}__' if institInfo["station_number"] == stationNo else institInfo["label"],
            institInfo["station_number"],
            reportAbsAndPercent(st["_total"], totalVistAs),
            f'{len(st["patient"]["byValueCount"]):,}',
            dltSetMU
            # 687 didn't need - enforced above. But keeping TODO in case others?
            # muBVC(st["source_id_type"]["byValueCount"]),            
            # muBVC(st["assigning_authority"]["byValueCount"])
        ]
        if not vistaAllUSVHA:
            row.append(muBVC(st["assigning_authority"]["byValueCount"]) if "assigning_authority" in st else "&nbsp;")
        tbl.addRow(row)
        info = {
            "institutionIEN": institInfo["ien"],
            "institutionLabel": institInfo["label"],
            "institionStationNo": institInfo["station_number"],
            "total": st["_total"],
            "patientCounts": len(st["patient"]["byValueCount"]) # too many for all
        }
        vistaInstitutions.append(info)
    mu += tbl.md() + "\n\n"
    
    if cernerST:
        mu += "## Cerner\n\n"
        mu += f'Cerner, station number _200CRNR_, now accounts for <span class="yellowIt">{reportAbsAndPercent(cernerST["_total"], totalWInP)}</span> entries with an "assigning authority" of _USDVA_. That number will grow substantially as more and more facilities are moved to Cerner.' + "\n\n"
    else:
        mu += "## Cerner\n\nCurrently this VistA has no entries from Cerner in its Treating Facility List.\n\n"

    totalSCISTs = sum(st["_total"] for st in sciSTs)
    mu += "## Spinal Chord Injury Centers\n\n"
    mu += f"""In all cases, the \"assigning authority\" is _USVHA_. These centers supply <span class='yellowIt'>{reportAbsAndPercent(totalSCISTs, totalWInP)}</span> of the entries ...

"""
    tbl = MarkdownTable([":Name", "Station Number", ":Parent Facility", "Count", "Patients"])
    spinalInstitutions = []
    for st in sorted(sciSTs, key=lambda x: x["_total"], reverse=True):
        institInfo = st["__institInfo"]
        tbl.addRow([
            f'__{institInfo["label"]}__',
            institInfo["station_number"],
            institInfo["parent_facility"]["label"] if "parent_facility" in institInfo else "&nbsp;",
            reportAbsAndPercent(st["_total"], totalSCISTs),
            f'{len(st["patient"]["byValueCount"]):,}'
        ])
        info = {
            "institutionIEN": institInfo["ien"],
            "institutionLabel": institInfo["label"],
            "institionStationNo": institInfo["station_number"],
            "total": st["_total"],
            "patients": st["patient"]["byValueCount"]
        }
        if "parent_facility" in institInfo:
            info["parentInstitutionLabel"] = institInfo["parent_facility"]["label"]
            info["parentInstitutionIEN"] = institInfo["parent_facility"]["id"].split("-")[1]
        spinalInstitutions.append(info)
    mu += tbl.md() + "\n\n"
    
    totalVADoDInternalSTs = sum(st["_total"] for st in vaDoDInternalSTs)
    mu += "## VA or DoD Centralized Systems\n\n"
    mu += f"""Together these systems account for <span class='yellowIt'>{reportAbsAndPercent(totalVADoDInternalSTs, totalWInP)}</span> of the entries ...

"""
    tbl = MarkdownTable([":Name", "Station Number", "Count", "Patients", ":Source Type", ":Assigning Authority"])
    vaDoDInternalInstitutions = []
    for st in sorted(vaDoDInternalSTs, key=lambda x: x["_total"], reverse=True):
        institInfo = st["__institInfo"]
        tbl.addRow([
            f'__{institInfo["label"]}__',
            institInfo["station_number"],
            reportAbsAndPercent(st["_total"], totalVADoDInternalSTs),
            f'{len(st["patient"]["byValueCount"]):,}',
            muBVC(st["source_id_type"]["byValueCount"]) if "source_id_type" in st else "&nbsp;",           
            muBVC(st["assigning_authority"]["byValueCount"]) if "assigning_authority" in st else "&nbsp;" 
        ])
        info = {
            "institutionIEN": institInfo["ien"],
            "institutionLabel": institInfo["label"],
            "institionStationNo": institInfo["station_number"],
            "total": st["_total"],
            "patientCounts": len(st["patient"]["byValueCount"]), # too many for all for now
            "sidBVC": st["source_id_type"]["byValueCount"] if "source_id_type" in st else {}, 
            "aaBVC": st["assigning_authority"]["byValueCount"] if "assigning_authority" in st else {}
        }
        vaDoDInternalInstitutions.append(info)
    mu += tbl.md() + "\n\n"
    
    """
    In Epic: {iso(1) member-body(2) us(840) epic(114350)}
    - Many in Epic are 1.2.840.114350.1.13.{SPECIAL}.2.7.3.688884.100
    
    In HL7: {joint-iso-itu-t(2) country(16) us(840) organization(1) hl7(113883)}
            .3 (externalUseRoots: delegated role authorities);
            .4 (commonPublicNamespaces: ...)
            .13 (externalValueSets)
            .17 (misc namespaces)
            ... .3 is the most common
        {joint-iso-itu-t(2) country(16) us(840) organization(1) hl7(113883) 17(17) sdbeacon(8)} - San Diego Beacon eHealth Community Project
    - .3 seem to be Exchanges ie/ 2.16.840.1.113883.3 HL73!
    - only other .4. is https://oidref.com/2.16.840.1.113883.4.391 which is eClinicalWorks
    - 2.16.840.1.113883.4.1 shouldn't be Walgreens as SSN! ... should be just 
    2.16.840.1.113883.3.2018
    - Brooklyn Health Information Exchange: HL7 (13.61) 
       https://oidref.com/2.16.840.1.113883.13.61
    - 2.16.840.1.113883.17.8.2
                
    In DoD Private Enterprise: 1.3.6.1.4.1
    - 1.3.6.1.4.1.12009 == Regenstrief
    - {iso(1) identified-organization(3) dod(6) internet(1) private(4) enterprise(1) 26580(26580)} ... Kaiser [Kaiser has an Epic too!]
    """
    totalOIDAssignedSTs = sum(st["_total"] for st in oidAssignedSTs)
    mu += "## Third Party Health-care Providers\n\n"
    mu += f"""All of these outside Health Providers are identified with _Object Identifiers_ (OID). Most individual providers have OIDs assigned by Epic Systems under their _1.2.840.114350.1.13_ tree. Most of the other providers are Health Information Exchanges (HIE) with either their own OID assigned by the HL7 standards organization or by the DoD. These providers account for <span class='yellowIt'>{reportAbsAndPercent(totalOIDAssignedSTs, totalWInP)}</span> of the entries ...

"""
    tbl = MarkdownTable([":Name", "Station Number", "Count", "Patients", ":Assigning Authority"])
    thirdPartyInstitutions = []
    for st in sorted(oidAssignedSTs, key=lambda x: x["_total"], reverse=True):
        institInfo = st["__institInfo"]
        aaBVC = Counter()
        hasEpic = False
        if "byValueCount" in st["assigning_authority"]: # TMP til Indiana done right
            for aa in st["assigning_authority"]["byValueCount"]:
                aaId = aa
                epicMatch = re.match(r'1\.2\.840\.114350\.1\.13\.(\d+)\.2\.7\.3\.688884\.100', aa)
                if epicMatch:
                    hasEpic = True
                    aaId = f'Epic ({epicMatch.group(1)})'
                else:
                    hl7Match = re.match(r'2\.16\.840\.1\.113883\.(\d+)\.(.+)', aa)
                    if hl7Match:
                        aaId = f'HL7{hl7Match.group(1)} ({hl7Match.group(2)})'
                    else:
                        dodPrivateEnterpriseMatch = re.match(r'1\.3\.6\.1\.4\.1\.(.+)', aa)
                        if dodPrivateEnterpriseMatch:
                            dodRegensMatch = re.match(r'1\.3\.6\.1\.4\.1\.12009\.1\.(\d+)\.1', aa)
                            if dodRegensMatch:
                                aaId = f'DoDRegenstrief ({dodRegensMatch.group(1)})'
                            else:
                                aaId = f'DoDPrivate ({dodPrivateEnterpriseMatch.group(1)})'
                aaBVC[aaId] = st["assigning_authority"]["byValueCount"][aa]
        # ignoring source_type_id as always National unique individual identifier
        tbl.addRow([
            f'__{institInfo["label"]}__' if hasEpic == False else institInfo["label"],
            institInfo["station_number"],
            reportAbsAndPercent(st["_total"], totalOIDAssignedSTs),
            f'{len(st["patient"]["byValueCount"]):,}',
            muBVC(aaBVC)
        ])
        info = {
            "institutionIEN": institInfo["ien"],
            "institutionLabel": institInfo["label"],
            "institionStationNo": institInfo["station_number"],
            "total": st["_total"],
            "patients": st["patient"]["byValueCount"],
            "aaBVC": aaBVC
        }
        thirdPartyInstitutions.append(info)
    mu += tbl.md() + "\n\n"
    
    # Write break down data to TMP for use in dirs
    # ... below do a combo report with an About VistAs summary table too => need meta
    info = {
        "stationNo": stationNo,
        "vistaName": meta["name"],
        "vistaCutDate": meta["cutDate"],
        "trfCount": totalWInP,
        "trfPatientCount": len(patientCount),
        
        "vistaInstitutions": vistaInstitutions,
        "spinalInstitutions": spinalInstitutions,
        "vaDoDInternalInstitutions": vaDoDInternalInstitutions,
        "thirdPartyInstitutions": thirdPartyInstitutions
    }
    tmpLocn = "{}{}/{}".format(VISTA_DATA_BASE_DIR, stationNo, "TmpWorking")
    json.dump(info, open(f"{tmpLocn}/trfReduction.json", "w"), indent=4)
    
    userSiteDir = SITE_DIR_TEMPL.format(stationNo)
    print(f'Serializing Report to {userSiteDir}')
    open(f'{userSiteDir}treatingFacilityList.md', "w").write(mu) 

"""
Cross VistA Report focusing on VA DOC Internal Institutions and Third Party Institutions
"""
def webReportCrossVistAs():

    # FUTURE: HOMEVISNVISTAS = vistasOfVISNByOne(stationNo)     
    stationNos = ["531", "663", "687", "757", "692", "653"]

    trfInfoByStationNo = {}
    for stationNo in stationNos:
        tmpLocn = "{}{}/{}".format(VISTA_DATA_BASE_DIR, stationNo, "TmpWorking")
        trfInfoFL = f"{tmpLocn}/trfReduction.json"
        try:
            trfInfo = json.load(open(trfInfoFL))
        except:
            print(f"No {stationNo} TRF Reduction - skipping")
            continue
        trfInfoByStationNo[stationNo] = trfInfo
    if len(trfInfoByStationNo) == 0:
        raise Exception(f'No station number TRF information for any of {stationNos}')
    
    def muInstitutionSet(title, institSetId, showAA=False):
        institNamesBySNO = defaultdict(set)
        totalByInstitSNOBySNO = defaultdict(lambda: defaultdict(lambda: Counter()))
        totalBySNO = Counter()
        aaBVCByInstitId = {}
        for stationNo in trfInfoByStationNo:
            institSet = trfInfoByStationNo[stationNo][institSetId]
            for iinfo in institSet:
                totalByInstitSNOBySNO[iinfo["institionStationNo"]][stationNo] = iinfo["total"]
                institNamesBySNO[
                iinfo["institionStationNo"]].add(iinfo["institutionLabel"])
                totalBySNO[stationNo] += iinfo["total"]
                aaBVCByInstitId[iinfo["institionStationNo"]] = iinfo["aaBVC"]
        cols = [":Institution", ":Station Number"]
        if showAA:
            cols.append("National Id")
        cols.extend(sorted(totalBySNO))
        tbl = MarkdownTable(cols)
        for institSNO in sorted(totalByInstitSNOBySNO, key=lambda x: sum(totalByInstitSNOBySNO[x][y] for y in totalByInstitSNOBySNO[x]), reverse=True):
            row = [
                f'__{sorted(list(institNamesBySNO[institSNO]))[0]}__',
                institSNO
            ]
            for stationNo in sorted(totalBySNO):
                if len(row) == 2 and showAA:
                    if len(aaBVCByInstitId[institSNO]) == 1 and len(list(aaBVCByInstitId[institSNO].keys())[0]) > 10:
                        row.append(list(aaBVCByInstitId[institSNO].keys())[0][0:9] + "...")
                    elif len(aaBVCByInstitId[institSNO]) < 4:
                        row.append(", ".join(sorted(aaBVCByInstitId[institSNO])))
                    else: # regens
                        row.append(", ".join(sorted(aaBVCByInstitId[institSNO])[0:2]) + " ...")
                if stationNo not in totalByInstitSNOBySNO[institSNO]:
                    row.append("&nbsp;")
                    continue
                row.append(reportAbsAndPercent(
                totalByInstitSNOBySNO[institSNO][stationNo], totalBySNO[stationNo]))
            tbl.addRow(row)
        ismu = f"""## {title}
        
<span class='yellowIt'>{len(totalByInstitSNOBySNO):,}</span> institutions{'' if showAA == False else ', identified with Object Identifiers, many in the namespace of Epic Systems'} ...

"""
        ismu += tbl.md() + "\n\n"
        return ismu
        
    print("Producing cross VistA Treating Facility List Report")
        
    mu = TOP_MD_TEMPL.format("Treating Facility List Across VistAs")
    
    mu += "# Treating Facility List Across VistAs\n\n"
    
    mu += f"""The following describes the Treating Facility List (\"TFL\") in a series of VistAs. Specifically it reports on the entries from [1] VA or DoD Centralized Systems and from [2] Third Party Health-care Providers.\n\n"""
        
    mu += muInstitutionSet("VA or DoD Centralized Systems", "vaDoDInternalInstitutions")

    mu += muInstitutionSet("Third Party Health-care Providers and HIEs", "thirdPartyInstitutions", True)
        
    mu += f'## Source VistA Details\n\n'
    mu += "Data for this report came from the following production VistA copies cut on the following dates ...\n\n"
    tbl = MarkdownTable([":Name", ":Station \#", "TFL \#", "Patient \#", "Clone Cut Date"])
    for sno in sorted(trfInfoByStationNo):
        trfInfo = trfInfoByStationNo[sno]
        tbl.addRow([
            f'__{trfInfo["vistaName"]}__',
            sno,
            f'{trfInfo["trfCount"]:,}',
            f'{trfInfo["trfPatientCount"]:,}',
            trfInfo["vistaCutDate"]
        ])
    mu += tbl.md() + "\n\n"
    
    userSiteDir = SITE_DIR_TEMPL.format("Common")
    print(f'Serializing Report to {userSiteDir}')
    open(f'{userSiteDir}treatingFacilityList.md', "w").write(mu) 
        
# ################################# DRIVER #######################
               
def main():
    
    assert sys.version_info >= (3, 6)

    try:
        stationNo = sys.argv[1]
    except IndexError:
        webReportCrossVistAs()
        return
            
    webReportTRF(stationNo)
                        
if __name__ == "__main__":
    main()
    