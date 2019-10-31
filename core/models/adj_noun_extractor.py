# conda install spacy
# pip install bert_score
import collections
import json
import spacy

from bert_score import score


def pos_tagging(text):
    adj_list = []
    noun_list = []

    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)

    for token in doc:
        if token.pos_ == 'ADJ':
            adj_list.append(token.text)
        elif token.pos_ == 'NOUN':
            noun_list.append(token.text)
    
    return adj_list, noun_list



def read_a_business(review_list):

    most_useful_adj_list = collections.Counter()
    most_useful_noun_list = collections.Counter()

    for text in text_list:
        adj_list, noun_list = pos_tagging(text)
        P_noun, _, _ = score(noun_list, len(noun_list)*[text], "bert-base-uncased")
        P_adj, _, _  = score(adj_list, len(adj_list)*[text], "bert-base-uncased")

        most_useful_adj_list.update(P_adj.index(max(P_adj)))
        most_useful_noun_list.update(P_noun.index(max(P_noun)))

    return most_useful_adj_list, most_useful_noun_list


def read_all_businesses(business_id_list):


    adj_lists = []
    noun_lists = []

    file_path = os.path.join("data", "reviewSelected100.json")


    json_list = json.loads(file_path)

    business_id_list = ['8Z72HW5ydzQFydUxZglurg',
                        'QeEQXdto_4wFRaNKyIygRA',
                        'IUMyUYOIR9UQ7XGIEQKOuA',
                        'Rii85bzYKGC9P0zOyAem6A',
                        'i-2OzvZUDtvKCMq1vcRSZg']

    business_id_list_dict = dict(zip(business_id_list, []))

    for json_element in json_list:
        if json_element['review_id'] in business_id_list:
            business_id_list_dict[json_element['review_id']].append(json_element['text'])


    for business_id in business_id_list:
        review_list = business_id_list_dict[business_id]
        adj_list, noun_list = read_a_business(review_list)

        adj_lists[business_id] = adj_list
        noun_lists[business_id] = noun_list


    for business_id in business_id_list:
        for word, count in adj_lists[business_id].most_common(5):
            print(word, count)

        for word, count in noun_lists[business_id].most_common(5):
            print(word, cound)

