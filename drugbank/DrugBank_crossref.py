#!/usr/bin/env python

from bs4 import BeautifulSoup
import glob

orig_filename = "full database 2.xml"

#look into that file and open one file (one drug entry per file) per loop
for filename in glob.glob("/home/mdt16kk/cross-ref/xml-file-split-by-drug/*"):
	#print(filename)
	f = open(filename).read()

#make soup object
	soup = BeautifulSoup(f, "lxml")

#look inside single drug entry
	for drug in soup.find_all('drug'):

#finds primary drugbank id and finds other elements
		drugbank_id = drug.find('drugbank-id', { 'primary' : 'true' })
	
		if drugbank_id is None:
			continue
		# == if drugbank_id is not None (without an indent)

#find drugbank name and print it
		name = drug.find('name')
		print("DrugBank:"+drugbank_id.string+"\tDrugBank Name:"+name.string+"\tDrugBank "+orig_filename)

#find cas_number and check if it was provided then print
		cas_number = drug.find('cas-number')
		if cas_number.string is not None:
			print("DrugBank:"+drugbank_id.string+"\tCasRN:"+cas_number.string+"\tDrugBank "+orig_filename)
	
#find ATC code, check if it was given and print
		atc_code = drug.find("atc-code")
		if atc_code is not None:
			code = atc_code.get("code")
			print("DrugBank:"+drugbank_id.string+"\tATC:"+code+"\tDrugBank "+orig_filename)
		
#find external ids section, then run over all individual external ids and print the resource and identifier
		for ext_ids in drug.find_all("external-identifiers"):
			for ext_id in ext_ids.find_all("external-identifier"):
				if ext_id is not None: #new addition to fix the empty lines?
					resource = ext_id.find("resource").string.strip()
					identifier = ext_id.find("identifier").string.strip()
					print("DrugBank:"+drugbank_id.string+"\t"+resource+":"+identifier+"\tDrugBank "+orig_filename)	

