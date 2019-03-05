import re
import sys
from uniprot_name import *
from ensembl import *
from ncbi import *
from GO import *
from prosite import *
from kegg import *
from pfam import *


#récuperer les infos
#~ with open('GeneSymbols.txt','r') as f:
	#~ l = f.read().splitlines()
	
	
#~ tempfile = open('table.html','r')
#~ outputfile = open('result.html','w')
#~ outputfile.write(tempfile.read())
	
relative_path = sys.path[0]
tempfile = open(relative_path + '/table.html','r')
outputfile = open(relative_path + '/result.html','w')
tempfile_end = open(relative_path + '/end_template.html', 'r')
outputfile.write(tempfile.read())

with open(sys.argv[1],'r') as f:
	l = f.read().splitlines()

#récuperer les gènes et le nom des organismes à partir du fichier GeneSymbols.txt
for line in l:
	outputfile.write("<tr>")
	line=line.split("\t")
	gene=line[0]
	print(gene)
	outputfile.write("<td>{}</td>\n".format(gene))
	organism=line[1]
	organism1=re.sub("(\s)$","",organism)
	organism2=re.sub(" ","_",organism1)
	outputfile.write("<td>{}</td>\n".format(organism1))
	
#récupérer les ID UNIPROT
	list_uniprot = uniprot_fct(gene, organism2, outputfile) #appel de la fonction uniprot
	outputfile.write("<td>")
	for element in list_uniprot :
		id_prot=element[0]
		string_fct(id_prot, outputfile) #appel de la fonction string
	outputfile.write("</td>\n")
	
	outputfile.write("<td>")
	for element in list_uniprot :
		id_prot=element[0]
		pdb_fct(id_prot, outputfile) #appel de la fonction pdb
	outputfile.write("</td>\n")
	
#récupérer les ID ensembl	
	list_ensembl = ensembl_id_fct(gene, organism2) #appel de la fonction ensembl
	k=0
	outputfile.write("<td>")
	for donnee in list_ensembl:
		id_ens=list_ensembl[k]["id"]
		ensembl_trans_prot_fct(id_ens) #appel de la fonction transcrits et proteines ensembl
		k+=1
		outputfile.write('<a href=\"https://www.ensembl.org/{0}/Gene/Summary?db=core;g={1}">{1}</a><br>\n'.format(organism2, id_ens))
		list_trans_prot=ensembl_trans_prot_fct(id_ens)
		ensembl_orthologue_fct(organism2, id_ens, outputfile) #appel de la fonction orthologues ensembl
	outputfile.write("</td>\n")

#récupérer les transcrits ensembl	
	k=0
	outputfile.write("<td>")
	for donnee in list_ensembl:
		id_ens=list_ensembl[k]["id"]
		ensembl_trans_prot_fct(id_ens)
		k+=1
		list_trans_prot=ensembl_trans_prot_fct(id_ens)
		
		i=0
		for element in list_trans_prot:
			transcript=list_trans_prot[i]["id"]
			outputfile.write('<a href=\"https://www.ensembl.org/{0}/Transcript/Summary?db=core;t={1}">{1}</a><br>\n'.format(organism2, transcript))
			i+=1
	outputfile.write("</td>\n")
	
#récupérer les protéines ensembl
	k=0
	outputfile.write("<td>")
	for donnee in list_ensembl:
		id_ens=list_ensembl[k]["id"]
		ensembl_trans_prot_fct(id_ens)
		k+=1
		list_trans_prot=ensembl_trans_prot_fct(id_ens)
				
		j=0
		for element in list_trans_prot:
			transcript=list_trans_prot[j]["id"]
			if list_trans_prot[j]["biotype"]=="protein_coding" :
				protein=list_trans_prot[j]["Translation"]["id"]
				outputfile.write('<a href=\"https://www.ensembl.org/{0}/Transcript/ProteinSummary?db=core;t={1}">{2}</a><br>\n'.format(organism2, transcript, protein))
				
			elif list_trans_prot[j]["biotype"]=="LRG_gene":	
				protein=list_trans_prot[j]["Translation"]["id"]
				outputfile.write('<a href=\"https://www.ensembl.org/{0}/Transcript/ProteinSummary?db=core;t={1}">{2}</a><br>\n'.format(organism2, transcript, protein))	
			j+=1	
	outputfile.write("</td>\n")
	
	list_ncbi = ncbi_id(gene, organism2, outputfile) #appel de la fonction ID NCBI
	
#appel de la fonction refseq pour les nucléotides et les protéines
	refseq_fct("nucleotide", "M", organism2, gene, outputfile) 
	refseq_fct("protein", "P", organism2, gene, outputfile)
	
#appel de la fonction GO pour les différentes fonctions
	id_prot=list_uniprot[0][0]
	go_fct(id_prot,"biological_process", outputfile)
	go_fct(id_prot,"molecular_function", outputfile)
	go_fct(id_prot,"cellular_component", outputfile)
	
	prosite_fct(id_prot, outputfile)#appel de la fonction prosite
	
	pfam_fct(id_prot, outputfile) #appel de la fonction pfam
	
	id_ncbi = list_ncbi[0]
	kegg_fct(id_ncbi, outputfile) #appel de la fonction KEGG
	
	outputfile.write("</tr>\n")
	
