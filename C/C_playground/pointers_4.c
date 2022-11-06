#include<stdio.h>
#include<string.h>
//https://www.youtube.com/watch?v=zuegQmMdy8M

int main(){
    char C[4];
    C[0] = 'J';
    C[1] = 'O';
    C[2] = 'H';
    C[3] = 'N';  
    printf("%s\n", C); // actually looks like we don't need to terminate (as he says in the vid.)
    
    int len = strlen(C);
    printf("length = %d\n", len);
    return 0;
}