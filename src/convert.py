#!/usr/bin/env python

"""convert.py: Converts a raw downloaded Gmail chat log to a HTML file."""

import quopri
import re
import sys

def convert(inputFile, outputFilename = ""):
    if outputFilename == "":
        outputFilename = inputFile.split('.')[0] + ".html"

    outputText = '<html>\n<head><meta http-equiv="content-type" content="text/html; charset=UTF-8">\n</head>\n<body>'
    outputText += "\n<i>" + getDate(inputFile) + "</i>"
    outputText += "\n<br><br>\n"
    outputText += extractConvo(getRaw(inputFile))
    outputText += "\n</body>\n</html>"
    toFile(outputFilename, outputText)

    print "'" + inputFile + "' converted to '" + outputFilename + "'."

def convertFilelist(filelist, separateOutputFiles, outputFilename = "output.html"):
    if separateOutputFiles:
        for filename in filelist:
            convert(filename)
    else:
        outputText = '<html>\n<head><meta http-equiv="content-type" content="text/html; charset=UTF-8">\n</head>\n<body>'
        for filename in filelist:
            outputText += "\n<i>" + getDate(filename) + "</i>"
            outputText += "\n<br><br>\n"
            outputText += extractConvo(getRaw(filename))
            outputText += "<hr><br>"
        outputText += "\n</body>\n</html>"
        toFile(outputFilename, outputText)
        print str(len(filelist)) + " files converted to '" + outputFilename + "'."

def getRaw(filename):
    file = open(filename, 'r')
    text = file.read()
    file.close()
    return text

def getDate(filename):
    file = open(filename, 'r')
    text = file.readline(50)
    file.close()
    text = re.findall(r"Date: (\w{3}, \d{1,2} \w{3} \d{4}) \d{2}:\d{2}:\d{2}", text)
    date = text[0]
    return date

def extractConvo(text):
    text = text.split('Content-Type: text/html; charset=', 1)[1]
    text = text.split('\r\n\r\n', 1)[1]
    text = text.split('------=_Part_')[0]
    text = quopri.decodestring(text)
    return text

def toFile(filename, data):
    file = open(filename, 'w')
    file.write(data)
    file.close()

def main():
    args = sys.argv
    if len(args) != 2:
        filename = raw_input("File: ")
    else:
        filename = args[1]

    convert(filename)

if __name__ == '__main__':
    main()
