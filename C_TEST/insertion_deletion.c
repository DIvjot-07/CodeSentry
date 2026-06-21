#include <stdio.h>
#define MAX 100
int size;
void insert(int Arr[],int pos);
void delete(int Arr[],int pos);

int main(){
    int Arr[MAX],pos_insert,pos_delete,choice;
    printf("Enter the SIze of Array: ");
    scanf("%d",&size);
    for(int i=0;i<size;i++){
        printf("Enter the Element %d: ",i+1);
        scanf("%d",&Arr[i]);
        }
    printf("Entered Array:");
    for(int j=0; j<size ;j++){
        printf("%d ",Arr[j]);
    }
    while(1){
        printf("\n\n#1 for Insertion \n#2 for Deletion \n#3 for Quit \nEnter Choice:");
        scanf("%d",&choice);
        if(choice==1){
            printf("\nEnter the position of Element to be inserted: ");
            scanf("%d",&pos_insert);
            insert(Arr,pos_insert);
            }
        else if(choice==2){
            printf("\nEnter the position of Element to be deleted: ");
            scanf("%d",&pos_delete);
            delete(Arr,pos_delete);
            }
        else if(choice==3){
            printf("Thanks for using the program");
            return 0;
        }
        else{
            printf("Invalid Choice");
            }
        }
        return 0;
    }

void insert(int Arr[], int pos){
    if(pos< 1|| pos>size+1){
        printf("Invalid Position");
        }
    else{
        int num;
        printf("Enter the Element to be inserted: ");
        scanf("%d",&num);
        for(int i=size-1;i>=pos-1;i--){
            Arr[i+1]=Arr[i];
            }
        Arr[pos-1]=num;
        size++;
        printf("Updated Array:");
        for(int j=0;j<size;j++){
            printf("%d ",Arr[j]);
            }
        }
    }

void delete(int Arr[],int pos){
    if(pos<1 || pos>size){
        printf("Invalid Position");
        }
    else{
        printf("Deleted Element is: %d\n",Arr[pos-1]);
        for(int i=pos-1;i<size-1;i++){
            Arr[i]=Arr[i+1];
            }
        size--;
        printf("Updated Array:");
        for(int j=0;j<size;j++){   
            printf("%d ",Arr[j]);
            }
        }
    }