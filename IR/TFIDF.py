from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from ReadStopwords import ReadStopwords
import numpy as np

class TFIDF:

    def __init__(self, doclist):
        self.stopwords = ReadStopwords().get_stopwords()
        self.doclist = doclist

    def get_matrix(self):
        vectorizer = CountVectorizer()
        #print '1'
        transformer = TfidfTransformer()
        #print '2'
        tfidf = transformer.fit_transform(
            vectorizer.fit_transform(self.doclist))
        #print '3'
        word = vectorizer.get_feature_names()
        #print '4'
        weight = tfidf.toarray().T
        #for i in range(len(weight[0])):
        #    print "-----", i , "doc 's term weight------"
        #    for j in range(len(word)):
        #        print word[j], weight[j][i]
        # weight[i][j] -- the weight of word i in doc j
        return [word, weight]

if __name__ == "__main__":
    doclist = [["word list is a word anela, nerwoer"],["abc ef"]]
    stopwords = ReadStopwords().get_stopwords()
    test = TFIDF(doclist)
    [word, weightmatirx] = test.get_matrix()
    print weightmatirx
    print "term - doc"
    print np.zeros(len(word))
    #print weightmatirx.T
    #print LA.norm(weightmatirx)