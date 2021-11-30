import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


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
    print(linked_pages)
    for i in range(len(corpus[page])):
        prob = damping_factor/len(linked_pages)
        for page in thedict:
            if page in linked_pages:
                thedict[page] = prob
        #prob_distribution[corpus[page][i]] = prob
#With probability 1 - damping_factor, the random surfer should randomly choose one of all pages in the corpus with equal probability.
    second_prob = (1-damping_factor)/len(thedict)
    for page in thedict:
        thedict[page] = thedict[page] + second_prob
    print(thedict)
    return thedict



def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    sum1 = 0
    sum2 = 0
    sum3 = 0
    sum4 = 0
    samples = []
    pageRank = {"1.html":0,"2.html":0,"3.html":0,"4.html":0}
    print(corpus)
    for i in range(n):
        random_page = random.randint(0,(len(corpus)-1))
        corpus_keys = list(corpus.keys())
        page = corpus_keys[random_page]
        samples.append(transition_model(corpus,page,damping_factor))
    for index in range(n):
        for key in samples[index]:
            if key == "1.html":
                sum1 = sum1 + samples[index][key]
            elif key == "2.html":
                sum2 = sum2 + samples[index][key]
            elif key == "3.html":
                sum3 = sum3 + samples[index][key]
            elif key == "4.html":
                sum4 = sum4 + samples[index][key]
    print(sum1,sum2,sum3,sum4)
    pageRank["1.html"] = sum1/10000
    pageRank["2.html"] = sum2/10000
    pageRank["3.html"] = sum3/10000
    pageRank["4.html"] = sum4/10000
    print(pageRank)
    return pageRank

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    print("TODO")
    return 0

if __name__ == "__main__":
    main()
