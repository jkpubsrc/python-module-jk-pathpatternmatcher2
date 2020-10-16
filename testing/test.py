#!/usr/bin/python3


import re

from jk_pathpatternmatcher2 import *





PATTERNS = {
	"":						None,
	"some/***/path":		None,
	"some/path/":			None,
	"some//path":			None,
	"some/x**/path":		None,
	"some/**x/path":		None,
	"some/x**x/path":		None,

	"some/path":			r"^some/path$",
	"/some/path":			r"^/some/path$",
	"some/*/path":			r"^some/[^/]*/path$",
	"some/**/path":			r"^some/.*/path$",
	"some/path*":			r"^some/path[^/]*$",
	"some/path*/xy":		r"^some/path[^/]*/xy$",
	"some/path/*":			r"^some/path/[^/]*$",
	"some/path/**":			r"^some/path/.*$",
	"some/*.txt":			r"^some/[^/]*\.txt$",
}



TESTS = {
	"":							[],
	"some/***/path":			[],
	"some/path/":				[],
	"some//path":				[],
	"some/x**/path":			[],
	"some/**x/path":			[],
	"some/x**x/path":			[],

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
	"some/**/path": [
		(	"some/path",				False	),
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




nSucceeded = 0
nFailed = 0

for testName, testRecords in TESTS.items():
	print(repr(testName))

	regExProvided = PATTERNS[testName]
	regexCompiled = compilePattern(testName, raiseExceptionOnError=False)
	if regexCompiled:
		s = regexCompiled.regexPattern
		if isinstance(regexCompiled, PathPatternMatcher):
			if regexCompiled.regexPattern == regExProvided:
				nSucceeded += 1
				pre = "OK\t"
			else:
				nFailed += 1
				pre = "ERR\t"
		else:
			nFailed += 1
			pre = "ERR\t"
	else:
		s = None
		if regExProvided:
			nFailed += 1
			pre = "ERR\t"
		else:
			nSucceeded += 1
			pre = "OK\t"
	print("\t" + pre + "compiled = " + repr(s) + ", expected = " + repr(regExProvided))

	if regExProvided:
		print()
		reTest = re.compile(regExProvided)
		for testStr, expectedResult in testRecords:
			m = reTest.match(testStr)
			bResult = m is not None
			if bResult == expectedResult:
				nSucceeded += 1
				pre = "OK\t"
			else:
				nFailed += 1
				pre = "ERR\t"
			print("\t" + pre + repr(testStr) + "  ::  result = " + str(bResult) + ", expected = " + str(expectedResult))

	print()

print()
print("nSucceeded =", nSucceeded)
print("nFailed =", nFailed)










