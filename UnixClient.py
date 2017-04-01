from FSTree import Tree
from File import File
import subprocess
import os
import time
import mimetypes
import logging

logging.basicConfig(level = logging.DEBUG) # debug level highest level of logging, can log everything

class UnixClient():
	def __init__(self):
		self.__fsTree = Tree()

	def copyTree(self, this): # can access private member of itself
		self.__fsTree = this.__fsTree

	def createTree(self):
		self.__check(".", "./")
		os.chdir("Main")

	def __check(self, cwd, path):
		os.chdir(cwd)
		# if cwd was root that means our path is ./
		# so path += cwd + "/", if it was path would give you ./root/
		# we don't want that and we want ./whateverisnext
		# cwd is the name of the folder the function is currently in
		if cwd != ".": #checks if the path provided is root or not
			path += cwd + "/"
		proc = subprocess.Popen("ls", stdout = subprocess.PIPE)
		output = proc.stdout.read()
		output = output.decode("utf-8")

		if "FSTree.py" in output: output = output.replace("FSTree.py\n", "")
		if "File.py" in output: output = output.replace("File.py\n", "")
		if "UnixClient.py" in output: output = output.replace("UnixClient.py\n", "")
		if "UnixServer.py" in output: output = output.replace("UnixServer.py\n", "")
		if "__pycache__" in output: output = output.replace("__pycache__\n", "")

		ls = output.split("\n") # creates an array out of std out

		if "" in ls: ls.remove("")

		for i in range(len(ls)):
			if os.path.isdir(ls[i]): # if not a file then go into the sub folder using recursive calls
				self.__check(ls[i], path)
			if not os.path.isdir(ls[i]): # store all the files in the sub folder into an array as file objects
				obj = File(ls[i], path, time.ctime(os.path.getmtime(ls[i])), None, None, mimetypes.guess_type(ls[i])[0]) # constructing the file obj with its name, path and date time
				self.__fsTree.add(obj)

		os.chdir("..") # end of each instance of the function you cd .. out of the folder you were in


	def deleteFileInFs(self, file):
		logging.info("Deleting files from file system...")
		path = file.getDir # gets the path name from the file object
		path = path[2:] # skips the "." in a path which looks like this "./blah/blah/blah"
		# if the folder is in root the path will look like something like this "/"
		# therefore in the recursive call extractFolder will be called with the path "/"
		# in the extractFolder method the while loop won't be executed
		# path returned will be ""
		# and folder returned will be ""
		# therefore the then in the second recursive call the base case will be hit resulting in removing
		# the folder
		self.__walkAndDelete(path, file.getName, 0) # walks the directory and deletes the file


	def __deleteEmptyFolder(self):
		# ls the folder currently in and store it in a list
		proc = subprocess.Popen("ls", stdout = subprocess.PIPE)
		output = proc.stdout.read()
		output = output.decode("utf-8")
		ls = output.split("\n") # creates an array out of std out
		if "" in ls: ls.remove("")
		# if the list is empty then add the folder name to the list
		folder = ""
		if len(ls) == 0:
			cwd = os.getcwd()
			length = len(cwd) # gives you the length of the string
			# traverse the string backwards to obtain the folder
			while cwd[length - 1] != "\\":
				folder += cwd[length - 1]
				length -= 1
		newFolder = "" # if is not then make a newFolder to store the actual string representation
		if folder != "": # checks if the folder is an empty string or not
			folderLength = len(folder) - 1 # makea  while loop to traverse backwards
			while folderLength != -1: # runs a while loop and takes the reverse of a reversed list, needs to be -1 because we need the index 0 to store it, when it reaches -1 the while loop won't execute and we won't hit index out of bounds
				newFolder += folder[folderLength] # stores the reversed reversed list into the newFolder
				folderLength -= 1

		return newFolder

	def __walkAndDelete(self, path, name, hops):
		if path == "": # checks if we have no more folders to traverse
			os.system("rm " + name) # makes the system call to remove
			for i in range(hops): # as you cd out delete the empty folders
				emptyFolder = self.__deleteEmptyFolder() # gets name of the current folder
				os.chdir("..") # need to actually cd out of the current folder to delete the folder itself
				if emptyFolder != "":
					os.removedirs(emptyFolder) # now deletes the folder
			return # if return is not there then the function will execute rest of the body which will result in an error

		addr = self.__extractFolder(path)
		os.chdir(addr[0]) # index 0 of tuple addr

		return self.__walkAndDelete(addr[1], name, hops + 1) # addr[1] is the new modified string after being passed into the function

	# path --> "./one/two/three/four/"
	def __extractFolder(self, path):
		i = 0
		folder = ""
		while path[i] != "/":
			folder += path[i] # shoves letters one by one into the string
			i += 1
		path = path[i + 1:] # path excluding the "/"
		return (folder, path) # returns a tuple containing folder name and new path



	def __fCleanUp(self, cwd):
		isEmpty = False # defines a variable which is an indicator if the folder is empty of not
		if cwd != ".": # first time when this function gets called the path will be "." so we dont have to change directory to "." as we already will be in it
			os.chdir(cwd)

		# create the list of files and directories
		# ------------------------
		proc = subprocess.Popen("ls", stdout = subprocess.PIPE)
		output = proc.stdout.read()
		output = output.decode("utf-8")
		ls = output.split("\n") # creates an array out of std out
		if "" in ls: ls.remove("")
		# -------------------------
		for i in range(len(ls)):
			if os.path.isdir(ls[i]):
				self.__fCleanUp(ls[i]) # can't return the function as we need to grow the stack as there is instructions pending after the recursive call in that particular instance of the recursive call

		# we also got to make sure that the current directory is not root because we do not want to cd out of root
		if cwd != ".":
			# when loop ends we successfully traversed all the necessary folders, so cd out of the current directory
			os.chdir("..") # before the stack collapses it cds out of the current directory that it cded into in that particular instance of the recursive call

		if ls == []: # if ls is empty, it means that the folder is empty, if it is then delete the folder
			logging.info("Deleting empty folder from file system...")
			os.removedirs(cwd)

	def houseKeeping(self):
		return self.__fCleanUp(".") # start traversing from the root directory

	def deleteFileInTree(self, file):
		self.__fsTree.deleteFile(file)

	def printFS(self):
		self.__fsTree.print()

	def findInFS(self, obj):
		return self.__fsTree.find(obj)

	def addToFS(self, obj):
		return self.__fsTree.add(obj)

	def getFileList(self):
		return self.__fsTree.listOfFiles

	def deleteTree(self):
		self.__fsTree = None
		self.__fsTree = Tree()
