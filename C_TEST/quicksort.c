#include <stdio.h>

void swap(int *a,int *b){
    int temp=*b;
    *b=*a;
    *a=temp;
}

int partition(int A[],int low,int high){
    int i=low,x=A[i];
    for(int j=low+1;j<=high;j++){
        if(A[j]<=x){
            i++;
            swap(&A[i],&A[j]);
        }
    }
    swap(&A[i],&A[low]);
    printf("pivot: %d\n",i);
    return i;
}

void display(int A[],int n){
    printf("Array:");
    for(int i=0;i<n;i++){
        printf("%d ",A[i]);
    }
    printf("\n");
}

void quicksort(int A[],int low,int high){
    if(low<high){
        int pivot=partition(A,low,high);
        quicksort(A,low,pivot-1);
        quicksort(A,pivot+1,high);
    }
}

int main(){
    int A[]={2,5,1,7,4,3};
    int n=6;
    display(A,n);
    quicksort(A,0,n-1);
    printf("Sorted ");
    display(A,n);
}