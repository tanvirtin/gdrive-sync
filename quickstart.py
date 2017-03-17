
from pydrive.auth import GoogleAuth

gauth = GoogleAuth()
gauth.LocalWebserverAuth() # Creates local webserver and auto handlesc

from pydrive.drive import GoogleDrive

drive = GoogleDrive(gauth)


# always start off at the root
file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()

for file in file_list:
	print('title: %s, id: %s, mimeType: %s parent: %s' % (file['title'], file['id'], file['mimeType'], file['parents']))
	print("")



file_list_two = drive.ListFile({'q': "'0B1yR_SIg6FVhN2FxdDd1c0NWNXc' in parents and trashed=false"}).GetList()

for file in file_list_two:
	print('title: %s, id: %s, mimeType: %s parent: %s' % (file['title'], file['id'], file['mimeType'], file['parents']))
	print("")



# the mimeType of folders in google drive is: application/vnd.google-apps.folder
# if you need to traverse inside put them in a folder and use recursion to go into them



# You always have to create the file either you delete or upload or download

'''
	uploading a file

'''

# file5 = drive.CreateFile()
# # Read file and set it as a content of this instance.
# file5.SetContentFile('Blah.txt')
# file5.Upload() # Upload the file.



# '''
# 	downloading a file

# '''
# # Initialize GoogleDriveFile instance with file id.
# file6 = drive.CreateFile({'id': file5['id']})
# file6.GetContentFile('catlove.png') # Download file as 'catlove.png'.
# # the few lines above are enough for the module to automatically care the folder and write it to your drive
# # no need to open a file and write bytes to it!
# '''
# 	deleting a file

# '''

# #file1 = drive.CreateFile({'id': '<some file ID here>'})

# file1 = drive.CreateFile({"id" : "0B1yR_SIg6FVhRndENjFnbHhvVlk"})

# file1.Delete()  # Permanently delete the file.
