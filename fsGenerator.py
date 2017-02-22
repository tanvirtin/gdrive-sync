from os import system


def delete(list_one, list_two):
	for i in range(len(list_one)):
		system("rmdir " + list_one[i])
		system("rm " + list_two[i])

def main():
	mkdir = "mkdir "
	fs = []
	delFolders = []
	delFiles = []
	for i in range(20):
		fs.append("touch " + str(i) + ".txt")
		delFiles.append(str(i) + ".txt")
		fs.append("mkdir " + str(i))
		delFolders.append(str(i))

	for i in range(len(fs)):
		system(fs[i])

	delete(delFolders, delFiles)


if __name__ == '__main__':
	main()