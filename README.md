# PageRank

Search engines display pages based on their importance, but how does a search engine like Google know one page is more important than another? 
The Pagerank algorithm created by Google's cofounders is based on the concept that a page is important if other pages links to it. In addition, links
from other important pages carry more weight than links from less important pages. 

Pagerank.py calculates pagerank by sampling pages using Markov Chain random surfer and iteratively using the pagerank formula: 
PR(p) = ((1-d)/N)+dΣ((PR(i))/NumLinks(i)) where PR(p) is the pagerank of page, p. N is the total number of pages. d is the damping factor, the probability
of choosing a page from N. i is all pages that link to page, p. NumLinks(i) is the number of links present on page i. 

An introduction to AI with python project by Harvard University Online
