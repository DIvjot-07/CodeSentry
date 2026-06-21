#include <stdio.h>
int main(){
    int a ,b;
    printf("Enter a & b with space:");
    scanf("%d %d" ,&a ,&b);
    int sum=a+b;
    printf("Sum of %d and %d is %d",a,b,sum);
    return 0;
}