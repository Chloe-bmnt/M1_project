#!/usr/bin/env python
#-*-coding:utf-8-*-p

import requests
import re

	
def prosite_fct(id_prot, outputfile):
	url = "https://prosite.expasy.org/cgi-bin/prosite/PSScan.cgi?seq={}&output=json".format(id_prot)
	r = requests.get(url)
	outputfile.write("<td>")
	if r.ok:
		response = r.json()
		i=0
		while i < len(response["matchset"]):
			prosite_acc = response["matchset"][i]["signature_ac"]
			prosite_id = response["matchset"][i]["signature_id"]
			outputfile.write('<a href="https://prosite.expasy.org/{1}">{1} : {0}</a><br>\n'.format(prosite_id, prosite_acc))
			i +=1
		
	else :
		outputfile.write("<td> No data available</td>\n")
		
	url2 =  "https://prosite.expasy.org/cgi-bin/prosite/PSScan.cgi?seq={}".format(id_prot)
	r2 = requests.get(url)
	if r2.ok:
		response2 = r2.text
		graph = re.findall("<a href=\"(.*)\">Graphical view</a>",response2)
		outputfile.write('<a href="{}">graphical viewer</a><br>\n'.format(graph))
		outputfile.write("</td>\n")
	else :
		outputfile.write("<td> No data available</td>\n")

