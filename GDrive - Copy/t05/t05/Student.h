#ifndef STUDENT_H
#define STUDENT_H


class Student
{
  public:
    Student(string="000000000", string="");
    ~Student();
    string getName() const;
    void setName(string);
    void print() const;

  private:
    const string  number;
    string  name;
};

#endif
