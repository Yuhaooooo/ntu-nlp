import pandas as pd
import re
import spacy
import random
from os.path import join
from nltk.tokenize import sent_tokenize
from collections import Counter
nlp = spacy.load("en_core_web_sm")

def selectNBusinessId(df, seed=4, numberOfBusineesId=5):

    business_id_list = df.business_id.values.tolist()
    random.Random(4).shuffle(business_id_list)

    df_5 = df[df.business_id.isin(business_id_list[:numberOfBusineesId])]

    bs_text_map = dict()
    for bid in business_id_list[:numberOfBusineesId]:
        bs_text_map[bid] = df_5[df_5['business_id'] == bid].text.tolist()

    print('\n\n{} Selecting {} business ID {}\n'.format('-'*20, numberOfBusineesId, '-'*20))

    for b in bs_text_map.keys():
        print('Business ID: ' ,b)
    
    return bs_text_map

class NounAndAdjPair:
    
    patterns=['(ADJ )*(NOUN )+(ADV )*(VERB )+(ADV )*ADJ ', # The Korean grill is good
              '(NOUN )+.*PRON (VERB )+(ADV )*ADJ ', # I like the food, which is good
              '(ADV )*ADJ (NOUN )+', # good service
             ]
    
    def __init__(self, doc, withExtra=False):
        
        def getDoc():
            return re.sub(' +', ' ', self.original_doc.replace('\n', ' ').strip()).lower()
        
        def getOriginalSentences():
            return [s for s in sent_tokenize(self.doc)] #nltk tokenizer

        def getSentences():
            return [' '.join([w.text for w in nlp(s)]) for s in self.original_sentences] # spacy word tokenizer

        def getTaggings():
            return [' '.join([w.pos_ for w in nlp(s)])+' ' for s in self.original_sentences]  
        
        self.withExtra = withExtra
        self.original_doc = doc
        self.doc = getDoc()
        self.original_sentences = getOriginalSentences()
        self.sentences = getSentences()
        self.taggings = getTaggings()
#         print(len(self.sentences), len(self.taggings))

    def getPairsWithFSA(self, returnOnlyPairs=False, returnInDf=False):
        
        def checkIfAdjAndNounExists(tagging):
            if 'ADJ' in tagging and 'NOUN' in tagging:
                return True
            return False
        
        def getWoldsByTaggingIndex(target_tagging_index, no_sentence, no_pattern):
            
            original_sentence = self.sentences[no_sentence]
            original_tagging = self.taggings[no_sentence].strip()
            
            baseIndex = 0 if target_tagging_index[0]==0 else len(original_tagging[:target_tagging_index[0]].strip().split(' '))
            buildIndex = len(original_tagging[target_tagging_index[0]:target_tagging_index[1]].strip().split(' '))
            
            trimmed_tagging_list = original_tagging.strip().split(' ')[baseIndex: baseIndex+buildIndex]
            trimmed_sentence_list = original_sentence.split(' ')[baseIndex: baseIndex+buildIndex]
            
            noun_adj_pair = []
            
            
            if no_pattern==0: # the first pattern
                if self.withExtra:
                    last_verb_index = len(trimmed_tagging_list)-trimmed_tagging_list[::-1].index('VERB')-1
                    for i in range(len(trimmed_tagging_list)):
                        if trimmed_tagging_list[i] not in ['ADJ', 'NOUN']: #filter out adv
                            break        
                    noun_adj_pair.append(' '.join(trimmed_sentence_list[:i]))
                    noun_adj_pair.append(' '.join(trimmed_sentence_list[last_verb_index+1:]))
                else:
                    noun_adj_pair.append(' '.join([trimmed_sentence_list[i] for i in [i for i, t in enumerate(trimmed_tagging_list) if t == "NOUN"]]))
                    noun_adj_pair.append(trimmed_sentence_list[-1])
                    
                
            elif no_pattern==1:
                if self.withExtra:
                    last_noun_end_index = len(trimmed_tagging_list)-trimmed_tagging_list[::-1].index('NOUN')-1
                    last_noun_start_index = last_noun_end_index
                    for i in range(last_noun_end_index, 0, -1):
                        if trimmed_tagging_list[i]=='NOUN':
                            last_noun_start_index = i
                        else:
                            break

                    last_verb_index = len(trimmed_tagging_list)-trimmed_tagging_list[::-1].index('VERB')-1

                    noun_adj_pair.append(' '.join(trimmed_sentence_list[last_noun_start_index:last_noun_end_index+1]))
                    noun_adj_pair.append(' '.join(trimmed_sentence_list[last_verb_index+1:]))
                else:
                    noun_index = [i for i, t in enumerate(trimmed_tagging_list) if t == "NOUN"][::-1]
                    if len(noun_index)==1:
                        noun_adj_pair.append(' '.join([trimmed_sentence_list[i] for i in noun_index]))
                    else:
                        for noun_start_index in range(1, len(noun_index)):
                            if noun_index[noun_start_index]!=noun_index[noun_start_index-1]-1:
                                break
                        noun_adj_pair.append(' '.join([trimmed_sentence_list[i] for i in noun_index[:noun_start_index][::1]]))
                    noun_adj_pair.append(trimmed_sentence_list[-1])
                    
                    
            elif no_pattern==2:
                if self.withExtra:
                    noun_index = trimmed_tagging_list.index('NOUN')
                    noun_adj_pair.append(' '.join(trimmed_sentence_list[noun_index:]))
                    noun_adj_pair.append(' '.join(trimmed_sentence_list[:noun_index]))
                else:
                    noun_adj_pair.append(' '.join([trimmed_sentence_list[i] for i in [i for i, t in enumerate(trimmed_tagging_list) if t == "NOUN"]]))
                    noun_adj_pair.append(trimmed_sentence_list[trimmed_tagging_list.index('ADJ')])
                    
            
            return tuple(noun_adj_pair)
        
        
        def formDf(sentence_adjNoun_pair):
            df = pd.DataFrame(columns=['Sentence', 'AdjNounPair'])
            pd.set_option('display.max_colwidth', -1)
            df.Sentence, df.AdjNounPair = list(sentence_adjNoun_pair.keys()), list(sentence_adjNoun_pair.values())
            return df
        
        sentence_adjNoun_pair = dict(zip(self.sentences, [[] for i in range(len(self.sentences))]))
        
        for i in range(len(self.sentences)):
            s = self.sentences[i]
            t = self.taggings[i]
            
            if checkIfAdjAndNounExists(t):
                for p in self.patterns:
                    for x in re.finditer(p, t):
                        sentence_adjNoun_pair[s].append(getWoldsByTaggingIndex(x.span(), i, self.patterns.index(p)))
                        
        if returnOnlyPairs:
            pairs = []
            for p in sentence_adjNoun_pair.values():
                pairs.extend(p)
            return pairs
                        
        if returnInDf:
            return formDf(sentence_adjNoun_pair)
            
        return sentence_adjNoun_pair

def getPairs(bs_text_map, numberOfPairs=5, returnInDf=True):

    bs_pair_map = dict(zip(list(bs_text_map.keys()), [[] for i in range(len(list(bs_text_map.keys())))]))

    print('\n{} Getting pairs {}\n'.format('-'*25, '-'*25))

    for b in list(bs_pair_map.keys()):
        print('Processing reviews from business ID: {} ...'.format(b))
        docs = bs_text_map[b]
        for doc in docs:
            doc_nlp = NounAndAdjPair(doc)
            bs_pair_map[b].extend(doc_nlp.getPairsWithFSA(returnOnlyPairs=True))
        
    

    for bs in list(bs_pair_map.keys()):
        keys = list(Counter(bs_pair_map[bs]).keys())# equals to list(set(words))
        values = list(Counter(bs_pair_map[bs]).values())
        keys_index = sorted(range(len(values)), key=lambda k: values[k], reverse=True)
        bs_pair_map[bs] = [(keys[i], values[i]) for i in keys_index[:numberOfPairs]]

    if returnInDf:
        df = pd.DataFrame(columns=['BusinessId', 'AdjNounPair'])
        df.BusinessId, df.AdjNounPair = list(bs_pair_map.keys()), list(bs_pair_map.values())
        return df

    return bs_pair_map


if __name__ == "__main__":

    df = pd.read_csv(join('..','..','data','data.csv'))

    BusinessPairs = getPairs(selectNBusinessId(df), returnInDf=False)
    
    print('\n\n\n{} RESULT {}\n\n'.format('-'*28, '-'*28))

    for b, p in BusinessPairs.items():
        print(b, ':\n', p, '\n')




