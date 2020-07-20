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
    trans_model=dict()
    n=len(corpus)
    if len(corpus[page])==0:
        p=1/n
        for key in corpus.keys():
            trans_model[key]=p
    else:
        for x in corpus[page]:
            trans_model[x]=damping_factor/(len(corpus[page]))
        for key in corpus.keys():
            if key in trans_model.keys():
                trans_model[key]+=(1-damping_factor)/n
            else:
                trans_model[key]=(1-damping_factor)/n
    return trans_model

    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    raise NotImplementedError


def sample_pagerank(corpus, damping_factor, n):
    samples=[]
    pages=list(corpus.keys())
    current_page=random.choice(pages)
    samples.append(current_page)
    for i in range(n-1):
        weights=[]
        trans_model=transition_model(corpus,current_page,damping_factor)
        for page in pages:
            weights.append(trans_model[page])
        new_page=random.choices(pages,weights)
        samples.append(new_page[0])
        current_page=new_page[0]

    page_rank=dict()
    for p in pages:
        count=0
        for l in samples:
            if p==l:
                count+=1
        page_rank[p]=count/len(samples)

    return page_rank

    


    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    raise NotImplementedError

def sigma(corpus,page,page_rank):
    s=0
    links=[]
    set_pages=set()
    for x in corpus.keys():
        set_pages.add(x)
    for key in corpus.keys():
        if len(corpus[key])==0:
            corpus[key]=set_pages
    for key in corpus.keys():
        if page in corpus[key]:
            links.append(key)
    if len(links)==0:
        s=0
        # for x in corpus.keys():
        #     if len(corpus[x])==0:
        #         s+=page_rank[x]/len(corpus)
        #     else:
        #         s+=page_rank[x]/len(corpus[x])
    else:
        for x in links:
            if len(corpus[x])==0:
                s+=page_rank[x]/len(corpus)
            else:
                s+=page_rank[x]/len(corpus[x])
    return s



def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    n=len(corpus)
    page_rank=dict()
    #print(corpus)
    for key in corpus.keys():
        page_rank[key]=1/n
    for i in range(10000):
        #print(page_rank)
        for key in corpus.keys():
            page_rank[key]=((1-damping_factor)/n)+(damping_factor*sigma(corpus,key,page_rank))
    return page_rank
    raise NotImplementedError


if __name__ == "__main__":
    main()
    #print(transition_model({"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {"2.html"}},"1.html",0.85))
