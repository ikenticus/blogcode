// Easy
// https://www.hackerrank.com/challenges/c-tutorial-pointer/problem

#include <stdio.h>
#include <stdlib.h> // abs

void update(int *a,int *b) {
    // Complete this function
    int ia = (*a);
    int ib = (*b);
    (*a) = ia + ib;
    (*b) = abs(ia - ib);
}

int main() {
    int a, b;
    int *pa = &a, *pb = &b;
    
    scanf("%d %d", &a, &b);
    update(pa, pb);
    printf("%d\n%d", a, b);

    return 0;
}

