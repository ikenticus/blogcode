import Foundation



guard let N = Int((readLine()?.trimmingCharacters(in: .whitespacesAndNewlines))!)
else { fatalError("Bad input") }

if N % 2 == 1 || (N >= 6 && N <= 20) {
   print("Weird");
} else {
   print("Not Weird");
}

