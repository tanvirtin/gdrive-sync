/* Exercise-03 */

/*
	Student Name: Tanvir Islam
	Student Number: 100969657
*/

#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>
#include <signal.h>
#include <stdbool.h>


void createProcess();
void handler(int);

volatile sig_atomic_t flag = true;

int main() {
	createProcess();
	return 0;
}

void createProcess() {
	int pid = fork();
	if (pid == -1) printf("Failed to create a process! %s\n", strerror(errno));

	if (pid > 0) {
		signal(SIGUSR1, handler);
		while (flag) {
			pause();
		}
		puts("SIGUSR1 was raised!");
	}
	else if (pid == 0) if (kill(getppid(), SIGUSR1) != 0) printf("Failed to send signal! %s\n", strerror(errno));
}

void handler(int signal) {
	(signal == SIGUSR1) ? (flag = false) : (flag = true);
}