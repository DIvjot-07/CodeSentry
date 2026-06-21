#include <iostream>

void swap(int *a,int *b){
    int temp=*a;
    *a=*b;
    *b=temp;
}

int partition(int A[],int low,int high){
    int i=low;
    int x=A[low];
    for(int j=low+1;j<=high;j++){
        if(A[j]<=x){
            i++;
            swap(&A[i],&A[j]);
        }
    }
    swap(&A[i],&A[low]);
    return i;
}

void quick_sort(int A[],int low,int high){
    if(high>low){
        int pivot=partition(A,low,high);
        quick_sort(A,low,pivot-1);
        quick_sort(A,pivot+1,high);
    }
}

void display(int A[],int n){
    std::cout << "Array : " ;
    for(int i=0;i<n;i++){
        std::cout << A[i] << " ";
    }
    std::cout << std::endl;
}

int main(){
    int A[]={10,4,2,1,12,112,7};
    int n=sizeof(A)/sizeof(A[0]);
    display(A,n);
    quick_sort(A,0,n-1);
    display(A,n);
}