import Foundation

// Complete the solve function below.
func solve(meal_cost: Double, tip_percent: Int, tax_percent: Int) -> Void {
    let tip = Double(tip_percent) / 100;
    let tax = Double(tax_percent) / 100;
    print(String(format: "The total meal cost is %.0f dollars.", meal_cost * (1 + tip + tax)));
}

guard let meal_cost = Double((readLine()?.trimmingCharacters(in: .whitespacesAndNewlines))!)
else { fatalError("Bad input") }

guard let tip_percent = Int((readLine()?.trimmingCharacters(in: .whitespacesAndNewlines))!)
else { fatalError("Bad input") }

guard let tax_percent = Int((readLine()?.trimmingCharacters(in: .whitespacesAndNewlines))!)
else { fatalError("Bad input") }

solve(meal_cost: meal_cost, tip_percent: tip_percent, tax_percent: tax_percent)

