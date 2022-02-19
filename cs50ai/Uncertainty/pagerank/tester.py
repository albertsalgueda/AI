import collections
import functools
import operator
import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000

def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    #With probability damping_factor, the random surfer should randomly choose one of the links from page with equal probability.
    #divide damping_factor into all the keys except its current page
    thekeys = list(corpus.keys())
    thedict = dict.fromkeys(thekeys,0)
    linked_pages = list(corpus[page])
    #print(linked_pages)
    for i in range(len(corpus[page])):
        prob = damping_factor/len(linked_pages)
        for page in thedict:
            if page in linked_pages:
                thedict[page] = prob
        #prob_distribution[corpus[page][i]] = prob
#With probability 1 - damping_factor, the random surfer should randomly choose one of all pages in the corpus with equal probability.
    second_prob = (1-damping_factor)/len(thedict)
    for page in thedict:
        thedict[page] = round((thedict[page] + second_prob),4)
    #print(thedict)
    return thedict

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    samples = []
    
    for i in range(n):
        random_page = random.randint(0,(len(corpus)-1))
        corpus_keys = list(corpus.keys())
        page = corpus_keys[random_page]
        samples.append(transition_model(corpus,page,damping_factor)) #list of dictionaries
    #pageRank = dict.fromkeys(corpus_keys,0)
    #print(pageRank)
    #print(samples)
    #print(pageRank)
    #sum list of dictionaries with the same key 
    pageRank = dict(functools.reduce(operator.add,
         map(collections.Counter, samples)))
    #divide all values x n
    a = {k: round((v / n),4) for k, v in pageRank.items()}        
    #print(a)
    #print(pageRank)
    return a


corpus = {"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {"2.html"}}
page = '1.html'
        
print(sample_pagerank(corpus, DAMPING, SAMPLES))
