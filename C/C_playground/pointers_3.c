#include<stdio.h>
//https://www.youtube.com/watch?v=zuegQmMdy8M
//pointer arithmetic
int main(){
    int A[] = {2, 4, 5, 8, 1};
    printf("A val. = %d. A val. = %d\n", A[0], (*(A+0))); // equivalent
    
    int *p;
    p = &A[0];
    printf("p = %p, *p = %d\n", p, *p);
    printf("p+1 = %p, *(p+1) = %d\n", p+1, *(p+1)); // parenthesis here important

    int i;
    for(i=0;i<5;i++){
        printf("address = %p ", &A[i]);
        printf("value = %d\n", A[i]);
    } 

    return 0;
}