let debug = false;

// Translated to hard-data, post-interview, to analyze:
let wiki = {};
wiki['Bitcoin'] = [ 'Cryptocurrency', 'Digital Currency', 'Central Bank', 'Fiat Money' ];
wiki['Fiat Money'] = [ 'Gold', 'Bitcoin', 'Silver', 'Copper', 'Bronze', 'Tin' ];
wiki['Copper'] = [ 'One', 'Two', 'Tri', 'For', 'Fib' ];
wiki['Two'] = [ 'Hello', 'World' ];
wiki['Tri'] = [ 'I', 'Love', 'You' ];
 
function getWikiLinks(term) {
    return Object.keys(wiki).indexOf(term) > -1 ? wiki[term] : [];
}

function topicDistance(term1, term2) { 
    if (debug) console.log('topicDistance', term1, term2);
    if (!Array.isArray(term2)) term2 = [term2];
    let term = term2.pop();
    if (getWikiLinks(term1).indexOf(term) > -1) {
        if (debug) console.log('trail:', term2);
        return term2.length; // 2. terminate recursion  
    } else {
        let terms = getWikiLinks(term1);
        for (let t = 0; t < terms.length; t++) {
            if (term2.indexOf(terms[t]) < 0) { // prevent 'Bitcoin' infinite loop
                let test = topicDistance(terms[t], term2.concat([term1, term]));
                // 1. iterate forwards (or backwards) in order to recurse ^
                if (test) return test; // 3. trickle backwards
            }
        }
    }
}
 
['Cryptocurrency', 'Copper', 'For', 'Love'].forEach((t) => {
    console.log(topicDistance('Bitcoin', t));
    if (debug) console.log('=====');
});

