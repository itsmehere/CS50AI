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
    # Dict of link probabilities
    pageProbabilities = dict()

    # If the there are no links from the current page, choose any page at random.
    if len(corpus[page]) == 0:
        for aPage in corpus:
            pageProbabilities[aPage] = 1 / len(corpus)
    else:
        # Add the probabilities for if the page was chosen randomly - note: This has to be above otherwise the key won't exist.
        for aPage in corpus:
            pageProbabilities[aPage] = (1 - damping_factor) / len(corpus)

        # Add the probabilities for the pages that are linked.
        for aPage in corpus[page]:
            pageProbabilities[aPage] += damping_factor / len(corpus[page])

    return pageProbabilities
    

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Dictionary that holds probability values - Initialized with values from corpus
    pageRanks = dict()
    for eachPage in corpus:
        pageRanks[eachPage] = 0

    # Dictionary to keep track of page occurances
    pageOccurances = dict()
    for eachPage in corpus:
        pageOccurances[eachPage] = 0

    # Choose first page at random
    currentPage = random.choice(list(corpus.keys()))
    pageOccurances[currentPage] += 1

    # Fill dictionary with number of occurances
    for i in range(1, n + 1):
        linkProbabilites = transition_model(corpus, currentPage, damping_factor)
        currentPage = random.choices(list(linkProbabilites.keys()), list(linkProbabilites.values()), k = 1)[0]
        pageOccurances[currentPage] += 1

    # Calculate probability
    for page in pageRanks:
        pageRanks[page] =  pageOccurances[page] / n

    return pageRanks


            


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Create dict to hold pageRanks - set all PageRanks to be equal at first
    pageRanks = dict()
    for page in corpus:
        pageRanks[page] = 1 / len(corpus)

    # Tells us when to exit the process
    notComplete = True
    # Checks how many pages have accurate values
    numAccuratePages = 0

    while notComplete:
        # For each page in pageRanks, update the value
        for page in pageRanks:
            value = (1 - damping_factor) / len(corpus) + iterSum(corpus, page, damping_factor, pageRanks)

            # If the pageRanks are farily accurate, exit the process. Otherwise, continue updating
            if abs(pageRanks[page] - value) < 0.001:
                numAccuratePages += 1
                # If all pages have accurate values, then quit
                if numAccuratePages == len(pageRanks):
                    notComplete = False
                    break
            else:
                pageRanks[page] = value

    return pageRanks

def iterSum(corpus, currentPage, damping_factor, pageRanks):
    # Probability that we can get to currentPage via links
    linkedPageSum = 0

    # If a page in the corpus has link to currentPage, add probability of getting to currentPage via that link to the total Sum
    for page in corpus:
        if currentPage in corpus[page]:
            linkedPageSum += pageRanks[page] / len(corpus[page])

    # Chances of using a link is damping_factor
    return damping_factor * linkedPageSum



if __name__ == "__main__":
    main()
