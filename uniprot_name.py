#!/usr/bin/env python
#-*-coding:utf-8-*-p

import requests
import re


def uniprot_fct(gene, organism, outputfile):
	liste=[]
	r = requests.get("https://www.uniprot.org/uniprot/?query=gene_exact%3A{}+organism%3A{}+fragment%3Ano&sort=score&columns=id,protein_names&format=tab".format(gene, organism))
	result=r.text
	result1=result.splitlines()
	del (result1[0])
	outputfile.write("<td>")
	i=0
	for element in result1 :
		result2=result1[i].split("\t")
		result2[1] = re.sub('( [\(|\[].*[\)|\]])', '', result2[1])
		
		i+=1
		
		liste.append(result2)
		outputfile.write("<a href=\"https://www.uniprot.org/uniprot/" + result2[0] + "\">" + result2[0] + "</a><br>\n" )
	outputfile.write("</td>")
	outputfile.write("<td>")
	i=0
	for element in result1 :
		result2=result1[i].split("\t")
		result2[1] = re.sub('( [\(|\[].*[\)|\]])', '', result2[1])
		i+=1
		
		outputfile.write(result2[1] + "<br>\n")
	outputfile.write("</td>")
	return liste
	
	
def string_fct(id_prot,outputfile):	
	r2 = requests.get("https://string-db.org/api/image/network?identifiers={}".format(id_prot))
	if r2.ok :	
		result=r2.url
		outputfile.write("<iframe src=\"" + result + "\"> " + " </iframe><br>\n")
		outputfile.write("<a href=\"" + result + "\"> interaction map" + " </a><br>\n")	
		

def pdb_fct(id_prot, outputfile):
	url = "https://www.rcsb.org/pdb/rest/search"
	data= """ 
	<orgPdbQuery>

	<queryType>org.pdb.query.simple.UpAccessionIdQuery</queryType>


	<accessionIdList>{}</accessionIdList>

	</orgPdbQuery>

	""".format(id_prot)
	header={"Content-Type":"Application/x-www-form-urlencoded"}

	r = requests.post(url,data=data,headers=header)
	result2=r.text
	
	if result2 != "null\n":
		result3=re.sub("(:\d{1})","",result2)
		result4=result3[:-1]
		list_pdb=result4.split("\n")
		for pdb in list_pdb :
			outputfile.write("<a href=\"https://www.rcsb.org/structure/" + pdb + "\">" + pdb + "</a><br>\n")


	

