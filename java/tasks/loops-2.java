// Easy
// https://www.hackerrank.com/challenges/java-loops/problem

import java.util.*;
import java.io.*;

class Solution{
    public static void main(String []argh){
        Scanner in = new Scanner(System.in);
        int t=in.nextInt();
        Double d = new Double(2);
        for(int i=0;i<t;i++){
            int a = in.nextInt();
            int b = in.nextInt();
            int n = in.nextInt();
            int sum = a;
            for (int x=0; x<n; x++) {
                sum += Math.round(b * Math.pow(d, Double.valueOf(x)));
                System.out.printf("%d ", sum);
            }
            System.out.println();
        }
        in.close();
    }
}

