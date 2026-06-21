#include <iostream>
#include <string>//Library for strings

int main(){
	int a=10;
	double b=10.555;
	char c='A';
    bool d=true;
    std::string e="Hello";
	std::cout << "Value of a: " << a << std::endl;
	std::cout << "Value of b: " << b << std::endl;
	std::cout << "Value of c: " << c << std::endl;
	std::cout << "Value of d: " << d << std::endl;
	std::cout << "Value of e: " << e << std::endl;

    const int f=99; //Cannot change value
	std::cout << "Value of f:" << f << std::endl;

	auto g=994;
	auto h=12.455;
	std::cout << "Value of g:" << g <<"\nVariable Type of g: " << typeid(g).name() << std::endl;
	std::cout << "Value of h:" << h <<"\nVariable Type of h: " << typeid(h).name() << std::endl;

	return 0;
}