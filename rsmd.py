#! /usr/bin/python3
#
# @(!--#) @(#) rsmd.py, version 004, 29-may-2018
#
# really simple mark down to HTML converter
#

######################################################################


######################################################################

#
# imports
#

import sys
import os
import argparse
import random

######################################################################

#
# constants
#

STYLE_NONE    = 0
STYLE_PARA    = 1
STYLE_LIST    = 2
STYLE_CODE    = 3

######################################################################

def allsamechar(s, c):
    same = True
    
    for c2 in s:
        if c2 != c:
            same = False
            break
            
    return same

######################################################################

def html(s):
    h = ''
    
    for c in s:
        if c == '<':
            h += '&lt;'
        elif c == '>':
            h += '&gt;'
        elif c == '&':
            h += '&amp;'
        else:
            h += c

    return h

######################################################################

def extractheading(line):
    words = line.split()
    
    if len(words) < 2:
        return 0, ''

    firstword = words[0]
    
    if (len(firstword) < 1) or (len(firstword) > 6):
        return 0, ''
    
    if not allsamechar(firstword, '#'):
        return 0, ''
        
    return len(firstword), ' '.join(words[1:])

######################################################################

def extractquote(line):
    words = line.split()
    
    if len(words) < 2:
        return ''
        
    if words[0] != '>':
        return ''

    return ' '.join(words[1:])

######################################################################

def extractlistitem(line):
    words = line.split()
    
    if len(words) < 2:
        return ''
        
    if words[0] != '*':
        return ''

    return ' '.join(words[1:])

######################################################################
    
def flushstyle(style, outputfile):
    if style == STYLE_PARA:
        print('</p>', file=outputfile)
    elif style == STYLE_LIST:
        print('</ul>', file=outputfile)
    elif style == STYLE_CODE:
        print('</pre>', file=outputfile)
        
    return

######################################################################

def processlines(lines, firstheading, outputfile):
    if firstheading == '':
        firstheading = 'No title'
        
    print('<html>', file=outputfile)
    print('<head>', file=outputfile)

    print('<title>{}</title>'.format(html(firstheading)), file=outputfile)
    
    print('<style>', file=outputfile)
    print('blockquote { background-color: lightgrey; margin-left: 50px; margin-right: 50px; }', file=outputfile)
    print('pre { background-color: lightgreen; margin-left: 50px; }', file=outputfile)
    print('</style>', file=outputfile)
    
    print('</head>', file=outputfile)
    print('', file=outputfile)
    print('<body>', file=outputfile)
    print('', file=outputfile)

    style = STYLE_NONE
    
    linecount = 0
    for line in lines:
        linecount += 1

        if len(line) == 0:
            if style != STYLE_CODE:
                flushstyle(style, outputfile)
                style = STYLE_NONE
            print('', file=outputfile)
            continue
            
        if line[0] == '#':
            flushstyle(style, outputfile)
            style = STYLE_NONE
            hc, headingtext = extractheading(line)
            if hc > 0:
                print('<h{}>{}</h{}>'.format(hc, html(headingtext), hc), file=outputfile)
            else:
                print('{}: badly formed heading line at line {} - ignoring'.format(progname, linecount), file=sys.stderr)
            continue
        
        if line[0] == '>':
            flushstyle(style, outputfile)
            style = STYLE_NONE
            quote = extractquote(line)
            if quote != '':
                print('<blockquote>{}</blockquote>'.format(html(quote)), file=outputfile)
            else:
                print('{}: badly formed quote line at line {} - ignoring'.format(progname, linecount), file=sys.stderr)
            continue
        
        if line[0] == '*':
            if style != STYLE_LIST:
                flushstyle(style, outputfile)
                print('<ul>', file=outputfile)
                style = STYLE_LIST
            listitem = extractlistitem(line)
            if listitem != '':
                print('<li>{}</li>'.format(html(listitem)), file=outputfile)
            else:
                print('{}: badly formed list item line at line {} - ignoring'.format(progname, linecount), file=sys.stderr)
            continue
            
        if line == '```':
            if style == STYLE_CODE:
                flushstyle(style, outputfile)
                style = STYLE_NONE
            else:
                flushstyle(style, outputfile)
                style = STYLE_CODE
                print('<pre>', file=outputfile)
            continue
        
        if style == STYLE_NONE:
            print('</p>', file=outputfile)
            style = STYLE_PARA
            
        print("{}".format(html(line)), file=outputfile)
        
    flushstyle(style, outputfile)

    print('', file=outputfile)
    print('</body>', file=outputfile)
    print('</html>', file=outputfile)
    
    return    

######################################################################
def rsmd(inputfilename, outputfilename):
    try:
        inputfile = open(inputfilename, 'r', encoding='utf-8')
    except IOError:
        print('{}: unable to open file "{}" for reading'.format(progname, inputfilename), file=sys.stderr)
        sys.exit(1)
    
    try:
        outputfile = open(outputfilename, 'w', encoding='utf-8')
    except IOError:
        print('{}: unable to open file "{}" for writing'.format(progname, outputfilename), file=sys.stderr)
        sys.exit(1)

    firstheading = ''
    lines = []
    
    for line in inputfile:
        line = line.strip()
        lines.append(line)
        
        if firstheading == '':
            hc, fh = extractheading(line)
            if hc > 0:
                firstheading = fh

    inputfile.close()
    
    processlines(lines, firstheading, outputfile)
    
    outputfile.flush()
    outputfile.close()
            
    return    
    
######################################################################

#
# Main
#

progname = os.path.basename(sys.argv[0])

parser = argparse.ArgumentParser()
parser.add_argument("--infile", help="input file", default="README.md")
parser.add_argument("--outfile", help="output file", default="README.htm")
args = parser.parse_args()

rsmd(args.infile, args.outfile)

sys.exit(0)
