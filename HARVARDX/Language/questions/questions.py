from re import T
import nltk
from nltk.tokenize import word_tokenize
import sys
import os
import math
import collections

FILE_MATCHES = 1
SENTENCE_MATCHES = 3


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
        for passage in files[filename]:
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
    print('loading data...')
    files = {}
    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        with open(file_path) as f:
            files[file] = f.readlines()
    print('success ;) ')
    return files


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    stringed_doc = ''.join([str(item) for item in document])
    stringed_doc = stringed_doc.lower()
    tokens = word_tokenize(stringed_doc)
    words = []
    for word in tokens:
        if word.isalpha() and word != "https":
            words.append(word)
    return words


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    IDF = {}
    total_docs = len(documents)
    # idf(word) = log(total documents / docs containing word)
    # math.log
    #iterate and add found words
    for doc in documents:
        found_words = set()
        for word in documents[doc]:
            if word in documents[doc]:
                found_words.add(word)
        #assign found word to the dict
        for word in found_words:
            if word in IDF:
                IDF[word] += 1
            else:
                IDF[word] = 1
    #compute the idf value
    for word in IDF:
        IDF[word] = math.log(total_docs/IDF[word])
    #return the dict with words and idf value
    return IDF


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    #create a dictionary that maps file with idfs scoring 
    #file scoring would be the sum of all the scores of all the words that appear in the query
    #to compute the scoring of a word multiply the idf ( which already know ) to its tf ( which we have to compute)
    query_files = {}
    # file1: [word_score, word_score, word_score...], file2:scoring.... 
    for doc in files:
        scoring = []
        for word in query:
            if word in files[doc]:
                #compute its tf scoring
                frequency = collections.Counter(files[doc])
                tf = frequency[word]
                #find words idf scoring
                idfscore = float(idfs[word])
                #compute its tf-idf
                tf_ids = tf*idfscore
                if tf_ids != 0:
                    scoring.append(tf_ids)
            #compute file's 
        query_files[doc] = scoring
    #print(query_files)
    for doc in files:
        query_files[doc] = float(sum(query_files[doc]))
    top_files = dict(sorted(query_files.items(), key=lambda item: item[1]))
    top = list(top_files.keys())
    top.reverse()
    #print(top_files
    return top[:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    #print(sentences)
    query_sentences = {}
    word_density = {}
    for sentence in sentences:
        for word in query:
            scoring = []
            density = []
            if word in sentences[sentence]:
                #find words' idf scoring
                idfscore = float(idfs[word])
                scoring.append(idfscore)
        query_sentences[sentence] = scoring

    for sentence in sentences:
        #calculate word density
        word_density = len(query_sentences[sentence])/len(sentence)
        #word_density[sentence] = [word_density]
        #TypeError: 'float' object does not support item assignment
        query_sentences[sentence] = float(sum(query_sentences[sentence]))
    top_sentences = dict(sorted(query_sentences.items(), key=lambda item: item[1]))
    #check if there are two with the same scoring
    #choose the one with the highest word density
    top = list(top_sentences.keys())
    top.reverse()
    return top[:n]


if __name__ == "__main__":
    main()
