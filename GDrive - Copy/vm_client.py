'''
	Author: Md. Tanvir Islam
	Purpose: Clients requesting to the server for files
'''
from ftplib import FTP
import os # module used for making low level system calls
import optparse # module for taking in command line arguments

'''
	name: connect_client
	purpose: initiates connection with the server with specific username, password
			 and ip address
	in: ftp, username, password, ip
	out: ftp
'''
def connect_client(ftp, username, password, ip):
	try:
		ftp.connect(ip, 2406)
		ftp.login(username, passwd = password)
		ftp.cwd("./")
		print(ftp.getwelcome()) # shows what the server sends you
	except Exception as e:
		print(e)
		os.sys.exit()
'''
	name: get_file
	purpose: makes request for a specific file for the server, grabs the file and 
			 saves it in the client's machine
	in: ftp, filename
'''
def get_file(ftp, filename):
	try:
		with open(filename, "wb") as host_file:
			ftp.retrbinary("RETR " + filename, host_file.write, 1024) # binary data is grabbed from remove server 1024 is in reference to a buffer, 1024 bytes are transferd at chunks till full operation is completed
			print("Download successful!")
	except Exception as e:
		print(e)
		os.sys.exit() # exits the program
'''
	name: check_ip
	purpose: error checking function for ip input
	in: ip
'''
def check_ip(ip):
	flag = True
	for letters in ip:
		if ord(letters) < 46 or ord(letters) > 57:
			print("Ip should not contain letters")
			flag = False
			break
	return flag
'''
	name: cmds
	purpose: bunch of print statements to construct a command menu for the user to use
'''
def cmds():
	print("---------------- Commands ---------------")
	print("   ls -l = List files in current directory")
	print("   pwd = Show current directory on the server")
	print("   dl <filename> = Download")
	print("   clear = Clear the screen")
	print("   cmds = Show commands available to you again")
	print("   exit = Exits the program")
	print("-----------------------------------------")
'''
	name: dir_arr
	purpose: ftp
	in: error checks and returns a list consisting of strings, containing all the folders and
	    files in the current directory the server is in
'''
def dir_arr(ftp):
	files = []
	try:
		files = ftp.nlst() # returns a list
	except Exception as e: 
		pass # continues with program
	finally:
		return files
'''
	name: url
	purpose: provides user interface and creates a terminal/shell which gives remote control to user for
			 the server side machine
	in: ftp
'''
def ui(ftp):
	cmds()
	while True:
		cmd = input("---> ")
		if cmd == "ls -l" or cmd == "l":
			ftp.dir()
		elif cmd == "pwd":
			print(ftp.pwd())
		elif cmd == "clear" or cmd == "c":
			os.system('cls' if os.name == 'nt' else 'clear')
		elif cmd == "exit":
			os.sys.exit()
		elif cmd == "cmds":
			cmds()
		elif "dl " in cmd:
			cmd = cmd[3:] # removes first 3 letters "dl "
			arr = dir_arr(ftp) # returns a list files as strings in a directory
			if cmd in arr:
				get_file(ftp, cmd)
			else:
				print("No such files in the directory")
		elif cmd == "":
			continue # if enter is pressed then continue back to the start of the loop
		else:
			print("Command " + cmd + " not found")
'''
	name: main
	purpose: main drive force of this program, also uses optparse to take in command line arguments for username and password
'''
def main():
	ftp = FTP()
	parser = optparse.OptionParser("-u <username> -p <password>")
	parser.add_option("-u", dest = "user", type = "string", help = "Provide the username")
	parser.add_option("-p", dest = "passwd", type = "string", help = "Provide the password")

	(option, args) = parser.parse_args()
	
	if (option.user == None or option.passwd == None):
		print(parser.usage)
		os.sys.exit(0) 
	else:
		while True:
			ip = input("Ip ---> ")
			ip = str(ip)
			if not check_ip(ip):
				continue
			else:
				if ip == "" or len(ip) < 8 or len(ip) > 15:
					print("Please input a valid ip address")
				else:
					break
		connect_client(ftp, option.user, option.passwd, ip)
		ui(ftp)
	try:
		ftp.quit()
	except: 
		print("Client could not connect to the server...")
		os.sys.exit()


if __name__ == '__main__':
	main()