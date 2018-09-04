// Easy
// https://www.hackerrank.com/challenges/java-regex/problem

import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.Scanner;

class Solution{

    public static void main(String[] args){
        Scanner in = new Scanner(System.in);
        while(in.hasNext()){
            String IP = in.next();
            System.out.println(IP.matches(new MyRegex().pattern));
        }

    }
}

//Write your code here
class MyRegex {
    // Matches octets > 255, fails Testcase(s) 1-2
    //public String pattern = "([0-9]{1,3}\\.){3}[0-9]{1,3}";
    public String pattern = "((25[0-5]|2[0-4][0-9]|[0-1]?[0-9]?[0-9])\\.){3}(25[0-5]|2[0-4][0-9]|[0-1]?[0-9]?[0-9])";
}

