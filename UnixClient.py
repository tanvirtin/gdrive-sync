from FSTree import Tree
from File import File
import subprocess
import os
import time
import mimetypes

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

	def printFS(self):
		self.__fsTree.print()

	def findInFS(self, obj):
		return self.__fsTree.find(obj)

	def getFileList(self):
		return self.__fsTree.listOfFiles

