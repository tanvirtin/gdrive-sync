#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <unistd.h>

/* create a child process running a new program
   program=name of the program to run
   arg_list=argument list, a NULL-terminated list of character strings   
 */

void create (char* program, char** arg_list)
{
  /* put your code here */
}

int main ()
{
  /* argument list for the "ls" command.  */
  char* arg_list[] = {
    "ls",     /* argv[0], the name of the program  */
    "-l", 
    "/",
    NULL      /* The argument list must end with a NULL.  */
  };

  /* create a child process running the "ls" command  */
  create ("ls", arg_list);

  sleep(10); /* sleep 10 seconds */

  create ("dosomethinginvalid", NULL); 

  sleep(10); /* sleep 10 seconds */

  printf ("Normal main program termination\n");

  return 0;
}
