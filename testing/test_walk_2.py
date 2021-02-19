#!/usr/bin/python3


import jk_utils
import jk_logging
from jk_pathpatternmatcher2 import *










with jk_logging.wrapMain() as log:

	nTotalErrors = 0
	nTotalFiles = 0
	nTotalDirs = 0
	nTotalSymLinks = 0
	nTotalFileSize = 0

	with log.descend("Scanning ...") as log2:
		for e in walk(
				"..",
				ignoreDirPathPatterns = [
					".git",
					".vscode",
				],
				emitDirs = False,
				emitBaseDirs = False,
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




















