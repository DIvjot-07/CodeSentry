#include <iostream>

double get_total(double price[],int size){
    double total=0.0;
    for(int i=0; i< size; i++){
        total += price[i];
    }
    return total;
}
int main(){
    double price[]={122.99, 11.23, 23.42, 328.14, 42.52};
    int size=((sizeof(price))/(sizeof(price[0])));
    double result = get_total(price,size);
    std::cout << "Total : " << result << std::endl;
    return 0;
}