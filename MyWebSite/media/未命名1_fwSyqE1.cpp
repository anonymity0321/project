#include<stdio.h>
#include<stdlib.h>
struct tree {
	int val;
	tree *left;
	tree *right;
}; 
tree *Build(tree *root ,int val){
	if(root==NULL){
		root = (tree*)malloc(sizeof(tree));
		root->val = val;
		root->left = NULL;
		root->right = NULL;
	}
	else
		if(root->val>val)
			root->left=Build(root->left,val);
		else if(root->val<val)
			root->right=Build(root->right,val);
	return root;

}
void print(tree *root){
	if(root==NULL)
		return ;
	printf("%d ",root->val);
	
	print(root->left);
	
	print(root->right);
} 
int main(){
	int n;
	tree *root=NULL;
	printf("请输入数据个数:");
	scanf("%d",&n);
	for(int i=0;i<n;i++){
		int num;
		printf("请输入数据:");
		scanf("%d",&num);
		root=Build(root,num);
	}
	print(root);
} 
