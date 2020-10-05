#Name: Display Build Progress
#Info: During printing, display the percentage of build complete
#Depend: GCode
#Type: postprocess

# Written by Peter Monaco, Dec 22, 2015
# Drop in your <CuraInstallation>/plugins directory

import re

### Un-comment these lines to use as a standalone script:
#import sys
#inputFilename = sys.argv[1]
#outputFilename = "tmpout"

### Comment-out these lines to make it a standalone script:
inputFilename = filename
outputFilename = filename

# returns a float, or -1 if no Extrusion value is present in that line
def findEValueInLine(line):
    tokens = line.split()
    for token in tokens:
        if (token.startswith("E")):
            floatVal = token[1:(len(token))]
            try:
                v = float(floatVal);
                if (v > 0):
                    return v
            except ValueError:
                continue
    return -1

def findLargestExtrusionValue(lines):
    for line in reversed(lines):
        eVal = findEValueInLine(line)
        #print "Found {} in {}".format(eVal, line)
        if (eVal > 0):
            return eVal
    return 1



with open(inputFilename, "r") as f:
	lines = f.readlines()

# Find the largest extrusion value in the file, searching backward from the end
# We will compute percent-complete as a fraction of total extrusion

maxExtrusion = findLargestExtrusionValue(lines)
#print "Found max extrusion to be: {}".format(maxExtrusion)
            

lastPct = 0
with open(outputFilename, "w") as f:
    for line in lines:
	f.write(line)
	eValue = findEValueInLine(line)
        if (eValue > 0):
            # compute the %
            pct = int(100.0 * eValue / maxExtrusion)
            if (pct > lastPct and pct < 100):
                f.write("M73 P{}\n".format(pct))
                lastPct = pct



