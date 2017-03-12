#include <iostream>
using namespace std;
#include <string>

#include "Student.h"


Student::Student(string nu, string na)
    : number(nu), name(na) { }

Student::~Student() { }

string Student::getName() const { return name; }

void Student::setName(string n) { name = n; }

void Student::print() const  
{
  cout<<"Student:  "<<number<<"  "<<name<<endl;
}

