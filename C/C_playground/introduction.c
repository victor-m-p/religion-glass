#include <stdio.h>
#include <stdlib.h> // e.g. pow()
#include <math.h>

// prototyping
double cube(double num); // prototyping
int max(int num1, int num2, int num3);
int min(int num1, int num2, int num3);

// basically a class
struct Student{
    char name[50]; // maximum 50 characters
    char major[50];
    int age;
    double gpa;
}; // important to also escape this 

int main() { // special function which gets called when we execute
    // basics
    char characterName[] = "John";  
    int characterAge = 35; 
    // printf() displays the string inside quotation
    printf("He is called %s\n", characterName);
    printf("He is %d years old\n", characterAge);
    // modify one of the variables
    characterAge = 36;
    printf("Wups, now he is %d years old\n", characterAge);

    // data types
    int easyInteger = 40;
    double floatDouble = 3.7; 
    char singleCharacter = 'H'; // notice single quotes
    char stringArray[] = "Hello"; // notice double quotes

    // printf
    printf("My favority number is %d\n", 500); // single digit
    printf("My favority %s is %d", "number", 500); // several 
    printf("My favority number is %f\n", 500.1); // for double / float
    printf("My favority number is %f\n", 5 + 5.1);
    printf("2 ** 3 = %f\n", pow(2, 3)); // 2 ** 3
    printf("square root of 36: %f\n", sqrt(36)); // sqrt
    printf("ceil of 36.356: %f\n", ceil(36.356)); // ceil
    printf("floor of 36.356: %f\n", floor(3.356)); // floor
    
    // constants
    const int FAV_NUM = 5; // constants generally ALL CAPITAL
    printf("My favorite constant is %d\n", FAV_NUM);

    // get user input
    /*
    int age;
    printf("Enter your age: ");
    scanf("%d", &age); // what type and where to store (the & is a POINTER)
    printf("You are %d years old\n", age);
    */
   
    // basic calculator
    int num1 = 5;
    int num2 = 10;
    printf("total: %d\n", num1 + num2);

    // arrays and variables
    int numberArray[] = {1, 2, 4, 8};
    printf("element index 0: %d\n", numberArray[0]);
    numberArray[0] = 100;
    printf("element index 0 is now: %d\n", numberArray[0]);
    // initializing without the values
    int undefinedArray[10]; // capacity = 10 (memory allocation)
    undefinedArray[1] = 8; // putting in a value at index 1 
    
    // functions without return 
    sayHi(); // calling the function 
    sayHo("Victor", 26); // we already specified string (array of character) in sayHo()

    // function with return 
    printf("Answer: %f\n", cube(2.5));
    //answer = cube(2.5);
    //printf("Answer %f: answer")

    // if statements
    printf("largest value: %d\n", max(2, 3, 1));
    printf("smallest value: %d\n", min(2, 3, 1));

    // better calculator
    /*
    double numx;
    double numy;
    char op;

    printf("Enter a number: ");
    scanf("%lf", &numx);
    printf("Enter operator: ");
    scanf(" %c", &op);
    printf("Enter a number: ");
    scanf("%lf", &numy);

    if(op == '+'){ // important with single quotes here! 
        printf("%f\n", numx + numy);
    } else if(op == '-'){
        printf("%f\n", numx - numy);
    } else if(op == '/'){
        printf("%f\n", numx / numy);
    } else if(op == '*'){
        printf("%f\n", numx * numy);
    } else{
        printf("invalid operator\n");
    }
    */

    // switch statements
    char grade = 'B';

    switch(grade){
        case 'A' : 
            printf("You did great\n");
            break;
        case 'B' :
            printf("You did OK\n");
            break;
        case 'C' :
            printf("You did poorly\n");
            break;
        default : 
            printf("Invalid grade");
    }

    switch(grade);

    // structs
    struct Student student1; // creating an instance (container)
    student1.age = 22;
    student1.gpa = 3.5;
    strcpy( student1.name, "Jim");
    strcpy( student1.major, "Archaeology");
    printf("gpa of student1: %f\n", student1.gpa);
    printf("major of student %s\n", student1.major);

    struct Student student2;
    student2.age = 33;
    student2.gpa = 10.0;
    strcpy( student2.name, "Baptiste");
    strcpy( student2.major, "Millitary");
    printf("name of student2 %s\n", student2.name);

    // while loop
    int index = 1;
    printf("while loop:\n");
    while(index <= 5){
        printf("%d\n", index);
        index++; // shortcut for index = index + 1
    }

    // for loops
    int i; 
    printf("for loop 1:\n");
    for(i = 1; i <= 5; i++){ // initial, while, increment
        printf("%d\n", i);
    }

    // for loop over array of elements
    int loopNumbers[] = {1, 2, 4, 8, 16, 32, 64, 128};
    printf("for loop 2:\n");
    for(i = 0; i < 6; i++){
        printf("%d\n", loopNumbers[i]);
    };

    // two-dimensional arrays & nested loops
    printf("--two dimensional arrays--\n");
    int nums[3][2] = { // have to specify size
                    {1, 2},
                    {3, 4},
                    {5, 6}
                    };

    printf("printing index (0, 0): %d\n", nums[0][0]);

    // nested for-loops
    int ix, jx; // just because we used i, j earlier
    for(ix = 0; ix < 3; ix++){
        for(jx = 0; jx <2; jx++){
            printf("%d,", nums[ix][jx]);
        }
        printf("\n");
    };
    
    // memory addresses
    int ages = 30; // this gets stored in a specific RAM memory location
    double gpas = 3.4;
    char grades = 'A';

    // printing out the physical memory address
    printf("age stored at: %p\n", &ages); // p stands for pointer

    // pointers (a memory address)
    // not clear what this is useful for thought
    int agex = 30;
    int * pAgex = &agex; // formality to start with p and then the name of var
    printf("agex memory address: %p\n", &agex); // &agex is a pointer

    // dereferencing pointers
    printf("%d\n", *pAgex); // getting the value from the mem. location

    // writing files
    //FILE * fpointer = fopen("employees.txt", "w"); // could also append (a).
    //fprintf(fpointer, "Jim, Salesman\nPam, Receptionist");
    //fclose(fpointer); // always want to close (remove from memory)

    // reading files
    char line[255];
    FILE * fpointer = fopen("employees.txt", "r");
    fgets(line, 255, fpointer); // read first line of file (generator)
    printf("%s", line);
    fclose(fpointer);

    // return 
    return 0;
}

// functions without return 
void sayHi(){ // void: no return type (no return)
    printf("Hi user\n");
}

// function without return (with parameter)
void sayHo(char name[], int age){
    printf("Ho %s, you are %d years old\n", name, age);
}

// functions with return
double cube(double num){
    double result = num * num * num;
    return result;
}

// if statement (and: &&) (or: ||)
int max(int num1, int num2, int num3){
    int result;
    if(num1 >= num2 && num1 >= num3){
        result = num1;
    } else if(num2 >= num1 && num2 >= num3){
        result = num2;
    } else{
        result = num3;
    }
    return result;
} 

// if statement with negation
// does not actually quite return min, but we get the syntax idea
int min(int num1, int num2, int num3){
    if(!(num1 >= num2 && num1 >= num3)){
        return num1;
    } else if(!(num2 >= num1 && num2 >= num3)){
        return num2; 
    } else{
        return num3;
    }
}
