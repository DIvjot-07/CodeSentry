#include <iostream>
#include <cmath>

int main(){
    using std::cout,std::cin,std::endl;
    double height,base,hypotenuse;
    cout << "Enter Height : " ;
    cin >> height;
    cout << "Enter Base : " ;
    cin >> base;
    hypotenuse = sqrt(pow(height,2)+pow(base,2));
    cout << "Hypotenuse : " << hypotenuse << endl;
    return 0;
}