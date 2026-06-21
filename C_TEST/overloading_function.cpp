#include <iostream>

void car(std::string company){
    std::cout << "Car Company : " << company << std::endl;
    std::cout << std::endl;
}

void car(std::string company,std::string model){
    std::cout << "Car Company : " << company << std::endl;
    std::cout << "Car Model : " << model << std::endl;
    std::cout << std::endl;
}

void car(std::string company,std::string model,int capacity){
    std::cout << "Car Company : " << company << std::endl;
    std::cout << "Car Model : " << model << std::endl;
    std::cout << "Car Capacity : " << capacity << " Litres" << std::endl;
    std::cout << std::endl;
}

void car(std::string company,std::string model,int capacity,std::string engine){
    std::cout << "Car Company : " << company << std::endl;
    std::cout << "Car Model : " << model << std::endl;
    std::cout << "Car Capacity : " << capacity << " Litres" << std::endl;
    std::cout << "Car Engine : " << engine << std::endl;
    std::cout << std::endl;
}

int main(){
    car("BMW");
    car("Ferari","F40");
    car("Mclaren","P1",72);
    car("Toyata","Supra Mk4",70,"3 Litre Inline 6");
    return 0;
}