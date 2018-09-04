// Easy
// https://www.hackerrank.com/challenges/java-string-tokens/problem

import java.io.*;
import java.util.*;

public class Solution {

    public static void main(String[] args) {
        Scanner scan = new Scanner(System.in);

        if (scan.hasNext() && scan.hasNextLine()) {
            String s = scan.nextLine();       
            // Write your code here.

            // Without trim(), fails Testcase(s) 3-8,10
            //String[] words = s.trim().split("[^A-za-z]+");

            // Using [^A-za-z] fails Testcase(s) 4-9
            String[] words = s.trim().split("[ !,?._'@]+");

            System.out.println(words.length);
            for (String w: words)
                System.out.println(w);
        } else {
            // Empty or whitespace string fails Testcase 9
            System.out.println(0);            
        }

        scan.close();
    }
}


