# Hootan Hosseinzadeganbushehri



import os
from bs4 import BeautifulSoup
import collections
from nltk.tokenize import RegexpTokenizer
import pickle




def extract_name_tag(path ,extract_html):

    t_list = list()
    tokenizer = RegexpTokenizer(r'\w+')
    soup_remove_tag = extract_html(["style","script"])
    for remove_text in soup_remove_tag:
        remove_text.decompose()
    body_tag = extract_html.find_all('body')
    body_tag += extract_html.find_all('head')
    for item in body_tag:
        words = tokenizer.tokenize(item.text)
        for w in words:
            if((w in sw_list) == False):
                t_list.append(w.lower())
    count_dict = collections.defaultdict(int)
    for i in t_list:
        count_dict[i] += 1
    for key, val in count_dict.items():
        w_score = 0
        t_tuple = (path, val,w_score)
        inverted_index_dict[key].append(t_tuple)



    h1_tag = extract_html.find_all('h1')
    t_list = list()
    for item in h1_tag:
        words = tokenizer.tokenize(item.text)
        for w in words:
            if((w in sw_list) == False):
                t_list.append(w.lower())
    count_dict = collections.defaultdict(int)
    for key in t_list:
        if key in inverted_index_dict.keys():
            count = 0
            for doc in inverted_index_dict[key]:
                if doc[0] == path:
                    w_score = 4
                    w_score += doc[2]
                    t_tuple = (path,doc[1],w_score)
                    inverted_index_dict[key][count] = t_tuple
                count += 1

    h2_tag = extract_html.find_all('h2')
    t_list = list()
    for item in h2_tag:
        words = tokenizer.tokenize(item.text)
        for w in words:
            if((w in sw_list) == False):
                t_list.append(w.lower())
    count_dict = collections.defaultdict(int)
    for key in t_list:
        if key in inverted_index_dict.keys():
            count = 0
            for doc in inverted_index_dict[key]:
                if doc[0] == path:
                    w_score = 3
                    w_score += doc[2]
                    t_tuple = (path,doc[1],w_score)
                    inverted_index_dict[key][count] = t_tuple
                count += 1

    strong_tag = extract_html.find_all('strong')
    t_list = list()
    for item in strong_tag:
        words = tokenizer.tokenize(item.text)
        for w in words:
            if((w in sw_list) == False):
                t_list.append(w.lower())
    count_dict = collections.defaultdict(int)
    for key in t_list:
        if key in inverted_index_dict.keys():
            count = 0
            for doc in inverted_index_dict[key]:
                if doc[0] == path:
                    w_score = 2
                    w_score += doc[2]
                    t_tuple = (path,doc[1],w_score)
                    inverted_index_dict[key][count] = t_tuple
                count += 1
            

    b_tag = extract_html.find_all('b')
    t_list = list()
    for item in b_tag:
        words = tokenizer.tokenize(item.text)
        for w in words:
            if((w in sw_list) == False):
                t_list.append(w.lower())
    count_dict = collections.defaultdict(int)
    for key in t_list:
        if key in inverted_index_dict.keys():
            count = 0
            for doc in inverted_index_dict[key]:
                if doc[0] == path:
                    w_score = 1
                    w_score += doc[2]
                    t_tuple = (path,doc[1],w_score)
                    inverted_index_dict[key][count] = t_tuple
                count += 1         
        
        

if __name__ == '__main__':

    st = open("stopwords.txt", 'r')
    sw_read = st.read()
    sw_list = sw_read.split('\n')
    st.close()
    inverted_index_dict = collections.defaultdict(list)
    file_names = os.walk("/users/hootan/downloads/WEBPAGES_RAW")
    for sub_dir in file_names:
        for f in sub_dir[2]:
            path = sub_dir[0]+ "/" + f
            opened_f = open(path, encoding = "utf-8")
            read_f = opened_f.read().lower()
            extract_html = BeautifulSoup(read_f , "lxml")
            extract_name_tag(path ,extract_html)
            opened_f.close()
    dir_path = str(os.getcwd() + '\inverted_index.pickle')
    with open(dir_path, 'wb') as f:
        pickle.dump(inverted_index_dict, f)
    f.close()
    