#!/usr/bin/env python
#-*-coding:utf-8-*-p

import requests
import re


def go_fct(id_prot, type_go, outputfile):
	url_id = "https://www.ebi.ac.uk/QuickGO/services/annotation/search?includeFields=goName&aspect=" + type_go + "&geneProductId=" + id_prot
	r = requests.get(url_id, headers={"Accept": "application/json"})
	outputfile.write("<td>")
	if r.ok:
		response = r.json()
		list_go = []
		
		i=0
		while i < len(response['results']):
			if response['results'][i]['goId'] not in list_go:
				list_go.append(response['results'][i]['goId'])
				id_go = response['results'][i]['goId']
				name_go = response['results'][i]['goName']
				outputfile.write('<a href="https://www.ebi.ac.uk/QuickGO/term/{}">{}</a><br>\n'.format(id_go, name_go))
			i+=1
		
	else:
		outputfile.write(" QuickGo not available \n")
	
	outputfile.write("</td>\n")	
	
