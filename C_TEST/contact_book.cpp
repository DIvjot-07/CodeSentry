#include <iostream>
#include <string>
#define N 5

std::string name[N], phones[N];
int n=0;

void addContact(){
    if(n==N){
        std::cout << "Contact Book Full" << std::endl;
        return;
    }
    std::string Name,number;
    std::cout << "Enter Name : ";
    std::cin.ignore();
    std::getline(std::cin,Name);
    std::cout << "Enter Number : ";
    std::getline(std::cin,number);
    name[n]=Name;
    phones[n]=number;
    n++;
}

void display(){
    if(n==0){
        std::cout << "No Contacts\n";
        return;
    }
    std::cout << "\n----Contacts----\n" << std::endl; 
    for(int i=0 ; i < n ; i++){
        std::cout << "Name : " << name[i] << "\nNumber : " << phones[i] << "\n" << std::endl;
    }
}

std::string * SearchContact(std::string na){
    for(int i = 0 ; i < n ; i++ ){
        if(na==name[i]){
            return &name[i];
        }
    }
    return nullptr;
}

int main(){
    std::cout << "\n----Main Menu----\n" << std::endl; 
    std::cout << "1. Add Contact \n2. Search Contact \n3. View All \n4. Exit\n";
    while(true){
        int choice;
        std::cout << "\nEnter Choices (1-4) : ";
        std::cin >> choice;
        std::cout << "Your Choice : " << choice << std::endl;
        if(choice == 1){
            addContact();
        }
        else if(choice == 2){
            std::string na;
            std::cout << "Enter Name for Searching : ";
            std::cin.ignore();
            std::getline(std::cin ,na);
            std::string *result = SearchContact(na);
            if(result==nullptr){
                std::cout << "Contact Not found" << std::endl;
            }
            else{
                for(int i = 0 ; i < n ; i++){
                    if(name[i]== *result){
                        std::cout << "Contact Number : " << phones[i] << std::endl;
                    }
                }
            }
        }
        else if(choice == 3){
            display();
        }
        else if(choice == 4){
            break;
        }
        else{
            std::cout << "Wrong Choice " << std::endl;
        }
    }
    return 0;
}