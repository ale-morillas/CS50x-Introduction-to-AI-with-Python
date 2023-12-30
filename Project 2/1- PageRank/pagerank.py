import os
import random
import re
import sys
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
    # Probability distribution dictionary
    prob_dist = {}
    
    # If no outgoing links return a probability distribution with equal probability.
    if len(corpus[page]) == 0:
        for page_name in corpus:
            prob_dist[page_name] = 1 / len(corpus)
    
    else:
        # With probability 0.85 among pages
        for page_name in corpus:
            prob_dist[page_name] = (1 - damping_factor) / len(corpus)
           
        # With probability 0.85 among links 
        for link in corpus[page]:
            prob_dist[link] += damping_factor / len(corpus[page])
    
    return prob_dist   
    

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Dictionary of PageRanks
    page_ranks = {}
    for key in corpus.keys():
        page_ranks[key] = 0
    
    # Random page
    random_page = random.choices(list(corpus.keys()))[0]
    
    for i in range(1, n):
        prob_dist = transition_model(corpus, random_page, damping_factor)

        for page in page_ranks:
            page_ranks[page] = (((i - 1) * page_ranks[page]) + prob_dist[page]) / i
        
        random_page = random.choices(list(page_ranks.keys()), weights=list(page_ranks.values()), k=1)[0]
        
    return page_ranks

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Dictionary of PageRanks
    N = len(corpus)
    page_ranks = {}
    for key in corpus.keys():
        page_ranks[key] = 1 / N
        
    stop = True
    
    while stop:
        stop = False
        page_ranks_copy = copy.deepcopy(page_ranks)
        for page in corpus:
            page_ranks[page] = iterative_formula(corpus, page_ranks, page)

            stop = stop or abs(page_ranks_copy[page] - page_ranks[page]) > 0.001
            
    return page_ranks
        
        
def iterative_formula(corpus, page_ranks, page):
    """
    Calculate the iterative formula for PageRank for a given page.
    """
    damping_factor = DAMPING
    N = len(corpus)
    total_probability = 0

    for i in corpus:
        if page in corpus[i]:
            total_probability += page_rank[i] / len(corpus[i])
            
    formula = ((1 - damping_factor) / N) + damping_factor * total_probability

    return formula
    


if __name__ == "__main__":
    main()
