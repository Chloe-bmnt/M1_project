#!/usr/bin/env python
#-*-coding:utf-8-*-p

import requests
import re


def pfam_fct(id_prot, outputfile):
	result=[]
	url = "https://pfam.xfam.org/protein/{}?output=xml".format(id_prot)
	r= requests.get(url)
	outputfile.write("<td>\n")
	if r.ok:
		response = r.text
		id_list = re.findall("<match accession=\"(.*)\" id=\"(.*)\" type", response)
		for id_pfam in id_list:
			if id_pfam not in result:
				result.append(id_pfam)
				outputfile.write("<a href=\"https://pfam.xfam.org/family/{0}\">{1} : {0}</a><br>\n".format(id_pfam[0], id_pfam[1]))
				outputfile.write('<a href="https://pfam.xfam.org/protein/{0}">graphical viewer</a><br>\n'.format(id_prot))
	else:
		outputfile.write("No data available")
	outputfile.write("</td>\n")

