#include <iostream>

namespace circle{
    std::string area = "2*PI*Radius";
}
namespace square{
    std::string area = "Side*Side";
}
namespace rectangle{
    std::string area = "2*(length+width)";
}

int main(){
    using std::cout,std::endl;
    
    cout << "Area of Circle : " << circle::area << endl;

    cout << "Area of Square : " << square::area << endl;
    
    cout << "Area of Rectangle : " << rectangle::area << endl;
    
    return 0;
}
