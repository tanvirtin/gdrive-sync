from Drive import GDrive
from UnixClient import UnixClient
import time
import threading

class DriveControl:
	def __init__(self):
		self.__googleDrive = GDrive()
		self.__fileSystem = UnixClient()
		self.__firstLaunch = True

	def launch(self):
		self.__populateFS()

		while True:
			self.__routineCheck()
			time.sleep(10)


	def __populateFS(self):
		self.__fileSystem.createTree()

	def __upload(self, file):
		forbidden = ["Drive.py", "DriveControl.py", "FSTree.py", "File.py", "UnixClient.py", "client_secrets.json", "fsGenerator.py", "quickstart.py", "__main__.py"]
		if file.getName not in forbidden:
			self.__googleDrive.uploadFile(file)

	def __delete(self, file):
		self.__googleDrive.deleteFile(file)

	def __routineCheck(self):

		# FORGOT TO CHECK LAST MODIFIED AND UPLOADING
		
		print("Routine Check")

		hkThread = threading.Thread(target = self.__houseKeeping)
		hkThread.daemon = True # terminates with the normal termination of program
		hkThread.start()
		
		tempFs = UnixClient()
		tempFs.createTree()

		prevFileList = self.__fileSystem.getFileList()
		
		if self.__firstLaunch: # if its the first program launch then send everything
		# modify later so that you sync it with your actual google drive
			for i in range(len(prevFileList)):
				self.__upload(prevFileList[i])
			self.__firstLaunch = False
			return

		currFileList = tempFs.getFileList() 

		self.__googleDrive.deleteTree()
		self.__googleDrive.createTree()

		# get changes
		for i in range(len(prevFileList)):
			if not tempFs.findInFS(prevFileList[i]):
				self.__delete(prevFileList[i]) # if previous files don't exist in the new tree generated then delete the old ones
	
		for i in range(len(currFileList)):
			if not self.__fileSystem.findInFS(currFileList[i]):
				self.__upload(currFileList[i]) # if previous files don't exist in the new tree generated then delete the old ones

		self.__fileSystem.copyTree(tempFs)


	# run this function every 5 minutes
	def __houseKeeping(self):
		print("House Keeping!")
		self.__googleDrive.houseKeeping()
		time.sleep(1)

