#include <stdio.h>
#define N 20

int profit[N];
int deadline[N];
int slot[N];
int job_id[N];

void bubble(int num){
    for(int i=0;i<num-1;i++){
        for(int j=0;j<num-1-i;j++){
            if(profit[j] < profit[j+1]){
                int temp1=profit[j+1];
                profit[j+1]=profit[j];
                profit[j]=temp1;
                int temp2=deadline[j+1];
                deadline[j+1]=deadline[j];
                deadline[j]=temp2;
                int temp3 = job_id[j+1];
                job_id[j+1] = job_id[j];
                job_id[j] = temp3;
            }
        }
    }
}

int job_sequencing(int num,int max){
    for(int i=0 ;i<num;i++){
        for(int j=deadline[i];j>0;j--){
            if(slot[j] == -1){
                slot[j] = i;
                break;
            }
        }
    }
    int total_profit = 0;
    for(int i = 1 ;i<=max;i++){
        if(slot[i] != -1){
            total_profit += profit[slot[i]];
            printf("J%d >> ", job_id[slot[i]]);
        }
    }
    printf("Deadline reached\n");
    return total_profit;
}

int main() {
    int num;
    printf("Enter Number of Jobs:");
    scanf("%d",&num);
    printf("\n");
    for(int i=0;i<num;i++){
        job_id[i] = i + 1;
    }
    for(int i=0;i<num;i++){
        printf("For Job %d\n",i+1);
        printf("Enter profit:");
        scanf("%d",&profit[i]);
        printf("Enter Deadline:");
        scanf("%d",&deadline[i]);
        printf("\n");
    }
    int max = deadline[0];
    for(int i = 1; i < num; i++) {
        if(deadline[i] > max) {
            max = deadline[i];
        }
    }
    for(int i=1;i<=max;i++){
        slot[i]=-1;
    }
    bubble(num);
    printf("Maximum Profit is %d",job_sequencing(num,max));
    return 0;
}