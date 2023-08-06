import pandas as pd
import numpy as np
import spacy
from spacy.matcher import Matcher
from termcolor import colored
import time
import regex as re
from itertools import chain 
import string
from tqdm import tqdm 

import tqdm.notebook as tq

class PassivePyAnalyzer:
    
        """
            Get the data from a dataframe.

            Clean the dataset based on the given regex patterns.
            Match passive voice sentence level or corpus level.
            save the output to a file

        """
        def __init__(self, spacy_model = "en_core_web_lg"):

            """
            Create the Detector

            n_processses: number of core to use
            batch_size: size of batches of records passed onto the matcher
            regex_patterns: Patterns that should be detected and cleaned from the data
            
            
            """
        
            self.nlp = spacy.load(spacy_model, disable=["ner"])

        def create_matcher(self):

            """creates a matcher on the following vocabulary"""
            
            matcher = Matcher(self.nlp.vocab)

            # list of verbs that their adjective form 
            # is sometimes mistaken as a verb
            verbs_list = ["associate", "involve", "exhaust", "base", 
                        "lead", "stun", "overrate",  "fill", "bear",
                        "complicate", "reserve", "complicate"]


            #--------------------------rules--------------------#

            

            passive_rule_1 = [
                {"DEP": "auxpass"},
                {"DEP":"neg", "TAG":"RB", "OP":"*"},
                {"DEP":"HYPH", "OP":"*"},
                {"DEP":"advmod", "TAG":"RB", "OP":"*"},
                { "TAG":"VBN", "LEMMA":{"NOT_IN" : verbs_list}}
            ]

            """
            sentence : The book was read by him.
            dependencies : ['det', 'nsubjpass', 'auxpass', 'ROOT', 'agent', 'pobj', 'punct']
            Tags : ['DT', 'NN', 'VBD', 'VBN', 'IN', 'PRP', '.']
            """
            passive_rule_2 = [
                {"DEP": {"IN": ["attr", 'nsubjpass', 'appos']}},
                {"TAG": "RB", "DEP": "advmod", "OP" : "*"},
                {"DEP": "PUNCT", "OP" : "*"},
                {"TAG": "VBN", "DEP": "acl","LEMMA": {"NOT_IN" : verbs_list}}
            ]

            """
            sentence : there was no change detected in her behavior.
            dependencies : ['expl', 'ROOT', 'det', 'attr', 'acl', 'prep', 'poss', 'pobj', 'punct']
            tags : ['EX', 'VBD', 'DT', 'NN', 'VBN', 'IN', 'PRP$', 'NN', '.']
            """


            passive_rule_3 = [
                {"DEP":"cc"},
                {"DEP":"advmod", "TAG":"VBN", "OP": "*", "LEMMA": {"NOT_IN":["pre"]}},
                {"DEP": "conj", "TAG": "VBN", "LEMMA":{"NOT_IN" : verbs_list}},
                {"DEP":"pobj", "OP":"!"}
            ]

            """
            Used for the second part with "and ..." 
            sentence : it was determined and formed.
            dependencies : ['nsubjpass', 'auxpass', 'ROOT', 'cc', 'conj', 'punct']
            tags : ['PRP', 'VBD', 'VBN', 'CC', 'VBN', '.']
            """

            passive_rule_4 = [
                {"DEP":"advcl", "TAG":"VBN"},
                {"DEP": "agent", "TAG":"IN"},
                {"OP":"*"},
                {"DEP": "pobj", "TAG":"NN"},
            ]

            """
            sentence : killed by the police, he never thought this would be his end.
            dependencies : ['advcl', 'agent', 'det', 'pobj', 'punct', 'nsubj', 'neg', 'ROOT', 'nsubj', 'aux', 'ccomp', 'poss', 'attr']
            tags : ['VBN', 'IN', 'DT', 'NN', ',', 'PRP', 'RB', 'VBD', 'DT', 'MD', 'VB', 'PRP$', 'NN']
            """

            passive_rule_5 = [
                {"DEP": "nsubj"},
                {"DEP": "ROOT"},
                {"DEP": "attr", "TAG": "VBN", "LEMMA":{"NOT_IN" : verbs_list}},
                {"DEP": "prep", "TAG": "IN", "OP":"*"}
            ]

            """
            sentence : Bears are dreamt of in your fantasies!
            dependencies : ['nsubjpass', 'auxpass', 'ROOT', 'prep', 'prep', 'poss', 'pobj', 'punct']
            tags : ['NNS', 'VBP', 'VBN', 'IN', 'IN', 'PRP$', 'NNS', '.']
            """


            passive_rule_6 = [
                {"LEMMA": {"IN": verbs_list}},
                {"LOWER":"by"}
            ]


            """
            to avoid the confusion between the adjective and passive version of specific 
            verbs, we dedicated a new rule to some verbs to be detected when used with 
            an agent (by)

            sentence : Natural resources are exhusted by humans.
            dependencies : ['amod', 'nsubjpass', 'auxpass', 'ROOT', 'agent', 'pobj']
            tags : ['JJ', 'NNS', 'VBP', 'VBN', 'IN', 'NNS']
            """


            # ------------------adding rules to the matcher----------#

            matcher.add("passive_rule_1", [passive_rule_1])
            matcher.add("passive_rule_2", [passive_rule_2])
            matcher.add("passive_rule_3", [passive_rule_3])
            matcher.add("passive_rule_4", [passive_rule_4])
            matcher.add("passive_rule_5", [passive_rule_5])
            matcher.add("passive_rule_6", [passive_rule_6])

            print('Matcher is built.')

            return matcher




        def detect_sents(self, cleaned_corpus, batch_size, n_process):
                         
            print('Detecting Sentences...')

            """Separates sentences from each other in each record
             and puts them in a list along side the count of sentences in each 
             document in another list"""
            

            all_sentences = []
            count_sents = []
            unwanted = []
            puncs = set(string.punctuation)
            start = time.process_time()

            m = 0
            for record_doc in tq.tqdm(self.nlp.pipe(cleaned_corpus, batch_size=batch_size, n_process = n_process), 
                                    leave=True,
                                    position=0,
                                    total=len(cleaned_corpus)):


                sentences = list(record_doc.sents)
                sentences = [str(sentence) for sentence in sentences if len(sentence)>=2] 
                # more than 2 to remove titles and extras


                for sentence in sentences:
                    i = sentences.index(sentence)
                
                    
                    #...........................joining with the previous one.............................#
                    # ones that start with but and their previous record doesn't have dot at its end
                    if i!=0:
                        if (re.search(r'^ *but', sentence) and not re.search(r'.$', sentences[i-1])) or all((re.search(r'^[A-Z0-9]', word) or re.search(r'^[\(\)\.\-]', word)) for word in sentence.split()) or re.search(r'^\(.*\)[\.\!\,]*', sentence):
                            j = 0
                            for j in range(1, i):
                                if i-j not in unwanted:
                                    sentences[i-j] = sentences[i-j] + sentences[i]
                                    unwanted.append(i)
                                    break
                            
                
                    #.........................joining with the next one..........................#
                    if i != len(sentences)-1:


                        if re.search(r', *$', sentence): # remove the one that's ended with comma
                            sentences[i] = ' '.join([sentences[i], sentences[i+1]])
                            unwanted.append(i+1)

                        if re.search(r'\- *$', sentence): 
                            # see if it's ended with hyphen then look at the next one
                            # if it has and in the beginning, forget about this one and go to the next to analyze the and 
                            # and not duplicate the process
                            if re.search(r'^ *(\([\w\. ]*\))* *and', sentences[i+1]):
                                continue
                            else: 
                                # but if there was no and in the next one,
                                #  join this with the next

                                sentences[i] = ' '.join([sentences[i], sentences[i+1]])
                                unwanted.append(i+1)
                        # see if it ends with and and join it with the 
                        elif re.search(r'and *$', sentence):
                            sentences[i] = ' '.join([sentences[i], sentences[i+1]])
                            unwanted.append(i+1)

                        # end with 'as well as' and join with the next one
                        elif re.search(r'((as well as) *)$', sentence):
                            sentences[i] = ' '.join([sentences[i], sentences[i+1]])
                            unwanted.append(i+1)

                        # end with the following phrasees and join with the next ones
                        elif re.search(r'((Exp\.)|(e\.g\.)|(i\.e\.))$', sentence):
                            sentences[i] = ' '.join([sentences[i], sentences[i+1]])
                            unwanted.append(i+1)


                m+=1
                for index in sorted(set(unwanted), reverse=True):
                    del sentences[index]
                unwanted = []

                
                count_sents.append(len(sentences))
                all_sentences.append(sentences) 

            all_sentences = list(chain.from_iterable(all_sentences))
            print(f'\n\nTotal number of sentences: {len(all_sentences)}')


            end = time.process_time()

            # calculating the time taken
            taken_t = round(end-start, 2)
            if taken_t < 60:
                print('time taken: ', taken_t, ' s')
            else: print('time taken: ',  (taken_t)//60 , ' min ', round(taken_t%60, 1) , ' s')

            return np.array(count_sents, dtype='object'), np.array(all_sentences, dtype='object')



        def find_doc_idx(self, count_sents):

            """ finds the indices required for the documents and sentences"""

            m = 1
            sent_indices = []
            doc_indices = []
            for i in count_sents:
                n = 1
                for j in range(i):
                    sent_indices.append(n)
                    doc_indices.append(m)
                    n+=1
                m+=1
            return np.array(sent_indices), np.array(doc_indices)




        def add_other_cols(self, df, colName, count_sents):

            """ creates a dataframe of all the other columns
            with the required number of repetitions for each """

            # create a list of all the col names
            fields = df.columns.tolist()
            # remove colName
            del fields[fields.index(colName)]

            other_columns = {}
            # create a df of all the other cols with 
            # appropriate number of repetitions
            for col in fields:
                properties = []
                for i in range(len(count_sents)):
                    properties.append(count_sents[i]*[df.loc[i, col]])
                
                properties = list(chain.from_iterable(properties))
                other_columns[col] = properties

            df_other_cols = pd.DataFrame.from_dict(other_columns)

            return df_other_cols  



        
        def match_text(self, cleaned_corpus, matcher, batch_size=1, n_process=1):

            """ This function finds passive matches in one sample sentence"""

            # seperating sentences
            count_sents, all_sentences = self.detect_sents([cleaned_corpus], batch_size, n_process)

            print(all_sentences)
            matches, passive_c, binaries = self.find_matches(matcher, all_sentences, batch_size, n_process)
            

            s_output = pd.DataFrame(np.c_[all_sentences, binaries, matches, passive_c],
                        columns=['sentence', 'binary', 'passive_match(es)', 'raw_passive_count'])
            
            return s_output

        def find_matches(self, matcher, corpora, batch_size, n_process):

            """ finds matches from each record """

            # mark the start
            print(colored('Starting to find passives...', 'red'))  

            # tracking time
            start = time.process_time()

            passive_c = [] # the list of outputs for the number of matches for each sentence
            matches = [] # all the matches for each record
            binaries = []
            i = 0

            # stating with batches and n cores
            for doc in tq.tqdm(self.nlp.pipe(corpora, batch_size=batch_size, n_process=n_process), 
                                    leave=True,
                                    position=0,
                                    total=len(corpora)):


                
                match_i = []
                
                all_matches = matcher(doc)


                # we check for duplicates and append only
                # the unique ones to the match_i
                # then add all these matches to matches list
                if all_matches:
                    spans = [doc[s:e] for id_, s,e in all_matches]

                    for span in spacy.util.filter_spans(spans):
                        match_i.append(str(span))

                    matches.append(match_i)
                    passive_c.append(len(all_matches))
                    binaries.append(1)

                # if there were no matches
                else:
                    matches.append(None)
                    passive_c.append(0)
                    binaries.append(0)
                    

                i+=1

            end = time.process_time()
            
            # calculating the time taken
            taken_t = round(end-start, 2)

            if taken_t < 60:
                print('time taken: ', taken_t, ' s')
            else: print('time taken: ',  (taken_t)//60 , ' min ', round(taken_t%60, 1) , ' s')

            print('Detection is done!')

            return np.array(matches, dtype='object'), np.array(passive_c, dtype='object'), np.array(binaries, dtype='object')



        def match_sentence_level(self, matcher, df, colName, n_process = 1,
                                batch_size = 1000, add_other_columns=True):

            """
            finds matches based on sentences in all records and
            outputs a csv file with all the sentences in every document


            Parameters

            matcher: the matcher which has been initialized
            colName: name of the column with text
            level: whether the user wants corpus level or sentence level
            results
            n_process: number of cores to use can be any number
            between 1 and the maximum number of cores available
            (set it to -1 to use all the cores available)
            batch_size: give records in batches to the matcher
            record when passed
            add_other_columns: True\False whether or not to add the other columns 
            to the outputted dataframe
            """
            df = df.reset_index(drop=True)
            # create a list of the column we will process
            cleaned_corpus = df.loc[:, colName].values.tolist()

            # seperating sentences
            count_sents, all_sentences = self.detect_sents(cleaned_corpus, batch_size, n_process)

            # find indices required for the final dataset
            # based on the document and sentence index
            sent_indices, doc_indices = self.find_doc_idx(count_sents)

            matches, passive_c, binaries = self.find_matches(matcher, all_sentences, batch_size, n_process)
            

            s_output = pd.DataFrame(np.c_[doc_indices, sent_indices, all_sentences, binaries, matches, passive_c],
                        columns=['docId', 'sentenceId', 'sentence', 'binary', 'passive_match(es)', 'raw_passive_count'])


            passive_perc = len(s_output[s_output['raw_passive_count']>=1]) / len(s_output)
            
            print(f'The percentage of passive records: {passive_perc *100:.2f}')

            # now we have all the matches we just have to
            # create a dataframe for the results
            if add_other_columns==True:
                other_cols_df = self.add_other_cols(df, colName, count_sents)
                

                assert len(other_cols_df) == len(s_output)

                df_final = pd.concat([s_output, other_cols_df], axis = 1)
                return df_final

            else:
                return s_output


            




        def match_corpus_level(self, matcher, df, colName, n_process = 1,
            batch_size = 1000, add_other_columns=True,
            percentage_of_passive_sentences = True):

            """finds matches based on sentences in all records and
            outputs a csv file with all the sentences in every document


            Parameters

            matcher: the matcher which has been initialized
            colName: name of the column with text
            level: whether the user wants corpus level or sentence level
            results
            n_process: number of cores to use can be any number
            between 1 and the maximum number of cores available
            (set it to -1 to use all the cores available)
            batch_size: give records in batches to the matcher
            record when passed
            add_other_columns: True\False whether or not to add the other columns 
            to the outputted dataframe
            sentences to the output dataset
            """
            
            df = df.reset_index(drop=True)
            # create a list of the column we will process
            cleaned_corpus = df.loc[:, colName].values.tolist()

            if percentage_of_passive_sentences:

                s_output = self.match_sentence_level(matcher, df, colName, n_process = n_process,
                                batch_size = batch_size, add_other_columns=add_other_columns)
                matches = []
                passive_c = []
                binaries = []
                percentages = []
                count_sents = []
                count_p_sents = []


                for i in s_output.docId.unique():

                    rows = s_output[s_output['docId'] == i]

                    count_sents.append(len(rows))
                    count_p_s = sum(rows.binary)
                    count_p_sents.append(count_p_s)
                    percent =  count_p_s/ len(rows)
                    percentages.append(percent)



                    if any(rows.binary) == 1:
                        binaries.append(1)
                    else: binaries.append(0)

                    passives = [val for val in rows['passive_match(es)'].values if val!=None]
                    passives = list(chain.from_iterable(passives))
                    matches.append(passives)
                    passive_c.append(len(passives))

                passive_c = np.array(passive_c, dtype='object')
                matches = np.array(matches, dtype='object')
                percentages = np.array(percentages, dtype='object')
                binaries = np.array(binaries, dtype='object')
                count_sents = np.array(count_sents, dtype='object')
                cleaned_corpus = np.array(cleaned_corpus, dtype='object')
                count_p_sents = np.array(count_p_sents, dtype='object')

                assert len(cleaned_corpus) == len(binaries) == len(percentages) == len(matches) == len(passive_c) == len(count_p_sents)
                d_output = pd.DataFrame(np.c_[cleaned_corpus, binaries, matches, passive_c, count_p_sents, count_sents, percentages],
                                        columns=['document', 'binary', 'passive_match(es)', 'raw_passive_count', 'raw_passive_sents_count', 'raw_sentence_count', 'passive_sents_percentage' ])



            elif percentage_of_passive_sentences==False:
                matches, passive_c, binaries = self.find_matches(matcher, cleaned_corpus, batch_size, n_process)
                d_output = pd.DataFrame(np.c_[cleaned_corpus, binaries, matches, passive_c],
                                        columns=['Document', 'binary', 'passive_match(es)', 'raw_passive_count' ])

                print(f'The percentage of passive records: {passive_perc*100:.2f}')

            assert len(cleaned_corpus) == len(matches) == len(passive_c)

            

            passive_perc = len(d_output[d_output['raw_passive_count']>=1]) / len(d_output)


            # now we have all the matches we just have to
            # create a dataframe for the results
            if add_other_columns==True:

                # create a list of all the col names
                fields = df.columns.tolist()
                # remove colName
                del fields[fields.index(colName)]

                

                assert len(df[fields]) == len(d_output)

                d_output = pd.concat([d_output, df[fields]], axis = 1)
                

            


            
            return d_output



