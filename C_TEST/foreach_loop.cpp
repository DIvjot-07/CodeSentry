#include <iostream>

int main(){
    std::string cars[] = {"BMW M4","Ferrai SF90","Ford shelby 1967"};
    for (std::string car:cars){
        std::cout << car << std::endl;
    }
    return 0;
}