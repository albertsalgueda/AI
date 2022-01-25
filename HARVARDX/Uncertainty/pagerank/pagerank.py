from asyncio import DatagramProtocol
import os
import random
import re
import sys
import collections, functools, operator

DAMPING = 0.85
SAMPLES = 50000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


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
    range_pages = list(range(0,(len(corpus))))
    for i in range(n):
        if i==0:
            random_page = random.randint(0,(len(corpus)-1))
        else:
            Weights = samples[-1].values()
            random_page = int(random.choices(range_pages,weights=Weights,k=1)[0])
            #print(Weights, random_page)
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

def recursive(corpus,damping_factor,pageRank):
    
    outcome = {}
    for key in pageRank:
        hence = 0
        for kay in corpus:
            if key in corpus[kay]:
                hence = hence + pageRank[kay]/len(corpus[kay])
        now = (1-damping_factor)/len(corpus) + damping_factor*hence
        outcome[key] = pageRank[key]
        pageRank[key] = now
        
    for key in pageRank:
        if pageRank[key] - outcome[key] < 0.001 and outcome[key] - pageRank[key]<0.001:
            continue
        else:
            return recursive(corpus,damping_factor,pageRank)
    
    return pageRank
            

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.
    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    #let's grab all the variables for the algorithm
    pageRank = {}
    for key in corpus:
        pageRank[key] = 1/len(corpus)
    outcome = recursive(corpus,damping_factor,pageRank) 
    return outcome

if __name__ == "__main__":
    main()
