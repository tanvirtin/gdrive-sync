'''
	Author: Md. Tanvir Islam
	Purpose: Server with a handler waiting for requests
'''
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import socket
import os # module used for making low level system calls
import optparse # module for taking in command line arguments
'''
	name: get_ip 
	purpose: opens up a UDP socket and sendts packets to google.com, you can pick any website you want to ping,
		     this returns the address of the host which is a tuple. Tuple looks like this (ip, port), first index
		     will return the ip address
'''
def get_ip():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("www.google.com", 0))
	ip = s.getsockname()[0]
	s.close()
	return ip
'''
	name: server
	purpose: creates virtual users with a specific user and password, handler function 
			 that serves requests and waits forever for requests
	in: username, password, ip
'''
def server(username, password, ip):
	authorizer = DummyAuthorizer()
	authorizer.add_user(username, password, ".", perm = "elradfmwM")
	authorizer.add_anonymous(os.getcwd())
	
	handler = FTPHandler
	handler.authorizer = authorizer

	handler.banner = "Connection established!"

	address = (ip, 2406)
	server = FTPServer(address, handler)

	server.max_cons = 256
	server.max_cons_per_ip = 5

	server.serve_forever()
'''
	name: main
	purpose: main drive force of this program, also uses optparse to take in command line arguments for username and password
'''
def main():
	parser = optparse.OptionParser("-u <username> -p <password>")
	parser.add_option("-u", dest = "user", type = "string", help = "Provide the username")
	parser.add_option("-p", dest = "passwd", type = "string", help = "Provide the password")

	(option, args) = parser.parse_args()

	if (option.user == None or option.passwd == None):
		print(parser.usage)
		exit(0)
	else:
		ip = get_ip()
		server(option.user, option.passwd, ip)

if __name__ == "__main__":
	main()