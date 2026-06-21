#include <stdio.h>
void swap(int *a,int *b){
    int temp=*a;
    *a=*b;
    *b=temp;
}
int partition(int A[],int low ,int high){
    int i=low-1;
    int pivot=A[high];
    for(int j=low;j<high;j++){
        if(A[j]<=pivot){
            i++;
            swap(&A[i], &A[j]);
        }
    }
    swap(&A[high],&A[i+1]);
    return i+1; 
}
void display(int A[],int n){
    printf("ARRAY:");
    for(int i=0;i<n;i++){
        printf("%d ",A[i]);
    }
    printf("\n");
}
void quicksort(int A[],int low,int high){
    if(low<high){
    int p=partition(A,low,high);
    quicksort(A,low,p-1);
    quicksort(A,p+1,high);
    }
}
int main(){
    int Arr[6]={1,3,4,1,5,8};
    int p=partition(Arr,0,5);
    printf("Partition:%d\n",p);
    display(Arr,6);
    quicksort(Arr,0,5);
    printf("QUICK SORTED ");
    display(Arr,6);
    return 0;
}