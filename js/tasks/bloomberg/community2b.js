let debug = true;

// Translated to hard-data, post-interview, to analyze:
let wiki = {};
wiki['Bitcoin'] = [ 'Cryptocurrency', 'Digital Currency', 'Central Bank', 'Fiat Money' ];
wiki['Fiat Money'] = [ 'Gold', 'Silver', 'Copper', 'Bronze', 'Tin' ];
wiki['Copper'] = [ 'One', 'Two', 'Tri', 'For', 'Fib' ];
wiki['Two'] = [ 'Hello', 'World' ];
wiki['Tri'] = [ 'I', 'Love', 'You' ];
 
function getWikiLinks(term) {
    return Object.keys(wiki).indexOf(term) > -1 ? wiki[term] : [];
}

function topicDistance(term1, term2) { 
    if (debug) console.log('topicDistance', term1, term2);
    if (getWikiLinks(term1).indexOf(term2) > -1) {
        if (debug) console.log('trail:', hops);
        return 0; // 2. terminate recursion
    } else {
        let terms = getWikiLinks(term1);
        for (let t = 0; t < terms.length; t++) {
            let test = topicDistance(terms[t], term2); // recurse
            if (test || test === 0) return test + 1; // trickle
        }
    }
}
 
['Cryptocurrency', 'Copper', 'For', 'Love'].forEach((t) => {
    console.log(topicDistance('Bitcoin', t));
    if (debug) console.log('=====');
});

// Lessons learned:
// 1. iterated variable not necessary for recursion
// 2. hops starting at zero required (|| test === 0)

