//Enter your code here. Read input from STDIN. Print output to STDOUT
BufferedReader reader = new BufferedReader(new InputStreamReader(System.in))
n = reader.readLine().toInteger()
for (i = 1; i <= 10; i++) {
   System.out.println("$n x $i = " + (n*i))
}
