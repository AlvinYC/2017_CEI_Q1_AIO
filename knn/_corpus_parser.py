# -*- coding: utf-8 -*-

import json
import csv
#import sys
import logging
import re
import copy
import gensim


code_version = "0616"
model = gensim.models.KeyedVectors.load_word2vec_format('word2vec_model/w2v.bin',binary=True)
logging.basicConfig(level=logging.DEBUG)
#reload(sys)                        
#sys.setdefaultencoding('utf-8')

corpus_input_file = "corpus.csv"
corpus_json_file = "corpus.json"
corpus_jieba_file = "corpus_jieba.txt"
notag = -1
tag = 1

def WordSegmentation(utterance, word_vec):
    wordseg = [utterance]
    wordindex = [notag]

    for word in sorted(word_vec, key=len, reverse = True):
        #logging.info(word)
        split_noun = word
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
                    wordindex_new.append(tag)
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
    ##logging.info(json.dumps(wordseg_dejson, encoding='utf-8', ensure_ascii=False))
    ##logging.info(wordindex)
    
    word_seg_result = {"wordseg":wordseg, "wordindex": wordindex}
    
    return word_seg_result

def word2vec(word):
    word_vector = []
    try:
        vec = model[word]
        for j in range(0, len(vec)):
            word_vector.append( repr(vec[j]) )
    except:
        for j in range(0,250):
            word_vector.append( 0 )
    return word_vector

def sentence2vec( sentence, word_vec ):
    #logging.info( json.dumps({"sentence":sentence}, encoding='utf-8', ensure_ascii=False))
    word_seg_result = WordSegmentation( sentence, word_vec )
    wordseg = word_seg_result["wordseg"]
    wordindex = word_seg_result["wordindex"]
    
    s2v = []
    for k in range(0,250):
        s2v.append(0)

    for i in range(0,len(wordindex)):
        if wordindex[i] != notag:
            w2v = word_vec[ wordseg[i] ]["Vector"]
            #logging.info(w2v)
            for j in range(0,250):
                s2v[j] = s2v[j] + float(w2v[j])
    return s2v

def generate_jieba_dict(word_vec, system, version):
    f_jieba = open(corpus_jieba_file, "w")
    f_jieba.write(system.replace(" ","_") + "_" + version.replace(" ","_") + " 100 " + system.replace(" ","_"))
    for word in word_vec:
        f_jieba.write("\n" + word.replace(" ","_") + " 100000 " + system.replace(" ","_"))
    f_jieba.close()    
    
def corpus_parser():
    corpus_file = open(corpus_input_file, 'r')
    corpus_json = {"System":"Eye Love", "Version":"4-5-0", "Code Version": code_version, "Original_Corpus":[],"Word_Vec":{},"Sentence_Vec":{}}

    skip = True
    #for solve UTF-8 with BOM
    for row in csv.reader(corpus_file):
        if skip == True:
            skip = False
            continue
        ##logging.info(json.dumps({"corpus csv file":row[1]}, encoding='utf-8', ensure_ascii=False))
        if row[0] == "System":
            #logging.info("System")
            corpus_json["System"] = row[1]
            continue
        if row[0] == "Version":
            #logging.info("Version")
            corpus_json["Corpus Version"] = row[1]
            continue
        if row[0] == "Index" or row[0] == "":
            #logging.info("Index")
            continue
        #logging.info("Index: %s", row[0])
        corpus_row = {}
        corpus_row['Utterance'] = row[1]
        corpus_row['Intent'] = row[2]
        corpus_row['Model'] = int(row[3])
        corpus_row['Entity'] = []
        for entity_index in range(4,len(row)-1):
            if row[entity_index] != "":
                wordseg_tmp = row[entity_index].split(":")
                #logging.info(wordseg_tmp)
                word_type = wordseg_tmp[0]
                word_value = wordseg_tmp[1] 
                corpus_row['Entity'].append({ word_type : word_value })
                if word_value not in corpus_json['Word_Vec']:
                    corpus_json['Word_Vec'][ word_value ] = {"Type": word_type ,"Vector": word2vec(word_value) }
        ##logging.info(json.dumps(corpus_row, encoding='utf-8', ensure_ascii=False))
        corpus_json['Original_Corpus'].append(corpus_row)
        corpus_json['Sentence_Vec'][ corpus_row['Utterance'] ] = {"Intent":corpus_row['Intent'],"Vector": [] }
    corpus_file.close()

    for utterance in corpus_json['Sentence_Vec']:
        corpus_json['Sentence_Vec'][utterance]["Vector"] = sentence2vec( utterance, corpus_json['Word_Vec'] )

    #logging.info(json.dumps(corpus_json, encoding='utf-8', ensure_ascii=False))
    with open(corpus_json_file, 'w') as outfile:
        json.dump(corpus_json, outfile, encoding='utf-8', ensure_ascii=False)
        
    generate_jieba_dict(corpus_json['Word_Vec'], corpus_json["System"], corpus_json["Version"])

#logging.info("start")
corpus_parser()
#logging.info("end")
