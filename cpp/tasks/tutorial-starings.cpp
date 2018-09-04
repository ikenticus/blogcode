// Easy
// https://www.hackerrank.com/challenges/c-tutorial-strings/problem

#include <iostream>
#include <string>
using namespace std;

int main() {
	// Complete the program
    
    string a, b;
    cin >> a >> b;
    cout << a.size() << " " << b.size() << "\n";
    cout << a + b << "\n";
  
    // swap first letter
    string A = a;
    string B = b;
    a[0] = B[0];
    b[0] = A[0];
    cout << a << " " << b << "\n";
    
    return 0;
}
