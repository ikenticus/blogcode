// Easy
// https://www.hackerrank.com/challenges/java-strings-introduction/problem

import java.io.*;
import java.util.*;

public class Solution {

    public static void main(String[] args) {
        
        Scanner sc=new Scanner(System.in);
        String A=sc.next();
        String B=sc.next();
        /* Enter your code here. Print output to STDOUT. */
        System.out.println(A.length() + B.length());
        if (A.charAt(0) > B.charAt(0)) {
            System.out.println("Yes");        
        } else {
            System.out.println("No");
        }
        System.out.printf("%s%s %s%s\n",
                          A.substring(0, 1).toUpperCase(), A.substring(1),
                          B.substring(0, 1).toUpperCase(), B.substring(1));
    }
}

