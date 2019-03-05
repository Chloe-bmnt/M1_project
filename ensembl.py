#!/usr/bin/env python
#-*-coding:utf-8-*-p

import requests
import re
import sys
	

def ensembl_id_fct(gene, organism):
	server = "https://rest.ensembl.org"
	ext = "/xrefs/symbol/{}/{}?".format(organism, gene)
	 
	r = requests.get(server+ext, headers={ "Content-Type" : "application/json"})
	 
	if not r.ok:
		server = "https://rest.ensemblgenomes.org"
		ext = "/xrefs/symbol/{}/{}?".format(organism, gene)
		r = requests.get(server+ext, headers={ "Content-Type" : "application/json"})
	 

	decoded = r.json()
	return decoded


def ensembl_trans_prot_fct(id_ens):
	server2 = "https://rest.ensembl.org"
	ext2 = "/lookup/id/{}?expand=1".format(id_ens)
	 

	r2 = requests.get(server2+ext2, headers={ "Content-Type" : "application/json"})
	 
	if not r2.ok:
		server2 = "https://rest.ensemblgenomes.org"
		ext2 = "/lookup/id/{}?expand=1".format(id_ens)
		r2 = requests.get(server2+ext2, headers={ "Content-Type" : "application/json"})
	 
	decoded2 = r2.json()
	return decoded2["Transcript"]



def ensembl_orthologue_fct(organism, id_ens):
		r4=requests.get("https://rest.ensembl.org/homology/id/{}?format=condensed;type=orthologues;content-type=application/json".format(id_ens))
		result=r4.json()
		if len(result["data"])==0:
			r4=requests.get("https://rest.ensemblgenomes.org/homology/id/{}?format=condensed;type=orthologues;content-type=application/json".format(id_ens))
			result=r4.json()
		
		
		
def ensembl_orthologue_fct(organism, id_ens, outputfile):
		r4=requests.get("https://rest.ensembl.org/homology/id/{}?format=condensed;type=orthologues;content-type=application/json".format(id_ens))
		result=r4.json()
		if len(result["data"])==0:
			r4=requests.get("https://rest.ensemblgenomes.org/homology/id/{}?format=condensed;type=orthologues;content-type=application/json".format(id_ens))
			result=r4.json()
		
		
		if len(result["data"][0]["homologies"])>1:
			db_list = ["ensembl", "plants.ensembl", "bacteria.ensembl", "fungi.ensembl", "protists.ensembl", "metazoa.ensembl"]
			for db in db_list :
				r3 = requests.get("http://{}.org/{}/Gene/Compara_Ortholog?db=core;g={}".format(db, organism, id_ens))
				if r3.ok :
					url_final = r3.url
					outputfile.write("<a href=\"{}\">Orthologue : {}</a><br>\n".format(url_final, id_ens))
					break
				else :
					outputfile.write("No orthologue")
				
			
		
			
