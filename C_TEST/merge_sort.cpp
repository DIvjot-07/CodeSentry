#include <iostream>

void merge(int A[], int low, int mid, int high){
    int i,j,k=low;
    int n1=mid-low+1, n2=high-mid;
    int L[n1],R[n2];
    for(i=0;i<n1;i++){
        L[i]=A[i+low];
    }
    for(j=0;j<n1;j++){
        R[j]=A[j+mid+1];
    }
    i=j=0;
    while(i<n1 && j<n2){
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

void merge_sort(int A[],int low,int high){
    if(high>low){
        int mid=(high+low)/2;
        merge_sort(A,low,mid);
        merge_sort(A,mid+1,high);
        merge(A,low,mid,high);
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
    merge_sort(A,0,n-1);
    display(A,n);
}