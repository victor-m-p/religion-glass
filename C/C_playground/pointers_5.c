#include<stdio.h>
int main(){

    int A[5];
    int *p = A;
    printf("p = %p, *p = %d\n", p, *p);

    int B[2][3];
    printf("hello: %d\n", B[1][1]);
    printf("sizeof B: %d\n", sizeof(B[1]));     
    //int (*p)[3] = B;

    return 0;
}