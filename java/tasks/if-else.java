// Easy
// https://www.hackerrank.com/challenges/java-if-else/problem

import java.io.*;
import java.math.*;
import java.security.*;
import java.text.*;
import java.util.*;
import java.util.concurrent.*;
import java.util.regex.*;

public class Solution {



    private static final Scanner scanner = new Scanner(System.in);

    public static void main(String[] args) {
        int N = scanner.nextInt();
        scanner.skip("(\r\n|[\n\r\u2028\u2029\u0085])?");
        // Exactly the conditional syntax as javascript
        if (N % 2 == 1 || (N >= 6 && N <= 20)) {
            System.out.println("Weird"); // console.log => System.out.println
        } else {
            System.out.println("Not Weird"); // single quote for literals only
        }
        scanner.close();
    }
}

