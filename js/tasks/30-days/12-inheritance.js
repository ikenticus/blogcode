'use strict';

var _input = '';
var _index = 0;
process.stdin.on('data', (data) => { _input += data; });
process.stdin.on('end', () => {
    _input = _input.split(new RegExp('[ \n]+'));
    main();    
});
function read() { return _input[_index++]; }

/**** Ignore above this line. ****/

class Person {
    constructor(firstName, lastName, identification) {
        this.firstName = firstName;
        this.lastName = lastName;
        this.idNumber = identification;
    }
    
    printPerson() {
        console.log(
            "Name: " + this.lastName + ", " + this.firstName 
            + "\nID: " + this.idNumber
        )
    }
}

class Student extends Person {
    /*	
    *   Class Constructor
    *   
    *   @param firstName - A string denoting the Person's first name.
    *   @param lastName - A string denoting the Person's last name.
    *   @param id - An integer denoting the Person's ID number.
    *   @param scores - An array of integers denoting the Person's test scores.
    */
    // Write your constructor here
    constructor(firstName, lastName, identification, scores) {
        super(firstName, lastName, identification);
        this.scores = scores;
    }

    /*	
    *   Method Name: calculate
    *   @return A character denoting the grade.
    */
    // Write your method here
    calculate() {
        let sum = 0;
        for (let i = 0; i < this.scores.length; i++) {
            sum += parseInt(this.scores[i], 10 );
        }
        let avg = sum / this.scores.length;
        
        let grade;
        switch(true) {
           case avg <= 100 && avg >= 90:
                grade = 'O';
                break;
            case avg < 90 && avg >= 80:
                grade = 'E';
                break;
           case avg < 80 && avg >= 70:
                grade = 'A';
                break;
           case avg < 70 && avg >= 55:
                grade = 'P';
                break;
           case avg < 55 && avg >= 40:
                grade = 'D';
                break;
           default:
                grade = 'T';        
        }
        return grade;
    }
}

function main() {
    let firstName = read()
    let lastName = read()
    let id = +read()
    let numScores = +read()
    let testScores = new Array(numScores)
    
    for (var i = 0; i < numScores; i++) {
        testScores[i] = +read()  
    }

    let s = new Student(firstName, lastName, id, testScores)
    s.printPerson()
    s.calculate()
    console.log('Grade: ' + s.calculate())
}

