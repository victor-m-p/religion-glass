#include <stdio.h> 
#include <string.h>
#include <stdlib.h> // e.g. malloc
// https://www.youtube.com/watch?v=dqa0KMSMx2w
typedef struct // alias with typedef 
{
    char name[50];
    char id[10];
    int age;
    int grades[5];
} Student; 

typedef struct
{
    int x;
    int y;
} Point;

typedef struct 
{
    int *array;
} Data;

void print_student(Student student); // function declaration 

int main(void)
{
    Student kevin; // do not need struct here because of typedef 
    kevin.age = 40;
    strcpy(kevin.name, "Kevin");
    strcpy(kevin.id, "000123123");
    kevin.grades[0] = 1;
    kevin.grades[1] = 2;
    kevin.grades[2] = 3;
    kevin.grades[3] = 4;
    kevin.grades[4] = 5;
    print_student(kevin);
    
    Point p1 = {5, 10}; // assign x = 5, y = 10
    printf("p1.x: %d, p1.y: %d\n", p1.x, p1.y);
    Point p2 = {.x = 2, .y = 8}; // same -- then we can also reverse.. 
    printf("p2.x %d, p2.y %d\n", p2.x, p2.y);
    
    Data x; 
    Data y;
    x.array = malloc(sizeof(int) * 5); // allocate size of five integers
    y.array = malloc(sizeof(int) * 5); // same 

    x.array[0] = 1;
    x.array[1] = 2;
    x.array[2] = 3;
    x.array[3] = 4;
    x.array[4] = 5;

    y.array[0] = 9;
    y.array[1] = 9;
    y.array[2] = 9;
    y.array[3] = 9;
    y.array[4] = 9;

    x = y;

    for (int i=0;i<5;i++){
        printf("x.array[%d] = %d\n", i, x.array[i]);
    }

    return 0;
}

void print_student(Student student){ // function definition 
    printf("Age: %d\n", student.age);
    printf("id; %s\n", student.id);
    printf("Name: %s\n", student.name);
    int i;
    for(i=0;i<5;i++){
        printf("Grade %d = %d\n", i, student.grades[i]);
    }
}

