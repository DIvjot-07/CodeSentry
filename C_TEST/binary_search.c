#include <stdio.h>

int binarysearch(int A,int low ,int high,int el){
    if(low>high){
        return -1;
    }
    int mid = (low + high)/ 2;
    if (A[mid] == el){
        return mid;
    }
    else if (A[mid] > el){
        return binarySearch(A, low, mid - 1, el);
    }
    else{
        return binarySearch(A, mid + 1, high, el);
    }
}

void display(int A[],int n){
    printf("ARRAY:");
    for(int i=0;i<n;i++){
        printf("%d ",A[i]);
    }
    printf("\n");
}
int main(){
    int Arr[6]={1,3,4,1,5,8},el;
    display(Arr,6);
    printf("Enter Element to search:");
    scanf("%d",&el);
    int bs=binarysearch(Arr,0,6,el);
    if (bs == -1){
        printf("\nElement %d not found in array\n", el);
    }
    else{
        printf("\nElement %d found at index %d\n", el,bs);
    }
    return 0;
}