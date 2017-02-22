from File import File
import collections
'''
	Class Name: Tree
	Purpose: The purpose of this represent data listings in a tree structure of a
			 given file system.
'''
class Tree():
	def __init__(self):
		self.__root = self.__tree()
		self.__root["ROOT"] = []
	'''
		Name: __tree
		Purpose: Private method for constructing the multidimensional dictionary,
				 function is used in the constructor.
		return:  a multidimensional dictionary object
	'''
	def __tree(self):
		return collections.defaultdict(self.__tree)
	'''
		Name: add
		Purpose: Adds the file object to the tree
		in: fileObj
		return: a boolean on success or failure
	'''
	def add(self, fileObj):	
		if (not fileObj.getDir or fileObj.getDir == "")  and fileObj:
			self.__root["ROOT"].append(fileObj)
		elif fileObj.getDir:
			numberOfFolders = 0
			for i in range(len(fileObj.getDir)):
				if ((fileObj.getDir)[i] == "/"):
					numberOfFolders += 1
			index = 0
			cd = self.__root["ROOT"]
			while numberOfFolders != 0:
				temp = ""
				if (fileObj.getDir)[index] == "/":
					index += 1
				while (fileObj.getDir)[index] != "/":
					temp += (fileObj.getDir)[index]
					index += 1
				flag = False
				for i in range(len(cd)):
					if isinstance(cd[i], dict):
						for key, value in cd[i].items():
							if temp == key:
								flag = True
								cd = cd[i][temp]
								break
				if not flag:
					cd.append(self.__tree())
					cd[len(cd) - 1][temp] = []
					cd = cd[len(cd) - 1][temp]
				numberOfFolders -= 1 # folder done
			if fileObj:
				cd.append(fileObj)
	'''
		Name: find
		Purpose: Finds the file object thats provided through the parameter.
		in: fileObj
		return: false upon failure and file object upon success
	'''		
	def find(self, fileObj):
		flag = False
		if (not fileObj.getDir or fileObj.getDir == "")  and fileObj:
			cd = self.__root["ROOT"]
			for i in range(len(cd)):
				if not isinstance(cd[i], dict):
					if cd[i].getName == fileObj.getName:
						return cd[i]
			return flag
		elif fileObj.getDir:
			numberOfFolders = 0
			for i in range(len(fileObj.getDir)):
				if ((fileObj.getDir)[i] == "/"):
					numberOfFolders += 1
			index = 0
			cd = self.__root["ROOT"]
			while numberOfFolders != 0:
				flag = False
				innerFlag = False # changes made
				temp = ""
				if (fileObj.getDir)[index] == "/":
					index += 1
				while (fileObj.getDir)[index] != "/":
					temp += (fileObj.getDir)[index]
					index += 1
				
				for i in range(len(cd)):
					if isinstance(cd[i], dict):
						for key, value in cd[i].items():
							if temp == key:
								cd = cd[i][temp]
								flag = True
								innerFlag = True # changes made
								break
					if innerFlag == True: break # changes made
				numberOfFolders -= 1 # folder done
			for i in range(len(cd)):
				if not isinstance(cd[i], dict):
					if cd[i].getName == fileObj.getName:
						return cd[i]
			if not flag:
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
		if (not fileObj.getDir or fileObj.getDir == "")  and fileObj:
			cd = self.__root["ROOT"]
			for i in range(len(cd)):
				if not isinstance(cd[i], dict):
					if cd[i].getName == fileObj.getName:
						del cd[i]
						return True
			return flag
		elif (fileObj.getDir) and fileObj:
			numberOfFolders = 0
			for i in range(len(fileObj.getDir)):
				if ((fileObj.getDir)[i] == "/"):
					numberOfFolders += 1
			index = 0
			cd = self.__root["ROOT"]
			while numberOfFolders != 0:
				temp = ""
				if (fileObj.getDir)[index] == "/":
					index += 1
				while (fileObj.getDir)[index] != "/":
					temp += (fileObj.getDir)[index]
					index += 1
				for i in range(len(cd)):
					if isinstance(cd[i], dict):
						for key, value in cd[i].items():
							if temp == key:
								cd = cd[i][temp]
								flag = True
								break
				numberOfFolders -= 1 # folder done
			for i in range(len(cd)):
				flag2 = False
				if not isinstance(cd[i], dict):
					if cd[i].getName == fileObj.getName:
						flag2 = True
						tempFile = cd[i]
						del cd[i]
						if len(cd) == 0: # prevents from having empty folders
							self.deleteFolder(tempFile.getDir)
						return True
			if not flag or not flag2:
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

def main():
	db = Tree()
	obj1 = File("Tanvir.txt", "comp2404/", "Tuesday")
	obj2 = File("Tanvir.txt", "", "Wednesday")
	
	db.add(obj1)
	db.add(obj2)
	db.deleteFile(obj2)
	db.print()	

	print(db.find(obj1).getName)

if __name__ == '__main__':
	main()