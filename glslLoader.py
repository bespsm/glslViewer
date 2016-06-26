#!/usr/bin/env python

import sys, urllib, os, re

COMMAND='./glslViewer'
SHADER_PATH = '';

if len(sys.argv) > 1:
    SHADER_PATH = sys.argv[1]
else:
    print 'This script dowload a shader and their resorces:\nUse:\n$ ./glslLoader.py [URL|LOG_#]\n'
    exit()

if SHADER_PATH.isdigit():
    SHADER_PATH='https://thebookofshaders.com/log/' + SHADER_PATH + '.frag'

if SHADER_PATH.startswith('http'):
    http = urllib.URLopener()
    http.retrieve(SHADER_PATH, 'shader.frag')
    SHADER_PATH='shader.frag'

COMMAND += ' ' + SHADER_PATH
counter=0
with open(SHADER_PATH) as f:
    for line in f:
        result = re.search('uniform\\s*sampler2D\\s*([\\w]*);\\s*\\/\\/\\s*([\\w|\\:\\/\\/|\\.|\\-|\\_]*)', line, re.M)
        if result:
            uniform = result.group(1)
            url = result.group(2)
            ext = os.path.splitext(url)[1]
            img = str(counter) + ext
            print counter,uniform,url,ext
            http = urllib.URLopener()
            http.retrieve(url, img)
            COMMAND += ' -' + uniform + ' ' + img
            counter += 1

print COMMAND
os.system(COMMAND)