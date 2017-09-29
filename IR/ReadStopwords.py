class ReadStopwords:

    def __init__(self):
        self.stopwords = []

    def get_stopwords(self, query_words):
        f = open("./proj1-stopword.txt", "r")
        lines = f.readlines()
        for line in lines:
            #print line,
            if line.strip('\n') not in query_words:
                self.stopwords.append(line.strip('\n'))
        #print self.stopwords
        return self.stopwords


'''
 # debug
if __name__ == "__main__":
    test = ReadStopwords()
    test.get_stopwords("./proj1-stopword.txt")
'''
