using System;
using System.Collections.Generic;
using System.IO;

class Solution {
    static void Main(String[] args) {
        int i = 4;
        double d = 4.0;
        string s = "HackerRank ";

        // Declare second integer, double, and String variables.
        int i2;
        double d2;
        String s2;

        // Read and save an integer, double, and String to your variables.
        i2 = Convert.ToInt32(Console.ReadLine());
        d2 = Convert.ToDouble(Console.ReadLine());
        s2 = Console.ReadLine();

        // Print the sum of both integer variables on a new line.
        Console.WriteLine(i + i2);

        // Print the sum of the double variables on a new line.
        Console.WriteLine(d + d2);
        
        // Concatenate and print the String variables on a new line
        // The 's' variable above should be printed first.
        Console.WriteLine(s + s2);
                
    }
}
