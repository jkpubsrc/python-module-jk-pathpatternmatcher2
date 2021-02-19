#!/usr/bin/python3


import re

import jk_utils
import jk_logging
from jk_pathpatternmatcher2 import *





PATTERNS = {
	"":						None,
	"some/***/path":		None,
	#"some/path/":			None,
	"some//path":			None,
	"some/x**/path":		None,
	"some/**x/path":		None,
	"some/x**x/path":		None,

	"**":					r"^xxxxxxxxxxxxx$",
	"**/path":				r"^(.*/)?path$",
	"some/path":			r"^some/path$",
	"/some/path":			r"^/some/path$",
	"some/*/path":			r"^some/[^/]*/path$",
	"some/**/path":			r"^some/(.*/)?path$",
	"some/*/**/path":		r"^some/[^/]*/(.*/)?path$",
	"some/path*":			r"^some/path[^/]*$",
	"some/path*/xy":		r"^some/path[^/]*/xy$",
	"some/path/*":			r"^some/path/[^/]*$",
	"some/path/**":			r"^some/path/.*$",
	"some/*.txt":			r"^some/[^/]*\.txt$",
}



TESTS = {
	"":							[],
	"some/***/path":			[],
	#"some/path/":				[],
	"some//path":				[],
	"some/x**/path":			[],
	"some/**x/path":			[],
	"some/x**x/path":			[],
	"**/path":					[],

	"some/path": [
		(	"some/path",				True	),
		(	"some",						False	),
		(	"some/other/path",			False	),
		(	"/some/path",				False	),
		(	"/some",					False	),
		(	"/some/other/path",			False	),
	],
	"/some/path": [
		(	"some/path",				False	),
		(	"some",						False	),
		(	"some/other/path",			False	),
		(	"/some/path",				True	),
		(	"/some",					False	),
		(	"/some/other/path",			False	),
	],
	"some/*/path": [
		(	"some/path",				False	),
		(	"some/other/path",			True	),
		(	"some/more/other/path",		False	),
		(	"/some/path",				False	),
		(	"/some/other/path",			False	),
		(	"/some/more/other/path",	False	),
	],
	"some/*/**/path": [
		(	"some/path",				False	),
		(	"some/other/path",			True	),
		(	"some/more/other/path",		True	),
		(	"/some/path",				False	),
		(	"/some/other/path",			False	),
		(	"/some/more/other/path",	False	),
	],
	"some/**/path": [
		(	"some/path",				True	),
		(	"some/other/path",			True	),
		(	"some/more/other/path",		True	),
		(	"/some/path",				False	),
		(	"/some/other/path",			False	),
		(	"/some/more/other/path",	False	),
	],
	"some/path*": [
		(	"some/xy",					False	),
		(	"some/path",				True	),
		(	"some/pathXX",				True	),
		(	"some/pathXX/as",			False	),
		(	"/some/xy",					False	),
		(	"/some/path",				False	),
		(	"/some/pathXX",				False	),
		(	"/some/pathXX/as",			False	),
	],
	"some/path*/xy": [
		(	"some/xy",					False	),
		(	"some/path",				False	),
		(	"some/path/xy",				True	),
		(	"some/pathX",				False	),
		(	"some/pathY/xy",			True	),
		(	"some/pathY/abc/xy",		False	),
		(	"/some/xy",					False	),
		(	"/some/path",				False	),
		(	"/some/path/xy",			False	),
		(	"/some/pathX",				False	),
		(	"/some/pathY/xy",			False	),
		(	"/some/pathY/abc/xy",		False	),
	],
	"some/path/*": [
		(	"some/xy",					False	),
		(	"some/path",				False	),
		(	"some/path/XX",				True	),
		(	"some/path/XX/as",			False	),
		(	"/some/xy",					False	),
		(	"/some/path",				False	),
		(	"/some/path/XX",			False	),
		(	"/some/path/XX/as",			False	),
	],
	"some/path/**": [
		(	"some/xy",					False	),
		(	"some/path",				False	),
		(	"some/path/XX",				True	),
		(	"some/path/XX/as",			True	),
		(	"/some/xy",					False	),
		(	"/some/path",				False	),
		(	"/some/path/XX",			False	),
		(	"/some/path/XX/as",			False	),
	],
	"some/*.txt": [
		(	"some/abc",					False	),
		(	"some/.tx",					False	),
		(	"some/txt",					False	),
		(	"some/.txt",				True	),
		(	"some/abc.txt",				True	),
		(	"/some/abc",				False	),
		(	"/some/.tx",				False	),
		(	"/some/txt",				False	),
		(	"/some/.txt",				False	),
		(	"/some/abc.txt",			False	),
	]
}


with jk_logging.wrapMain() as log:

	nSucceeded = 0
	nFailed = 0

	for testName, testRecords in TESTS.items():
		with log.descend("Testing: " + repr(testName)) as log2:
			regExProvided = PATTERNS[testName]
			regexCompiled = compilePattern(testName, raiseExceptionOnError=False)

			bResult = None
			if regexCompiled:
				s = regexCompiled.regexPattern
				if isinstance(regexCompiled, PathPatternMatcher):
					bResult = regexCompiled.regexPattern == regExProvided
				else:
					bResult = False
			else:
				s = None
				if regExProvided:
					bResult = False
				else:
					bResult = True

			if bResult is None:
				raise jk_utils.ImplementationError()
			if bResult:
				nSucceeded += 1
				log2.info("OK : compiled = " + repr(s) + ", expected = " + repr(regExProvided))
			else:
				nFailed += 1
				log2.error("ERR : compiled = " + repr(s) + ", expected = " + repr(regExProvided))

			if regExProvided:
				reTest = re.compile(regExProvided)
				for testStr, expectedResult in testRecords:
					m = reTest.match(testStr)
					bResult = m is not None
					if bResult == expectedResult:
						nSucceeded += 1
						log2.info("OK : " + repr(testStr) + "  ::  result = " + str(bResult) + ", expected = " + str(expectedResult))
					else:
						nFailed += 1
						log2.error("ERR : " + repr(testStr) + "  ::  result = " + str(bResult) + ", expected = " + str(expectedResult))

	if nFailed:
		log.error("nSucceeded = " + str(nSucceeded))
		log.error("nFailed = " + str(nFailed))
	else:
		log.success("nSucceeded = " + str(nSucceeded))
		log.success("nFailed = " + str(nFailed))

#








