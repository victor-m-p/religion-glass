#include<stdio.h>
//https://www.youtube.com/watch?v=zuegQmMdy8M

int main()
{
    int x = 5; // declare int
    int *p; // declare int pointer
    p = &x; // assign pointer
    *p = 6; // modify the value we are pointing to (i.e. modifying x)
    
    // print p and *p (dereferenced p)
    printf("p is %p, *p is %d, x is %d\n", p, *p, x);

    int **q = &p; // declare pointer to pointer
    int ***r = &q; // declare more crazy pointer...

    // double dereferencing:
    printf("value of (q, *q, **q), (%p, %d, %d)\n", q, *q, *(*q));
    return 0;
}
// 