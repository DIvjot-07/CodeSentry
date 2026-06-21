#include <stdio.h>

void merge(int A[],int low ,int mid,int high){
    int i,j,k=low;
    int n1=mid-low+1;
    int n2=high-mid;
    int L[n1],R[n2];
    for(i=0;i<n1;i++){
        L[i]=A[low+i];
    }
    for(j=0;j<n2;j++){
        R[j]=A[mid+1+j];
    }
    i=j=0;
    while(i<n1 &&j<n2){
        if(L[i]<=R[j]){
            A[k++]=L[i++];
        }
        else{
            A[k++]=R[j++];
        }
    }
    while(i<n1){
        A[k++]=L[i++];
    }
    while(j<n2){
        A[k++]=R[j++];
    }
}

void mergesort(int A[],int low ,int high){
    if(low<high){
        int mid=(high+low)/2;
        mergesort(A,low,mid);
        mergesort(A,mid+1,high);
        merge(A,low,mid,high);
    }
}
void display(int A[],int n){
    printf("Array:");
    for(int i=0;i<n;i++){
        printf("%d ",A[i]);
    }
    printf("\n");
}

int main() {
    int A[]={2,5,1,0,7,3,6,4,9};
    int n=9;
    display(A,n);
    mergesort(A,0,n-1);
    printf("Merge Sorted ");
    display(A,n);
    return 0;
}