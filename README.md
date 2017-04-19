# Google-Drive-File-System-Synchronization-with-Ubuntu

# Context:

Google Drive is a file storage and synchronization service developed by Google. It allows users to store files in the cloud, synchronize them across devices, and share them. In addition to a website, it offers apps which automatically synchronize with Windows and Mac OS computers, as well as Android and iOS smartphones and tablets.
As one of the biggest companies in the world, Google’s platform is more secure (By secure I am are referring to API secure), and more efficient than its lesser known counterparts.  Until now, the Google Drive app feature was only accessible to Windows and Mac OS users—but not to Linux Ubuntu users; the purpose of this project is to integrate it with Linux Ubuntu’s file system.

# Summary of Results:
  
Through my project, I aim to achieve a complete integration of Google Drive with the Ubuntu file system, in the style of Google Drive’s applications with other operating systems.

As soon as the operating system completes its boot, my adding the script to the **Starup Applications Program** in Ubuntu, the program automatically begins to run. It opens the default browser and navigates to the Google login page. At this point, Google will ask the user for their username and password, after which it will notify the users that our program is asking for full access to their Google Drive. Once the user grants this permission, my program is located in a directory in the Ubuntu file system which will get synchronized with Google Drive. If the user closes the browser by mistake, or any error occurs, the user has a simple button to relaunch the application and repeat the login process as shown in Figure-1 below.

The very first thing the program does upon authorization is download all the files and directories from Google Drive to the Ubuntu file system, such that anything currently in Ubuntu file system but not in Google Drive gets deleted. This allows different users with Google Drive accounts to use our program, as the file system needs to mimic their own individual Google Drive. Then it maintains the synchronization by making several checks regularly every ten seconds such as checking for downloads, deletes, changes made in the file system or in Google Drive to update, etc. Depending on the results of the checks our program makes the necessary updates by acting as a medium to directly send and receive data to and from Google Drive. Our program also maintains execution till the operating system shuts down. If there is any connection error, the program simply pauses its execution and waits till the user is connected to the internet again.

All the actions mentioned above allows me to solve the problem being addressed, that is, to make the Linux Ubuntu file system one with the Google Drive per user.

# Installation:

The program is written in Python3 programming language and Python version 3 and above is required for the program to run. In addition to that pip3 should also be installed.

After the following have been installed simply open up a **terminal** and type in **sudo pip3 install pydrive**.

Move to the directory where the **/scripts** directory is located and simply type in **python3 __main__.py** to execute the program.

The directory is now your new Google Drive!
