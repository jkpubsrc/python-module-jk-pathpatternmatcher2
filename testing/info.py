#!/usr/bin/python3


from jk_pathpatternmatcher2 import *




nTotalErrors = 0
nTotalFiles = 0
nTotalDirs = 0
nTotalSymLinks = 0
nTotalFileSize = 0

for e in walk(
		"/etc",
		#ignoreDirPathPatterns=[
		#	"/etc/php",
		#	"rc*",
		#	"/etc/mono",
		#	"*/system",
		#	"**/Input",
		#	"**/Text",
		#]
	):
	#print(e)
	if e.type.startswith("e"):
		nTotalErrors += 1
	elif e.type == "f":
		nTotalFiles += 1
		nTotalFileSize += e.size
	elif e.type == "d":
		nTotalDirs += 1
	elif e.type == "l":
		nTotalSymLinks += 1

print("nTotalErrors =", nTotalErrors)	
print("nTotalFiles =", nTotalFiles)
print("nTotalDirs =", nTotalDirs)
print("nTotalSymLinks =", nTotalSymLinks)
print("nTotalFileSize =", nTotalFileSize)






















