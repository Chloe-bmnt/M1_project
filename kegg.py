#!/usr/bin/env python
#-*-coding:utf-8-*-p

import requests
import re


def kegg_fct(id_ncbi, outputfile):
		url = "http://rest.kegg.jp/conv/genes/ncbi-geneid:{}".format(id_ncbi)
		kegg_url = "https://www.genome.jp/dbget-bin/www_bget?"
		pathway_url = "https://www.genome.jp/kegg-bin/show_pathway?"
		r = requests.get(url)
		if r.ok:
			response = r.text.rstrip()
			list_split = response.split("\t")
			list_kegg = list_split[1::2]
			outputfile.write("<td>\n")
			if len(list_kegg) != 0:
				for id_kegg in list_kegg:
					outputfile.write("<a href=\"{0}{1}\">{1}</a><br>\n".format(kegg_url, id_kegg))
				outputfile.write("</td>\n")
			
				outputfile.write("<td>\n")
				for id_kegg in list_kegg:
					url2 =  "http://rest.kegg.jp/get/+{}".format(id_kegg)
					r2 = requests.get(url2)
					if r2.ok:
						letters = id_kegg[:3] 
						regex_path = " (" + letters + "\d{5})  (.*)" 
						list_id_name = re.findall(regex_path, r2.text)
						if len(list_id_name) != 0:
							for id_name in list_id_name:
								outputfile.write("<a href=\"{0}{1}\">{1} : {2}</a><br>\n".format(pathway_url, id_name[0], id_name[1]))
					else : 
						outputfile.write("No data available")
				outputfile.write("</td>\n")
			else :
				outputfile.write("<td>No data available</td>\n")
		else:
			outputfile.write("<td>No data available</td>\n")	
			
			
