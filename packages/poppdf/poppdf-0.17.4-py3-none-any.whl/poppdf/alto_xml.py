#!/usr/bin/env python

""" alto_tools.py: simple methods to perform operations on ALTO xml files """

import argparse
import codecs
import io
import os
import sys
import xml.etree.ElementTree as ET
from io import StringIO

__version__ = '0.0.2'


def alto_parse(alto):
    """ Convert ALTO xml file to element tree """
    try:
        xml = ET.fromstring(alto)
    except ET.ParseError as e:
        sys.stdout.write('\nERROR: Failed parsing "%s" - ' % alto.name + str(e))
    # Register ALTO namespaces
    # https://www.loc.gov/standards/alto/ | https://github.com/altoxml
    # alto-bnf (unoffical) BnF ALTO dialect - for further info see
    # http://bibnum.bnf.fr/alto_prod/documentation/alto_prod.html
    namespace = {'alto-1': 'http://schema.ccs-gmbh.com/ALTO',
                 'alto-2': 'http://www.loc.gov/standards/alto/ns-v2#',
                 'alto-3': 'http://www.loc.gov/standards/alto/ns-v3#',
                 'alto-4': 'http://www.loc.gov/standards/alto/ns-v4#',
                 'alto-bnf': 'http://bibnum.bnf.fr/ns/alto_prod'}
    # Extract namespace from document root
    if 'http://' in str(xml.tag.split('}')[0].strip('{')):
        xmlns = xml.tag.split('}')[0].strip('{')
    else:
        try:
            ns = xml.getroot().attrib
            xmlns = str(ns).split(' ')[1].strip('}').strip("'")
        except IndexError:
            sys.stderr.write('\nERROR: File "%s": no namespace declaration found.' % alto.name)
            xmlns = 'no_namespace_found'
    if xmlns in namespace.values():
        return alto, xml, xmlns
    else:
        sys.stdout.write('\nERROR: File "%s": namespace %s is not registered.\n' % (alto.name, xmlns))


def alto_text(xml, xmlns, x_ratio, y_ratio):
    """ Extract text content from ALTO xml file """

    full_text=""
    text_lines=[]
    # Ensure use of UTF-8
    # Find all <TextLine> elements
    for lines in xml.iterfind('.//{%s}TextLine' % xmlns):
        text_line={"words":[]}
        # New line after every <TextLine> element
        full_text+='\n'
        # Find all <String> elements
        for line in lines.findall('{%s}String' % xmlns):
            # Check if there are no hyphenated words
            if ('SUBS_CONTENT' not in line.attrib and 'SUBS_TYPE' not in line.attrib):
            # Get value of attribute @CONTENT from all <String> elements
                text = line.attrib.get('CONTENT')
                word_dict = {"value": text, "left":int(int(line.attrib.get('HPOS'))*x_ratio), "top":int(int(line.attrib.get('VPOS'))*y_ratio), "right": int(int(line.attrib.get('HPOS'))*x_ratio)+ int(int(line.attrib.get('WIDTH'))*x_ratio), "bottom": int(int(line.attrib.get('VPOS'))*y_ratio)+int(int(line.attrib.get('HEIGHT'))*y_ratio),"width":int(int(line.attrib.get('WIDTH'))*x_ratio), "height":int(int(line.attrib.get('HEIGHT'))*y_ratio)}
                text_line["words"].append(word_dict)
                full_text+=text
        text_line["words"]=sorted(text_line["words"], key=lambda x:x["left"])
        text_lines.append(text_line)




    return text_lines, full_text



def alto_confidence(xml, xmlns):
    """ Calculate word confidence for ALTO xml file """
    score = 0
    count = 0
    # Find all <String> elements
    for conf in xml.iterfind('.//{%s}String' % xmlns):
        # Get value of attribute @WC (Word Confidence) of all <String> elements
        wc = conf.attrib.get('WC')
        # Calculate sum of all @WC values as float
        score += float(wc)
        # Increment counter for each word
        count += 1
        # Divide sum of @WC values by number of words
    if count > 0:
        confidence = score / count
        result = round(100 * confidence, 2)
        return result
    else:
        return 0.0




def process_alto_xml(alto_xml, x_ratio, y_ratio):
    if sys.version_info < (3, 0):
        sys.stdout.write('Python 3 is required.\n')
        sys.exit(-1)

    try:
        alto, xml, xmlns = alto_parse(alto_xml)
    except IndexError:
        pass
    confidence=alto_confidence(xml, xmlns)

    text_lines, full_text=alto_text(xml, xmlns, x_ratio, y_ratio)

    text_lines=[merge_words(tl) for tl in text_lines]
    return sorted(text_lines, key=lambda t: (t["top"], t["left"])), full_text, confidence



def merge_words(text_line):
    if len(text_line["words"])==0:
        text_line["value"]=""
        return text_line

    text_line["left"]=min([b["left"] for b in text_line["words"]])
    text_line["top"]=min([b["top"] for b in text_line["words"]])
    text_line["right"]=max([b["right"] for b in text_line["words"]])
    text_line["bottom"]=max([b["bottom"] for b in text_line["words"]])
    text_line["value"]=' '.join([b["value"] for b in text_line["words"]])


    return text_line