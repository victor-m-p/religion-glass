#include<stdio.h>
#include<string.h>
//https://www.youtube.com/watch?v=zuegQmMdy8M

void print(const char* C){ // const ensures that we cannot modify C
    int i = 0;
    while(*C != '\0')
    {
        //printf("%c", C[i]);
        printf("%c\n", *C);
        printf("%p\n", C);
        C++;
    }
    printf("\n");
}
int main(){
    //char *C = "Hello"; // constant (cannot be changed)
    char C[20] = "Hello";
    print(C);
    return 0;
}