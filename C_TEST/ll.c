#include<stdio.h>
#include<stdlib.h>
#define N 5

int Stack[N];
int TOS=-1;

void Push(){
    if(TOS==N-1){
        printf("Stack Overflow");
        return;
    }
    int value;
    printf("Enter Element:");
    scanf("%d",&value);
    TOS++;
    Stack[TOS]=value;
    printf("Entered Element is %d\n",value);
    }

void Pop(){
    if(TOS==-1){
        printf("Stack Underflow");
        return;
    }
    printf("Deleted Element is %d\n",Stack[TOS]);
    TOS--;
    }
    
void Peak(){
    printf("Top of the Stack:%d\n",Stack[TOS]);
    }
    
void Display(){
    if(TOS==-1){
        printf("Stack Underflow");
        return;
        }
    printf("Stack:");
    for(int i=0;i<=TOS;i++){
        printf("%d  ",Stack[i]);
        }
    }  

int main(){
    printf("CHOICES\n#1 For Push\n#2 For Pop\n#3 For Display\n#4 For Peak\n#5 For Exit\n");
        while(1){
        int choice;
        printf("\nEnter choice:");
        scanf("%d",&choice);
        if(choice==1){
            Push();
            }
        else if(choice==2){
            Pop();
            }
        else if(choice==3){
            Display();
            }
        else if(choice==4){
            Peak();
            }
        else if(choice==5){
            printf("Thanks for using program");
            exit(0);   
            }
        else{
            printf("Invalid Choice\n");
            }
            }
            
    return 0;
}
