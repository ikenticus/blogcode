// Easy 
// https://www.hackerrank.com/challenges/c-tutorial-for-loop/problem

#include <iostream>
#include <cstdio>
using namespace std;

int main() {
    // Complete the code.
    const char *words[] = {"zero", "one","two","three","four","five","six","seven","eight","nine"};
    int a, b;
    cin >> a >> b;
    for (int n = a; n <= b; n++) {
        if (n < 10) {
            printf("%s\n", words[n]);
        } else {
            cout << (n % 2 == 0 ? "even" : "odd") << endl;
        }
    }
    return 0;
}

