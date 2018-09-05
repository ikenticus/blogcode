class Person
    attr_accessor :age
    def initialize(initialAge)
        # Add some more code to run some checks on initialAge   
        self.age = initialAge
        if self.age < 0
            puts "Age is not valid, setting age to 0.\n"
            self.age = 0
        end
    end
    def amIOld()
      # Do some computations in here and print out the correct statement to the console
        if self.age < 13
            print "You are young.\n"
        elsif self.age >= 13 and self.age < 18
            print "You are a teenager.\n"
        else
            print "You are old.\n"
        end
    end
    def yearPasses()
      # Increment the age of the person in here
        self.age += 1
    end
end

T=gets.to_i
for i in (1..T)do
    age=gets.to_i
    p=Person.new(age)
    p.amIOld()
    for j in (1..3)do
        p.yearPasses()
    end
    p.amIOld
  	puts ""
end

