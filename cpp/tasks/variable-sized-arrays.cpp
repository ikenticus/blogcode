// Easy
// https://www.hackerrank.com/challenges/variable-sized-arrays/problem

#include <cmath>
#include <cstdio>
#include <vector>
#include <iostream>
#include <algorithm>
#include <bits/stdc++.h>

using namespace std;

vector<string> split_string(string);

int main() {
    /* Enter your code here. Read input from STDIN. Print output to STDOUT */       

    string nq_temp;
    getline(cin, nq_temp);

    vector<string> nq = split_string(nq_temp);

    int n = stoi(nq[0]);
    int q = stoi(nq[1]);

    vector<vector<int>> queries(q);
    for (int i = 0; i < q; i++) {
        int k;
        cin >> k;
        queries[i].resize(k);

        for (int j = 0; j < k; j++) {
            cin >> queries[i][j];
        }

        //cin.ignore(numeric_limits<streamsize>::max(), '\n');
    }

    for (int a = 0; a < q; a++) {
        int i, j;
        cin >> i >> j;
        cout << queries[i][j] << "\n";
    }

    return 0;
}

vector<string> split_string(string input_string) {
    string::iterator new_end = unique(input_string.begin(), input_string.end(), [] (const char &x, const char &y) {
        return x == y and x == ' ';
    });

    input_string.erase(new_end, input_string.end());

    while (input_string[input_string.length() - 1] == ' ') {
        input_string.pop_back();
    }

    vector<string> splits;
    char delimiter = ' ';

    size_t i = 0;
    size_t pos = input_string.find(delimiter);

    while (pos != string::npos) {
        splits.push_back(input_string.substr(i, pos - i));

        i = pos + 1;
        pos = input_string.find(delimiter, i);
    }

    splits.push_back(input_string.substr(i, min(pos, input_string.length()) - i + 1));

    return splits;
}

