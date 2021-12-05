import os
import random
import re
import sys
import numpy
import copy

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
       
    probabilityDistribution = dict()
        
    keys = corpus.keys()
    NoOfPages = len(corpus)

    if len(corpus[page]) != 0:
        links = corpus[page]
        linksNumber = len(links)

        #probability of choosing one of the links in random
        chooseLinkProbability = damping_factor / linksNumber
        
        #probability of choosing one of the pages in random
        choosePageProbability = (1 - damping_factor) / NoOfPages

        #setting the probability for the given page
        probabilityDistribution[page] = choosePageProbability

        #setting the probabilities for the link pages
        for link in links:
            probabilityDistribution[link] = chooseLinkProbability + choosePageProbability

        #setting probability for other pages not in links
        for key in keys:
            if key not in probabilityDistribution.keys():
                probabilityDistribution[key] = choosePageProbability    


    elif len(corpus[page]) == 0:
        choosePageProbability = 1 / NoOfPages

        for key in keys:
                probabilityDistribution[key] = choosePageProbability 

    return probabilityDistribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    PageRank = dict()
    keys = list(corpus.keys())
    
    #choosing a page at random at first
    page = random.choice(keys)
    
    #dict to keep track of the number of times a page is viewed
    pageClicked = dict()

    #initializing all values to 0
    for key in keys:
        pageClicked[key] = 0


    for i in range(SAMPLES):
        #getting transition model for the page
        sampleDistribution = transition_model(corpus,page,damping_factor)
        
        sampleProbabilities = list(sampleDistribution.values())
        samplePages = list(sampleDistribution.keys())  
         
        #using numpy to select a page with given probabilities
        choice = numpy.random.choice(samplePages,1,p=sampleProbabilities)    
        
        page = choice[0]
        
        #updating the values for viewed pages
        for key in keys:
            if page == key:
                pageClicked[page] += 1

    #setting the pagerank on the basis of times a page is viewed
    for key in keys:
        PageRank[key] = pageClicked[key] / SAMPLES

    return PageRank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pageRank1 = dict()
    pageRank2 = dict()
    pages = list(corpus.keys())
    NoOfPages = len(pages)

    #initialize the pagerank to 1/N
    for page in pages:
        pageRank1[page] = 1 / NoOfPages

    #add all the pages as links if a page has no links
    for pg in pages:
        if len(corpus[pg]) == 0:
            for pg1 in pages:
                corpus[pg].add(pg1)

    stop = False

    while not stop:
        for page in pages:
            firstPart = (1 - damping_factor) / NoOfPages
            linkedTo = []
            
            #getting a list of all the incoming links to a page
            for page1 in pages:
                if page in corpus[page1]:
                    linkedTo.append(page1)
            ratio = 0.0

            #summation of all the pages linked to the page
            for link in linkedTo:
                linksNumber = len(list(corpus[link]))
                ratio += ((pageRank1[link]) / linksNumber)

            pagerank = firstPart + (damping_factor * ratio)

            pageRank2[page] = pagerank
        
        for page in pages:
            if abs((pageRank2[page]) - (pageRank1[page])) < 0.001:
                stop = True
                
        pageRank1 = copy.deepcopy(pageRank2)
            
    return pageRank2



if __name__ == "__main__":
    main()
