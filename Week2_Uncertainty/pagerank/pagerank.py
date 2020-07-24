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
    # Dict of link probabilities
    pageProbabilities = dict()

    # If the there are no links from the current page, choose any page at random
    if len(corpus[page]) == 0:
        for currentPage in corpus:
            pageProbabilities[currentPage] = 1 / len(corpus)
    else:
        # Add the probabilities for if the page was chosen randomly
        for currentPage in corpus:
            pageProbabilities[currentPage] = (1 - damping_factor) / len(corpus)

        # Add the probabilities for the pages that are linked
        for currentPage in corpus[page]:
            pageProbabilities[currentPage] += damping_factor / len(corpus[page])

    return pageProbabilities
    

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.

    EDIT: This way is probably not the best way to implement page sampling simply because we
    have to create two dictonaries - one for the actual page ranks, and the other to hold the occurances. 
    We can imagine with a larger corpus, this solution would not be optimal. For the sake of this problem, 
    it is probably okay.
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

    # Fill dictionary with number of occurances. This loop will run n - 1 times because range is exclusive.
    # This is what we want since technically, the first iteration was choosing the first page (lines 104 - 105).
    for i in range(1, n):
        linkProbabilites = transition_model(corpus, currentPage, damping_factor)

        # Choose a random page using linkProbabilites(weights)
        currentPage = random.choices(list(linkProbabilites.keys()), list(linkProbabilites.values()), k = 1)[0]
        pageOccurances[currentPage] += 1

    # Calculate probability based on occurances
    for page in pageRanks:
        pageRanks[page] =  pageOccurances[page] / n

    print(f"Sampling Sum: {accurateSum(pageRanks)}")
    return pageRanks          


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    ACCURACY = 0.001
    # Holds final pageRanks
    pageRanks = dict()
    # Holds pageRanks to calculate values
    tempPageRanks = dict()

    # Both variables below are used to determine when to end the loop
    complete = False
    numAccuratePages = 0

    # Set all PageRanks to be equal at first
    for page in corpus:
        pageRanks[page] = 1 / len(corpus)

    while not complete:
        tempPageRanks = copy.deepcopy(pageRanks)

        for page in tempPageRanks:
            pageRanks[page] = ((1 - damping_factor) / len(corpus)) + (damping_factor * iterSum(corpus, page, tempPageRanks))

            # Check if a fairly accurate value has been reached
            if abs(tempPageRanks[page] - pageRanks[page]) < ACCURACY:
                numAccuratePages += 1

                # If all pages have accurate values, then exit the process
                if numAccuratePages == len(tempPageRanks):
                    complete = True
                    break

        # Reset number of accurate pages for next iteration
        numAccuratePages = 0

    print(f"Iterative Sum: {accurateSum(pageRanks)}")
    return pageRanks


def iterSum(corpus, currentPage, pageRanks):
    # Probability that we can get to currentPage via links
    linkedPageSum = 0

    for page in corpus:
        # For page i containing a link to currentPage, pageRank of currentPage is pageRank of i ÷ all i's links
        if currentPage in corpus[page]:
            linkedPageSum += pageRanks[page] / len(corpus[page])
        # If a page has no links, assume it has a link to all pages
        elif len(corpus[page]) == 0:
            linkedPageSum += pageRanks[page] / len(corpus)

    return linkedPageSum


# Returns an unrounded sum of pageRanks
def accurateSum(pageRanks):
    totalSum = 0

    for page in pageRanks:
        totalSum += pageRanks[page]

    return totalSum


if __name__ == "__main__":
    main()