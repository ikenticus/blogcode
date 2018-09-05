using System.CodeDom.Compiler;
using System.Collections.Generic;
using System.Collections;
using System.ComponentModel;
using System.Diagnostics.CodeAnalysis;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Runtime.Serialization;
using System.Text.RegularExpressions;
using System.Text;
using System;

class Solution {

    // Complete the solve function below.
    static void solve(double meal_cost, int tip_percent, int tax_percent) {
        double tip = Convert.ToDouble(tip_percent) / 100;
        double tax = Convert.ToDouble(tax_percent) / 100; 
        double total_cost = meal_cost * (1 + tip + tax);
        Console.WriteLine("The total meal cost is {0} dollars.\n", total_cost.ToString("F0"));
        // https://docs.microsoft.com/en-us/dotnet/standard/base-types/standard-numeric-format-strings#example
    }

    static void Main(string[] args) {
        double meal_cost = Convert.ToDouble(Console.ReadLine());

        int tip_percent = Convert.ToInt32(Console.ReadLine());

        int tax_percent = Convert.ToInt32(Console.ReadLine());

        solve(meal_cost, tip_percent, tax_percent);
    }
}

