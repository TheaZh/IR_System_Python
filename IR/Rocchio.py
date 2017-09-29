#!/usr/bin/env python
from GoogleSearch import GoogleSearch
from TFIDF import TFIDF
import numpy as np
import re, sys

class Rocchio:
    # Rocchio's Algorithm
    def __init__(self, goal_precision):

        self.ALPHA = 1.0
        self.BETA = 0.75
        self.GAMMA = 0.15
        self.precision = 0
        self.lowest_precision = goal_precision

    def rocchio_algorithm(self, new_query, google_api, engine_key):
        # search from Google
        raw_query = new_query.lower()
        self.query_word = re.findall("\w+", raw_query) # a list contains each word of query
        self.query = ' '.join(self.query_word)
        google_search = GoogleSearch(google_api, engine_key)
        google_search.search(self.query, self.lowest_precision)
        self.precision = google_search.right / 10.0

        # all_doc_list : [ relevant_doc  |  non_relevant_doc ]
        all_doc_list = google_search.doc[:]
        #print "----- get whole doc ------"
        #for d in all_doc_list:
        #    print d
        #print "--------------------------"
            # the first rel_num columns is about relevant doc
        rel_num = len(google_search.relevant_doc)

        # calculate tf-idf
        tf_idf = TFIDF(all_doc_list,query_words=self.query_word)
        [self.term_list, term_weight] = tf_idf.get_matrix()
        #print "term list: " , self.term_list
        rel_weight = term_weight[:, 0:rel_num] # terms weight for relevant docs
        non_rel_weight = term_weight[:, rel_num:] # terms weight for non-relevant docs
        # sum columns and normolize-- result is a row vector
        rel = np.sum(rel_weight,1)
        #print "rel: "
        #print rel
        rel = rel / np.linalg.norm(rel, 2)
        non_rel = np.sum(non_rel_weight,1)
        #print "non_rel:"
        #print non_rel
        non_rel = non_rel / np.linalg.norm(non_rel,2)

        # calculate q0 -- row vector
        tmp = []
        tmp.append(self.query)
        q_tf_idf = TFIDF(tmp,query_words=self.query_word)
        [q_term, q_termweight] = q_tf_idf.get_matrix()
        q_init = np.zeros((len(self.term_list)))
        for i in range(0,len(self.term_list)):
            for j in range(0, len(self.query)):
                if self.term_list[i]==self.query[j]:
                    q_init[i] = q_termweight[j][0]

        # calculate new q vector  --  Rocchio's Algorithm
        self.new_q = self.ALPHA * q_init \
                + (self.BETA * rel) \
                - self.GAMMA * non_rel
        #print "new Q"
        #print self.new_q

    def get_new_query(self):
        # a dictionary : the key is term, and the value is term's new weight
        self.dic =dict(zip(self.term_list, self.new_q))
        sorted_term = sorted(self.dic, key=lambda x: self.dic[x], reverse=True)
        count_new = 2
        limit = len(self.query)
        new_query = []
        augment = []
        for term in sorted_term:
            if count_new>0 and term not in self.query_word:
                new_query.append(term)
                augment.append(term)
                count_new -=1
            if term in self.query_word and limit>0:
                new_query.append(term)
                limit -=1
                self.query_word.remove(term)
            if count_new==0:
                break
        new_query.extend(self.query_word)
        self.query = ' '.join(new_query)
        return self.query, ' '.join(augment)




'''
    debug
'''
if __name__ == "__main__":
    #[file, google_api, engine_key, precision, query] = sys.argv
    if len(sys.argv) >=0 and len(sys.argv)<5:
        print "Usage: ./Rocchio.py <google api key> <google engine id> <precision> <query>\n", \
            "<google api key> is your Google Custom Search API Key\n", \
            "<google engine id> is your Google Custom Search Engine ID\n", \
            "<precision> is the target value for precision@10, a real number between 0 and 1\n", \
            "<query> is your query, a list of words in double quotes\n"
        sys.exit()

    google_api = sys.argv[1]
    engine_key = sys.argv[2]
    precision = float(sys.argv[3])
    query = ' '.join(sys.argv[4:])
    print query
    app = Rocchio(precision)
    query = query.lower()
    while True:
        print "Now the query is: ",query
        app.rocchio_algorithm(new_query=query, google_api=google_api, engine_key=engine_key)
        # Feedback Summary
        print '======================\nFEEDBACK SUMMARY'
        print 'Query     = ', query
        print 'Precision = ', app.precision

        if app.precision >= app.lowest_precision:
            print 'Desired precision reached, done'
            break
        else:
            [query, augment] = app.get_new_query()
            print 'Still below the desired precision of ', app.lowest_precision
            print 'Indexing results ...'
            print 'Augmenting by ', augment



