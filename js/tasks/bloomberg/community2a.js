/*
Imagine you are tasked with determining the similarity of two search terms using Wikipedia. Specifically, you are asked to implement the following function

topicDistance(term1, term2) = minimum number of links separating the two pages

You are given the following function to return a list of links for a given term

getWikiLinks(term) = list of terms found on the Wikipedia page for term

Ex

    getWikiLinks(Bitcoin) = [ Cryptocurrency, Digital Currency, Central Bank, Fiat Money ... ]

    getWikiLinks(Fiat Money) = [ ... Copper ... ]


    topicDistance(Bitcoin, Cryptocurrency) = 0 (since term2 appears directly on term1's page)

    topicDistance(Bitcoin, Copper) = 1 (Bitcoin - Fiat Money, Copper found after 1 hop on Fiat Money's page)
 

Determine the minimum number of hops required to reach term2 from term1.
*/

function topicDistance(term1, term2) { 
    if (getWikiLinks(term1).indexOf(term2) > -1) {
        return 0;
    } else {
        let test;
        getWikiLinks(term1).forEach((term) => {
            if (getWikiLinks(term).indexOf(term1) < 0) { // B
                test = topicDistance(term, term2);
                if (test === 0) break;  // A
            }
        });
        if (test === 0) return 1 + test;
    }
}

// Unable to get recursion to work properly
// originally looping through Bitcoin, it would return on the 0th item: Cryptocurrency

// Follow up question from Sara:
// how would you do it differently if the Fiat Money terms were:
//    getWikiLinks(Fiat Money) = [ ... Bitcoin, Copper ... ]
// Add conditional B line to search for existance of term?

