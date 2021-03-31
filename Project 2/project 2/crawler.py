import logging
import re
from urllib.parse import urlparse, urljoin

import nltk

from corpus import Corpus
from lxml import html # to get html contents
from bs4 import BeautifulSoup


logger = logging.getLogger(__name__)

class Crawler:
    """
    This class is responsible for scraping urls from the next available link in frontier and adding the scraped links to
    the frontier
    """

    def __init__(self, frontier, corpus):
        self.frontier = frontier
        self.corpus = corpus
        self.linkCounter = 0  # count for links in a specific page
        self.currentMax = 0  # current max for links
        self.currentMaxLink = ''  # link for current link with max URLs
        self.downloadedList = []  # downloaded list of URLs
        self.trapList = []  # list of traps
        self.wordCount = {}  # dictionary of counted words
        self.longestPage = ''  # longest page string
        self.longestPageCounter = 0  # counter for page with most amount of words
        self.subDomainDict = {}

    def start_crawling(self):
        """
        This method starts the crawling process which is scraping urls from the next available link in frontier and adding
        the scraped links to the frontier
        """
        while self.frontier.has_next_url():
            url = self.frontier.get_next_url()
            logger.info("Fetching URL %s ... Fetched: %s, Queue size: %s", url, self.frontier.fetched, len(self.frontier))
            url_data = self.fetch_url(url)

            for next_link in self.extract_next_links(url_data):
                if self.corpus.get_file_name(next_link) is not None:
                    if self.is_valid(next_link):
                        self.frontier.add_url(next_link)

    def fetch_url(self, url):
        """
        This method, using the given url, should find the corresponding file in the corpus and return a dictionary
        containing the url, content of the file in binary format and the content size in bytes
        :param url: the url to be fetched
        :return: a dictionary containing the url, content and the size of the content. If the url does not
        exist in the corpus, a dictionary with content set to None and size set to 0 can be returned.
        """
        url_data = {
            "url": url,
            "content": None,
            "size": 0
        }
        return url_data

    def extract_next_links(self, url_data):
        """
        The url_data coming from the fetch_url method will be given as a parameter to this method. url_data contains the
        fetched url, the url content in binary format, and the size of the content in bytes. This method should return a
        list of urls in their absolute form (some links in the content are relative and needs to be converted to the
        absolute form). Validation of links is done later via is_valid method. It is not required to remove duplicates
        that have already been fetched. The frontier takes care of that.

        Suggested library: lxml
        """
        # html. is from the lxml library
        outputLinks = []
        if url_data['final_url']:
            if url_data['final_url'] not in self.subDomainDict:
                self.subDomainDict[url_data['final_url']] = 0
        else:
            if url_data['url'] not in self.subDomainDict:
                self.subDomainDict[url_data['url']] = 0

        soup = BeautifulSoup(url_data['content'], 'html.parser')  # parses html with beautiful soup instead of LXML

        filters = re.compile('[^A-Za-z]')  # filters words for counting
        tokenList = soup.get_text().lower()
        tokenList = nltk.word_tokenize(tokenList) # using NLTK library to tokenize recompiled words
        result = [re.split(filters, word) for word in tokenList]
        result = [j for i in result for j in i if j]

        if len(result) > self.longestPageCounter:  # checks for page with most amount of words
            self.longestPageCounter = len(result)
            self.longestPage = url_data['url']

        for word in result:  # places words into dictionary to keep track of how many of each word we see
            if word in self.wordCount:
                self.wordCount[word] += 1
            else:
                self.wordCount[word] = 1

        self.linkCounter = 0  # counter for how many links are on a specific page
        for link in soup.find_all('a'): # finding all 'a' tags with find_all function in beautiful soup library
            self.linkCounter = self.linkCounter + 1
            try:
                if url_data['final_url']:
                    url_result = urljoin(url_data['final_url'], link['href'])
                    self.subDomainDict[url_data['final_url']] += 1
                    outputLinks.append(url_result)
                else:
                    url_result = urljoin(url_data['url'], link['href'])
                    self.subDomainDict[url_data['url']] += 1
                    outputLinks.append(url_result)
            except:
                continue
        if self.linkCounter > self.currentMax:  # updates max link counter and url to be url with most ammount of links
            self.currentMax = self.linkCounter
            self.currentMaxLink = url_data['url']
        return outputLinks

    def is_valid(self, url):
        """
        Function returns True or False based on whether the url has to be fetched or not. This is a great place to
        filter out crawler traps. Duplicated urls will be taken care of by frontier. You don't need to check for duplication
        in this method
        """
        parsed = urlparse(url)
        if len(parsed.query) > 100:  # if too long throw it out
            self.trapList.append(url)
            return False
        if len(parsed.path) > 100:  # if too long throw it out
            self.trapList.append(url)
            return False
        if parsed.scheme not in ["http", "https"]:
            return False
        if parsed.fragment:  # not suppose to crawl pages with fragments
            self.trapList.append(url)
            return False
        if "~eppstein" in parsed.path and "pix" in parsed.path:  # filters out epsteins thousands of pics
            self.trapList.append(url)
            return False
        if "DeepCons" in parsed.path:  # filter out num.py from corpus that take way too long to parse
            self.trapList.append(url)
            return False
        if "rules" in parsed.path: # filter out rules and append it to trap list
            self.trapList.append(url)
            return False
        if "maven-contents.txt" in parsed.path:
            self.trapList.append(url)
            return False
        if "precision=second" in parsed.query:  # to filter out https://grape.ics.uci.edu/wiki/public/timeline?from=2018-11-21T08%3A52%3A24-08%3A00&precision=second
            self.trapList.append(url)
            return False
        if "ml/datasets" in parsed.path and "view=table" in parsed.query:  # to filter out https://archive.ics.uci.edu/ml/datasets.html?format=&task=other&att=cat&area=&numAtt=&numIns=&type=uvar&sort=taskUp&view=table
            self.trapList.append(url)
            return False
        if "difftype=sidebyside" in parsed.query:  # to filter out https://swiki.ics.uci.edu/doku.php/start?do=diff&rev2%5B0%5D=1467224066&rev2%5B1%5D=1478024862&difftype=sidebyside
            self.trapList.append(url)
            return False

        try:
            result = ".ics.uci.edu" in parsed.hostname \
                     and not re.match(".*\.(css|js|bmp|gif|jpe?g|ico" + "|png|tiff?|mid|mp2|mp3|mp4" \
                                      + "|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf" \
                                      + "|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso|epub|dll|cnf|tgz|sha1" \
                                      + "|thmx|mso|arff|rtf|jar|csv" \
                                      + "|rm|smil|wmv|swf|wma|zip|rar|gz|pdf)$", parsed.path.lower())
            if result:  # if true add url to downloaded list
                self.downloadedList.append(url)
                return result
            else:
                return result

        except TypeError:
            # print("TypeError for ", parsed)
            return False


