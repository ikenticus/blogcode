// Easy
// https://www.hackerrank.com/challenges/java-currency-formatter/problem

import java.util.*;
import java.text.*;

public class Solution {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        double payment = scanner.nextDouble();
        scanner.close();
        
        /*
        // Uses the following:
        import java.text.NumberFormat;
        import java.util.Locale;
        */
        NumberFormat us = NumberFormat.getCurrencyInstance(Locale.US);
        NumberFormat china = NumberFormat.getCurrencyInstance(Locale.CHINA);
        NumberFormat france = NumberFormat.getCurrencyInstance(Locale.FRANCE);

        //NumberFormat india = NumberFormat.getCurrencyInstance(Locale.INDIA);
        // Locale.INDIA does not exist, construct it from Locale:
        NumberFormat india = NumberFormat.getCurrencyInstance(new Locale("en", "IN"));

        System.out.println("US: " + us.format(payment));
        System.out.println("India: " + india.format(payment));
        System.out.println("China: " + china.format(payment));
        System.out.println("France: " + france.format(payment));
    }
}

