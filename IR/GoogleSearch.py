from googleapiclient.discovery import build
import re

class GoogleSearch:

    def __init__(self,google_api, engine_key):
        self.API_KEY = google_api
        self.ENGINE_KEY = engine_key
        self.doc = []
        self.right = 0
        self.relevant_doc = [] # relevant docs, each list is the content of the doc
        self.non_relevant_doc = [] # non-relevant docs

    def search(self, query, lowest_precision):
        # query is a string list of query word (eg. ["a", "b", "c"]
        service = build("customsearch", "v1", developerKey=self.API_KEY)
        res = service.cse().list(q=query, cx=self.ENGINE_KEY,).execute()

        print "Parameters:"
        print "Client Key = ", self.API_KEY
        print "Engine Key = ", self.ENGINE_KEY
        print "Query      = ", query
        print "Precision  = ", lowest_precision
        print "Google Search Results:"
        print "======================"
        index = 1
        for item in res['items']:
            print 'Result ', index
            index += 1
            print '['
            print ' URL: ', item['displayLink']
            print ' Title: ', item['title']
            print ' Summary: ', item['snippet']
            print ']\n'

            # convert to split word list which contains all words in the doc
            tmp = item['title'].lower() + ' ' + item['snippet'].lower()
            wordlist = self.get_wordlist(tmp)
            #self.doc.append(wordlist)

            # user enter Y/N to determine whether this is relevant
            if_relevant = raw_input("Relevant (Y/N)? ").lower()
            if if_relevant == 'y':
                self.relevant_doc.append(wordlist)
                self.right +=1
            else:
                self.non_relevant_doc.append(wordlist)
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

