#! /usr/bin/env python3
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
    dictionary={}

    if len(corpus[page])>0:
        for key in corpus.keys():
            dictionary[key]= (1-damping_factor)/(len(corpus.keys()))
            
        for link in corpus[page]:
            dictionary[link]+= damping_factor/len(corpus[page])
    else:
        for key in corpus.keys():
            dictionary[key]=(1/len(corpus.keys()))

    return dictionary


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    sys.setrecursionlimit(11000)
    dictionary={}
    count=0
    for key in corpus.keys():
        dictionary[key]=0

    sample=random.choice(list(corpus.keys()))
    dic=get_sample(count,dictionary,sample,corpus,damping_factor)
    for key in dic.keys():
        dic[key]=dic[key]/SAMPLES
    return dic


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    dictionary={}
    for key in corpus.keys():
        dictionary[key]=1/(len(corpus.keys()))

    differences={}
    for key in corpus.keys():
        differences[key]=1000
    pageRanks=formula(corpus,damping_factor,dictionary,differences)

    total=0
    for page in pageRanks:
        total+= pageRanks[page]
    for page in pageRanks:
        pageRanks[page]=pageRanks[page]/total
        
    return pageRanks

def get_sample(count,dictionary,sample,corpus,damping_factor):
    if count==SAMPLES:
        print(dictionary)
        return dictionary 
    
    probability=transition_model(corpus,sample,damping_factor)
    keys=[]
    values=[]
    for key,value in probability.items():
        keys.append(key)
        values.append(value)
    s=random.choices(keys,values,k=1)
    sample_n=s[0]
    dictionary[sample_n]+=1
    count+=1
    return get_sample(count,dictionary,sample_n,corpus,damping_factor)


def summing(pageI,dictionary,corpus):
    if len(pageI) == 0:
        return 0
    total=0
    for page in pageI:
        if len(corpus[page]) == 0:
            numLinks=len(corpus.keys())
        else:
            numLinks=len(corpus[page])
        sumI=dictionary[page]/numLinks
        total+=sumI
    return total


def check_differences(differences):
    return any(float(v)>0.001 for v in differences.values())

def formula(corpus,damping_factor,dictionary,differences):
    if check_differences(differences):

        newRank=dictionary.copy()
        for key in corpus.keys():
            pageI=[]
            for i in corpus.keys():
                if key in corpus[i]:
                    pageI.append(i)
            pageRank=((1-damping_factor)/len(corpus.keys()))+(damping_factor*summing(pageI,dictionary,corpus))
            dictionary[key]=pageRank

        for key in differences.keys():
            differences[key]=format(abs(dictionary[key]-newRank[key]),'.3f')

        return formula(corpus,damping_factor,dictionary,differences)
    
    else:
        return dictionary

if __name__ == "__main__":
    main()
