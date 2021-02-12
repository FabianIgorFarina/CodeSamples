/* 
 * @file    monte_carlo_pi.cpp
 * @author  Fabian Farina
 * @date    12/2/2021
 * @version 1.0
 *
 * In this program we use random numbers to approximate the value of pi.
 * It is one of the standard examples being used to introduce the idea 
 * of monte carlo methods. The logic behind this program can be found at
 * the end of this file.
 * 
 * There are many algorithms that converge much faster to the real value
 * of pi than the one shown this example. But on the other hand this is 
 * one of the most intuitive ways for its calculation.
 * 
*/

#include <iostream>
#include <random>
#include <cmath>
#include <chrono>  

//Initializing the Mersenne Twister for the creation of random numbers
#define MT_RAND_MAX (std::mt19937_64().max() - std::mt19937_64().min())
std::mt19937_64 mt_random(std::chrono::duration_cast< std::chrono::milliseconds >(
    std::chrono::system_clock::now().time_since_epoch()).count());

//macros for later use (detailed explanation below the main function)
#define NUM unsigned long   //positive integer type
#define MAX_VALUE ~(NUM)0  //largest unsigned integer number 

//defining the macro M_PI if it is unknown to the compiler
#ifndef M_PI
#define M_PI 3.1415926535897932384626
#endif

using namespace std;

//function will print predefined texts to the console
void show_text(int choice=-1);

//function for the positive boundary of a circle with radius 'r'
double circle(double x,double r=1.);

//generating 'num_total' random points and increase 'num_inside'
//whenever a point lies inside the circle
void count_in_circle(NUM* num_inside,NUM num_total);

int main() 
{
    NUM num_total = 0;    ///> total number of points
    NUM num_inside = 0;   ///> number of points inside the circle
    NUM num_threads = 1;
    NUM temp[num_threads];
    double pi;            ///> placeholder for pi
    
    //requesting the number of points from the user
    show_text(); cin >> num_total; cout << "\n" << endl;
    show_text(num_total); cout << endl;
    if(num_total==0) num_total = MAX_VALUE;
  
    for(NUM i=0;i<num_threads;i++)
    {
		temp[i] = 0;
		count_in_circle(&temp[i],(NUM)((long)num_total/(long)num_threads));
	}
	for(NUM i=0;i<num_threads;i++) num_inside += temp[i];
	
	count_in_circle(&num_inside,(NUM)((long)num_total%(long)num_threads));
	
    //calculating pi with the gathered data
    pi = 4.*num_inside/(double)num_total;
    
    //preparing the console to present the data for good comparison
    cout.setf( ios::fixed, ios::floatfield );
    cout.precision(10);
    cout << "Pi (approximation)  :   " << pi << endl;
    cout << "Pi (real value)     :   " << M_PI << endl;
    cout << "Difference          :   " << abs(pi-M_PI) << endl;
    
    return 0;
}

void show_text(int choice)
{
    //switch is used to print texts depending on 'choice'
    switch(choice)
    {
        case -1 : 
          cout << "Please enter the number of points you would like\n";
          cout << "to use to approximate pi (0 for the maximum): "; 
          break;
        case 0  :
          cout << "The algorithm will pick " << MAX_VALUE << " points\n";
          cout << "for the calculation (this might take a while).\n\n";
          break;
        default :
          cout << "The algorithm will pick " << choice << " points\n";
          cout << "for the calculation.\n\n";
          break;
    }
}

double circle(double x,double r)
{
    if(abs(x)<=r) return sqrt(r*r-x*x);
    return 0.;
}

void count_in_circle(NUM* num_inside,NUM num_total)
{
	NUM temp = 0;
    double point[2];      ///> placeholder for points in the plane
	for(NUM i=0;i<num_total;i+=1)
    {
        //assigning random values between 0 and 1 to the coordinates
        point[0] = mt_random()/(double)MT_RAND_MAX;  // x
        point[1] = mt_random()/(double)MT_RAND_MAX;  // y
        point[0] = circle(point[0]);         // f(x)
        
        //whenever y<=f(x) is true the point lies in the circle
        if(point[1]<=point[0]) temp+=1;
    }
    *num_inside = *num_inside + temp;
}

/* Method explanation:
 *  We know that the area of a circle is given by Ac = pi*radius^2.
 *  The unit circle has the radius = 1, so Ac = pi. We will only use 
 *  the first quadrant of the cartesian plane to keep the code simple.
 *  A quadrat with the side length l = 1 has an area of Aq = 1.
 *  The percentage of it being covered by a quarter circle can be 
 *  calculated with p% = ((Ac/4)/Aq)*100% = (pi/4)*100%. We randomly
 *  pick a certain number 'num_total' of points (x,y) in the quadrat 
 *  and check if they also lie inside the circle. The number of them
 *  'num_inside' should roughly be around p% of all points (it gets 
 *  closer to this value for ever larger values of 'num_total').
 *  Therefore we can approximately calculate:
 *                                  
 *  --> pi = 4*num_inside/num_total
*/
