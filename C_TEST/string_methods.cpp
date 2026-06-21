#include <iostream>

int main(){
    using std::string,std::cout,std::cin,std::endl;
    string name ,num;
    cout << "Enter Name : ";
    std::getline(cin,name);
    cout << "Enter Number : ";
    std::getline(cin, num);
    cout << "String : " << name << endl;
    int fin = name.find(" ");
    cout << "Space Found In String At Index: " << fin << endl;
    cout << "Erased Space From String : " << name.erase(fin,1) << endl;
    cout << "String Length : " << name.length() << endl;
    cout << "Is String Empty? : " << name.empty() << endl;
    cout << "String Append : " << name.append(num) << endl;
    cout << "String Insert : " << name.insert(name.length(),"@gmail.com") << endl;
    cout << "**** String Traverse ****" << endl;
    for(int i = 0; i < name.length(); i++){
        cout << "String Element At Index " << i << ": " << name.at(i) << endl;
    }
    name.clear();
    cout << "String Deleted " << endl;
    cout << "Is String Empty? : " << name.empty() << endl;
}