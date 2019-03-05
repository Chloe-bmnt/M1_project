#!/usr/bin/env python
#-*-coding:utf-8-*-p

import requests
import re


def ncbi_id(gene, organism, outputfile):
	server = "https://eutils.ncbi.nlm.nih.gov"
	ext = "/entrez/eutils/esearch.fcgi?db=gene&term={}[ORGN]+{}[GENE]&idtype=acc&retmode=json".format(organism, gene)
	r = requests.get(server+ext)
	decoded = r.json()
	list_id = decoded["esearchresult"]["idlist"]
	outputfile.write("<td>")
	for id_ncbi in list_id:
		server = "https://eutils.ncbi.nlm.nih.gov"
		ext = "/entrez/eutils/esummary.fcgi?db=gene&id={}&retmode=json".format(id_ncbi)
		r2 = requests.get(server+ext)
		if r2.ok:
			response = r2.json()
			name = response['result']['{}'.format(id_ncbi)]['description']
			outputfile.write('<a href="https://www.ncbi.nlm.nih.gov/gene/{0}">{0} : {1}</a><br>\n'.format(id_ncbi, name))		
	outputfile.write("</td>\n")	
	return(list_id)	


def refseq_fct(db_refseq, type_refseq, organism, gene, outputfile):
		server = "https://eutils.ncbi.nlm.nih.gov"
		ext = "/entrez/eutils/esearch.fcgi?db={}&term=({}[ORGN]+{}[Gene%20Name])&idtype=acc&retmode=json".format(db_refseq, organism, gene)
		r = requests.get(server+ext)
		if r.ok:
			response = r.json()
			listid = response["esearchresult"]["idlist"]
			list_id = []
			for id_refseq in listid:
				if "{}_".format(type_refseq) in id_refseq:
					list_id.append(id_refseq)
			if len(list_id) != 0:
				outputfile.write('<td>')
				
				for id_ref in list_id:
					if "NM" in id_ref:
						ucsc_url = "http://genome.ucsc.edu/cgi-bin/hgTracks?org={}&position={}".format(organism, id_ref)
						outputfile.write('<a href="https://www.ncbi.nlm.nih.gov/nuccore/{0}">{0}</a><br>\n'.format(id_ref, ucsc_url))
					else:
						outputfile.write('<a href="https://www.ncbi.nlm.nih.gov/nuccore/{0}">{0}</a><br>\n'.format(id_ref))
				outputfile.write('</td>\n')
			else:
				outpufile.write('<td>No data available</td>\n')
		else:
			outpufile.write('<td>No data available</td>\n')
