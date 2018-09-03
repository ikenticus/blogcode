// Easy
// https://www.hackerrank.com/challenges/c-tutorial-conditional-if-else/problem

#include <bits/stdc++.h>

using namespace std;



int main()
{
    int n;
    cin >> n;
    cin.ignore(numeric_limits<streamsize>::max(), '\n');

    // Write Your Code Here
    const char *words[] = {"zero", "one","two","three","four","five","six","seven","eight","nine"};

    if (n < 10) {
        printf(words[n]);
    } else {
        printf("Greater than 9");    
    }

    // ternary method
    //cout << ((n < 10) ? words[n] : "Greater than 9") << endl;

    return 0;
}

