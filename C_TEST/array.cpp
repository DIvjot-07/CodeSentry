#include <iostream>
#include <vector>

int main(){
    int arr[]={1,2,3,4,5}; //static
    int n=sizeof(arr)/sizeof(arr[0]);
    std::cout << "Array : ";
    for(int i=0;i<n;i++){
        std::cout << arr[i] << "  ";
    }
    std::cout << std::endl;
    std::vector<int> v={1,3,5}; //Dynamic
    std::cout << "Size of Vector before pop/push: " << v.size() << std::endl;
    v.push_back(7);
    v.push_back(8);
    v.push_back(9);
    v.pop_back();
    v.pop_back();
    v.push_back(9);
    std::cout << "Vector : ";
    for(int i=0;i<v.size();i++){
        std::cout << v[i] << "  ";
    }
    std::cout << std::endl;
    std::cout << "Size of Vector : "<< v.size() << std::endl;
    return 0;
}