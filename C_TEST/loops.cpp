#include <iostream>

int main(){
    int x=20;
    std::cout << "Numbers from 1 to " << x << " : ";
    for(int i=0;i<x;i++){
        std::cout << i+1 <<" ";
    }
    std::cout << std::endl;

    int y=12;
    while(y!=5){
        if(y>5){
            std::cout << "Big, y = " << y-- << std::endl;
        }
        if(y<5){
            std::cout << "Small, y = " << y++ << std::endl;
        }
    }
    std::cout << "y==" << y << std::endl;

    return 0;
}