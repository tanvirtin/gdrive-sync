'''
Author: Md. Tanvir Islam
'''
from File import File
import collections
'''
	Class Name: Tree
	Purpose: The purpose of this represent data listings in a tree structure of a
			 given file system.
'''
class Tree():
	# init/constructor
	def __init__(self):
		self.__root = self.__tree()
		self.__root["ROOT"] = []
		self.__fileList = []

	# repr method for debugging and printing
	# you don't get one end line statement because it is probably a nested structure
	def __repr__(self):
		return "\n"
	'''
		Name: __tree
		Purpose: Private method for constructing the multidimensional dictionary,
				 function is used in the constructor.
		return:  a multidimensional dictionary object
	'''
	def __tree(self):
		return collections.defaultdict(self.__tree)

	@property
	def listOfFiles(self):
		return self.__fileList

	'''
		name: __traverse
		Purpose: Traverses the structure depending on the file path
		return: the folder after the traversal
	'''
	def __traverse(self, fileObj):
		numberOfFolders = 0
		for i in range(len(fileObj.getDir)):
			if ((fileObj.getDir)[i] == "/"):
				numberOfFolders += 1 
		index = 0 # index to match with the forward slash
		cd = self.__root["ROOT"] # lets start from our root node
		while numberOfFolders != 0:
			innerFlag = False 
			temp = "" 
			if (fileObj.getDir)[index] == "/": 
				index += 1
			while (fileObj.getDir)[index] != "/": 
				temp += (fileObj.getDir)[index] 
				index += 1  # this is necessary to move forward to the next subfolder if any
			flag = False
			for i in range(len(cd)):
				if isinstance(cd[i], dict): # for all the folders in that folder
					for key, value in cd[i].items(): 
						if temp == key: 
							flag = True
							innerFlag = True
							cd = cd[i][temp]
							break
				if innerFlag == True: break # breaks the loop and goes into a new instance
			if not flag: 
				cd.append(self.__tree()) # if not simply create the folder
				cd[len(cd) - 1][temp] = []
				cd = cd[len(cd) - 1][temp]
			numberOfFolders -= 1 
		return cd 

	'''
		Name: add
		Purpose: Adds the file object to the tree
		in: fileObj
		return: a boolean on success or failure
	'''
	def add(self, fileObj):	
		# if no subfolders, then it must be in the root directory
		if (not fileObj.getDir or fileObj.getDir == "")  and fileObj:
			self.__root["ROOT"].append(fileObj)
			self.__fileList.append(fileObj)

		elif fileObj.getDir:
			cd = self.__traverse(fileObj)
			cd.append(fileObj)
			self.__fileList.append(fileObj)
	'''
		Name: find
		Purpose: Finds the file object thats provided through the parameter.
		in: fileObj
		return: false upon failure and file object upon success
	'''		
	def find(self, fileObj):
		flag = False
		if not fileObj.getDir or fileObj.getDir == "":
			cd = self.__root["ROOT"]
			for i in range(len(cd)):
				if not isinstance(cd[i], dict):
					if cd[i].getName == fileObj.getName:
						return cd[i]
			return flag
		elif fileObj.getDir:
			cd = self.__traverse(fileObj)
			for i in range(len(cd)):
				if not isinstance(cd[i], dict):
					if cd[i].getName == fileObj.getName and cd[i].getDir == fileObj.getDir: # change made
						return cd[i]
			if not flag: # failed to find the following file
				return False
	'''
		Name: deleteFile
		Purpose: Finds the file object provided and deletes the file, also deletes folders
			     with empty folder.
		in: fileObj
		return: boolean indicating success or failure
	'''
	def deleteFile(self, fileObj):
		flag = False
		if not fileObj.getDir or fileObj.getDir == "":
			cd = self.__root["ROOT"]
			for i in range(len(cd)):
				if not isinstance(cd[i], dict):
					if cd[i].getName == fileObj.getName:
						del cd[i]
						return True
			return flag
		elif fileObj.getDir:
			cd = self.__traverse(fileObj)
			for i in range(len(cd)):
				flag2 = False
				if not isinstance(cd[i], dict):
					if cd[i].getName == fileObj.getName and cd[i].getDir == fileObj.getDir: # changees made
						flag2 = True
						tempFile = cd[i]
						del cd[i]
						if len(cd) == 0: # prevents from having empty folders
							self.deleteFolder(tempFile.getDir) # self deletes empty folders
						return True
			if not flag or not flag2: # failed to find the folder
					return False
	'''
		Name: deleteFolder
		Purpose: Finds folder provided and removes it from the tree.
		in: path
		return: boolean indicating success or failure
	'''
	def deleteFolder(self, path):
		flag = False
		numberOfFolders = 0
		for i in range(len(path)):
			if (path[i] == "/"):
				numberOfFolders += 1
		index = 0
		cd = self.__root["ROOT"]
		while numberOfFolders != 0:
			flag = False
			temp = ""
			if path[index] == "/":
				index += 1
			while path[index] != "/":
				temp += path[index]
				index += 1
			numberOfFolders -= 1 # folder done
			for i in range(len(cd)):
				if isinstance(cd[i], dict):
					for key, value in cd[i].items():
						if temp == key:
							if numberOfFolders == 0:
								del cd[i][temp]
								return True
							cd = cd[i][temp]
							flag = True
							break
		if not flag:
			return flag
	'''
		Name: print
		Purpose: a simple method for displaying the tree
	'''
	def print(self):
		print(self.__root)