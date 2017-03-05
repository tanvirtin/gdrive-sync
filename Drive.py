from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from File import File
from FSTree import Tree

class GDrive:
	def __init__(self):
		self.__gauth = GoogleAuth()
		self.__gauth.LocalWebserverAuth()
		self.__drive = GoogleDrive(self.__gauth)
		self.__gTree = Tree()

	def walk(self):
		self.__walk("root", ".", "./")

	def __walk(self, id, cwd, path):
		ls = self.__drive.ListFile({'q': "'%s' in parents and trashed=false" %(id)}).GetList()
		# if cwd was root that means our path is ./
		# so path += cwd + "/", if it was path would give you ./root/
		# we don't want that and we want ./whateverisnext
		
		if cwd != ".": # checks if the path provided is root or not
			path += cwd + "/"
		
		# id = google id, title = name, modifiedDate, mimeType = folder or not, 
		# dir = application/vnd.google-apps.folder

		# loops over checks if item in the list is a folder or not if not then add file to the folder
		for i in range(len(ls)):
			if ls[i]["mimeType"] == "application/vnd.google-apps.folder":
				self.__walk(ls[i]["id"], ls[i]["title"], path)

			if ls[i]["mimeType"] != "application/vnd.google-apps.folder":
				obj = File(ls[i]["title"], path, ls[i]["modifiedDate"], ls[i]["id"])
				self.__gTree.add(obj)

	def printDrive(self):
		self.__gTree.print()

def main():
	gDrive = GDrive()
	gDrive.walk()
	gDrive.printDrive()


if __name__ == "__main__":
	main()