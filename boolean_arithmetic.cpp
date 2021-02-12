/* 
 * @file    boolean_arithmetic.cpp
 * @author  Fabian Farina
 * @date    2/12/2019
 * @version 1.0
 *
 * This is a short demonstration of how to use bit manipulation for
 * addition and multiplication of integer types.
 * 
*/
#include <iostream>

int add(int, int);
int multiply(int, int);

int main()
{
  std::cout << add(14,15) << std::endl;
  std::cout << multiply(14,19) << std::endl;
  return 0;
}

int add(int lhs, int rhs)
{
  if(rhs == 0) return lhs;
  add((lhs^rhs), ((lhs&rhs) << 1));
}

int multiply(int lhs, int rhs)
{
  int result = 0;
  int test = 1;
  do
  {
    if(rhs & test) result = add(result, lhs);
    lhs <<= 1;
    test <<= 1;
  }
  while(test <= rhs);
  return result;
}
