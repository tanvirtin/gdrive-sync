from Drive import GDrive
from UnixClient import UnixClient
import time
import threading

class DriveControl:
	def __init__(self):
		self.__googleDrive = GDrive()
		self.__fileSystem = UnixClient()
		self.__workInProg = False

	def launch(self):
		self.__populateGDrive()
		self.__populateFS()

		hkThread = threading.Thread(target = self.__houseKeeping)
		hkThread.daemon = True # terminates with the normal termination of program
		hkThread.start()
		
		while True:
			time.sleep(30)
			print("Still running!")

	def __populateGDrive(self):
		self.__googleDrive.createTree()

	def __populateFS(self):
		self.__fileSystem.createTree()

	def __upload(self, fileList):
		#fileList = self.__fileSystem.getFileList()
		self.__workInProg = True # about to start interaction with server
		for i in range(len(fileList)):
			self.__googleDrive.uploadFile(fileList[i])
		self.__workInProg = False

	def __delete(self, fileList):
		#fileList = self.__fileSystem.getFileList()
		self.__workInProg = True
		for i in range(len(fileList)):
			self.__googleDrive.deleteFile(fileList[i])
		self.__workInProg = False

	# run this function every 5 minutes
	def __houseKeeping(self):
		while True:
			print("House Keeping!")
			self.__googleDrive.houseKeeping()
			time.sleep(300)

	def __routineCheck(self):
		# creates new FS and checks with the prev fileSystem for changes
		# depending on the changes googleDrive is updated
		# should call upload or delete depending on the situation
		pass
