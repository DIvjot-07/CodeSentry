#include <iostream>
#include <cmath>

int main(){
    using std::cout,std::cin,std::endl;
    cout << "****CAlCULATOR MENU****" << endl;
    cout << "1. for Addition \n2. for Subtraction \n3. for multiplication \n4. for Division \n5. for Exponential \n6. for Exit " << endl ;
    while(true){
        double choice, num1, num2, innerchoice = 0;
        cout << "\nEnter Choice : ";
        cin >> choice ;
        if(choice == 6){
            break;
        }
        else if(choice > 6 || choice < 1){
            cout << "Invalid Choice" << endl;
            continue;
        }

        cout << "Enter Number 1 : ";
        cin >> num1 ;
        cout << "Enter Number 2 : ";
        cin >> num2 ;

        if(choice == 1){
            cout << "Addition : " << num1 + num2 << endl;
        }
        else if(choice == 2){
            cout << "1. for Number 1 - Number 2 \n2. for Number 2 - Number 1 "<< endl;
            cout << "Enter Choice : ";
            cin >> innerchoice ;
            if(innerchoice == 1) cout << "Subtraction : " << num1 - num2 << endl;
            else if(innerchoice == 2) cout << "Subtraction : " << num2 - num1 << endl;
            else cout << "Invalid Choice" << endl;
        }
        else if(choice == 3){
            cout << "Multiplication : " << num1 * num2 << endl;
        }
        else if(choice == 4){
            cout << "1. for Number 1 / Number 2 \n2. for Number 2 / Number 1 "<< endl;
            cout << "Enter Choice : ";
            cin >> innerchoice ;
            if(innerchoice == 1) cout << "Division : " << num1 / num2 << endl;
            else if(innerchoice == 2) cout << "Division : " << num2 / num1 << endl;
            else cout << "Invalid Choice" << endl;
        }
        else if(choice == 5){
            cout << "1. for Number 1 ^ Number 2 \n2. for Number 2 ^ Number 1 "<< endl;
            cout << "Enter Choice : ";
            cin >> innerchoice ;
            if(innerchoice == 1) cout << "Exponential : " << pow(num1,num2) << endl;
            else if(innerchoice == 2) cout << "Exponential : " << pow(num2,num1) << endl;
            else cout << "Invalid Choice" << endl;
        }
    }
    return 0;
}