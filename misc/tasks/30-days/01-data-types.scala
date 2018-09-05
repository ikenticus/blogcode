object Solution {
    def main(args: Array[String]) {
        val i = 4
        val d = 4.0
        val s = "HackerRank "

		// Read values of another integer, double, and string variables
        // Note use scala.io.StdIn to read from stdin
        val i2 = scala.io.StdIn.readLine().toInt
        val d2 = scala.io.StdIn.readLine().toDouble
        val s2 = scala.io.StdIn.readLine()

        // Print the sum of both the integer variables
        println(i + i2)
        
        // Print the sum of both the double variables
        println(d + d2)
        
        // Concatenate and print the string variables
        // The 's' variable above should be printed first.
        println(s + s2)
    }
}
