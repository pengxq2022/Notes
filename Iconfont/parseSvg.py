#!/usr/bin/env python  
# encoding: utf-8  

import urllib
import sys
import os
import xml.etree.cElementTree as ET

def download_file(url, file_path):
	urllib.URLopener().retrieve(url, file_path)

def parse_svg_file(file_path):
	tree = ET.ElementTree(file=file_path)
	codes = []
	keys = []
	for elem in tree.iter():
		dict = elem.attrib
		un = dict.get('unicode')
		if un:
			tenString = un.encode('ascii', 'xmlcharrefreplace')[2:7]
			if (tenString):
				codes.append('<string>' + hex(int(tenString))[2:6] + '</string>')
				keys.append('<key>' + 'icon_font_' + dict.get('glyph-name') + '</key>')
	return codes, keys

def file_name(type):
    file_name = ''
    if type == '-u':
        file_name = 'iconfont_uban'
    elif type == '-m':
        file_name = 'iconfont_masheng'
    elif type == '-x':
        file_name = 'iconfont_xiaowo'
    else:
        file_name = 'iconfont_uban'
    return file_name

def plist_prefix():
    docuEncoding = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
    desc = "<!DOCTYPE plist PUBLIC \"-//Apple//DTD PLIST 1.0//EN\" \"http://www.apple.com/DTDs/PropertyList-1.0.dtd\">"
    version = "<plist version=\"1.0\">"
    dictPrefix = "<dict>"
    return docuEncoding + '\n' + desc + '\n' + version + '\n' + dictPrefix + '\n'

def plist_suffix():
    dictSuffix = "</dict>";
    plistSuffix = "</plist>";
    return dictSuffix + '\n' + plistSuffix

if __name__ == "__main__":

    url = sys.argv[1]
    svg_url = 'https://' + url + '.svg'
    svg_file_path = os.path.join(os.path.abspath('.'), 'iconfont.svg')
    download_file(svg_url, svg_file_path)
    codes, keys = parse_svg_file(svg_file_path)

    resources_path = os.path.join(os.path.abspath('..'), 'Resources')
    
    type = sys.argv[2]
    file_name = file_name(type)
    plist_file_name = file_name + '.plist'
    plist_file_path = os.path.join(resources_path, plist_file_name)

    ttf_url = 'https://' + url + '.ttf'
    ttf_file_name = file_name + '.ttf'
    ttf_file_path = os.path.join(resources_path, ttf_file_name)
    download_file(ttf_url, ttf_file_path)

    f = open(plist_file_path, 'w');
    f.write(plist_prefix())

    index = 0
    count = len(keys)
    while count > index:
        f.write(keys[count - index - 1] + '\n')
        f.write(codes[count - index - 1] + '\n')
        index = index + 1

    f.write(plist_suffix())
    f.close()

    os.remove(svg_file_path)
