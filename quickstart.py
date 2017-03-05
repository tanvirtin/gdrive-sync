from pydrive.auth import GoogleAuth

gauth = GoogleAuth()
gauth.LocalWebserverAuth() # Creates local webserver and auto handlesc

from pydrive.drive import GoogleDrive

drive = GoogleDrive(gauth)


# always start off at the root
file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()

# Each file in the list is actually an object which can be accessed like a python dictionary
# containing several key/value pairs

# file_list contains a list of all the objects

for file1 in file_list:
	print('title: %s, id: %s, mimeType: %s' % (file1['title'], file1['id'], file1['mimeType']))


# for i in range(len(ls)):
# 	for key, value in ls[i].items():
# 		print(key, value)
# 	print("")





file_list_two = drive.ListFile({'q': "'0B1yR_SIg6FVhY3d5OS1VY0RIRE0' in parents and trashed=false"}).GetList()


print(" ")

for file in file_list_two:
	print('title: %s, id: %s, mimeType: %s' % (file['title'], file['id'], file['mimeType']))


# the mimeType of folders in google drive is: application/vnd.google-apps.folder
# if you need to traverse inside put them in a folder and use recursion to go into them



# # You always have to create the file either you delete or upload or download

# '''
# 	uploading a file

# '''

# file5 = drive.CreateFile()
# # Read file and set it as a content of this instance.
# file5.SetContentFile('TEST.txt')
# file5.Upload() # Upload the file.
# print('title: %s, mimeType: %s' % (file5['title'], file5['mimeType']))
# # title: cat.png, mimeType: image/png


# '''
# 	downloading a file

# '''

#file1 = drive.CreateFile({'id': '<some file ID here>'})
# content = file7.GetContentFile()

# '''
# 	deleting a file

# '''

# #file1 = drive.CreateFile({'id': '<some file ID here>'})

# file1 = drive.CreateFile({"id" : "0B1yR_SIg6FVhRndENjFnbHhvVlk"})

# file1.Delete()  # Permanently delete the file.
