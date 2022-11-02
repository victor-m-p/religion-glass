#include<stdio.h>
#define flip(X)  ((X) < 0 ? 1 : -1)
int main()
{
    int x = 1;
    int y = 0;
    int z = -1;
    printf("size of float: %zu\n", sizeof(float));
    printf("value of (x, y, z) unflipped (%d, %d, %d)\n", x, y, z);
    printf("value of (x, y, z) flipped (%d, %d, %d)\n", flip(x), flip(y), flip(z));
    return 0;
}
// 