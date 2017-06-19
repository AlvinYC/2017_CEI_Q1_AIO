# -*- coding: utf-8 -*-

import json
import sys
import logging
import re
import math

from __aio_dict   import aio_dict
from __aio_cpdict import aio_cpdict
from __aio_s2v    import aio_s2v
from __aio_w2v    import aio_w2v
from __combineCNN import combineCNN

logging.basicConfig(level=logging.DEBUG)
reload(sys)                        
sys.setdefaultencoding('utf-8')

notag = -1
cpbase = 1000

intent_mapping = {
"None":0,
"HomeControl":1,
"BackHome":2,
"LeaveHome":3,
"Confirm":4,
"Time":5,
"Weather":6,
"Traffic":7,
"Greeting":8,
"MorningBriefing":9,
"English":10,
"Hello":11
}

def cosine_similarity(v1, v2):
    sum_xx, sum_xy, sum_yy = 0.0, 0.0, 0.0
    for i in range(0, len(v1)):
        sum_xx += math.pow(v1[i], 2)
        sum_xy += v1[i] * v2[i]
        sum_yy += math.pow(v2[i], 2)

    return sum_xy / math.sqrt(sum_xx * sum_yy)

def Sentence2Vec(wordseg, wordindex):
    s2v = []
    for k in range(0,250):
        s2v.append(0)

    for i in range(0,len(wordindex)):
        if wordindex[i] != notag:
            try:
                w2v = aio_w2v[wordseg[i]]
                for j in range(0,250):
                    s2v[j] = s2v[j] + w2v[j]
            except:
                logging.info("Compute vector fail:" + wordseg[i])
    return s2v

def KNNIntentAnalyzer(utterance, wordseg, wordindex):
    s2v = Sentence2Vec(wordseg, wordindex)
    if s2v[0] == 0:
        # return "None"
        max_cos_list = []
        for i in range(0,len(intent_mapping)):
            max_cos_list.append(0)
        intent = combineCNN(utterance, max_cos_list)
        return intent
    else:
        max_key = 0
        max_cos   = 0
        max_key_list = []
        max_cos_list = []
        for i in range(0,len(intent_mapping)):
            max_key_list.append(-1)
            max_cos_list.append(0)
        #cos_list = []
        for s in aio_s2v:
            cos_sim = cosine_similarity(s2v, aio_s2v[s][1])
            cos_sim = 0.5*cos_sim + 0.5
            
            if cos_sim > max_cos:
                max_key = s
                max_cos = cos_sim
            intent_index = intent_mapping[aio_s2v[s][0]]
            if cos_sim > max_cos_list[intent_index]:
                max_key_list[intent_index] = s
                max_cos_list[intent_index] = cos_sim

        word_dejson = {'nearest term': max_key.decode("utf-8") }
        vector_dejson = {'max_cos_list':max_cos_list, 'max_key_list':max_key_list}
        logging.info(json.dumps(word_dejson, encoding='utf-8', ensure_ascii=False))
        logging.info(json.dumps(vector_dejson, encoding='utf-8', ensure_ascii=False) )
        
        intent = combineCNN(utterance, max_cos_list)
        return intent
    
def IntentAnalyzer(wordseg, wordindex):
    s2v = Sentence2Vec(wordseg, wordindex)
    if s2v[0] == 0:
        return "None"
    else:
        max_key = 0
        max_cos   = -1
        for s in aio_s2v:
            cos_sim = cosine_similarity(s2v, aio_s2v[s][1])
            if cos_sim > max_cos:
                max_key = s
                max_cos = cos_sim

        word_dejson = {'nearest term': max_key.decode("utf-8") }
        logging.info(json.dumps(word_dejson, encoding='utf-8', ensure_ascii=False))
        return aio_s2v[max_key][0]

def WordSegmentation(utterance):
    wordseg = [utterance]
    wordindex = [notag]

    for k in range(0, len(aio_cpdict)):
        split_noun = aio_cpdict[k]['term']
        wordseg_tmp_result = []
        wordindex_tmp_result = []

        for j in range(0,len(wordseg)):
            if wordindex[j]!= notag:
                wordseg_tmp_result.append(wordseg[j])
                wordindex_tmp_result.append(wordindex[j])
            else:
                wordseg_tmp = wordseg[j].split(split_noun)

                if wordseg_tmp[0] == "":
                    wordseg_new = []
                    wordindex_new = []
                else:
                    wordseg_new = [wordseg_tmp[0]]
                    wordindex_new = [notag]        
                for i in range(1,len(wordseg_tmp)):
                    wordseg_new.append(split_noun)
                    wordindex_new.append( k+cpbase )
                    if( wordseg_tmp[i] != "" ):
                        wordseg_new.append(wordseg_tmp[i])
                        wordindex_new.append(notag)

                for w in wordseg_new: 
                    wordseg_tmp_result.append(w)
                for f in wordindex_new:
                    wordindex_tmp_result.append(f)
        wordseg = wordseg_tmp_result
        wordindex = wordindex_tmp_result    
    
    for k in range(0,len(aio_dict)):
        split_noun = aio_dict[k]['term']
        wordseg_tmp_result = []
        wordindex_tmp_result = []

        for j in range(0,len(wordseg)):
            if wordindex[j]!= notag:
                wordseg_tmp_result.append(wordseg[j])
                wordindex_tmp_result.append(wordindex[j])
            else:
                wordseg_tmp = wordseg[j].split(split_noun)

                if wordseg_tmp[0] == "":
                    wordseg_new = []
                    wordindex_new = []
                else:
                    wordseg_new = [wordseg_tmp[0]]
                    wordindex_new = [notag]
                for i in range(1,len(wordseg_tmp)):
                    wordseg_new.append(split_noun)
                    wordindex_new.append(k)
                    if( wordseg_tmp[i] != "" ):
                        wordseg_new.append(wordseg_tmp[i])
                        wordindex_new.append(notag)

                for w in wordseg_new: 
                    wordseg_tmp_result.append(w)
                for f in wordindex_new:
                    wordindex_tmp_result.append(f)
        wordseg = wordseg_tmp_result
        wordindex = wordindex_tmp_result

    wordseg_dejson = {'devide by inoun':wordseg}
    logging.info(json.dumps(wordseg_dejson, encoding='utf-8', ensure_ascii=False))
    logging.info(wordindex)
        
    confirm_term_exist = False
    not_confirm_term_exist = False
    for i in range(0,len(wordindex)):
        if wordindex[i] != -1:
            if wordindex[i] < cpbase:
                if aio_dict[ wordindex[i] ]['intent'] == "Confirm":
                    confirm_term_exist = True
                else:
                    not_confirm_term_exist = True                
            else:
                if aio_cpdict[ wordindex[i]-cpbase ]['intent'] == "Confirm":
                    confirm_term_exist = True
                else:
                    not_confirm_term_exist = True
    if confirm_term_exist == True and not_confirm_term_exist == True:
        for i in range(0,len(wordindex)):
            if wordindex[i] != -1:
                if wordindex[i]<cpbase and aio_dict[ wordindex[i] ]['intent'] == "Confirm":
                    wordindex[i] = -1
                elif wordindex[i]>=cpbase and aio_dict[ wordindex[i]-cpbase ]['intent'] == "Confirm":
                    wordindex[i] = -1
    wordseg_dejson = {'after_confirm_detection':wordseg}
    logging.info(json.dumps(wordseg_dejson, encoding='utf-8', ensure_ascii=False))
    logging.info(wordindex)
    
    word_seg_result = {"wordseg":wordseg, "wordindex": wordindex}
    
    return word_seg_result

def EntityParser(wordseg, wordindex):
    intern_content = u"HomeControl"
    subject_content = {}
    condition_content = {}
    action_content = {}

    for i in range(0, len(wordindex)):
        wid = wordindex[i]
        logging.info("%d, %d", i, wid)
        if wid == notag:
            logging.info("%s is not keyword", wordseg[i])
        elif wid < cpbase:
            logging.info(aio_dict[wid]['entity_type'])
            if aio_dict[wid]['entity_type'] == "subject":
                logging.info(aio_dict[wid]["type"])
                if aio_dict[wid]["type"] == "裝置":
                    if "裝置" not in subject_content:
                        subject_content["裝置"] = []
                        subject_content["裝置用詞"] = []
                    subject_content["裝置"].append(aio_dict[wid]["value"])
                    subject_content["裝置用詞"].append(aio_dict[wid]["term"])
                elif aio_dict[wid]["type"] == "娛樂":
                    if "娛樂" not in subject_content:
                        subject_content["娛樂"] = []
                        subject_content["娛樂用詞"] = []
                    subject_content["娛樂"].append(aio_dict[wid]["value"])
                    subject_content["娛樂用詞"].append(aio_dict[wid]["term"])
                else:
                    if aio_dict[wid]["type"] not in subject_content:
                        subject_content[ aio_dict[wid]["type"] ] = []
                    subject_content[ aio_dict[wid]["type"] ].append(aio_dict[wid]["value"])
            if aio_dict[wid]['entity_type'] == "condition":
                if aio_dict[wid]["type"] not in condition_content:
                    condition_content[ aio_dict[wid]["type"] ] = []
                condition_content[ aio_dict[wid]["type"] ].append(aio_dict[wid]["value"])
            if aio_dict[wid]['entity_type'] == "action":
                if aio_dict[wid]["type"] not in action_content:
                    action_content[ aio_dict[wid]["type"] ] = {}
                action_content[ aio_dict[wid]["type"] ] = aio_dict[wid]["value"]
        else:
            wid = wid - cpbase
            intern_content = aio_cpdict[wid]["intent"]
            logging.info(intern_content)
            if aio_cpdict[wid]["subject_type"] == "裝置":
                logging.info("裝置")
                if "裝置" not in subject_content:
                    subject_content["裝置"] = []
                subject_content["裝置"].append(aio_cpdict[wid]["subject_value"])
            elif aio_cpdict[wid]["subject_type"] == "娛樂":
                logging.info("娛樂")
                if "娛樂" not in subject_content:
                    subject_content["娛樂"] = []
                subject_content["娛樂"].append(aio_cpdict[wid]["subject_value"])
            elif aio_cpdict[wid]["condition_type"] != "":
                logging.info("其他")
                if aio_cpdict[wid]["subject_type"] not in subject_content:
                    subject_content[aio_cpdict[wid]["subject_type"]] = []
                subject_content[ aio_cpdict[wid]["subject_type"] ].append(aio_cpdict[wid]["subject_value"])
            logging.info("condition")
            if aio_cpdict[wid]["condition_type"] != "":
                if aio_cpdict[wid]["condition_type"] not in condition_content:
                    condition_content[ aio_cpdict[wid]["condition_type"] ] = []
                condition_content[ aio_cpdict[wid]["condition_type"] ].append(aio_cpdict[wid]["condition_value"])
            logging.info("action")
            if aio_cpdict[wid]["action_type"] != "":
                if aio_cpdict[wid]["action_type"] not in action_content:
                    action_content[ aio_cpdict[wid]["action_type"] ] = {}
                action_content[ aio_cpdict[wid]["action_type"] ] = aio_cpdict[wid]["action_value"]
    entity = {'Utterance':"ok",
              'Intent':[intern_content],
              'Entity':[{'Subject':subject_content,
                         'Condition':condition_content,
                         'Action':action_content
                        }
                       ]
              }

    return entity

def IntentEntity(utterance):
    word_seg_result = WordSegmentation(utterance.lower())
    intent_response = IntentAnalyzer(word_seg_result["wordseg"], word_seg_result["wordindex"])
    entity_response = EntityParser(word_seg_result["wordseg"], word_seg_result["wordindex"])

    entity_response['Intent'] = intent_response
    entity_response['Utterance'] = utterance
    logging.info(json.dumps(entity_response, encoding='utf-8', ensure_ascii=False))
    return entity_response

def KNNIntentEntity(utterance):
    word_seg_result = WordSegmentation(utterance.lower())
    intent_response = KNNIntentAnalyzer(utterance, word_seg_result["wordseg"], word_seg_result["wordindex"])
    entity_response = EntityParser(word_seg_result["wordseg"], word_seg_result["wordindex"])

    entity_response['Intent'] = intent_response
    entity_response['Utterance'] = utterance
    logging.info(json.dumps(entity_response, encoding='utf-8', ensure_ascii=False))
    return entity_response

'''
logging.info("start")
test_utterance = "今天氣溫如何"

word_seg_result = WordSegmentation(test_utterance.lower())

#intent_response = IntentAnalyzer(word_seg_result["wordseg"], word_seg_result["wordindex"])
intent_response = KNNIntentAnalyzer(word_seg_result["wordseg"], word_seg_result["wordindex"])

entity_response = EntityParser(word_seg_result["wordseg"], word_seg_result["wordindex"])
entity_response['Utterance'] = test_utterance
entity_response['Intent'] = intent_response
logging.info(json.dumps(entity_response, encoding='utf-8', ensure_ascii=False))

logging.info("end")
'''