#include <stdio.h>
//#include <math.h>
#define pi 3.14
int main(){
    int radius;
    printf("Enter Radius Of Circle:");
    scanf("%d",&radius);
    float area = pi * radius * radius;
    printf("Area:%f",area);
    return 0;
}