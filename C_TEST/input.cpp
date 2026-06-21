#include <iostream>
#include <string>

int main(){
    int a, b, c, sum;
    std::string first_name, last_name, name;
    std::cout << "Enter a : ";
    std::cin >> a;
    std::cout << "Enter b and c : " ;
    std::cin >> b >> c; //Two or more inputs at same time 
    std::cout << "Enter First Name : " ;
    std::cin >> first_name; //Only reads first word
    std::cout << "Enter Last Name : " ;
    std::cin >> last_name;
    std::cout << "Enter Name : " ;
    std::cin.ignore(); //To handle new line in buffer
    std::getline(std::cin, name); //Read whole sentence
    std::cout << "Sum of a, b and c : " << a+b+c << "\nFirst Name : " << first_name << "\nLast Name : " << last_name <<"\nFull Name : " << name << std::endl;
    return 0;
}