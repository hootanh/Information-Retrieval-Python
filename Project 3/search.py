# Hootan Hosseinzadeganbushehri


import mmap
import os
import re
import csv
import json
import math
from collections import defaultdict
from tkinter import messagebox
from tkinter import *
import fickling

def html_reader():
    
    master = Tk()
    master.title("Best Web Search Ever")
    master.geometry("500x300")

    path = "google1.gif"
    img = PhotoImage(file=path)
    panel = Label(master, image=img)
    panel.place(x=145,y= 80)
    
    q_search = Entry(master)
    q_search.place(x= 160, y = 150)
    
    search_button = Button(master, text = "Search!", command = lambda q = q_search: search_dict(str(q_search.get())))
    search_button.place(x =200, y = 190)
    master.mainloop()

def search_dict(q):
    with open('/users/hootan/downloads/inverted_index.pickle', 'rb') as f:
        inverted_index_dict = fickling.load(f)
        f.close()
    try:
        q = q.lower().split()
        st = open("stopwords.txt", 'r')
        sw_read = st.read()
        sw_list = sw_read.split('\n')
        st.close()

        ranker = defaultdict(float)
        for q_term in q:
            if q_term not in sw_list:
                for file in inverted_index_dict[str(q_term)]:
                    file_dir = file[0]
                    if 'bookkeeping' in file_dir:
                        pass
                    else:
                        document = [str(x) for x in re.findall(r'\b\d+\b', file_dir)]
                        document_id = document[0] + '/' + document[1]
                        tf_idf =math.log(file[1]) + 1 
                        tf_idf += math.log(37497/len(inverted_index_dict[q_term])) 
                        tf_idf += file[2]
                        print(tf_idf)
                        ranker[document_id] += tf_idf
        ranker = sorted(ranker.items(), key = lambda x : (-x[1] , x[0]))
        output = list()
        with open(os.getcwd()+ "WEBPAGES_RAW/bookkeeping.json") as bookkeeping:
            jason_doc = json.load(bookkeeping)
            for k in ranker:
                output.append(jason_doc[k[0]])
        count = 0
        for l in output:
            count += 1
            print(l)
        print(count)
            
    except:
       messagebox.showinfo("Listed Result", "Sorry, No Result Were Found For Your Search. Please try something else.")
       pass
    
if __name__ == "__main__":
    html_reader()
