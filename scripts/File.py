'''
	Class Name: File
	Purpose: The purpose of this class is represent data of a particular file
			 in a file system.
'''
class File:
	def __init__(self, name = None, directory = None, date = None, fId = None, folderId = None, extension = ""):
		self.__name = name
		self.__directory = directory
		self.__date = date
		self.__id = fId
		self.__folderId = folderId
		self.__mimeType = extension

	def __repr__(self):
		return self.getName
	'''
		Name: getName
		Purpose: A getter method for the name of the file.
		return: private attribute __name
	'''
	@property
	def getName(self):
		return self.__name
	'''
		Name: getDir
		Purpose: a getter method for the name of the directory the file is in.
		return: private attribute __directory
	'''
	@property
	def getDir(self):
		return self.__directory
	'''
		Name: getLastModified
		Purpose: a getter method for the date that the file was last modified at
		return: private attribute __date
	'''
	@property
	def getLastModified(self):
		return self.__date
	'''
		Name: getDetails
		Purpose: Returns the full file address of a file object.
		return: a string representing the full file details
	'''

	def getDetails(self):
		return self.getDir + self.getName
	
	@property
	def getFileId(self):
		return self.__id

	@property
	def getFolderId(self):
		return self.__folderId

	@property
	def getMimeType(self):
		return self.__mimeType