// Easy
// https://www.hackerrank.com/challenges/java-date-and-time/problem

import java.util.Scanner;

/* BEGIN Snippet */
import java.util.Calendar;
public class Solution {
    static String Day[] ={
        "SUNDAY",
        "MONDAY",
        "TUESDAY",
        "WEDNESDAY",
        "THURSDAY",
        "FRIDAY",
        "SATURDAY"
    };

    public static String getDay(String day, String month, String year) {
        Calendar cal = Calendar.getInstance();
        cal.set(Integer.parseInt(year), Integer.parseInt(month) - 1, Integer.parseInt(day));
        int dow = cal.get(Calendar.DAY_OF_WEEK);
        return(Day[dow - 1]);
    }
/* END Snippet */

    public static void main(String[] args) {
        Scanner in = new Scanner(System.in);
        String month = in.next();
        String day = in.next();
        String year = in.next();
        
        System.out.println(getDay(day, month, year));
    }
}

