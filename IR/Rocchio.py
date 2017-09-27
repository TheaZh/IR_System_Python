from GoogleSearch import GoogleSearch
from TFIDF import TFIDF
import numpy as np
import re

class Rocchio:
    # Rocchio's Algorithm
    def __init__(self):

        self.ALPHA = 1.0
        self.BETA = 0.75
        self.GAMMA = 0.15

    def rocchio_algorithm(self, new_query):
        # search from Google
        raw_query = new_query.lower()
        self.query_word = re.findall("\w+", raw_query) # a list contains each word of query
        self.query = ' '.join(self.query_word)
        google_search = GoogleSearch()
        google_search.search(self.query)

        # all_doc_list : [ relevant_doc  |  non_relevant_doc ]
        all_doc_list = google_search.doc[:]
        #print "----- get whole doc ------"
        #for d in all_doc_list:
        #    print d
        #print "--------------------------"
            # the first rel_num columns is about relevant doc
        rel_num = len(google_search.relevant_doc)

        # calculate tf-idf
        tf_idf = TFIDF(all_doc_list)
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
        q_tf_idf = TFIDF(tmp)
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
        for term in sorted_term:
            if count_new>0 and term not in self.query_word:
                new_query.append(term)
                count_new -=1
            if term in self.query_word and limit>0:
                new_query.append(term)
                limit -=1
                self.query_word.remove(term)
            if count_new==0:
                break
        new_query.extend(self.query_word)
        self.query = ' '.join(new_query)
        return self.query




'''
    debug
'''
if __name__ == "__main__":
    app = Rocchio()
    query = raw_input("Query: ").lower()
    for i in range(0,3):
        print query
        app.rocchio_algorithm(new_query=query)
        query = app.get_new_query()


