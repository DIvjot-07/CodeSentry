#include <iostream>
#include <cstdlib>
#include <ctime>

bool check(int guess, int number, int *attempt){
    (*attempt)++;
    if(guess > number){
        std::cout << "Guess Too High! Try Again " << std::endl;
        return false ;
    }
    if(guess < number){
        std::cout << "Guess Too Low! Try Again " << std::endl;
        return false ;
    }
    else{
        std::cout << "Yayayayay Correct Guess " << std::endl;
        return true ;
    }
}

int main(){
    srand(time(0));
    const int Max=100;
    int number=rand() % Max +1;
    int guess,attempt=0;
    bool won=false;
    std::cout << "Guess the number(1-100)" << std::endl;
    while(!won){
        std::cout << "Enter Guess : " ;
        std::cin >> guess;
        if(guess > Max || guess < 1){
            std::cout << "Enter Guess between 1 and 100 " << std::endl;
            continue;
        }
        won = check(guess,number,&attempt);
    }
    std::cout << "Attempts : " << attempt << std::endl;
    if(attempt <= 5){
        std::cout << "Amazing " << std::endl;
    }
    else if(attempt <= 10){
        std::cout << "Nice Try " << std::endl;
    }
    else{
        std::cout << "Keep Practicing " << std::endl;
    }
}