/*	
	COMP3000 - Exercise 1
	Name: Tanvir Islam
	Student Number: 100969657
*/

#include <fcntl.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>
#include <stdio.h>

char* read_from_file (const char* filename, size_t length) {
	char *buffer = malloc(sizeof(char) * (length + 1));
	if (buffer == NULL) {
		return NULL;
	} else {
		FILE *my_file;
		if (my_file = fopen(filename, "r")) {
			if (!fgets(buffer, length + 1, my_file)) {
				free(buffer);
				fclose(my_file);
				return NULL;
			}
		} else {
			free(buffer);
			return NULL;
		}
		fclose(my_file);
	}
	return buffer;
}

void main (int argc, char **argv) {
	char* buff;
	if ((buff = read_from_file("test1.txt",10)) == NULL) 
 		fprintf(stdout, "Failed to read test1.txt\n");
	else {
 		fprintf(stdout, "buff is: %s\n", buff);
	}
	if ((buff = read_from_file("test2.txt",10)) == NULL) 
 		fprintf(stdout, "Failed to read test2.txt\n");
	else {
 		fprintf(stdout, "buff is: %s\n", buff);
	}
	if ((buff = read_from_file("test3.txt",10)) == NULL) 
 		fprintf(stdout, "Failed to read test3.txt\n");
	else {
 		fprintf(stdout, "buff is: %s\n", buff);
	}
}
