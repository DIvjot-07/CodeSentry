#include <stdio.h>
#include <math.h>
int main(){
    int side;
    printf("Enter Side Of SQUARE:");
    scanf("%d",&side);
    int area = pow(side,2);
    printf("Area of SQUARE with side %d is %d", side, area);
    return 0;
}