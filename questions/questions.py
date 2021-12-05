import nltk
import sys
import os
import string
from math import log

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)



def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    filesDict = dict()
    files = os.listdir(directory)

    for fle in files:
        f = open(os.path.join(directory, fle), "r", encoding="cp437")
        contents = f.read()
        filesDict[fle] = contents

    return filesDict


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """

    tokens = nltk.word_tokenize(document)
    stopwords = nltk.corpus.stopwords.words('english')
    punctuation = list(string.punctuation)

    tokens = [token.lower() for token in tokens if token not in stopwords + punctuation]

    return tokens


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    idfs = dict()

    noOfDocuments = len(documents)

    #get a set of all the words in the document
    all_words = set()
    for filename in documents:
        all_words = all_words.union(documents[filename])

    #calculate idf for each word
    for word in all_words:
        count = sum(
            [1 for filename in documents if word in documents[filename]])
        idfs[word] = log(noOfDocuments/count)

    return idfs


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    topFiles = list(files.keys())
    tf = dict()
    
    for f in files:
        for word in files[f]:
            if (f, word) not in tf:
                tf[f, word] = 1
            else:
                tf[f, word] += 1

    #key function to sort according to tf-idf value
    def myfilter(f):
        score = 0
        for word in query:
            if word in files[f]:
                tf_idf = tf[f, word] * idfs[word]
                score += tf_idf
        return score

    topFiles.sort(reverse=True, key=myfilter)

    return topFiles[:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    topSentences = list()

    #calculate matching word measure and query term density
    for sentence in sentences:
        score = 0
        common = 0
        words = sentences[sentence]
        for word in query:
            if word in words:
                common += 1
                score += idfs[word]

        qtd = common / len(words)
        topSentences.append((sentence, score, qtd))

    #sort sentences according to matching word measure and query term density
    topSentences.sort(reverse=True, key=lambda t: (t[1], t[2]))
    matchSentences = topSentences[:n]

    return [sentence for sentence, score, qtd in matchSentences]

if __name__ == "__main__":
    main()
