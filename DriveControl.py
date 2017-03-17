from Drive import GDrive
from UnixClient import UnixClient
import time
import threading

class DriveControl:
	def __init__(self):
		self.__googleDrive = GDrive() # needed to keep track of what I am deleting and first launch
		self.__fileSystem = UnixClient() 

	def launch(self):
		self.__populateFS()
		self.__initialize()
		self.__routineCheck()

	def __initialize(self):
		# sync done when initial load occurs
		# next goal is to download what is on google drive but not your computer
		self.__googleDrive.createTree() # creates google drive	
		gFiles = self.__googleDrive.getFileList()
		FsFileList = self.__fileSystem.getFileList() # prevFileList is also the file list that gets created for the very first time
	
		# downloads the file (SOME FILES DONT GET DOWNLOADED FIX!!!)
		# after downloading I have to make sure that the FsFileList gets updated again and
		# filled with new files if not then whatever you download will get uploaded again
		for i in range(len(gFiles)):
			if not self.__fileSystem.findInFS(gFiles[i]): # if one of the google file is not found in the file system then download it
				self.__download(gFiles[i])
				self.addToFS(gFiles[i]) # updates the file system

		# uploads the file
		for i in range(len(FsFileList)):
			# only upload files that are not currently present in google drive
			if not self.__googleDrive.findInDrive(FsFileList[i]): # SO SLOW  OMG!!!
				self.__upload(FsFileList[i])

		# download the file which is on the google drive but not here
		# don't delete files that are not here when you first start up, 
		# because if you do you will be deleting anything that you upload using your phone 
		# or any other device automatically when this program starts running

	def __populateFS(self):
		self.__fileSystem.createTree()

	def __upload(self, file):
		forbidden = ["Drive.py", "DriveControl.py", "FSTree.py", "File.py", "UnixClient.py", "client_secrets.json", "fsGenerator.py", "quickstart.py", "__main__.py"]
		if file.getName not in forbidden:
			self.__googleDrive.uploadFile(file)

	def addToFS(self, obj):
		return self.__fileSystem.addToFS(obj)


	def __download(self, file):
		self.__googleDrive.downloadFile(file)

	def __delete(self, file):
		self.__googleDrive.deleteFile(file)

	def __routineCheck(self):
		# FORGOT TO CHECK LAST MODIFIED
		print("Routine Check")

		# house keeping thread
		
		hkThread = threading.Thread(target = self.__houseKeeping) # cleans up empty folders
		hkThread.daemon = True # terminates with the normal termination of program
		hkThread.start()
		
		tempFs = UnixClient()
		tempFs.createTree()

		prevFileList = self.__fileSystem.getFileList() # prevFileList is also the file list that gets created for the very first time
		
		currFileList = tempFs.getFileList() 

		self.__googleDrive.deleteTree()
		self.__googleDrive.createTree() # create it again

		# get changes
		for i in range(len(prevFileList)):
			if not tempFs.findInFS(prevFileList[i]):
				self.__delete(prevFileList[i]) # if previous files don't exist in the new tree generated then delete the old ones
	
		for i in range(len(currFileList)):
			if not self.__fileSystem.findInFS(currFileList[i]):
				self.__upload(currFileList[i]) # if previous files don't exist in the new tree generated then delete the old ones

		self.__fileSystem.copyTree(tempFs)

		time.sleep(10)

		self.__routineCheck() # run forever


	# run this function every 5 minutes
	def __houseKeeping(self):
		print("House Keeping!")
		self.__googleDrive.houseKeeping()
		time.sleep(1)

