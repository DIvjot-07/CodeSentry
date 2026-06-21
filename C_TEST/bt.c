#include<stdio.h>
#include<stdlib.h>

typedef struct BTnode{
    struct BTnode *lchild;
    int data;
    struct BTnode *rchild;
}BTnode;

BTnode *createBTnode(){
    int value;
    printf("Enter Data:");
    scanf("%d",&value);
    if(value==-1){
        return NULL;
    }
    else{
        BTnode *newbtnode = (BTnode*)(malloc(sizeof(BTnode)));
        newbtnode->data=value;
        newbtnode->lchild=NULL;
        newbtnode->rchild=NULL;
        printf("For Left Child of %d ,",newbtnode->data);
        newbtnode->lchild=createBTnode();
        printf("For Right Child of %d ,",newbtnode->data);
        newbtnode->rchild=createBTnode();
        return newbtnode;
    }
}

void inorder(BTnode *root){
        if(root==NULL){
            return;
        }
        inorder(root->lchild);
        printf("%d ",root->data);
        inorder(root->rchild);
}
    
void preorder(BTnode *root){
        if(root==NULL){
            return;
        }
        printf("%d ",root->data);
        preorder(root->lchild);
        preorder(root->rchild);
}

void postorder(BTnode *root){
        if(root==NULL){
            return;
        }
        postorder(root->lchild);
        postorder(root->rchild);
        printf("%d ",root->data);
}

int main(){
    printf("Create a Binary Tree(Enter -1 for no node)\n");
    BTnode *root=createBTnode();
    printf("\nInorder travesal: ");
    inorder(root);
    printf("\nPreorder traversal: ");
    preorder(root);
    printf("\nPostorder traversal: ");
    postorder(root);
    return 0;
    }