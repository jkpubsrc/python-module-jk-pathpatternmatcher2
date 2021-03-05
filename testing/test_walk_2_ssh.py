#!/usr/bin/python3





import os

import jk_utils
import jk_logging
from jk_pathpatternmatcher2 import *
import jk_pwdinput

import fabric




HOST = "localhost"
USER = jk_utils.users.lookup_username()
PORT = 22
PASSWORD = None
if not PASSWORD:
	PASSWORD = jk_pwdinput.readpwd("Password for {}@{}: ".format(USER, HOST))
	assert PASSWORD





with jk_logging.wrapMain() as log:

	ioAdapter = IFabricIOAdapter(host=HOST, port=PORT, user=USER, pwd=PASSWORD)

	nTotalErrors = 0
	nTotalFiles = 0
	nTotalDirs = 0
	nTotalSymLinks = 0
	nTotalFileSize = 0

	dirPath = os.path.abspath("..")

	with log.descend("Scanning ...") as log2:
		for e in walk(
				dirPath,
				ignoreDirPathPatterns = [
					".git",
					".vscode",
				],
				emitDirs = False,
				emitBaseDirs = False,
				ioAdapter = ioAdapter,
			):
			if e.typeID == "e":
				nTotalErrors += 1
				log2.warn(str(e))
			else:
				if e.typeID == "f":
					log2.notice(str(e))
					nTotalFiles += 1
					nTotalFileSize += e.size
				elif e.typeID == "d":
					log2.info(str(e))
					nTotalDirs += 1
				elif e.typeID == "l":
					log2.notice(str(e))
					nTotalSymLinks += 1
				else:
					raise jk_utils.ImplementationError()

	with log.descend("Summary:") as log2:
		log2.info("nTotalErrors = {}".format(nTotalErrors))
		log2.info("nTotalFiles = {}".format(nTotalFiles))
		log2.info("nTotalDirs = {}".format(nTotalDirs))
		log2.info("nTotalSymLinks = {}".format(nTotalSymLinks))
		log2.info("nTotalFileSize = {}".format(nTotalFileSize))

#




















