from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from File import File
from FSTree import Tree
import subprocess
import os

class GDrive():
	def __init__(self):
		self.__gauth = GoogleAuth()
		self.__gauth.LocalWebserverAuth()
		self.__drive = GoogleDrive(self.__gauth)
		self.__gTree = Tree()

	def createTree(self):
		self.__walkDrive("root", ".", "./", ".")

	def __walkDrive(self, id, cwd, path, folderId):
		print("Gathering Google Drive data...%s" %(path))
		ls = self.__drive.ListFile({'q': "'%s' in parents and trashed=false" %(id)}).GetList()
		# if cwd was root that means our path is ./
		# so path += cwd + "/", if it was path would give you ./root/
		# we don't want that and we want ./whateverisnext
		if cwd != ".": # checks if the path provided is root or not
			path += cwd + "/"

		folderId = id # id of the folder currently in
		
		# id = google id, title = name, modifiedDate, mimeType = folder or not, 
		# dir = application/vnd.google-apps.folder

		# loops over checks if item in the list is a folder or not if not then add file to the folder
		for i in range(len(ls)):
			if ls[i]["mimeType"] == "application/vnd.google-apps.folder":
				self.__walkDrive(ls[i]["id"], ls[i]["title"], path, folderId)

			if ls[i]["mimeType"] != "application/vnd.google-apps.folder":
				obj = File(ls[i]["title"], path, ls[i]["modifiedDate"], ls[i]["id"], folderId, ls[i]["mimeType"])
				self.__gTree.add(obj)

	def printDrive(self):
		self.__gTree.print()

	def findFile(self, fileObj):
		return self.__gTree.find(fileObj)

	def __createF(self, id, pathList):
		# starts off at the root and starts walking directory with each recursive call
		ls = self.__drive.ListFile({'q': "'%s' in parents and trashed=false" %(id)}).GetList()
		# makes sure the stack is not empty
		if len(pathList) != 0:
			for i in range(len(ls)):
				if ls[i]["mimeType"] == "application/vnd.google-apps.folder" and ls[i]["title"] == pathList[0]:
					del pathList[0] # pops the stack or the folder visited
					return self.__createF(ls[i]["id"], pathList)
		else: return id

		folder = self.__drive.CreateFile({'title': pathList[0], "parents":  [{"id": id}], "mimeType": "application/vnd.google-apps.folder"})
		folder.Upload()
		newLs = self.__drive.ListFile({'q': "'%s' in parents and trashed=false" %(id)}).GetList()
		
		for i in range(len(newLs)):
			if newLs[i]["mimeType"] == "application/vnd.google-apps.folder" and newLs[i]["title"] == pathList[0]:
				del pathList[0]
				return self.__createF(newLs[i]["id"], pathList)
		
	# returns the id of the last folder visited
	def __ccFolder(self, path):
		pathList = path.split("/")
		del pathList[0] # need to delete the . that always gets added in
		del pathList[len(pathList) - 1]
		return self.__createF('root', pathList)

	def __walkFS(self, path):
		pathList = path.split("/")
		del pathList[0]
		del pathList[len(pathList) - 1]
		return self.__walk(pathList, 0)


	def __walk(self, pathList, hops):
		if len(pathList) != 0:
			hops += 1 # increases the hops made
			os.chdir(pathList[0])
		proc = subprocess.Popen("ls", stdout = subprocess.PIPE)
		output = proc.stdout.read()
		output = output.decode("utf-8")
		ls = output.split("\n") # creates an array out of std out
		if "" in ls: ls.remove("")

		if len(pathList) != 0:
			for i in range(len(ls)):
				if os.path.isdir(ls[i]) and ls[i] == pathList[0]:
					del pathList[0] # pops the stack or the folder visited or hops to folder made
					return self.__walk(pathList, hops) # recursively visits folder
			return hops
		else: return hops

		
	def uploadFile(self, obj):
		print("Uploading %s...." %(obj.getName))
		id = self.__ccFolder(obj.getDir) # creates the folders necessary
		gfile = self.__drive.CreateFile({'title': obj.getName, "parents":  [{"kind": "drive#fileLink","id": id}]})
		hops = self.__walkFS(obj.getDir) # walks inside the folder of the file
		#gfile.SetContentFile(obj.getName) # finds the file
		gfile.Upload() # uploads the file
		for i in range(hops):
			os.chdir("..")
		
	def deleteFile(self, obj):
		print("Deleting %s...." %(obj.getName))
		fileObj = self.__gTree.find(obj)
		if fileObj:
			file = self.__drive.CreateFile({"id": fileObj.getFileId})
			file.Delete() 
			ls = self.__drive.ListFile({'q': "'%s' in parents and trashed=false" %(fileObj.getFolderId)}).GetList()
			if len(ls) == 0:
				folder = self.__drive.CreateFile({"id": fileObj.getFolderId})
				folder.Delete()
			return True
		else:
			return False

	def __fCleanUp(self, id):
		ls = self.__drive.ListFile({'q': "'%s' in parents and trashed=false" %(id)}).GetList()
		# makes sure the stack is not empty
		# if there are no folders or files then length of ls will be 0 
		# therefore it's okay to delete the folder while 
		# the for loop allows current stack to not get popped off as the function is pending
		# for the other recursion to finish
		
		if len(ls) == 0 and not id == "root":
			folder = self.__drive.CreateFile({"id": id})
			folder.Delete() # delete the empty folder

		for i in range(len(ls)):
			if ls[i]["mimeType"] == "application/vnd.google-apps.folder":
				self.__fCleanUp(ls[i]["id"])


	def getFileList(self):
		return self.__gTree.listOfFiles

	def houseKeeping(self):
		self.__fCleanUp("root")

	def findInDrive(self, obj):
		return self.__gTree.find(obj)

	def deleteTree(self):
		self.__gTree = None
		self.__gTree = Tree()

