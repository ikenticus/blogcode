import java.util.Scanner;

public class Solution {

    static boolean isAnagram(String a, String b) {
        // Complete the function
        
        /*
        // cannot find symbol, HashMap appears to not be imported
        Map<Character, Integer> mapA = new HashMap<>();
        Map<Character, Integer> mapB = new HashMap<>();
        for (int i = 0; i < a.length(); i++) {
            int cntA = mapA.containsKey(a.charAt(i)) ? mapA.get(a.charAt(i)) : 0;
            mapA.put(a.charAt(i), count + 1);
            int cntB = mapB.containsKey(b.charAt(i)) ? mapB.get(b.charAt(i)) : 0;
            mapB.put(b.charAt(i), count + 1);
        }
        return A.Equals(B);
        */

        // Testcase(s) 4, 5, 9, 10, 12, 15 are not the same length?
        if (a.length() != b.length()) return false;
        
        String A = a.toLowerCase();
        String B = b.toLowerCase();
        int fA[] = new int[26];
        int fB[] = new int[26];
        
        for (int i = 0; i < A.length(); i++) {
            fA[(int) A.charAt(i) - 97]++;
            fB[(int) B.charAt(i) - 97]++;
        }
        boolean anagrams = true;
        for (int i = 0; i < fA.length; i++) {
            if (fA[i] != fB[i]) {
                anagrams = false;
                break;
            }
        }
        return anagrams;
    }

    public static void main(String[] args) {
    
        Scanner scan = new Scanner(System.in);
        String a = scan.next();
        String b = scan.next();
        scan.close();
        boolean ret = isAnagram(a, b);
        System.out.println( (ret) ? "Anagrams" : "Not Anagrams" );
    }
}

