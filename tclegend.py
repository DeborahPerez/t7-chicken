#!\usr\bin\env python
########################################################################
#   USAGE:
#       python2 tclegend.py
#   DESCRIPTION:
#       html table conversion to json using Python 2.x
#-----------------------------------------------------------------------
#   CREATED BY: Deborah Perez
#   VERSION:    20170604
########################################################################
import urllib
import re

jsonFormatter = 'https://jsonformatter.curiousconcept.com/'
jsonLegend = '{"name": "Tekken Zaibatsu Legend", "description": "Tekken Legend ripped from Tekken Zaibatsu", "main": "tclegend.py", "author": "Deborah Perez <deborah.a.perez@gmail.com> (https://github.com/deborahperez/)", "legend": { ' #Initialize JSON file as a string
#print jsonLegend

link = "http://www.tekkenzaibatsu.com/legend.php"
f = urllib.urlopen(link)
rawFile = f.read()
myfile = rawFile.splitlines()
myfile = myfile[11:]
#for l in myfile:
#    print l

# Define function to search for substring
def btwnStartEnd(start, end, string):
    subString = (string.split(start))[1].split(end)[0]
    return subString
# Define instance naming convention
def instaName(string):
    output = [s.strip() for s in string.split(' ') if s]
    return output
#print jsonLegend

# Splice category chunks using location 1 and location 2
first = "<fieldset>"
last = "</fieldset>"
catFirst = '<legend>'
catLast = '</legend>'
acrFirst = '<td>'
acrAltFirst = '">'
acrLast = '</td>'
endTable = '</table>'
for i in range(len(rawFile)):
    if rawFile[i:i+len(first)] == first:
        location1 = i
    if rawFile[i:i+len(last)] == last:
        location2 = i
#        print '\nlocation 1: ', location1
#        print 'location 2: ', location2
        categorySection = rawFile[location1:location2]
#        print 'Category Section: ', categorySection
        # Turn section into lines in a list
        linesCatSect = categorySection.splitlines()
        sectionLength = len(linesCatSect)
#        print '\ncategory section in lines: ', linesCatSect
        # Search for category name substring in between <legend> and </legend>
        acronymMeanings = []
        for line in linesCatSect:
            if catFirst in line and catLast in line:
                category = btwnStartEnd(catFirst, catLast, line)
                category = '"{}"'.format(category)
                category += ': { '
#                print '\ncategory name: ', category
                jsonLegend += category
                count = 0

        # Search for substring in between <td> or "> and </td> and append to a list
            if acrFirst in line or acrAltFirst in line and acrLast in line:
                count += 1
                if acrFirst in line:
                    splicedWord = btwnStartEnd(acrFirst, acrLast, line)
                    splicedWord = '"{}"'.format(splicedWord)
                    acronymMeanings.append(splicedWord)
                if acrAltFirst in line:
                    splicedWord = btwnStartEnd(acrAltFirst, acrLast, line)
                    splicedWord = '"{}"'.format(splicedWord)
                    acronymMeanings.append(splicedWord)
                if count % 2 == 0:
                    splicedWord += ', '
                    jsonLegend += splicedWord
                else:
                    splicedWord += ': '
                    jsonLegend += splicedWord

            # Here account for end of section and add }
            if endTable in line:
                jsonLegend = jsonLegend[:-2]
                jsonLegend += '}, '

jsonLegend = jsonLegend[:-2]
jsonLegend += '}}'
print jsonLegend
