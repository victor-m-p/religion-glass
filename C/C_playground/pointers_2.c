#include<stdio.h>
//https://www.youtube.com/watch?v=zuegQmMdy8M

void Increment(int *p){
    *p = (*p) + 1;
}

int Increment2(int p){
    return p + 1;
}

int main(){
    int a;
    a = 10;
    Increment(&a); // basically does assignment without return 
    printf("a = %d\n", a);

    // achieving the same pythonically 
    int b;
    b = Increment2(a);
    printf("b = %d\n", b);

    return 0;
}