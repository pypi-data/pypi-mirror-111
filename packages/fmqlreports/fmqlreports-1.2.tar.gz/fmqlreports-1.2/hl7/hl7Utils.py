#!/usr/bin/env python
# -*- coding: utf8 -*-

import re
import json
from collections import defaultdict, Counter
from datetime import datetime, timedelta

from fmqlutils import VISTA_DATA_BASE_DIR
from fmqlutils.cacher.cacherUtils import FMQLReplyStore, FilteredResultIterator, metaOfVistA
from fmqlutils.reporter.reportUtils import reportPercent

# ############################ IFC Message Categorize and Extract ######################

"""
Beyond Segment Parse and Format, just for IFCs, categorize messages beyond just their names and to their purpose and then extract key properties.

This adds/duplicates the structured data on msgs in 772 and 773.

Final 123 Audit: doesn't correlate ACK or APP ACK to Message => don't know if errored. This means may think a message leads to a 123 entry but if it errors then that entry won't be there. Ditto for S TIU messages replaced with F message contents in the 123 audit.

Take message segments and transmission direction to [1] categorize and 
[2] extract key properties. Test of property coverage is that you can 
[3] make the consult trail of consults.

TODO: QA mode to comparse original message to a format from its parse (must do fuller extract first!)
TODO: may do this for other messages too ex/ SPQ
"""
def categorizeAndParseIFCHL7Message(message, transmissionType, deidentify):
 
    GENERIC_EXTRACTS = {
    
        "MSH[0]:dateTimeMessage": "dateTimeMessage",
        "MSH[0]:sendingFacility": "sendingFacility",
        "MSH[0]:receivingFacility": "receivingFacility",
        "MSH[0]:messageCtrlId": "messageId", # {stationNo}{vista 773 IEN}
        "MSH[0]:acceptAcknowledgementType": "acceptAcknowledgementType",
        "MSH[0]:applicationAcknowledgementType": "applicationAcknowledgementType",
        
        "ORC[0]:placerOrderNumber": "placerConsultId",
        "ORC[0]:fillerOrderNumber": "fillerConsultId"
        
    }
    
    # BIG TODO: take out the people and their roles (if want to synthesize/work
    # back to 123/activity (who_, remote_) then need that
    MSG_CATEGORIES = [
                
                # MTCH the error messages + the ACKs
                
                # Some NW has FI^FORWARD in orderControlCodeReason. Not distinguishing
                # (for now but see consults etc)
                {
                    "name": "NEW",
                    
                    "segmentTypes": ["MSH", "PID", "ORC", "OBR", "OBX:TX+", "OBX:CE:DIAG", "OBX:CE:TZ", "NTE:UCID"], 

                    "matches": {
                        "ORC[0]:orderControl": "NW" 
                        # no ORC[0]:orderStatus
                        # no ORC[0]:orderControlCodeReason
                    },
                    
                    # Its TX=Comments are 2000.02^REASON FOR REQUEST^AS4 vs the 
                    # ^COMMENTS^ in COMMENT etc below
                    "extracts": {
                        "OBR[0]:toServiceLabel": "toService", # tracks previous if forward
                        "OBX[valueType+=TX]:value": "comments", # COMMENT
                        "OBX[typeId=^PROVISIONAL DIAGNOSIS^]:value": "diagnosis", 
                        "OBX[typeId=^TIME ZONE^VA4.4]:value": "tz"
                    },
                    
                    "expected123Activity": {
                        "O": "CPRS RELEASED ORDER",
                        # TODO: also saw but not fully done, INITIAL REMOTE REQUEST
                        "I": "REMOTE REQUEST RECEIVED" 
                    }
                    
                },
                
                {
                    "name": "ACK", # simple ACK 
                    
                    "segmentTypes": ["MSH", "MSA"],
                    
                    "matches": {
                        "MSA[0]:ackCode": "CA"
                    },
                    
                    "extracts": {
                        "MSA[0]:msgCtrlIdLocal": "ackTo" # {SNO}{773IEN} of orig msg
                    }
                },
                
                { # only first NEW message has ORC in its APP ACK
                    "name": "ACK APP",
                    
                    "segmentTypes": ["MSH", "MSA", "ORC*"],
                    
                    "matches": {
                        "MSA[0]:ackCode": "AA"
                    },
                    
                    "extracts": {
                        "MSA[0]:msgCtrlIdLocal": "ackTo" # {SNO}{773IEN} of orig msg
                    }
                },
                
                {
                    "name": "ACK APP REJECT",
                    
                    "segmentTypes": ["MSH", "MSA", "ORC*"],
                    
                    "matches": {
                        "MSA[0]:ackCode": "AR"
                    },
                    
                    "extracts": {
                        "MSA[0]:msgCtrlIdLocal": "ackTo", # {SNO}{773IEN} of orig msg
                        "MSA[0]:text": "errorCode" # 201 or 802
                    }
                },
                                
                {
                    "name": "COMMENT",
                    
                    "segmentTypes": ["MSH", "PID", "ORC", "OBX:TX*", "OBX:CE:TZ"], 
                    
                    "matches": {
                        # I or O ie/ both directions - remote_ vs ... properties
                        "ORC[0]:orderControl": "IP", # TODO expand name
                        "ORC[0]:orderStatus": "IP"
                        # no ORC[0]:orderControlCodeReason
                    },
                    
                    # diagnosis 
                    # TX is ^COMMENTS^ vs the REASON for REQUEST in the first one
                    "extracts": {
                        "OBX[valueType+=TX]:value": "comments", # COMMENT
                        "OBX[typeId=^TIME ZONE^VA4.4]:value": "tz"
                    },

                    "expected123Activity": {
                        "I": "ADDED COMMENT",
                        "O": "ADDED COMMENT"
                    }                
                },
                
                {
                    "name": "RECEIVE",
                    
                    "segmentTypes": ["MSH", "PID", "ORC", "OBX:TX*", "OBX:CE:TZ"], 
                    
                    "matches": {
                        "ORC[0]:orderControl": "SC", # TODO expand name
                        "ORC[0]:orderStatus": "IP",
                        "ORC[0]:orderControlCodeReason": "R^RECEIVE^99GMRC"
                    },
                            
                    "extracts": {
                        # take OBX:tx - comment optional
                        "OBX[valueType+=TX]:value": "comments", # COMMENT
                        "OBX[typeId=^TIME ZONE^VA4.4]:value": "tz"
                    },

                    "expected123Activity": {
                        "I": "RECEIVED",
                        # See on O and have comment! Qualifies initial. 
                        # ... => RECEIVE means something more than COMMENT
                        "O": "RECEIVED"
                    }
                    
                },

                {
                    "name": "SCHEDULE", # Not fully QA'ed as not WWW placer
                    
                    "segmentTypes": ["MSH", "PID", "ORC", "OBX:TX*", "OBX:CE:TZ"], 
                    
                    "matches": {
                        "ORC[0]:orderControl": "SC", 
                        "ORC[0]:orderStatus": "SC",
                        "ORC[0]:orderControlCodeReason": "SC^SCHEDULE^99GMRC"
                    },
                            
                    "extracts": {
                        # take OBX:tx - comment optional
                        "OBX[valueType+=TX]:value": "comments", # COMMENT
                        "OBX[typeId=^TIME ZONE^VA4.4]:value": "tz"
                    },

                    "expected123Activity": {
                        "I": "SCHEDULED",
                        "O": "SCHEDULED" # Not QA'ed so TODO
                    }
                    
                },
                
                {
                    "name": "SIGFINDING", # Not fully QA'ed as not WWW placer
                    
                    "segmentTypes": ["MSH", "PID", "ORC", "OBX:TX*", "OBX:CE:TZ"], 
                    
                    "matches": {
                        "ORC[0]:orderControl": "RE", 
                        "ORC[0]:orderStatus": "CM",
                        "ORC[0]:orderControlCodeReason": "S^SIGNIFICANT FINDING^99GMRC"
                    },
                            
                    "extracts": {
                        # take OBX:tx - comment optional
                        "OBX[valueType+=TX]:value": "comments", # COMMENT
                        "OBX[typeId=^SIG FINDINGS^]:value": "sigFinding",
                        "OBX[typeId=^TIME ZONE^VA4.4]:value": "tz"
                    },

                    "expected123Activity": {
                        "I": "SIGFINDIN", # ??? gotta QA TODO
                        "O": "SIGFINDIN" # ??? gotta QA TODO
                    }
                    
                },
                
                {
                    "name": "DISASSOCIATE", # Not fully QA'ed as not WWW placer
                    
                    "segmentTypes": ["MSH", "PID", "ORC", "OBX:TX*", "OBX:CE:TZ"], 
                    
                    "matches": {
                        "ORC[0]:orderControl": "RE", 
                        "ORC[0]:orderStatus": "IP",
                        "ORC[0]:orderControlCodeReason": "D^DISASSOCIATE RESULT^99GMRC"
                    },
                            
                    "extracts": {
                        "OBX[0]:value": "tiuRef",
                        "OBX[typeId=^TIME ZONE^VA4.4]:value": "tz"
                    },

                    "expected123Activity": {
                        "O": "DISASSOCIATE", # TODO: don't know 123 ... fill in
                        "I": "DISASSOCIATE" # TODO: don't know 123 ... fill in
                    }
                    
                },
                
                # FILLER
                # previous_remote_service_name set by this FORWARDED FROM in 123/activity
                {
                    "name": "FORWARD", # I only but same as below
                    
                    "segmentTypes": ["MSH", "PID", "ORC", "OBR", "OBX:TX*", "OBX:CE:TZ"],
                    
                    "matches": {
                        "ORC[0]:orderControl": "XX", # TODO expand name
                        "ORC[0]:orderStatus": "IP",
                        "ORC[0]:orderControlCodeReason": "F^FORWARD^99GMRC" # F vs FI
                    },
                            
                    "extracts": {
                        "OBR[0]:toServiceLabel": "toService", # tracks previous if forward
                        "OBX[valueType+=TX]:value": "comments", # COMMENT
                        "OBX[typeId=^TIME ZONE^VA4.4]:value": "tz"
                    },
                    
                    # Will have previous (current) OBR[0]:toServiceLabel ie/ one replaced
                    "expected123Activity": {
                        "I": "FORWARDED FROM",
                        "O": "FORWARDED FROM" # TODO: QA THIS -- it's a guess (not QAed)
                    }
                
                },

                {
                    "name": "EDITRESUBMIT", # I only but same as below
                    
                    "segmentTypes": ["MSH", "PID", "ORC", "OBR", "OBX:TX*", "OBX:CE:TZ"],
                    
                    "matches": {
                        "ORC[0]:orderControl": "XO", 
                        "ORC[0]:orderStatus": "IP",
                        "ORC[0]:orderControlCodeReason": "E^EDIT-RESUBMIT^99GMRC" # F vs FI
                    },
                            
                    "extracts": {
                        "OBR[0]:toServiceLabel": "toService", # tracks previous if forward
                        "OBX[valueType+=TX]:value": "comments", # COMMENT
                        "OBX[typeId=^TIME ZONE^VA4.4]:value": "tz"
                    }
                    
                    # Will have previous (current) OBR[0]:toServiceLabel ie/ one replaced
                    # "expected123Activity": {
                    #    "I": "FORWARDED FROM",
                    #    "O": "FORWARDED FROM" # TODO: QA THIS -- it's a guess (not QAed)
                    # }
                
                },
                
                {
                    "name": "FORWARD", # O only but same as below
                    
                    "segmentTypes": ["MSH", "PID", "ORC", "OBR", "OBX:TX*", "OBX:CE:TZ"],
                    
                    "matches": {
                        "ORC[0]:orderControl": "XX", # TODO expand name
                        "ORC[0]:orderStatus": "IP",
                        "ORC[0]:orderControlCodeReason": "FI^FORWARD TO IFC^99GMRC" # FI vs F
                    },
                            
                    "extracts": {
                        "OBR[0]:toServiceLabel": "toService", # tracks previous if forward
                        "OBX[valueType+=TX]:value": "comments", # COMMENT
                        "OBX[typeId=^TIME ZONE^VA4.4]:value": "tz"
                    },
                    
                    "expected123Activity": {
                        "O": "FWD TO REMOTE SERVICE",
                        "I": "FWD TO REMOTE SERVICE"
                    }
                
                },
                
                {
                    "name": "DISCONTINUE",
                    
                    "segmentTypes": ["MSH", "PID", "ORC", "NTE*", "OBX:CE:TZ"],
                    
                    "matches": {
                        "ORC[0]:orderControl": "OD", 
                        "ORC[0]:orderStatus": "DC"
                        # no ORC[0]:orderControlCodeReason
                    },
                    
                    "extracts": {
                        "OBR[0]:toServiceLabel": "toService", # tracks previous if forward
                        "NTE[valueType+=L]:value": "comments", # COMMENT
                        "OBX[typeId=^TIME ZONE^VA4.4]:value": "tz"
                    },
                    
                    # Will have previous (current) OBR[0]:toServiceLabel ie/ one replaced
                    "expected123Activity": {
                        "I": "DISCONTINUED",
                        "O": "DISCONTINUED" # BUT CHECK as WCO! 692  
                    }
                    
                },
                
                {
                    "name": "DISCONTINUE", # CRNR only
                    
                    "segmentTypes": ["MSH", "PID", "ORC", "NTE*", "OBX:CE:TZ"],
                    
                    "matches": {
                        "ORC[0]:orderControl": "DC", 
                        "ORC[0]:orderStatus": "DC"
                        # no ORC[0]:orderControlCodeReason
                    },
                    
                    "extracts": {
                        "OBR[0]:toServiceLabel": "toService", # tracks previous if forward
                        "NTE[valueType+=L]:value": "comments", # COMMENT
                        "OBX[typeId=^TIME ZONE^VA4.4]:value": "tz"
                    },
                    
                    # Will have previous (current) OBR[0]:toServiceLabel ie/ one replaced
                    "expected123Activity": {
                        "I": "DISCONTINUED",
                        "O": "DISCONTINUED" # BUT CHECK as WCO! 692  
                    }
                    
                },
                
                {
                    "name": "CANCEL",
                    
                    "segmentTypes": ["MSH", "PID", "ORC", "NTE*", "OBX:CE:TZ"],
                    
                    "matches": {
                        "ORC[0]:orderControl": "OC", # TODO expand name
                        "ORC[0]:orderStatus": "CA"
                        # no ORC[0]:orderControlCodeReason
                    },
                    
                    "extracts": {
                        "OBR[0]:toServiceLabel": "toService", # tracks previous if forward
                        "NTE[valueType+=L]:value": "comments", # COMMENT
                        "OBX[typeId=^TIME ZONE^VA4.4]:value": "tz"
                    },
                    
                    # Will have previous (current) OBR[0]:toServiceLabel ie/ one replaced
                    "expected123Activity": {
                        "I": "DISCONTINUED",
                        "O": "DISCONTINUED" # BUT CHECK as WCO! 692  
                    }
                    
                },
                                
                # TODO: for the following one directions - once do FILER side, expect
                # both directions
                {
                    "name": "INCOMPL RPT",
                    
                    "segmentTypes": ["MSH", "PID", "ORC", "OBX", "OBX:CE:TZ"],
                    
                    "matches": {
                        "ORC[0]:orderControl": "RE", # TODO expand name
                        "ORC[0]:orderStatus": "A",
                        # no ORC[0]:orderControlCodeReason
                        "OBX[0]:valueType": "RP",
                        "OBX[0]:status": "S" # redundant with A from ORC?
                    },
                    
                    "extracts": {
                        "OBX[0]:value": "tiuRef", # TIU Ref in Remote Site (OBX:valueType=RP)
                        "OBX[typeId=^TIME ZONE^VA4.4]:value": "tz"
                    },              
                    
                    "expected123Activity": { # means S in both cases
                        "I": "INCOMPLETE RPT", 
                        "O": "INCOMPLETE RPT"  
                    }
                    
                },
                
                {
                    "name": "COMPL RPT",
                    
                    "segmentTypes": ["MSH", "PID", "ORC", "OBX", "OBX:CE:TZ"],
                    
                    "matches": {
                        "ORC[0]:orderControl": "RE", # TODO expand name
                        "ORC[0]:orderStatus": "CM",
                        # no ORC[0]:orderControlCodeReason
                        "OBX[0]:valueType": "RP", # Indicates TIU REF
                        "OBX[0]:status": "F" # redundant with CM from ORC?
                    },
                    
                    "extracts": {
                        "OBX[0]:value": "tiuRef", # TIU Ref in Remote Site (OBX:valueType=RP)
                        "OBX[typeId=^TIME ZONE^VA4.4]:value": "tz"
                    },              
                    
                    "expected123Activity": { # means F in both cases
                        "I": "COMPLETE/UPDATE",
                        "O": "NEW NOTE ADDED"
                    }  
                    
                },
                
                {
                    "name": "COMPL COMMENT",
                    
                    "segmentTypes": ["MSH", "PID", "ORC", "OBX:TX+", "OBX:CE:TZ"],
                    
                    "matches": {
                        "ORC[0]:orderControl": "RE", # TODO expand name
                        "ORC[0]:orderStatus": "CM",
                        # no ORC[0]:orderControlCodeReason
                        "OBX[-2]:valueType": "TX", # Indicates Comment
                        "OBX[-2]:status": "F" # redundant with CM from ORC?
                    },
                    
                    # Only one doing SIG FINDING for as don't see in others
                    # and doesn't appear in audit anyhow
                    "extracts": {
                        "OBX[typeId+=^COMMENTS^]:value": "comments", # COMMENT
                        "OBX[typeId=^SIG FINDINGS^]:value": "sigFinding",
                        "OBX[typeId=^TIME ZONE^VA4.4]:value": "tz"
                    },              
                    
                    "expected123Activity": {
                        "I": "COMPLETE/UPDATE",
                        "O": "COMPLETE/UPDATE" # TODO: double check - just guessed
                    }
                }
            
    ]
            
    hl7TemplateMaker = HL7TemplateMaker(deidentify)
    """
    # Want to see parse and format messages ALL the same (fix if missing/wrong)
    print(message)
    """
    psegments = hl7TemplateMaker.parseMessage(message) 
    """
    nmessage = hl7TemplateMaker.formatMessage(psegments)
    print(nmessage)
    if nmessage != message:
        raise Exception("Messages don't match")
    """
    segmentsByType = defaultdict(list)
    for segment in psegments:
        segmentsByType[segment["segmentType"]].append(segment)
    
    def matchOrExtract(segmentsByType, mtchType, mtchVal=""):
        mtchSegType = mtchType.split("[")[0]
        if mtchSegType not in segmentsByType:
            return ""
        segs = segmentsByType[mtchSegType]
        indxMtch = re.match(r'[A-Z]+\[([^\]\=]+)\]', mtchType)
        prop = mtchType.split(":")[1]
        if indxMtch:
            # -1 or 0->
            mtchSegIndx = int(indxMtch.group(1))
            if (mtchSegIndx < 0 and len(segs) < abs(mtchSegIndx)) or (mtchSegIndx > 0 and len(segs) < mtchSegIndx + 1):
                return ""
            seg = segs[mtchSegIndx]
            if prop not in seg:
                return ""
            if mtchVal and seg[prop] != mtchVal:
                return ""
            return seg[prop]
        if mtchVal:
            raise Exception("Can't have mtchVal setting for non indexed segs")
        assertionMtch = re.match(r'[A-Z]+\[([^\=\+]+)([\=\+]+)([^\]]+)\]', mtchType)
        if not assertionMtch:
            raise Exception("Neither int nor assertion in match clauses")
        aprop = assertionMtch.group(1)
        atype = assertionMtch.group(2)
        apropValue = assertionMtch.group(3)
        propVals = []
        for seg in segs:
            if aprop not in seg:
                continue
            # ex/ valType!="TX" 
            if apropValue != seg[aprop]:
                continue
            if prop not in seg:
                continue
            propVals.append(seg[prop])
        if atype == "=":
            if len(propVals) > 1:
                raise Exception("Didn't expect > 1 prop val extract")
            return "" if len(propVals) == 0 else propVals[0]
        return propVals if len(propVals) else None
    def matchMessageCategory(segmentsByType, messageCategory):
        mtchCount = 0
        for mtchType, mtchValue in messageCategory["matches"].items():
            if matchOrExtract(segmentsByType, mtchType, mtchValue) != "":
                mtchCount += 1
        if mtchCount == len(messageCategory["matches"]):
            return True
        return False    
    def extractFromMessageCategory(segmentsByType, extractDefns, extracts={}):
        for extractType in extractDefns:
            val = matchOrExtract(segmentsByType, extractType)
            if val: # non zero array or a value
                extracts[extractDefns[extractType]] = val # can be an array
        return extracts
    mtchs = []
    for messageCategory in MSG_CATEGORIES:
        if matchMessageCategory(segmentsByType, messageCategory):
            mtchs.append(messageCategory)
    if len(mtchs) > 1:
        print(json.dumps(mtchs, indent=4))
        raise Exception("MessageCategories imprecise")
    if len(mtchs) == 0:            
        print(json.dumps(message, indent=4))
        raise Exception("No match for this message")
    messageCategory = mtchs[0]
    # one COMPL COMMENT type O
    if "expected123Activity" in messageCategory: # 531 has new
        if transmissionType not in messageCategory["expected123Activity"]:
            print(json.dumps(psegments, indent=4))
            print(messageCategory)
            raise Exception(f'Matched messageCategory {messageCategory["name"]} does not account for transmission type {transmissionType}') 
        # TODO: Should be "" if ACK ERROR BUT NOT DOING ERRORS yet => suppress above
        expected123Activity = "{}:{}".format(messageCategory["expected123Activity"][transmissionType], "F" if transmissionType == "I" else "P")
    else:   
        expected123Activity = ""
        
    extracts = extractFromMessageCategory(segmentsByType, GENERIC_EXTRACTS)
    extracts = extractFromMessageCategory(segmentsByType, messageCategory["extracts"],  extracts)
        
    # P for O; F for I ie/ Filler
    messageCategoryNameT = f'{messageCategory["name"]}:{"P" if transmissionType == "O" else "F"}'

    return messageCategoryNameT, expected123Activity, extracts

# ############################## HL7 Template Maker ##############

"""
Parse and format message SEGMENTs including support for de-identification

Note: only QA'ed support for three message types needed for IFCs. Will expand QA (parsed-formatted == original etc) if expand use.

TODO (beyond beyond IFC):
- parse the APP ACK for error code ie/ don't leave to raw data entry
        replace: entry["errorCode"] = _773Entry["error_message"]

1. ACK: https://hl7-definition.caristix.com/v2/HL7v2.3/TriggerEvents/ACK

2. ORM^O01: https://hl7-definition.caristix.com/v2/HL7v2.3/TriggerEvents/ORM_O01
        > initiate the transmission of information about an order ... placing new orders, cancellation of existing orders, discontinuation, holding ... originate also with a placer, filler, or an interested third party. The trigger event for this message is any change to an order
... hence used for first placement, VIOLA/Grab, Partial and fully completed incoming as well as trailing outgoing messages that tell the filler about the placers final notes.
... TODO: ??? on final ... why the S and F?
    
3. ORR^O02: https://hl7-definition.caristix.com/v2/HL7v2.3/TriggerEvents/ORR_O02
        > The function of this message is to respond to an ORM message. An ORR message is the application acknowledgment to an ORM message.
    ... only used once.
    
Note that only ORM^O01 has a second part to its name in MSH: MESSAGE TYPE^TRIGGER EVENT
    ORM^O01^ORM_O01
Just makes naming and formatting awkward.
"""
class HL7TemplateMaker:

    def __init__(self, deidentifyFormat=False):
        self.__deidentifyFormat = deidentifyFormat
    
        self.__parsers = {
            "MSH": self.parseMSH,
            "MSA": self.parseMSA,
            
            "ORC": self.parseORC,
            "PID": self.parsePID,
            "OBR": self.parseOBR,
            "OBX": self.parseOBX,
            "NTE": self.parseNTE,
            
            "SPR": self.parseSPR,
            "RDF": self.parseRDF,
            "QAK": self.parseQAK,
            "RDT": self.parseRDT
        }
        
        self.__formatters = {
            "MSH": self.formatMSH,
            "MSA": self.formatMSA,
            
            "ORC": self.formatORC,
            "PID": self.formatPID,
            "OBR": self.formatOBR,
            "OBX": self.formatOBX,
            "NTE": self.formatNTE,
            
            "SPR": self.formatSPR,
            "RDF": self.formatRDF,
            "QAK": self.formatQAK,
            "RDT": self.formatRDT
        }
        
        self.__separators = [] # only parseMessage sets it
        
    def parseMessage(self, msgSegments):
        results = []
        msgSegments = [mseg for mseg in msgSegments if not re.match(r' *$', mseg)]
        if not re.match(r'MSH', msgSegments[0]): # TBD BHS!
            print(msgSegments[0])
            raise Exception("Expect first segment starts with MSH")
        sepValues = msgSegments[0].split(msgSegments[0][3])[1]
        self.__separators = [msgSegments[0][3]] # | or ^ or ...
        for sepValue in sepValues:
            self.__separators.append(sepValue)
        for msgSegment in msgSegments:
            segName = msgSegment.split(self.__separators[0])[0]
            if segName in self.__parsers:
                results.append(self.__parsers[segName](msgSegment))
            else:
                print(json.dumps(msgSegments, indent=4))
                raise Exception(f"No handle for {segName} segment - skipping") 
        return results
        
    """
    Goal: ability to pass 1 info with args to sprinkle through series of 
    segments of a message (would need to know how to format messages as a whole.
    """
    def formatMessage(self, infos):
        fsegs = []
        for info in infos:
            segmentType = info["segmentType"]
            if segmentType in self.__formatters:
                fsegs.append(self.__formatters[segmentType](info))
            else:
                raise Exception(f"No handle for {segmentType}")
        return "\n".join(fsegs)
                           
    """
    https://hl7-definition.caristix.com/v2/HL7v2.3/Segments/MSH
    
    MSH|^~\\&|GMRC IF (CONSULT|TEST)|{sendingFacility}|GMRC IF (CONSULT|TEST)|{receiving facility}|{dateTimeMessage}||{messageType ex/ ORR^O02}||{message id - 773 of sender}|P|2.3|||{ack}|{appAck}|{ex USA}
    
    where all after 2.3 are not sent if message is an ACK
    
    TODO: see AL|NE on incoming from PUGET. Am I missing ACKs for the message
    conversation?
    """
    def parseMSH(self, segment):
    
        if not re.match(r'MSH', segment):
            return None
            
        self.__separators = [] # always reset
        extr, segmentPieces = self.__parseSegment(segment)
        
        if len(segmentPieces) < 10:
            raise Exception(f"MSH Segment {segment} doesn't have expected number of pieces - {len(segmentPieces)} < 10")

        if segmentPieces[2]:            
            extr["sendingApplication"] = segmentPieces[2]
        if segmentPieces[3]:
            extr["sendingFacility"] = segmentPieces[3]
        if segmentPieces[4]:
            extr["receivingApplication"] = segmentPieces[4]
        if segmentPieces[5]:
            extr["receivingFacility"] = segmentPieces[5] 
        
        # GMRC IF CONSULT or GMRC IF TEST - removing as doing more general
        """
        if not (re.match(r'GMRC IF (CONSULT|TEST)', extr["sendingApplication"]) and re.match(r'GMRC IF (CONSULT|TEST)', extr["receivingApplication"])):
            raise Exception("Unexpected MSH sending and/or receiving application")
        """
        
        extr["dateTimeMessage"] = segmentPieces[6]
        
        # Blank normally but seems to be CRNR in CRNR/VDIF?
        if segmentPieces[7]:
            extr["security"] = segmentPieces[7]
        
        # Can be two part with type and trigger 
        if re.search(r'_', segmentPieces[8]):
            p8s = segmentPieces[8].split(self.__separators[1])
            extr["messageType"] = f'{p8s[0]}{self.__separators[1]}{p8s[1]}'
            extr["triggerEvent"] = f'{p8s[2]}'
        else:
            extr["messageType"] = segmentPieces[8] 
        
        extr["messageCtrlId"] = segmentPieces[9] # SNO{IEN 773}
        
        if len(segmentPieces) >= 11 and segmentPieces[10]:  
            extr["processingId"] = segmentPieces[10] # seems to be always P
        if len(segmentPieces) >= 12 and segmentPieces[11]:
            extr["versionId"] = segmentPieces[11] # seems to be 2.3 or 2.3.1
        
        # AL (always), ER, NE (never), SU
        # ... ex of AL|NE (app ack itself has this) and AL|AL (all other except ACK)
        # ... Note: ACK message back from Puget doesn't have these (don't ack ack!)
        # <------ TODO: missing ACKs etc sent out to Puget?
        if len(segmentPieces) >= 15 and segmentPieces[14]:
            extr["acceptAcknowledgementType"] = segmentPieces[14]
        if len(segmentPieces) >= 16 and segmentPieces[15]:
            extr["applicationAcknowledgementType"] = segmentPieces[15]
         
        # ACK ends in P|2.3
        # AA ends in P|2.3|||AL|NE|USA   
        # ex/ USA
        # <--------------- set on incoming from PUGET
        if len(segmentPieces) >= 17:
            extr["countryCode"] = segmentPieces[16] # USA
        
        return extr
        
    """
    info:
    - sendingFacilityCaret: 663^PUGET-SOUND.MED.VA.GOV (ie/ domain name)
    - receivingFacilityCaret
    - requestDateTimeGMT
    - messageTypeCaret (could be just ACK | ORR^O02 | ORM^O01^ORM_001 ie/ secondary or not)
    - messageCtrlId
    ---
    - acceptAcknowledgementType
    - applicationAcknowledgementType
    
    TODO: redo to take separator | or ^
    
    ie/ MSH^~|\& (ie/ ^ is sep) or MSH|^~\& (ie/ | is sep)
    """
    def formatMSH(self, info):    
        messageType = info["messageType"]
        # Only ORM^O01 has this - ORM^O01^ORM_O01
        if "triggerEvent" in info: # goes with message type
            messageType = f'{messageType}^{info["triggerEvent"]}'
        seps = "~|\&" if self.__separators[0] == "^" else "^~\&"
        msh = f'MSH{self.__separators[0]}{seps}{self.__separators[0]}{info.get("sendingApplication", "")}{self.__separators[0]}{info.get("sendingFacility", "")}{self.__separators[0]}{info.get("receivingApplication", "")}{self.__separators[0]}{info.get("receivingFacility", "")}{self.__separators[0]}{info["dateTimeMessage"]}{self.__separators[0]}{self.__separators[0]}{messageType}{self.__separators[0]}{self.__separators[0]}{info["messageCtrlId"]}{self.__separators[0]}{info["processingId"]}{self.__separators[0]}{info["versionId"]}{self.__separators[0]}{self.__separators[0]}{self.__separators[0]}{info.get("acceptAcknowledgementType", "")}{self.__separators[0]}{info.get("applicationAcknowledgementType", "")}{self.__separators[0]}{info.get("countryCode", "")}'
        return re.sub(r'\|+$', '', msh)
        
    """
    Alternative start to MSH: https://hl7-definition.caristix.com/v2/HL7v2.7/Segments/BHS
    """
    def parseBHS(self, segment):
        if not re.match(r'BHS', segment):
            return None
            
        self.__separators = [] # always reset
        extr, segmentPieces = self.__parseSegment(segment)
        
        if len(segmentPieces) > 14:
            raise Exception("Expected BSH to have at most 14 pieces")
                    
        extr["sendingApplication"] = segmentPieces[2]
        if segmentPieces[3]:
            extr["sendingFacility"] = segmentPieces[3]
        extr["receivingApplication"] = segmentPieces[4]
        if segmentPieces[5]:
            extr["receivingFacility"] = segmentPieces[5] 
        
        extr["creationDateTime"] = segmentPieces[6]
        
        if segmentPieces[7]:
            extr["security"] = segmentPieces[7]
        
        if segmentPieces[8]:
            extr["nameIdType"] = segmentPieces[8]
        
        if segmentPieces[9]:
            extr["comment"] = segmentPieces[9]
        
        if segmentPieces[10]:
            extr["ctrlId"] = segmentPieces[10] 
            
        if len(segmentPieces) >= 12 and segmentPieces[11]:
            extr["referenceCtrlId"] = segmentPieces[11]
            
        if len(segmentPieces) >= 13 and segmentPieces[12]:
            extr["sendingNetworkAddress"] = segmentPieces[12]
            
        if len(segmentPieces) == 14 and segmentPiecers[13]:
            extr["receivingNetworkAddress"] = segmentPieces[13]
            
        return extr
        
    """
    MSA - Message acknowledgement segment
    
        # https://hl7-definition.caristix.com/v2/HL7v2.3/Tables/0008 
        # https://hl7-definition.caristix.com/v2/HL7v2.3/Segments/MSA
        #
        # Key is second MSA
        #               "MSA|CA|{773 IEN for original}"
        # OR if ERROR
        #               "MSA|AR|{773 IEN for original}|201 (ie error code)
        
    SUCCESS: MSA|{ACKCODE ends in A}|{_773IEN} 
    ERROR: MSA|{ACKCODE ends E or R}|{_773IEN}|{ERRORCODE}
    """
    def parseMSA(self, segment):
            
        if not re.match(r'MSA', segment):
            return None
    
        extr, segmentPieces = self.__parseSegment(segment)
        
        extr["ackCode"] = segmentPieces[1]
        extr["msgCtrlIdLocal"] = segmentPieces[2] # 773 IEN of original
        if len(segmentPieces) == 4:
            extr["text"] = segmentPieces[3] # Error code or extra Ack info
        if len(segmentPieces) > 4:
            for i in range(4, len(segmentPieces)):
                extr[f'extra{i}'] = segmentPieces[i] # unexpected but keep
        
        return extr
        
    def formatMSA(self, info):
        return self.__formatSegmentCrude(info)
      
    """
    https://hl7-definition.caristix.com/v2/HL7v2.3/Segments/ORC
    
    https://hl7-definition.caristix.com/v2/HL7v2.3/Tables/0119
    
    > The Common Order segment (ORC) is used to transmit fields that are common to all orders (all types of services that are requested). The ORC segment is required in the Order (ORM) message. ORC is mandatory in Order Acknowledgment (ORR) messages if an order detail segment is present, but is not required otherwise.
    
    ORC|{orderControl}|{placerOrderNumber}|{fillerOrderNumber}||{orderStatus}...
    
    See details on quantity timing below
    """  
    def parseORC(self, segment): # ends in IP|....|{REMOTE SNO}
                
        if not re.match(r'ORC', segment):
            return None
    
        extr, segmentPieces = self.__parseSegment(segment)
        
        # NW->OK->SC->RE+
        # NW [first msg] == new order
        # OK [app ack] ==order accepted and ok (in ORR)
        # SC [viola] == status changed 
        # RE == observations to follow (all after Viola I or O)
        # OD == order discontinued (NTEs used for comments)
        # XX ==order changed or unsolicited    
        extr["orderControl"] = segmentPieces[1] 
        
        extr["placerOrderNumber"] = segmentPieces[2] # conIEN^SNO^GMRCIFR
        if segmentPieces[3]:
            extr["fillerOrderNumber"] = segmentPieces[3] # conIEN^SNO^GMRCIFC
        # there's a | skipped but not in standard descr
        # CM - completed (which can be TIU or just a comment if OBX is comment)
        # IP - in process ... comments or just RECEIVE or FORWARDED
        # A - Some, but not all, results available (used with OBX, TIU S)
        if segmentPieces[5]: # seems to go with fillerOrderNumber
            extr["orderStatus"] = segmentPieces[5] 
        # Quantity/timing (ORC-7, OBR-27) provides a means of specifying when the service 
        # described by the order segment is to be performed and how frequently.
        # ... https://hl7-definition.caristix.com/v2/HL7v2.3/DataTypes/TQ
        # ex/ of DAY DATE and indicator of priority ex/ ^^^20200323^^R
        # ... saw for must be attended to by end of next day? Time for patient reg?
        if segmentPieces[7]:
            extr["quantityTiming"] = segmentPieces[7]
        if segmentPieces[9]:
            extr["dateTimeTransaction"] = segmentPieces[9]
        if segmentPieces[10]: # see HOLLAND,KELLY vs the provider!
            extr["enteredBy"] = segmentPieces[10]
        if segmentPieces[11]:
            extr["verifiedBy"] = segmentPieces[11]
        if segmentPieces[12]:
            extr["orderingProvider"] = segmentPieces[12]
        if segmentPieces[14]: # VIOLA has # (and she enters and orders)
            extr["callBackPhoneNumber"] = segmentPieces[14]
        if segmentPieces[15]:
            extr["orderEffectiveDateTime"] = segmentPieces[15]
        # R^RECEIVE^99GMRC
        # F^FORWARD^99GMRC -- TODO: only XX?
        # FI^FOWARD TO IFC ...
        # "determines function of ORC segment"
        if segmentPieces[16]:
            extr["orderControlCodeReason"] = segmentPieces[16]
        # Just SNO or SNO^NAME
        extr["enteringOrganization"] = segmentPieces[-1]
        
        return extr
        
    def formatORC(self, info):
        info = self.__deidentify(info, ["enteredBy", "verifiedBy", "orderingProvider", "callBackPhoneNumber"])
        orc = f'ORC|{info["orderControl"]}|{info["placerOrderNumber"]}|{info.get("fillerOrderNumber", "")}||{info.get("orderStatus", "")}||{info.get("quantityTiming", "")}||{info.get("dateTimeTransaction", "")}|{info.get("enteredBy", "")}|{info.get("verifiedBy", "")}|{info.get("orderingProvider", "")}||{info.get("callBackPhoneNumber", "")}|{info.get("orderEffectiveDateTime", "")}|{info.get("orderControlCodeReason", "")}|{info.get("enteringOrganization", "")}'
        return re.sub(r'\|+$', '', orc)
        
    """
    https://hl7-definition.caristix.com/v2/HL7v2.3/Segments/PID
    
    PID|1|{icn}|{altid}|{ssnLast4}|{nameCaret}||{dob}|{sex}|...|{ssn}
    
    altid == {IEN in file 2}^{\d}^M10 where \d is 0 or 2 or 5 ???
    
    NOTE: in ICD 
    
    The OBR16 field will be shifted so that LASTNAME^FIRST^MIDDLE will become 
    NPI^LASTNAME^FIRST^MIDDLE, and the FIN# will be added to PID18. The EDIPI will be 
    retrieved from the VDIF registry and added to PID3.
    
    > PID|1||123^^^ICN^VETID~456^^^EDIPI^EDIPI||TEST^PATIENT^ONE||19730320|M |||||||||||1234567|123451234
    """
    def parsePID(self, segment):
    
        if not re.match(r'PID', segment):
            return None
    
        extr, segmentPieces = self.__parseSegment(segment)
        
        extr["setId"] = segmentPieces[1]
        extr["patientIdExternal"] = segmentPieces[2] # ICN
        extr["patientIdInternal"] = segmentPieces[3] # X^(5|6)^M10 <--- why X differs for same patient TODO
        extr["alternatePatientId"] = segmentPieces[4] # last 4 SSN
        extr["name"] = segmentPieces[5] # caret name
        extr["dateOrBirth"] = segmentPieces[7]
        extr["sex"] = segmentPieces[8]
        extr["ssn"] = segmentPieces[19]
                
        return extr
        
    def formatPID(self, info):
        info = self.__deidentify(info, ["patientIdExternal", "patientIdInternal", "alternatePatientId", "name", "dateOrBirth", "ssn"])
        pid = f'PID|{info["setId"]}|{info["patientIdExternal"]}|{info["patientIdInternal"]}|{info["alternatePatientId"]}|{info["name"]}||{info["dateOrBirth"]}|{info["sex"]}|||||||||||{info["ssn"]}'
        return pid
                    
    """
    OBR - Observation request segment
    
    https://hl7-definition.caristix.com/v2/HL7v2.3/Segments/OBR
    
    Note: 1235 = Service ... 1233 = Procedure (ie/ FM codes)
    OBR|{setId}|{localConsultRef}^GMRCIFR||{toServiceRef}^{vistASNO}VA1235||{requestDateTime}|...|{orderingProviderName}||O
    
    universal service identifier:
        IEN of consult type^Consult Type Name^687VISTA1235
    where 1235 == 123_5 request services, the 'consult type' file
    ... more VistA scoped service identifier for placer service.
    ... matches "to_service" of Consult 123
    
    Map to 123:
    - placerOrderNumber: local consult ien
    - universalServiceIdentifier: "to_service" (with diff name)
    - orderingProvider: "sending_provider"
    and
    - requestDateTime: matches that of MSH etc (ie/ of dispatch) and of time on first audit trail entry and "date_of_request"
    
    Only see in first message sent out.
    """
    def parseOBR(self, segment):
    
        if not re.match(r'OBR', segment):
            return None
    
        extr, segmentPieces = self.__parseSegment(segment)
        
        extr["setId"] = segmentPieces[1] 
        
        # IEN of consult^SNO^GMRCIFR
        extr["__placerOrderNumber"] = segmentPieces[2] 
        # we saw a TST1234 in 653
        fieldMatch = re.match(r'([A-Z\d]+)\^(\d+)\^GMRCIFR', extr["__placerOrderNumber"])
        if not fieldMatch:
            raise Exception(f"OBR: unexpected form for placer order number {extr['__placerOrderNumber']} - not A-Z\d+^\d+^GMRCIFC")
        extr["placerConsultIEN"] = fieldMatch.group(1)
        extr["placerVistASNO"] = fieldMatch.group(2)
        
        if segmentPieces[3]:
            extr["fillerOrderNumber"] = segmentPieces[3]
            
        # IEN of consult type^Consult Type Name^687VISTA123[35] (3 not 5 in one 663)
        # ... saw SR RHEUMATOLOGY 'OUTPT' in 663 (as Cerner?)
        extr["__universalServiceIdentifier"] = segmentPieces[4]
        fieldMatch = re.match(r"(\d+)\^([a-zA-Z\d\(\)\-\/\&\:' ]+)\^(\d+)VA(123[35])$", extr["__universalServiceIdentifier"])
        if not fieldMatch:
            pieces = extr["__universalServiceIdentifier"].split("^")
            # AMBULATORYREFRRALVA^Ambulatory Referral-VA
            if sum(1 for piece in pieces if not re.match(r'[a-zA-Z\- ]+$', piece)):
                raise Exception(f'** OBR: Expected only alpha pieces for Cerner based universalServiceIdentifier but {extr["__universalServiceIdentifier"]} in {segment}')                
            # AMBULATORYREFERRALVA | Report
            if len(pieces) > 2:
                raise Exception(f'** OBR: Expected at most two pieces for Cerner based universalServiceIdentifier but {extr["__universalServiceIdentifier"]} in {segment}')
            extr["toServiceLabel"] = pieces[0]
            if len(pieces) == 2:
                extr["toServiceLabel2"] = pieces[1]
        else:
            extr["toServiceIEN"] = fieldMatch.group(1)
            extr["toServiceLabel"] = fieldMatch.group(2)
            # should == placer SNO but for XX out sometimes is filler!
            extr["toServiceSNO"] = fieldMatch.group(3) 
            extr["toServiceVAQual"] = fieldMatch.group(3)
            
        if len(segmentPieces) > 6 and segmentPieces[6]:
            extr["requestedDateTime"] = segmentPieces[6]
        
        if len(segmentPieces) >= 17 and segmentPieces[16]:
            extr["orderingProvider"] = segmentPieces[16]
            
        if len(segmentPieces) >= 18 and segmentPieces[17]:
            extr["orderCallbackPhoneNumber"] = segmentPieces[17]
            
        if len(segmentPieces) >= 19 and segmentPieces[18]:
            extr["placerField1"] = segmentPieces[18] # O ... is this I vs O???
        
        return extr
        
    """
    setId
    
    Info:
        placerVistASNO
        placerConsultIEN
        toServiceIEN | toServiceLabel 
        toServiceLabel | toServiceLabel2
        requestedDateTime (GMT)
        orderingProvider
        
    TODO: tighten up format as seems to miss possible stuff in above
    """
    def formatOBR(self, info):
        info = self.__deidentify(info, ["orderingProvider"])
        # Seen in 663 during SPO's HL7 Router + vdif transition. 
        #   __universalServiceIdentifier wasn't parseable
        if "toServiceIEN" in info:
            obr = f'OBR|{info["setId"]}|{info["placerConsultIEN"]}^{info["placerVistASNO"]}^GMRCIFC||{info["toServiceIEN"]}^{info["toServiceLabel"]}^{info["toServiceSNO"]}VA{info["toServiceVAQual"]}||{info.get("requestedDateTime", "")}||||||||||{info.get("orderingProvider", "")}||O'
        else:
            obr = f'OBR|{info["setId"]}|{info["placerConsultIEN"]}^{info["placerVistASNO"]}^GMRCIFC||{info["toServiceLabel"]}{"^" + info["toServiceLabel2"] if "toServiceLabel2" in info else ""}||{info.get("requestedDateTime", "")}||||||||||{info.get("orderingProvider", "")}||O'
        return obr
                
    """
    https://hl7-definition.caristix.com/v2/HL7v2.3/Segments/OBX
    
    Key is value type (https://hl7-definition.caristix.com/v2/HL7v2.3/Tables/0125): 
        TX (text data display), CE (coded entry), RP (reference pointer)
        
    Note that setId probably doesn't matter per se. It just groups segments so 
    as long as you don't group independent items and do group related items, all 
    should be ok
    """
    def parseOBX(self, segment):
        
        if not re.match(r'OBX', segment):
            return None
    
        extr, segmentPieces = self.__parseSegment(segment)
            
        """
        OBX|{setId}|TX|2000.02^REASON FOR REQUEST^AS4|{#}|...|O
                or
        OBX|{setId}|TX|^COMMENTS^|{#}|{SC or other comment value}|...|P
        
        O not in table
        P == preliminary results
        
        ... for text, setId seems to be fixed at 1 (ie/ the set id?)
        
        BIG QUESTION TO ANS: copies of text in VistAs. Does the consult
        contain the TIU note's data? Does the remote consult alone have
        that data.
        
        BIG QUESTION FOR FLOW: does HL7 send back the text of the remote
        TIU note made or not?
        """
        if segmentPieces[2] == "TX":
            extr["setId"] = segmentPieces[1] 
            extr["valueType"] = "TX"
            extr["typeId"] = segmentPieces[3]
            extr["typeSubId"] = segmentPieces[4] # line number for sub id
            extr["value"] = segmentPieces[5] # is text
            if len(segmentPieces) >= 12:
                extr["status"] = segmentPieces[11] # O or P, F or S
            if len(segmentPieces) >= 15:
                extr["observationDate"] = segmentPieces[14]
            return extr
            
        """
        For coded values like timezone, 
        
        OBX|{setId}|CE|^TIME ZONE^VA4.4|1|{TIMEZONE ex PDT}
            or
        OBX|{setId}|CE|^PROVISIONAL DIAGNOSIS^|1|{I10 Values}|...|O|||{obsDate}
        """
        if segmentPieces[2] == "CE": # coded entry value type
            extr["setId"] = segmentPieces[1] # set id
            extr["valueType"] = "CE"
            extr["typeId"] = segmentPieces[3] # TIME ZONE or ...
            extr["typeSubId"] = segmentPieces[4]
            extr["value"] = segmentPieces[5] # observation value
            if len(segmentPieces) >= 12:
                extr["status"] = segmentPieces[11]
            if len(segmentPieces) >= 15:
                extr["observationDate"] = segmentPieces[14] # don't see time
            return extr        

        """
        TIU ref (ie/ reference pointer)   
               documentId: {VISTASNO}-{DOCIEN}   
        
        OBX|{setId}|RP|^TIU DOC^VA8925|1|{DOCIEN}^TIU DOCUMENT^{VISTASNO}||||||F
        
        S == partial
        F == final
        
        Note that VISTASNO (local or remote) depends on message direction. Outgoing
        will have local id.
        
        ... do we get partial document results ie/ not F?
        """    
        if segmentPieces[2] == "RP": # 'reference pointer' value type
        
            extr["setId"] = segmentPieces[1] # set id
            extr["valueType"] = "RP"
            
            extr["typeId"] = segmentPieces[3] # observation identifier
            if not re.search(r'VA8925', extr["typeId"]):
                raise Exception("OBX: only expecting TIU reference pointers")
                
            extr["typeSubId"] = segmentPieces[4] # observation sub id (always 1?)
            
            # {DOCIEN}^TIU DOCUMENT^{VISTASNO} -- leaving simple for now
            extr["value"] = segmentPieces[5] # observation value
            """
            extr["__value"] = segmentPieces[5] # observation value
            fieldMatch = re.match(r'(\d+)\^TIU DOCUMENT\^(\d+)$', extr["__value"])
            if not fieldMatch:
                raise Exception("OBX (RP): invalid value form")
            extr["docIEN"] = fieldMatch.group(1)
            extr["docVistASNO"] = fieldMatch.group(2)
            """
            
            if len(segmentPieces) >= 12:
                extr["status"] = segmentPieces[11]
                if extr["status"] not in ["S", "F", "D"]: # "D" seen in 692
                    raise Exception(f'Unexpected TIU OBX status: {extr["status"]}')
            
            if len(segmentPieces) >= 15:
                extr["observationDate"] = segmentPieces[14]
            
            return extr
            
        raise Exception(f"Unrecognized value type {segmentPieces[2]} for OBX")
        
    """
    setId
    
    info:
    - valueType of TX, CE or RP
    - typeId: 
    
    may break TX in two? ie/ for comment?
    """
    def formatOBX(self, info):
        if self.__deidentifyFormat:
            if info["valueType"] == "CE" or (info["valueType"] == "TX" and not re.match(r'[A-Z]+$', info["value"])):
                info = self.__deidentify(info, ["value"])
        obx =         f'OBX|{info["setId"]}|{info["valueType"]}|{info["typeId"]}|{info["typeSubId"]}|{info["value"]}||||||{info.get("status", "")}|||{info.get("observationDate", "")}'
        return re.sub(r'\|+$', '', obx)
        
    """
    NTE - Notes and comments segment
    
    https://hl7-definition.caristix.com/v2/HL7v2.3/Segments/NTE
    
    > common format for sending notes and comments
    
    This one - on its own - misses the setId and first column is for "source of comment".
    When this is the form, source is P for Placer ...
    
        NTE|P|UCID:{VISTASNO}_{ConsultIEN}
        
    But normal form is
    
        NTE|{setId}|{source of comment}|{comment}
    
    Note: very "flexible" use of standard to put a coded value in 'comment'
    """
    def parseNTE(self, segment):
    
        if not re.match(r'NTE', segment):
            return None
    
        extr, segmentPieces = self.__parseSegment(segment)
    
        if segmentPieces[1] == "P": # setId 
            if len(segmentPieces) != 3:
                raise Exception("Expect setId-less NTEs to = 3 segments")
            extr["sourceOfComment"] = segmentPieces[1] # L, O, P but expect P for placer
            extr["__comment"] = segmentPieces[2] # form UCID:{SNO}_{local consult ien}
            ucidCommentMatch = re.match(r'UCID:(\d+)_(\d+)$', extr["__comment"])
            if not ucidCommentMatch:
                raise Exception("Expect P NTE to have UCID form")
            extr["placerVistASNO"] = ucidCommentMatch.group(1)
            extr["placerConsultIEN"] = ucidCommentMatch.group(2)
            return extr

        if len(segmentPieces) != 4:
            raise Exception("Expect w/setId NTEs to = 3 segments")
        # See with ORC "OD"
        extr["setId"] = segmentPieces[1]
        extr["sourceOfComment"] = segmentPieces[2] 
        extr["comment"] = segmentPieces[3]
        return extr
        
    """
    Info: two forms
    
    P/no SetId
        sourceOfComment - always P
        placerVistASNO - from comment
        placerConsultIEN - from comment
        __comment - full comment (parsed out but no in composed infos)
    """
    def formatNTE(self, info):
        if "setId" in info:
            if self.__deidentifyFormat:
                info = self.__deidentify(info, ["comment"])
            nte = f'NTE|{info["setId"]}|{info["sourceOfComment"]}|{info["comment"]}'
        else:
            nte = f'NTE|{info["sourceOfComment"]}|UCID:{info["placerVistASNO"]}_{info["placerConsultIEN"]}'
        return nte
        
    # ################## SPQ Q08/ TBR R08 Specific #############
    
    """
    Query with SPQ, response with TBR (correlate with MSA)
    
    ... stored procedure request
    
    https://hl7-definition.caristix.com/v2/HL7v2.3.1/TriggerEvents/SPQ_Q08
    
    > The SPQ enables an application on one system to execute a stored procedure on
    > another system, which is coded to extract specific data. Since the SPR segment 
    > includes a response format code, the response could be tabular, display or 
    > segment pattern.
    
    MSH SPR [RDF] [DSC]. Seems like VistA Version is MSH SPR RDF
    
    https://hl7-definition.caristix.com/v2/HL7v2.3.1/TriggerEvents/TBR_R08    
    
    > Tabular Data Response
    
    which has an MSA but also an RDT that is 'column value' and can have any form.
    
    MSH MSA [ERR] QAK RDF RDT [DSC]. Seems like VistA doesn't have DSC?
    
    Unlike ORR ..., no HL7 ACK and APP ACK is the TBR
    """
    
    """
    SPR
    
    >  The SPR segment is used to issue queries using stored procedure calls
    
    https://hl7-definition.caristix.com/v2/HL7v2.5/Segments/SPR
    
    See parseInputParameterList for XWBESSO, RPC and P1 arguments
    inside here. In webReportIFCHL7
    """
    def parseSPR(self, segment):        
                        
        extr, segmentPieces = self.__parseSegment(segment)
        
        if len(segmentPieces) != 5:
            raise Exception("Expect SPR to have 4 pieces")

        # SPR.1 Query Tag ex/ SQBDRPC1928-551111_0
        extr["queryTag"] = segmentPieces[1]

        # SPR.2 Query/Response Format Code (D, R (record oriented), T (tabular)) 
        # ... always T?
        extr["queryResponseFormatCode"] = segmentPieces[2] 

        # SPR.3 Stored Procedure Name ... always ZREMOTE RPC?
        extr["storedProcedureName"] = segmentPieces[3]
        
        # SPR.4 Input Parameter List - \f, \n ...
        # format is QIP.1 QIP.2 with QIP.1 as field name of length 12 and 
        # QIP.2 as 'values' of max length 199
        # ...
        # KEY: seems to embed an XWBESSO in 
        #   \\F007XWBESSO069344583335 ie/ 7 char + #
        extr["inputParameterList"] = segmentPieces[4]
                
        """    
        ParameterList:
    
            XWB props, RPC (name) and P1 == TIU IEN
    
        - XWBESSO args sets sign on Log (it and name of RPC are main args) 
            "check that user can access remote system with ESSO" 
        - XWBESSO has the local user info used for a login. Will lead to new
    user creation if user is missing?
            (SLOG^XUS1)
            - Props of user for sign in
            FROM PUT^XUESSO1
            S SSN=$P(DATIN,U,1),NAME=$P(DATIN,U,2),SITE=$P(DATIN,U,3)
            S SITENUM=$P(DATIN,U,4),RMTDUZ=$P(DATIN,U,5),PHONE=$P(DATIN,U,6)
            S SECID=$P(DATIN,U,7) ;p655
            S NETWORK=$P(DATIN,U,8) ;p655
            - 1. SSN
            - 2. NAME
            - 3. SITE (ex/ J... M. WAINWRIGHT VAMC if from WWW)
            - 4. STATION NO (ex/ 687 if from WWW)
            - 5. IEN in 200 user file of sender 
            - 6. ? (a five digit #, code says phone!) ex/ 26320 
            - 7. "" blank
            - 8. n/w name ie VHA...
        - TODO: 
            - see if cnt == 12 indicates these HL7 users. (see 663 User)
            - what is DUZ("LOA") set to for HL7? [From 3.081 of real user going to 663, seems to be LOA 1 w/o MDWS?]
        - Expect a P\d argument == IEN of TIU (and XWBPCNT=1 for
    one argument) for TIU RPC but others can have > 1 P
        - Complication of P1(\d) form ie/ 5 length 
    
        P Encoding of \d{3}{VAL}\\F\\{VAL}\\F ... but no \\F or \\ at start or end
        """
        def parseInputParameterList(ipl):
            ipl = re.sub(r'\n', '', ipl) # TMP: need to revisit - see em and don't appear in sizings ... could eat up as go (even see tail of rvalue etc) but more complex
            if not re.match(r'\@SPR.4.2\~', ipl):
                raise Exception("INP doesn't start with SPR ... as expected")
            ipl = ipl[len("@SPR.4.2~"):]
            iplAsserts = ipl.split("&")
            parsedAsserts = {}
            for i, iplAssert in enumerate(iplAsserts, 1):
                lvalueLen = int(re.match(r'(\d{3})', iplAssert).group(1)) # always 3 long
                lvalue = iplAssert[3:lvalueLen+3]
                lenPlusRValue = iplAssert[lvalueLen+3:]
                # Len problem if \\F \\ splits as \\F\\ counts as 1
                rvalue = lenPlusRValue[3:] # can ignore len 2 as know 3 long
                rvalueLen = int(re.match(r'(\d{3})', lenPlusRValue).group(1))
                parsedAsserts[lvalue] = rvalue
                # Works for XWBESSO and any P's with embedded \\F's
                # Comment of: "change ^ < to \F\" ie/ to allow HL7 transport!
                # ... then change back. Form is ARGVALUE\\F\\ARGVALUE2\\F
                #       ARGVALUE1\\F\\ARGVALUE2\\F\\ARGVALUE3
                # ... ie/ first has no \\ to start and last has no \\F to end
                if re.search(r'\\F\\', rvalue):
                    # \\E \\ is for 2nd level splits ex/ extension in phone
                    crvalue = re.sub(r'\\E\\', '~', re.sub(r'\\F\\', '^', rvalue))
                    if len(crvalue) == rvalueLen: # len is for ^ uncompressed form
                        parsedAsserts[f"_{lvalue}UNC"] = crvalue.split("^")
                        if lvalue == "XWBESSO" and not re.match(r'\d{9}$', parsedAsserts["_XWBESSOUNC"][0]):
                            raise Exception("Didn't start with SSN - surprise!")
                        if re.match(r'P\d+\(', lvalue):
                            raise Exception("Don't expect to properly parse the - must go again - P{\d}(\d)")
                        continue
                    if lvalue == "XWBESSO":
                        raise Exception("Expected XWBESSO to be full size - ie/ no length embedded params")                        
                    # Marking bad parse as rvalue len 'wrong'. TODO, must go back
                    # on lvalue and redo whole pseg
                    # ... will see P1(1), P1(2) etc
                    parsedAsserts["_BADPPARSE"] = True
            return parsedAsserts
        
        extr["_inputParameterList"] = parseInputParameterList(segmentPieces[4])
        
        return extr
        
    """
    Most of the effort is going inside inp and into the \\F delimited user
    identification of XWBESSO
    """
    def formatSPR(self, info):
        inpVal = info["_inputParameterList"]
        xwbEssoInfo = inpVal["_XWBESSOUNC"] # only using inpVal itself for RPC id etc
        if self.__deidentifyFormat and xwbEssoInfo[0] not in ["888888888"]:
            if len(xwbEssoInfo[6]): # let's catch this and account for it later
                raise Exception(f"XWBESSO has argument 6 - {xwbEssoInfo}")
            if len(xwbEssoInfo) > 8:
                raise Exception("Expect at most 8 args in XWBESSO")
            xwbEssoInfo = [ 
                "111223333", # still de-id 88888888
                "JONES,BOB J" if xwbEssoInfo[0] not in ["888888888"] else xwbEssoInfo[1],
                xwbEssoInfo[2],
                xwbEssoInfo[3],
                "99999",
                "1115551212"[0:len(xwbEssoInfo[5])], # short no sometimes/ -'ed others!
                ""
            ]
            if len(xwbEssoInfo) == 8:
                xwbEssoInfo.append("VHAXXXJONESB") # may be missing all together
        xwbEsso = "\\\\F\\\\".join(xwbEssoInfo)
        allINPProps = set(["RPC", "RPCVER", "XWBPCNT", "XWBESSO", "XWBDVER", "XWBSEC"])
        inp = f'@SPR.4.2.~003RPC{len(inpVal["RPC"]):03}{inpVal["RPC"]}&006RPCVER{len(inpVal["RPCVER"]):03}{inpVal["RPCVER"]}&007XWBPCNT{len(inpVal["XWBPCNT"]):03}{inpVal["XWBPCNT"]}&007XWBESSO{len(xwbEsso):03}{xwbEsso}&007XWBDVER{len(inpVal["XWBDVER"]):03}{inpVal["XWBDVER"]}&006XWBSEC{len(inpVal["XWBSEC"]):03}{inpVal["XWBSEC"]}'
        spr = f"SPR{self.__separators[0]}{info['queryTag']}{self.__separators[0]}{info['queryResponseFormatCode']}{self.__separators[0]}{info['storedProcedureName']}{self.__separators[0]}{inp}"
        for pprop in inpVal: # add to inp
            # P\d+ or P\d+(\d+)
            if not re.match(r'P\d+(\(\d+\))?$', pprop):
                continue
            allINPProps.add(pprop)
            valde = inpVal[pprop]
            # TOO CRUDE but ...
            if self.__deidentifyFormat:
                valde = re.sub(r'[A-Z]', 'X', re.sub(r'[a-z]', 'z', re.sub(r'\d', '0', inpVal[pprop])))
            mup = f"&{len(inpVal[pprop]):03}{valde}"
            spr += mup
        inpValCoreProps = set([p for p in inpVal if not re.match(r'\_', p)])
        # Need to fix BADPPARSE as messes up format for examples too
        if allINPProps != inpValCoreProps: 
            print(f"** WARNING TO FIX: not all input props of SPR inputParameters were formatted out. Bad parse is {'_BADPPARSE' in inpVal} accounts for this? Missing is {';'.join(list(inpValCoreProps - allINPProps))}")
            """
            print("format", sorted(list(allINPProps)))
            print("input", sorted(list(inpVal)))
            print(json.dumps(inpVal, indent=4))
            raise Exception("Didn't format all SPR properties")
            """
        return spr
    
    """
    RDF (both SPQ and TBR messages)
    
    https://hl7-definition.caristix.com/v2/HL7v2.3.1/Segments/RDF
    
    > The RDF segment defines the content of the row data segments (RDT) in the tabular 
    > response (RTB).
    
    Always: ^1^@DSP.3~TXT~300 ?
    """    
    def parseRDF(self, segment):
    
        extr, segmentPieces = self.__parseSegment(segment)

        if len(segmentPieces) != 3:
            raise Exception("Expect RDF to have 3 pieces")

        extr["numberColsPerRow"] = segmentPieces[1] # always 1?
        extr["columnDescription"] = segmentPieces[2] # always DSP.3 etc?
        
        return extr
        
    def formatRDF(self, info):
        rdf = f"RDF{self.__separators[0]}{info['numberColsPerRow']}{self.__separators[0]}{info['columnDescription']}"
        return rdf
        
    """
    QAK (TBR messages)
    
    https://hl7-definition.caristix.com/v2/HL7v2.3.1/Segments/QAK
    
    ... "may appear as an optional segment placed after the (optional) ERR segment in any 
    query response (message) to any original mode query."
    """
    def parseQAK(self, segment):
    
        extr, segmentPieces = self.__parseSegment(segment)

        if len(segmentPieces) != 3:
            raise Exception("Expect QAK to have 3 pieces")

        # ? if MSA lines up message SPR to message TBR then is this just redundant, 
        # alignment wise?
        extr["queryTag"] = segmentPieces[1] # corresponds to SPR's query tag
        extr["queryResponseStatus"] = segmentPieces[2] # AE/AR/NF/OK
        
        return extr 
        
    def formatQAK(self, info):
        qak = f"QAK{self.__separators[0]}{info['queryTag']}{self.__separators[0]}{info['queryResponseStatus']}"
        return qak

    """
    RDT (TBR messages)
    
    https://hl7-definition.caristix.com/v2/HL7v2.3.1/Segments/RDT
    
    ... "may appear as an optional segment placed after the (optional) ERR segment in any 
    query response (message) to any original mode query."
    """        
    def parseRDT(self, segment):
        
        extr, segmentPieces = self.__parseSegment(segment)

        # Seems like a structured reply has at least 3 pieces
        # ie/ RDT^{PROP}^{VALUE}
        if len(segmentPieces) != 2:
            for i, segmentPiece in enumerate(segmentPieces[1:], 1):
                extr[f'columnValue{i}'] = segmentPiece
        else: 
            extr["columnValue"] = segmentPieces[1]
        return extr 
        
    """
    deidentify needs nuance. Ex for user return
        RDF^200;55.4^ 
    ie/ when there's a third element => structured => 
    keeping second element as a "property"
    """
    def formatRDT(self, info):
        columnValueProps = [p for p in info if re.match(r'columnValue', p)]
        if self.__deidentifyFormat: # and not (len(columnValueProps) == 2 and info[columnValueProps[0]] == "-1"): ... too dangerous as ICN etc can be in error!
            # deidentify all after first "property" column unless it has a space
            cvpsToDeId = columnValueProps[1:] if len(columnValueProps) > 1 and not re.search(r' ', info[columnValueProps[0]]) else columnValueProps
            dinfo = self.__deidentify(info, cvpsToDeId)
        else:
            dinfo = info
        rdt = "RDT"
        for cvp in columnValueProps:
            rdt += f"{self.__separators[0]}{dinfo[cvp]}"        
        return rdt
                        
    """
    Rough one
    """
    def __formatSegmentCrude(self, info):
        return "|".join([info[k] for k in info if not re.match(r'\_', k)])
        
    # Base
    def __parseSegment(self, segment): # sep can be ^ or |
    
        if len(self.__separators) == 0:
            self.__separators = []
            for i in range(3, 8): # allowing for 5
                if i == 3:
                    firstSep = segment[3]
                    self.__separators.append(firstSep)
                    continue
                if segment[i] == firstSep:
                    break
                self.__separators.append(segment[i]) 
        segmentPieces = re.sub(r'\n+$', '', segment).split(self.__separators[0])
        
        extr = {}
        extr["segmentType"] = segmentPieces[0]
        extr["_pieceCount"] = len(segmentPieces)
        extr["_pieceCountPop"] = sum(1 for p in segmentPieces if p != "") 
        extr["_raw"] = segment
        
        return extr, segmentPieces
        
    def __deidentify(self, info, propsToDeId=[]):
        if self.__deidentifyFormat:
            for p in info:
                if re.match(r'\_', p):
                    continue
                if p not in propsToDeId:
                    continue
                info[p] = re.sub(r'[a-z]', 'x', re.sub(r'[A-Z]', 'X', re.sub(r'\d', "0", info[p])))
        return info
        
"""
Utility to Fully Markup a De-identified Message

Note: to show properly in PDF, print style needs
    pre{white-space: pre-wrap};
"""
def muMessageACKAPPACK(messageInfo, deidentify=True): 
    hl7TemplateMaker = HL7TemplateMaker(deidentify)
    psegments = hl7TemplateMaker.parseMessage(messageInfo["message"]) 
    mh = f'{messageInfo["messageCategory"]}{":E" + messageInfo["errorCode"] if "errorCode" in messageInfo else ""}/{messageInfo["logicalLink"]}'
    mu = f'\n\n```text\n----- {mh} -----\n\n{hl7TemplateMaker.formatMessage(psegments)}\n\n' 
    if "acks" in messageInfo: 
        for i, ackMessageInfo in enumerate(messageInfo["acks"], 1):
            ackPSegments = hl7TemplateMaker.parseMessage(ackMessageInfo["message"])
            ackmu = f'----- {"ACK" if i == 1 else "APP ACK"}/{ackMessageInfo["logicalLink"]} -----\n\n{hl7TemplateMaker.formatMessage(ackPSegments)}\n\n'
            if "acks" in ackMessageInfo: # app acks have em
                appAckAckMessageInfo = ackMessageInfo["acks"][0] # only one
                ackAckPSegments = hl7TemplateMaker.parseMessage(appAckAckMessageInfo["message"])
                ackmu += f'----- ACK to ACK APP/{appAckAckMessageInfo["logicalLink"]} -----\n\n{hl7TemplateMaker.formatMessage(ackAckPSegments)}\n\n'
            mu += ackmu
    else: # TMP : will probably nix -- just want to see for QA for now
        mu += f'---------------\n\nNO ACKNOWLEDGEMENTS\n\n' 
    mu += f'```\n\n'
    # need messageType from message as event_type/message_type of 773 is
    # for last ACK!
    return mu
    
def muMessageAPPACK(messageInfo, deidentify=True):
    hl7TemplateMaker = HL7TemplateMaker(deidentify)
    psegments = hl7TemplateMaker.parseMessage(messageInfo["message"]) 
    mh = f'{messageInfo["messageCategory"]}{":E" + messageInfo["errorCode"] if "errorCode" in messageInfo else ""}/{messageInfo["logicalLink"] if messageInfo["transmissionType"] == "O" else "IN"}'
    mu = f'\n\n```text\n----- {mh} -----\n\n{hl7TemplateMaker.formatMessage(psegments)}\n\n' 
    if "acks" in messageInfo:
        ackMessageInfo = messageInfo["acks"][0]
        ackPSegments = hl7TemplateMaker.parseMessage(ackMessageInfo["message"])
        ackmu = f'----- APP ACK/{ackMessageInfo["logicalLink"]} -----\n\n{hl7TemplateMaker.formatMessage(ackPSegments)}\n\n'
        mu += ackmu
    mu += f'```\n\n'
    return mu

def assembleMessageTextLines(_772, _773):
    """
    Saw ex with \n's "<SP><NL>" and repeated. Combine with before. Happened
    in OBX ie/ newlines in document not property turned into OBXs so embed
    \n to handle that (could reparse OBXs?) ... BOI 692
    """
    def lastCleanLines(messageTextLines):
        if not re.match(r'MSH', messageTextLines[0]):
            raise Exception("Expect start with MSH")
        sep = messageTextLines[0][3] # | or ^
        nmessageTextLines = []
        nextSegment = ""
        for l in messageTextLines:
            if re.match('[A-Z]{3}' + f'\{sep}', l):  
                if nextSegment:
                    nmessageTextLines.append(nextSegment)
                nextSegment = l
                continue
            nextSegment += l
        if nextSegment: # last one
            nmessageTextLines.append(re.sub(r'\n', '', nextSegment))
        return nmessageTextLines
    messageTextLines = _772["message_text"].split("\n\n")
    msh = _773["msh"]
    messageTextLines.insert(0, msh)     
    messageTextLines = lastCleanLines(messageTextLines) 
    return messageTextLines
    
""" 
Saw ex with \n's "<SP><NL>" and repeated. Combine with before. Happened
in OBX ie/ newlines in document not property turned into OBXs so embed
\n to handle that (could reparse OBXs?) ... BOI 692
"""
def lastCleanLines(messageTextLines):
    separator = messageTextLines[0][3]
    nmessageTextLines = []
    nextSegment = ""
    for l in messageTextLines:
        if re.match('[A-Z]{3}' + f'\{separator}', l):
            if nextSegment:
                nmessageTextLines.append(re.sub(r'\n$', '', nextSegment))
            nextSegment = l
            continue
        nextSegment += "\n\n" + l
    if nextSegment:
        nmessageTextLines.append(re.sub(r'\n$', '', nextSegment))
    return nmessageTextLines
    
"""
Reduce 772, 773, mainly the message lines, to a HL7 Event

subscriberProtocolExpected = "GMRC IFC SUBSC" or "XWB RPC SUBSCRIBER"
"""
def makeBasicHL7Event(hl7Entry, subscriberProtocolExpected=""):
    _773Entry = hl7Entry["_773"]
    _772Entry = hl7Entry["_772"]
    messageTextLines = _772Entry["message_text"].split("\n\n")
    messageTextLines.insert(0, _773Entry["msh"])
    
    messageTextLines = lastCleanLines(messageTextLines)

    # Start with VistA parsed 773/772 and then add info from
    # own parse/categorization
    if _773Entry["status"]["label"] == "AWAITING PROCESSING":
        if "last_date_time_updated" in _773Entry:
            raise Exception("AWAITING PROCESSING didn't expect last_date_time set")
        _773Entry["last_date_time_updated"] = {"value": _773Entry["date_time_entered"]["label"]}
    try:
        entry = {
            "id": _773Entry["_id"].split("-")[1],
            # Note: not using message_type/event_type as they reflect LAST 
            # message to update ie/ the ACK message, usually ORR^O02
            # or you see TBR instead of SPQ! Means there is a TBR response
            "created": _773Entry["date_time_entered"]["label"],
            "status": _773Entry["status"]["label"],
            "lastUpdate": _773Entry["last_date_time_updated"]["value"],
            "transmissionType": _772Entry["transmission_type"].split(":")[0],
            "logicalLink": _773Entry["logical_link"]["label"],
            "subscriberProtocol": _773Entry["subscriber_protocol"]["label"],
            "message": messageTextLines
        }
    except Exception as e:
        print(e)
        print(json.dumps(_773Entry, indent=4))
        raise e    
    if "_messageType" in hl7Entry:
        entry["messageType"] = hl7Entry["_messageType"]
        entry["messageId"] = hl7Entry["_messageId"]
    
    # added by protocol reducer of TBR to SPQ matching and parsing message ids
    if "_ackToMessageId" in hl7Entry:
        entry["acknowledgeTo"] = hl7Entry["_ackToMessageId"] # message id
        if "_ackTo773IEN" in hl7Entry:
            entry["acknowledgementToIEN"] = hl7Entry["_ackTo773IEN"]

    if "priority" in _773Entry:
        entry["priority"] = _773Entry["priority"].split(":")[1] # IMMED or DEFERRED
        
    # Was fixed below as choice criteria so problem will never happen
    if subscriberProtocolExpected and entry["subscriberProtocol"] != subscriberProtocolExpected:
        raise Exception(f"Expect Sub Proto to be fixed to {subscriberProtocolExpected}")
                        
    if "fast_purge_dt_tm" in _773Entry:
        if not re.match(r'SUCCESS', entry["status"]):
            print(json.dumps(entry, indent=4))
            raise Exception("Only expected fast purge set for success messages/_773 entries")
        entry["fastPurgeDTTM"] = _773Entry["fast_purge_dt_tm"]["value"]
        
    # See if any examples of late patient registration
    createdDT = datetime.strptime(entry["created"], "%Y-%m-%dT%H:%M:%S")
    lastUpdateDT = datetime.strptime(entry["lastUpdate"], "%Y-%m-%dT%H:%M:%S")
    diffDT = lastUpdateDT - createdDT
    if diffDT > timedelta(hours=1):
        entry["isReceivedDelayed"] = True 
            
    # Can be VAWWW (ie/ home) if incoming that doesn't come back
    # on same link but ACK proper comes on same link? 
    # ... see IFC... for Cerner
    if "logical_link__in_queue" in _773Entry:
        entry["linkIn"] = _773Entry["logical_link__in_queue"]["label"]
            
    # Means ACK APP - MSA error and code taken. Not always taken BUT
    # only error_message if status=ERROR but not all ERROR have message set
    # ... made up for below with APP ACK parse.
    if entry["status"] == "ERROR":
        if "error_message" in _773Entry:
            entry["errorCode"] = _773Entry["error_message"]
        if "error_type" in _773Entry:
            entry["errorTypeLabel"] = _773Entry["error_type"]["label"]
    elif len(set(["error_code", "error_type"]).intersection(set(_773Entry.keys()))):
        raise Exception("Status NOT ERROR but error props in _773")

    return entry
    
"""
HL7 gather for protocols:
- IFC HL7 gather - subscriber protocol is GMRC IFC SUBSC
- SPQ: XWB SENDER, XWB RECEIVER, XWB RPC SUBSCRIBER, SPQ^Q08
... and bonus: _messageType added to (parsed) for _773 and _isAck added
to _772

See:
- all 773's get 772's 
- there are a few orphan 772's (no 773) [TODO follow up]
- purge not applied to all
  - SPQ/TBR: SPQ has it but (many) TBR doesn't => TBR's linger as report below show
    [TODO: why some TBRs and not all. Why linger these when don't linger SPQs =>
     MSA/ACK doesn't matter for purge]
     
TODO: round out purge which is more complex than HLO settings:
- 692 is 9 or 10 days and TBR(ACK) don't linger longer than their SPQs
- 687 is 3 days but TBR(ACK) do linger up to 9 or 10
maybe "PROTOCOL MATTERS" (ie/ XWB differs from GMRC as TBR behavior different) and/or
or settings/task setup is at play.
"""
def gatherAndQA772_773OfProtocol(stationNo, normalMsgRetentionDays=3, badMessageRetentionDays=30, subscriberProtocolLabel="", _773IENsToPrint=[]):
        
    dataLocn = f'{VISTA_DATA_BASE_DIR}{stationNo}/Data/'

    hl7 = {}

    """
    HL7 MESSAGE ADMINISTRATION (773) holds the msh (first message part) 
    adds 870 (links) and errors. It is 
    > to create and maintain unique message IDs
    ie/ here's the owner of the comms
    """  
    resourceIter = FilteredResultIterator(dataLocn, "773")
    hl7TemplateMaker = HL7TemplateMaker()
    byMT = Counter()
    skippedCount = 0
    _773IENByMessageId = {} # ties source system based msg id to local 773 IEN
    _773IENs = set()
    messageIdsIncluded = set()
    _772IENReferencedBy773 = set() # 772 orphan catching
    _773IENBy772IEN = {}
    _773IENBy772IENIncluded = {} # ones considered
    _773Dates = []
    _773DatesIfPurgeSet = []
    _773CntByDay = Counter()
    _773CntByMTByDay = defaultdict(lambda: Counter())
    _773SuccessCntByDay = Counter()
    byStatus = Counter()
    successPurge = Counter()
    successNoPurge = Counter() # not expected but counted below (means no three day clearer but cleaned up with errors)
    for i, resource in enumerate(resourceIter, 1):
            
        if len(_773IENsToPrint) and resource["_id"].split("-")[1] in _773IENsToPrint:
            print("_773 To Check", json.dumps(resource, indent=4))
            print()
                        
        _773IEN = resource["_id"].split("-")[1]
        _773IENs.add(_773IEN) # for 773 orphans - not expected
        _773IENByMessageId[resource["message_id"]] = _773IEN
                       
        _772IEN = resource["date_time_entered"]["id"].split("-")[1]
        _772IENReferencedBy773.add(_772IEN) # for 772 orphan catching below 
        _773IENBy772IEN[_772IEN] = resource["_id"].split("-")[1]
                                    
        # Pending Transmission Status etc? - AWAITING APP ACK, SUCCESS COMPLETE too (TBD)
        if "msh" not in resource:
            skippedCount += 1
            continue
                                
        # IFC decided by sub protocol. Same one is used for Place and Fill, for
        # ACK and others
        if not (
            subscriberProtocolLabel and
            "subscriber_protocol" in resource and 
            re.match(subscriberProtocolLabel, resource["subscriber_protocol"]["label"])
        ):
            skippedCount += 1
            continue
            
        # Only in 531 5/21 - same day as multiple transmissions and may be related. Just skipping
        if "fast_purge_dt_tm" in resource and resource["status"]["label"] != "SUCCESSFULLY COMPLETED":
            print(f'** Warning: fast_purge set for error - skipping: {resource["error_type"]["label"]} - {resource["date_time_entered"]["value"]}')
            skippedCount += 1
            continue               
                        
        messageIdsIncluded.add(resource["message_id"])
                                    
        # Can't trust event_type, message_type from 773 as ack overrides ie/
        # labeled TBR is TBR acks the SPQ but SPQ in MSH!
        extr = hl7TemplateMaker.parseMSH(resource["msh"])
        mt = extr["messageType"]
        byMT[mt] += 1
            
        # TODO: downgraded to warning for 653 
        if "open_attempts" in resource and resource["open_attempts"] != "1":
            print(f"*** WARNING: open attempts set expected 1 but {resource['open_attempts']} - transmission attempts: {resource['transmission_attempts']} - {resource['date_time_entered']['value']}") 
        
        # TODO: downgraded to warning for 531 5/21 - may mess up logic 
        if "transmission_attempts" in resource and resource["transmission_attempts"] != "1":    
            print(f"*** WARNING: transmission attempts expected 1 but {resource['transmission_attempts']} - {resource['date_time_entered']['value']}")
     
        # See report below where SETTING PURGE TIMING is up to the protocol. For
        # some ERROR requests linger; for others they don't. 687 has lingering
        # TBR(ACKs) where their SPQ/Req are purged but 692 doesn't! 
        _773Dates.append(resource["date_time_entered"]["label"])
        _773Day = resource["date_time_entered"]["label"].split("T")[0]
        _773CntByDay[_773Day] += 1
        _773CntByMTByDay[mt][_773Day] += 1
        if resource["status"]["label"] == "SUCCESSFULLY COMPLETED":
            _773SuccessCntByDay[_773Day] += 1    
        if "fast_purge_dt_tm" in resource:
            # Always SUCCESS and skip above if not as seen in 531                    
            if resource["status"]["label"] != "SUCCESSFULLY COMPLETED":
                raise Exception("Only expect fast purge for success")            
            _773DatesIfPurgeSet.append(resource["date_time_entered"]["label"]) # for purge check
                                              
        _772IEN = resource["date_time_entered"]["id"].split("-")[1]
        if _772IEN in _773IENBy772IENIncluded:
            raise Exception("> 1 772 for 773!")
        _773IENBy772IENIncluded[_772IEN] = resource["_id"].split("-")[1]
              
        hl7[_773IEN] = {"_773": resource, "_messageType": mt, "_messageId": resource["message_id"], "_status": resource["status"]["label"]}
        
        byStatus[resource["status"]["label"]] += 1
        
    _773DatesS = sorted(_773Dates)
    _773DatesIfPurgeSetS = sorted(_773DatesIfPurgeSet)     

    print(f"Seeding 772/773 with {len(hl7):,} 773 resources from {i:,} available - skipped {skippedCount:,}.")
    print(f"... first date is {_773DatesS[0]}, last is {_773DatesS[-1]} and where present (success only) purge time is {normalMsgRetentionDays} days though it isn't present and therefore isn't applied to all.")    
    print("MT breakdown (by day too):")
    print("... for SPQ/TBR, note purge window wasn't applied to TBRs (ACKs) in 687 => lingered but for 692, TBRs don't linger longer")
    for mt in sorted(byMT, key=lambda x: byMT[x], reverse=True):
        print(f"\t{mt} {byMT[mt]}")
        if mt in _773CntByMTByDay:
            for day in _773CntByMTByDay[mt]:
                print(f"\t\t{day} {_773CntByMTByDay[mt][day]}")
    print("Status breakdown:")
    for status in byStatus:
        print(f"\t{status} {byStatus[status]}")
    # Taking last date as 'cut date with time' and first date = first non purged success entry which should be within the config's time window for purging
    print("By Day:") 
    for i, day in enumerate(sorted(_773CntByDay), 1):
        print(f"\t{i}. {day} {_773CntByDay[day]:,} - {'-' if day not in _773SuccessCntByDay else reportPercent(_773SuccessCntByDay[day], _773CntByDay[day])}")
    
    """
    HL7 MESSAGE TEXT (772) has message text and status is always success!
    
    772 gives us access to the rest of the message, including MSA which is what
    makes an ACK, an ACK.
    """
    resourceIter = FilteredResultIterator(dataLocn, "772")
    protocolOfMatch = Counter()
    countFastPurgeSet772 = 0
    _772Orphans = set()
    _772RelatedEventProtocol = ""
    ofProtocolWMSACount = 0
    OfProtocolWMSAMatchedCount = 0 
    OfProtocolWMSAMatchedAckToSetCount = 0 # is acknowledgement_to set?
    dtEnteredNotAck = defaultdict(lambda: Counter()) # Ex SPQ
    dtEnteredAckWReq = Counter()
    dtEnteredAckNoReq = Counter()
    for i, resource in enumerate(resourceIter, 1):
        
        """
        if resource["date_time_entered"]["value"].split("T")[0] == "2020-03-25":
            print("=== 3-25 772")
            print(json.dumps(resource, indent=4))
        """
        _772IEN = resource["_id"].split("-")[1]
        
        """
        TODO MORE LATER
        - most are status ["ERROR", "AWAITING APPLICATION ACKNOWLEDGEMENT", "PENDING TRANSMISSION"]
        - or message_type B:BATCH OF MESSAGES
        - and most of the time, MSH is the first segment!
        """
        if _772IEN not in _773IENBy772IEN: # Never an MSA either
            _772Orphans.add(_772IEN)
            continue
 
        # Filter out for whatever criteria
        if _772IEN not in _773IENBy772IENIncluded:  
            continue
                        
        if "message_type" in resource and resource["message_type"] != "M:SINGLE MESSAGE":
            raise Exception("Only expected single messages")                        
        
        # Allows for TEST and EVENT of GMRC IFC ORM TEST
        if "related_event_protocol" in resource:
            if _772RelatedEventProtocol:
                if not re.match(_772RelatedEventProtocol, resource["related_event_protocol"]["label"]):
                    raise Exception(f'Expected one related event protocol for 772 which is {_772RelatedEventProtocol} but have {resource["related_event_protocol"]["label"]}')
            else: 
                pieces = resource["related_event_protocol"]["label"].split(" ")
                _772RelatedEventProtocol = " ".join(pieces[0:-1])
                
        _773IEN = _773IENBy772IENIncluded[_772IEN]
        hl7[_773IEN]["_772"] = resource
        _773Resource = hl7[_773IEN]["_773"]
        _773DAY = _773Resource["date_time_entered"]["label"].split("T")[0]
        
        # Expected fast purge in both or neither
        if ("fast_purge_dt_tm" in resource and "fast_purge_dt_tm" not in _773Resource) or ("fast_purge_dt_tm" not in resource and "fast_purge_dt_tm" in _773Resource):
            raise Exception("Unexpected purge in 773 and not 772 or vica versa")
        
        """
        Big novelty of full message in 772 let's us see MSA (is it an ACK?). For SPQ/TBR
        reinforces it is the ACK (TBR) that is kept outside the purge window and hence 
        there are unmatched ACKs
        """
        _772Psegments = resource["message_text"].split("\n") if "message_text" in resource else []
        msaSegments = [pseg for pseg in _772Psegments if re.match(r'MSA', pseg)] 
        if len(msaSegments) > 1:
            raise Exception("Expect at most one MSA segments") 
        if len(msaSegments):
            msaSegment = msaSegments[0] # doing first
            """
            Removed now as Custom: check for SPQ/TBR, showed all MSAs were TBRs
            """
            ofProtocolWMSACount += 1
            extr = hl7TemplateMaker.parseMSA(msaSegment)
            msaTo = extr["msgCtrlIdLocal"]
            hl7[_773IEN]["_ackToMessageId"] = msaTo # would embed SNO
            """
            Cases for protocol MSAs
            - there is a match to a (prior) message
            - furthermore, there is a match to a protocol message
            - for SPQ/TBR, seems like no TBR kept if error ack. SPQ notes
            error but TBR purged?
            """
            if msaTo in _773IENByMessageId:
                if msaTo not in messageIdsIncluded:
                    raise Exception("Only expect match to message of the protocol!")
                OfProtocolWMSAMatchedCount += 1
                dtEnteredAckWReq[_773DAY] += 1
                # if VistA records ack ie/ QA VistA parse
                if "acknowledgement_to" in _773Resource:
                    OfProtocolWMSAMatchedAckToSetCount += 1
                _773AckedIEN = _773IENByMessageId[msaTo]
                # will be subset of acked to message id as some 773's purged
                hl7[_773IEN]["_ackTo773IEN"] = _773AckedIEN
            else:
                dtEnteredAckNoReq[_773DAY] += 1
        else:
            dtEnteredNotAck[_773Resource["status"]["label"]][_773DAY] += 1

    notMatchedProtocol773Count = sum(1 for ien in hl7 if "_773" in hl7 and "_772" in hl7)
    if notMatchedProtocol773Count:
        raise Exception(f"Not all Protocol's 773's matched with a 772 - {notMatchedProtocol773Count}")
    print(f"Matched ALL {len(hl7):,} 773's of Protocol {subscriberProtocolLabel} to 772 with {_772RelatedEventProtocol} related event protocol")
    if len(_772Orphans):
        print(f"\tBut of {i:,} 772s, {len(_772Orphans):,} are \"orphans\" - w/o 773s (follow up later TODO)")
    print(f"Of Protocol, {reportPercent(ofProtocolWMSACount, len(hl7))} have MSA - {reportPercent(OfProtocolWMSAMatchedCount, ofProtocolWMSACount)} are matched to unpurged 773s of the protocol using their message id and {reportPercent(OfProtocolWMSAMatchedAckToSetCount, ofProtocolWMSACount)} have 'acknowledgement_to' set in their 773's")
    """
    Ex output for 687 shows ACKs were kept longer and so "orphaned" but that
    request (SPQs stayed within the purge window
    
    We see that ERRORs kept beyond purge window but largely SUCCESS are
    not
    
    Protocol: XWB RPC SUBSCRIBER (very few beyond window)
    This protocol contrasts with GMRC ... where many ERROR HL7s (originals/not MSAs)
    are before purge window. => SETTING PURGE TIMING IS UP TO THE PROTOCOL
    
    ACKs (MSA - _isAck) and Purge Windows (reinforces MSH from 773)
        Of Protocol Request (not MSA) Dates (expect in purge window):
                2020-03-17 8 <---- rogue
                2020-03-22 37 <---- 22 on
                2020-03-23 860
                2020-03-24 1911
                2020-03-25 465
        Of Protocol MSA matched Dates (expect in purge window)
                2020-03-22 37 <---- matches up with Request
                2020-03-23 860
                2020-03-24 1910
                2020-03-25 464
        Of Protocol MSA not matched Dates (expect < purge window ie linger):
                2020-03-18 602 <---- 18->21 before purge window
                2020-03-19 1440
                2020-03-20 835
                2020-03-21 439
    """
    print("ACKs (MSA - _isAck) and Purge Windows (reinforces MSH from 773)")
    print("\tOf Protocol Request (not MSA) Dates (expect in purge window):")
    for status in dtEnteredNotAck:
        print(f'\t\t{status}')
        for dt in dtEnteredNotAck[status]:
            print(f'\t\t\t{dt} {dtEnteredNotAck[status][dt]}')        
    print("\tOf Protocol MSA matched Dates (expect in purge window)")
    for dt in dtEnteredAckWReq:
        print(f'\t\t{dt} {dtEnteredAckWReq[dt]}')            
    print("\tOf Protocol MSA not matched Dates (expect < purge window ie linger):")
    for dt in dtEnteredAckNoReq:
        print(f'\t\t{dt} {dtEnteredAckNoReq[dt]}')                
                        
    # Need orphans total for 772's not covered by _773 and a _773IEN in hl7   
    return hl7, skippedCount, len(_772Orphans)
    
# HL7 config - retention days and the listener logical link (870)
def lookupConfig779_1(stationNo):
    dataLocn = "{}{}/{}".format(VISTA_DATA_BASE_DIR, stationNo, "Data") 
    fmqlReplyStore = FMQLReplyStore(dataLocn)
    hloSystemParametersReply = fmqlReplyStore.lastReplyOfType("779_1")
    if not hloSystemParametersReply:
        raise Exception("Expected HLO System Parameters 779_1 to have been cached but missing")
    if len(hloSystemParametersReply["results"]) != 1:
        raise Exception("Expected one and only one result in 779_1")
    hloSystemParameters = hloSystemParametersReply["results"][0]
    return hloSystemParameters
    