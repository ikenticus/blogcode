// Easy
// https://www.hackerrank.com/challenges/rectangle-area/problem

#include <iostream>

using namespace std;


/*
 * Create classes Rectangle and RectangleArea
 */
class Rectangle {
    public:
        int w, h;
        void read_input() {
            cin >> w >> h;            
        }
        void display() {
            cout << w << " " << h << "\n";
        }
};

class RectangleArea : public Rectangle {
    public:
        void display() {
            cout << w * h << "\n";
        }        
};



int main()
{
    /*
     * Declare a RectangleArea object
     */
    RectangleArea r_area;
    
    /*
     * Read the width and height
     */
    r_area.read_input();
    
    /*
     * Print the width and height
     */
    r_area.Rectangle::display();
    
    /*
     * Print the area
     */
    r_area.display();
    
    return 0;
}

