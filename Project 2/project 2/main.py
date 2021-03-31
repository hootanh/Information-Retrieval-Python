import atexit
import logging
import sys

from nltk.corpus import stopwords

from corpus import Corpus
from crawler import Crawler
from frontier import Frontier

if __name__ == "__main__":
    # Configures basic logging
    logging.basicConfig(format='%(asctime)s (%(name)s) %(levelname)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',
                        level=logging.INFO)

    # Instantiates frontier and loads the last state if exists
    frontier = Frontier()
    frontier.load_frontier()

    # Instantiates corpus object with the given cmd arg
    corpus = Corpus()

    # Registers a shutdown hook to save frontier state upon unexpected shutdown
    atexit.register(frontier.save_frontier)

    # Instantiates a crawler object and starts crawling
    crawler = Crawler(frontier, corpus)
    crawler.start_crawling()
    f1 = open("downloadedList.txt", "w+")
    f2 = open("trapList.txt", "w+")
    f3 = open("wordCount.txt", "w+")
    f4 = open("longestPage.txt", "w+")
    f5 = open("mostLinks.txt", "w+")
    f6 = open("subDomainCount.txt", "w+")
    for link in crawler.downloadedList:
        f1.write(str(link) + "\n")
    for link in crawler.trapList:
        f2.write(str(link) + "\n")

    stop_words = set(stopwords.words('english'))
    for k, v in list(crawler.wordCount.items()):
        if k in stop_words:
            if k in crawler.wordCount:
                del crawler.wordCount[k]
        if len(k) == 1:
            if k in crawler.wordCount:
                del crawler.wordCount[k]

    result = sorted(crawler.wordCount.items(), key=lambda x: (x[1], x[0]))
    result = sorted(result, key=lambda x: x[1], reverse=True)

    counter = 0
    for i in result:
        f3.write(str(i) + "\n")
        counter += 1
        if counter == 51:
            break
    f4.write("Longest page = " + str(crawler.longestPage))
    f5.write("Page with the most links = " + str(crawler.currentMaxLink))
    for j, k in crawler.subDomainDict.items():
        f6.write(str(j) + " " + str(k) + "\n")
    f1.close()
    f2.close()
    f3.close()
    f4.close()
    f5.close()
    f6.close()