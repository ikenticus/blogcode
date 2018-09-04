// Easy
// https://www.hackerrank.com/challenges/java-string-compare/problem

import java.util.Scanner;

public class Solution {

    public static boolean compare(String a, String b, int c) {
        boolean diff = false;
        for (int i = 0; i < a.length(); i++) {
            //System.out.printf("compare %d %d: %s %s\n", c, i, a, b);
            if (c < 0) {
                if (a.charAt(i) < b.charAt(i)) return true;
                if (a.charAt(i) > b.charAt(i)) return false;
            } else if (c > 0) {
                if (a.charAt(i) > b.charAt(i)) return true;
                if (a.charAt(i) < b.charAt(i)) return false;
            }
        }
        return diff;
    }

    public static String getSmallestAndLargest(String s, int k) {
        String smallest = "";
        String largest = "";
        
        // Complete the function
        // 'smallest' must be the lexicographically smallest substring of length 'k'
        // 'largest' must be the lexicographically largest substring of length 'k'
        int size = s.length() - k + 1;
        String words[] = new String[size]; 
        for (int c = 0; c < size; c++) {
            words[c] = s.substring(c, c + k);
        }

        smallest = largest = words[0];
        for (int w = 0; w < words.length; w++) {
            //System.out.printf("%d %s: %s %s\n", w, words[w], smallest, largest);
            /*
            if (words[w].charAt(0) < smallest.charAt(0))
                smallest = words[w];
            if (words[w].charAt(0) > largest.charAt(0))
                largest = words[w];
            */
            // Comparing just the first letter failed for Testcase(s) 2,4
            
            // Write function to compare each letter until unmatched
            if (compare(words[w], smallest, -1)) smallest = words[w];
            if (compare(words[w], largest, 1)) largest = words[w];
        }
        return smallest + "\n" + largest;
    }

    public static void main(String[] args) {
        Scanner scan = new Scanner(System.in);
        String s = scan.next();
        int k = scan.nextInt();
        scan.close();
      
        System.out.println(getSmallestAndLargest(s, k));
    }
}
