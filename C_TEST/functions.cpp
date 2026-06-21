#include <iostream>

int func(std::string name , int a,int b){
    std::cout << "Hello " << name << std::endl;
    return a+b;
}

void func1(int *a){
    *a*=2;
}

int main(){
    int a=20,b=13;
    std::string name = "Divjot";
    int sum=func(name,a,b);
    std::cout << "Sum of "  << a << " & " << b <<" : " << sum <<std::endl;
    std::cout << "Value of a before function " << a << std::endl;
    func1(&a);
    std::cout << "Value of a after function " << a << std::endl;
    return 0;
}