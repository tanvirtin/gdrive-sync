from Drive import GDrive
from UnixClient import UnixClient
import time
import threading
import socket
import logging
import os

logging.basicConfig(level = logging.DEBUG) # debug level highest level of logging, can log everything

class DriveControl:
	def __init__(self):
		self.__initialStart = True # constructing the object will make the initialStart True by default
		self.__lock = threading.Lock()
		self.__connection = False
		self.__googleDrive = None
		self.__fileSystem = None
		self.__justDownloaded = [] # list keeps track of recent downloads
		self.__checkConnection() # thread in the background which checks for connection
		self.__initSystem() # initializes the system
		self.__forbidden = ["Drive.py", "DriveControl.py", "FSTree.py", "File.py", "UnixClient.py", "client_secrets.json", "fsGenerator.py", "quickstart.py", "__main__.py"]


	# method that spawns a daemon thread which checks the connection continously
	def __checkConnection(self):
		conCheckThread = threading.Thread(target = self.__internetCheck) # cleans up empty folders
		conCheckThread.daemon = True # terminates with the normal termination of program
		conCheckThread.start()

	# initiliazes the entire system
	def __initSystem(self):
		if not self.__connection: # if connection variable is false that means, no internet therefore sleep a second and call this function again to try and connect
			logging.info("Houston we have a problem...")
			time.sleep(1)
			return self.__initSystem() # needs to return this statement to prevent the stack from building up
		self.__googleDrive = GDrive() # needed to keep track of what I am deleting and first launch, hence googleDrive data structure is required
		self.__fileSystem = UnixClient()

	def launch(self):
		self.__populateFS()
		self.__initialize()
		self.__routineCheck()

	# function responsible for checking connection by pinging google every 3 seconds
	# if a reply is found sleep for 3 seconds and then call the function again and check
	# if not then catch the error by spawning the function again after 3 seconds of sleeping
	# thread runs forever
	def __internetCheck(self): # spawn a thread now that keeps on checking it constantly
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		try:
			sock.connect(("www.google.com", 0))
		except:
			time.sleep(3)
			logging.info("Waiting for a connection...")
			self.__lock.acquire()
			self.__connection = False
			self.__lock.release()
			return self.__internetCheck() # ends function here
		finally: # we want to close the socket regardless of whether we catch an error or not!
			sock.close()
		self.__lock.acquire() # lock the thread while modding the value
		self.__connection = True
		self.__lock.release() # release the lock
		time.sleep(3)
		return self.__internetCheck() # even though this statement is the last thing to be executed call return to prevent stack from building up # ends function here

	# intial start was here causing an issue as I had routine check only running if initialStart was False
	def __initialize(self):
		# sync done when initial load occurs
		# next goal is to download what is on google drive but not your computer
		self.__googleDrive.createTree() # creates google drive
		gFiles = self.__googleDrive.getFileList()
		fsFileList = self.__fileSystem.getFileList() # prevFileList is also the file list that gets created for the very first time

		# downloads the file (SOME FILES DONT GET DOWNLOADED FIX!!!)
		# after downloading I have to make sure that the FsFileList gets updated again and
		# filled with new files if not then whatever you download will get uploaded again
		for i in range(len(gFiles)):
			if not self.__fileSystem.findInFS(gFiles[i]): # if one of the google file is not found in the file system then download it
				self.__download(gFiles[i])
				self.__addToFS(gFiles[i]) # updates the file system
		# delete files that are here but not in google drive, this makes sure that if a new user logs only the new
		# user files is shown and nothing else
		toBeDeleted = []
		for i in range(len(fsFileList)):
			if not self.__googleDrive.findInDrive(fsFileList[i]):
				self.__deleteFromFs(fsFileList[i]) # deletes from google drive needs to delete from file system
				self.__fileSystem.deleteFileInTree(fsFileList[i])

		for i in range(len(toBeDeleted)):
			self.__fileSystem.deleteFileInList(toBeDeleted[i])


	def __populateFS(self):
		self.__fileSystem.createTree()

	def __upload(self, file):
		if file.getName not in self.__forbidden:
			self.__googleDrive.uploadFile(file)

	def __addToFS(self, obj): # changed one thing here if something doesn't work look back
		return self.__fileSystem.addToFS(obj)

	def __download(self, file):
		if file.getName not in self.__forbidden:
			self.__googleDrive.downloadFile(file)

	def __delete(self, file):
		if file.getName not in self.__forbidden:
			self.__googleDrive.deleteFile(file)

	def __deleteFromFs(self, file):
		if file.getName not in self.__forbidden:
			self.__fileSystem.deleteFileInFs(file)

	def __update(self, oldFile, newFile):
		# need to check whether the file where changes are made is one of the scripting files
		if newFile.getName not in self.__forbidden: # newFile or oldFile doesn't matter both have the same name
			logging.info("\nUpdating changes...\n")
			self.__googleDrive.deleteFile(oldFile) # deletes old file
			self.__googleDrive.uploadFile(newFile) # uploads new modified file

	def __justDownloadChecker(self, file):
		for i in range(len(self.__justDownloaded)):
			if file.getName == self.__justDownloaded[i].getName:
				return True # return true immedietly and exit function if names match
		return False # return False after iteration

	# problem finding the file last modified between googleDrive file and currentFile systems file
	def __updateSystem(self):
		tempFs = UnixClient()
		tempFs.createTree()

		currFileList = tempFs.getFileList()

		for i in range(len(currFileList)):
			newFile = currFileList[i] # current files in the file system
			oldFile = self.__fileSystem.findInFS(newFile) # old files in google drive
			if oldFile: # If the oldFile with the same name and directory exists in the current FS, then compare last modified dates of the newFile in the current FS
				if oldFile.getLastModified != newFile.getLastModified and not self.__justDownloadChecker(oldFile): # checks differences in last modified date and whether the file was just downloaded or not
					self.__update(oldFile, newFile) # update the file then
		self.__justDownloaded = [] # reset just downloaded so that it doesn't check again

	def __routineCheck(self):
		# FORGOT TO CHECK LAST MODIFIED
		logging.info("Routine Check")

		while not self.__connection: # wait for connection to resume
			time.sleep(1)

		# house keeping thread
		hkThread = threading.Thread(target = self.__houseKeeping) # cleans up empty folders
		hkThread.daemon = True # terminates with the normal termination of program
		hkThread.start()

		self.__fileSystem.houseKeeping() # deletes empty folders in file system

		tempFs = UnixClient()
		tempFs.createTree()

		prevFileList = self.__fileSystem.getFileList() # prevFileList is also the file list that gets created for the very first time
		currFileList = tempFs.getFileList()

		self.__googleDrive.deleteTree()
		self.__googleDrive.createTree() # create it again

		gFiles = self.__googleDrive.getFileList()

		logging.info("\nStarting checks!\n")

		# deletes whats not there in google drive
		logging.info("\nChecking for deletes in Google Drive....\n")
		for i in range(len(prevFileList)):
			if not tempFs.findInFS(prevFileList[i]):
				self.__delete(prevFileList[i]) # if previous files don't exist in the new tree generated then delete the old ones
				size = len(gFiles)
				j = 0 # needs a new variable j because i is currently in this for loop which is being used by to find the index of prevFileList at i
				while j != size:
					if gFiles[j].getName == prevFileList[i].getName:
						del gFiles[j]
						size -= 1
					j += 1 # increase j as it has to match size in order to break the loop

		# uploads whats not there in google drive
		logging.info("\nChecking for uploads....\n")
		for i in range(len(currFileList)):
			if not self.__fileSystem.findInFS(currFileList[i]):
				self.__upload(currFileList[i]) # if previous files don't exist in the new tree generated then delete the old ones

		# update changes
		logging.info("\nChecking for updates....\n")
		if not self.__initialStart: # first call to this function will always make initialStart = True
			self.__updateSystem() # changes made

		# download whats not there in file system
		logging.info("\nChecking for downloads....\n")
		for i in range(len(gFiles)):
			if not tempFs.findInFS(gFiles[i]):
				self.__download(gFiles[i])
				tempFs.addToFS(gFiles[i]) # add new file to fs data structure
				self.__justDownloaded.append(gFiles[i])

		# delete files that are here but not in google drive, this makes sure that if a new user logs only the new
		# user files is shown and nothing else
		toBeDeleted = []
		logging.info("\nChecking for deletes in File System....\n")
		for i in range(len(currFileList)):
			if prevFileList[i].getName not in self.__forbidden and not self.__googleDrive.findInDrive(prevFileList[i]): # if the file isn't in the forbidden list and can't find it in google drive then proceed
				self.__deleteFromFs(prevFileList[i]) # deletes from google drive needs to delete from file system
				tempFs.deleteFileInTree(prevFileList[i])
				toBeDeleted.append(prevFileList[i])

		for i in range(len(toBeDeleted)):
			tempFs.deleteFileInList(toBeDeleted[i])

		self.__fileSystem.copyTree(tempFs)
		self.__initialStart = False # initialStart is made False everytime
		time.sleep(10)
		self.__routineCheck() # run forever


	# run this function every 5 minutes
	def __houseKeeping(self):
		logging.info("House Keeping!")
		self.__googleDrive.houseKeeping()
		time.sleep(1)
