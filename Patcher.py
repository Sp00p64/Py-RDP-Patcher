import os
import ctypes
import subprocess
import sys
import win32net
global versionstr
versionstr = ""
global version
version = ""
v1909or1903 = "39813c0600000f845d610100"
v1809 = "39813c0600000f843b2b0100"
v1803 = "8b993c0600008bb938060000"
v1709 = "39813c0600000f84b17d0200"
patch = "b80001000089813806000090"
username = os.getenv('username')
documents_dir = 'C:\\Users\\' + username + "\\" + "Documents"
import art
from art import text2art
print(text2art("PyRDPWrap", font="big"))
choice = input("This tool modifies a core Windows dll,proceeding could be dangerous for your system do you wish to continue ? (y/n) > ")
if choice == "n":
	print("Exiting ....")
	exit()
elif choice == "y":
	is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
	if is_admin == False:
		print("You need to be admin for this operation")
		print("Exiting....")
		exit()
	else:
		with open('C:/Windows/System32/termsrv.dll', 'rb') as f:
			content = f.read().hex()
		if v1909or1903 in content:
			version += v1909or1903
			versionstr += "version 1909 or 1903"
		elif v1809 in content:
			version += v1809
			versionstr += "version 1809"
		elif v1803 in content:
			version += v1803
			versionstr += "version 1803"
		elif v1709 in content:
			version += v1709
			versionstr += "version 1709"
		else:
			print("[!] Windows version not supported aborting...")
			exit()
		if 'logonserver' in os.environ:
			server = os.environ['logonserver'][2:]
		else:
			server = None
		groups = win32net.NetUserGetLocalGroups(server, os.getlogin())
		isadmin = False
		for group in groups:
			if group.lower().startswith('admin'):
				isadmin = True
				admingroup = group
		print('[*] Windows ' + versionstr + ' detected')
		print("[*] Making backup to " + documents_dir + "\\backup_termsrv.dll")
		output = subprocess.run("copy C:\\Windows\\System32\\termsrv.dll " + documents_dir + "\\" + "backup_termsrv.dll", stdout=subprocess.PIPE,shell=True, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
		print("[*] Taking ownership of termsrv file...")
		output = subprocess.run("takeown /F C:\\Windows\\System32\\termsrv.dll /A", stdout=subprocess.PIPE,shell=True, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
		output = subprocess.run("icacls C:\\Windows\\System32\\termsrv.dll /grant " + admingroup + ":F",stdout=subprocess.PIPE,shell=True, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
		print("[*] Stopping Remote Desktop service....")
		output = subprocess.run("net stop TermService /y",stdout=subprocess.PIPE,shell=True, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
		print("[*] Patching file...")
		content = content.replace(version, patch)
		with open('C:/Windows/System32/termsrv.dll', 'wb') as f:
			f.write(bytes.fromhex(content))
		print("[*] Restarting TermService")
		output = subprocess.run("net start TermService",stdout=subprocess.PIPE,shell=True, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
else:
	print("Input not recognized")

