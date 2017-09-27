from googleapiclient.discovery import build
import re

class GoogleSearch:

    def __init__(self):
        self.API_KEY = "AIzaSyBpMdM3c6XYISNPICI0qEdEECtRo5gemqA"
        self.ENGINE_KEY = "018258045116810257593:z1fmkqqt_di"
        self.doc = []
        self.relevant_doc = [] # relevant docs, each list is the content of the doc
        self.non_relevant_doc = [] # non-relevant docs

    def search(self, query):
        # query is a string list of query word (eg. ["a", "b", "c"]
        service = build("customsearch", "v1", developerKey=self.API_KEY)
        res = service.cse().list(q=query, cx=self.ENGINE_KEY,).execute()

        for item in res['items']:
            print 'title: ', item['title']
            print 'URL: ', item['displayLink']
            print 'Snippet: ', item['snippet']

            # convert to split word list which contains all words in the doc
            tmp = item['title'].lower() + ' ' + item['snippet'].lower()
            wordlist = self.get_wordlist(tmp)
            #self.doc.append(wordlist)

            # user enter Y/N to determine whether this is relevant
            if_relevant = raw_input("Relevant: ").lower()
            if if_relevant == 'yes':
                self.relevant_doc.append(wordlist)
            else:
                self.non_relevant_doc.append(wordlist)
            print '------------------------'
        self.get_all_term()

    def get_wordlist(self,word_string):
        word_list = re.findall("\w+",word_string)
        word_in_doc = ' '.join(word_list)
        return word_in_doc

    def get_all_term(self):
        # self.doc = [ relevant_doc  |  non_relevant_doc ]
        self.doc = self.relevant_doc[:]
        self.doc.extend(self.non_relevant_doc)






'''
    debug
'''
if __name__ == '__main__':
    test = GoogleSearch()
    test.search("java")
    test.get_all_term()
    print test.doc
    print '+++++++++++++++++++++++++++'
    for d in test.doc:
        print d

