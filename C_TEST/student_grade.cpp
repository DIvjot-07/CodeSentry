#include <iostream>
#include <string>

double average(int *arr,int size){
    int sum=0;
    for(int i=0 ; i<size ;i++){
        sum += *(arr + i);
    }
    return (double) sum / size;
}

int main(){
    int marks[5], size=5;
    std::string name;
    std::cout << "Enter Name : " ;
    std::getline(std::cin,name);
    for(int i=0 ; i<size ; i++){
        std::cout << "Enter Marks for Subject " << i+1 << " : " ;
        std::cin >> marks[i];
    }
    std::cout << "Name : " << name << std::endl;
    double avg=average(marks,size);
    std::cout << "Average : " << avg << std::endl;
    char grade ;
    if(avg>90){
        grade = 'A';
    }
    else if(avg>75 && avg<90){
        grade = 'B';
    }
    else if(avg>60 && avg<75){
        grade = 'C';
    }
    else if(avg>45 && avg<60){
        grade = 'D';
    }
    else if(avg>30 && avg<45){
        grade = 'E';
    }
    else{
        grade = 'F';

    }
    std::cout << "Grade : " << grade << std::endl;
    if(grade=='F'){
        std::cout << "Fail" << std::endl;
    }
    else{
        std::cout << "Pass" << std::endl;
    }

    return 0;
}