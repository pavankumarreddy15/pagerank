# pagerank
Developed AI to rank webpages by information using Random Surfer Model.

When search engines like Google display search results, they do so by placing more “important” and higher-quality pages higher in the search results than less important pages.
But how does the search engine know which pages are more important than other pages?

One heuristic might be that an “important” page is one that many other pages link to, since it’s reasonable to imagine that more sites will link to a higher-quality webpage than a lower-quality webpage.
We could therefore imagine a system where each page is given a rank according to the number of incoming links it has from other pages, and higher ranks would signal higher importance.

But this definition isn’t perfect: if someone wants to make their page seem more important,
then under this system, they could simply create many other pages that link to their desired page to artificially inflate its rank.

For that reason, the PageRank algorithm was created by Google’s co-founders (including Larry Page, for whom the algorithm was named).
In PageRank’s algorithm, a website is more important if it is linked to by other important websites, and links from less important websites have their links weighted less. 
This definition seems a bit circular, but it turns out that there are multiple strategies for calculating these rankings.

One way to think about PageRank is with the random surfer model, which considers the behavior of a hypothetical surfer on the internet who clicks on links at random. 

Consider a corpus of webpages below,

corpus has 4 pages page1,page2,page3,page4
page.  |         incoming_links.    | outgoing_links
page1. |          page2             |     page2
page2  |       page1,page3,page4    |     page1,page3
page3  |          page2             |     page2,page4
page4  |          page3             |     page2

The random surfer model imagines a surfer who starts with a web page at random, and then randomly chooses links to follow.
If the surfer is on Page 2, for example, they would randomly choose between Page 1 and Page 3 to visit next (duplicate links on the same page are treated as a single link, and links from a page to itself are ignored as well).
If they chose Page 3, the surfer would then randomly choose between Page 2 and Page 4 to visit next.

A page’s PageRank, then, can be described as the probability that a random surfer is on that page at any given time.
After all, if there are more links to a particular page, then it’s more likely that a random surfer will end up on that page.
Moreover, a link from a more important site is more likely to be clicked on than a link from a less important site that fewer pages link to, so this model handles weighting links by their importance as well.

One way to interpret this model is as a Markov Chain, where each page represents a state, and each page has a transition model that chooses among its links at random.
At each time step, the state switches to one of the pages linked to by the current state.

By sampling states randomly from the Markov Chain, we can get an estimate for each page’s PageRank.
We can start by choosing a page at random, then keep following links at random, keeping track of how many times we’ve visited each page.
After we’ve gathered all of our samples (based on a number we choose in advance), the proportion of the time we were on each page might be an estimate for that page’s rank.

However, this definition of PageRank proves slightly problematic, if we consider a network where a two pages have both links each other and they are the only links they have.

To ensure we can always get to somewhere else in the corpus of web pages, we’ll introduce to our model a damping factor d.
With probability d (where d is usually set around 0.85), the random surfer will choose from one of the links on the current page at random.
But otherwise (with probability 1 - d), the random surfer chooses one out of all of the pages in the corpus at random (including the one they are currently on).

Alternatively, we could also use iterative algortihm to find pagerank.
We can also define a page’s PageRank using a recursive mathematical expression. Let PR(p) be the PageRank of a given page p: the probability that a random surfer ends up on that page.
How do we define PR(p)? Well, we know there are two ways that a random surfer could end up on the page:
With probability 1 - d, the surfer chose a page at random and ended up on page p.
With probability d, the surfer followed a link from a page i to page p.
The first condition is fairly straightforward to express mathematically: it’s 1 - d divided by N, where N is the total number of pages across the entire corpus.
This is because the 1 - d probability of choosing a page at random is split evenly among all N possible pages.
For the second condition, we need to consider each possible page i that links to page p.
For each of those incoming pages, let NumLinks(i) be the number of links on page i. Each page i that links to p has its own PageRank, PR(i), representing the probability that we are on page i at any given time.
And since from page i we travel to any of that page’s links with equal probability, we divide PR(i) by the number of links NumLinks(i) to get the probability that we were on page i and chose the link to page p.



Open up pagerank.py. Notice first the definition of two constants at the top of the file: DAMPING represents the damping factor and is initially set to 0.85.
SAMPLES represents the number of samples we’ll use to estimate PageRank using the sampling method, initially set to 10,000 samples.

Now, take a look at the main function. It expects a command-line argument, which will be the name of a directory of a corpus of web pages we’d like to compute PageRanks for.
The crawl function takes that directory, parses all of the HTML files in the directory, and returns a dictionary representing the corpus.
The keys in that dictionary represent pages (e.g., "2.html"), and the values of the dictionary are a set of all of the pages linked to by the key (e.g. {"1.html", "3.html"}).

The main function then calls the sample_pagerank function, whose purpose is to estimate the PageRank of each page by sampling.
The function takes as arguments the corpus of pages generated by crawl, as well as the damping factor and number of samples to use.
Ultimately, sample_pagerank should return a dictionary where the keys are each page name and the values are each page’s estimated PageRank (a number between 0 and 1).

The main function also calls the iterate_pagerank function, which will also calculate PageRank for each page,
but using the iterative formula method instead of by sampling. The return value is expected to be in the same format, and we would hope that the output of these two functions should be similar when given the same corpus!

