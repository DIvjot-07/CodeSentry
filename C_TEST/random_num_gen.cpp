#include <iostream>
#include <ctime>

int main(){
    using std::cout;
    srand(time(NULL));
    int num1 = rand();
    cout << num1 << "\n";
    int num2 = rand()%100 + 1; //Number Between 1 And 100
    cout << num2 << "\n";
    return 0;
}