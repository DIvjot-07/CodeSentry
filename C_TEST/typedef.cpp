#include <iostream>

using text_t=std::string;
using num_t=int;

int main(){
    using std::cout,std::cin,std::endl;
    text_t name;
    cout << "Enter Name : " ;
    std::getline(cin,name);
    num_t age;
    cout << "Enter Age : " ;
    cin >> age;
    cout << "Name : " << name << "\nAge : " << age << endl;
}
