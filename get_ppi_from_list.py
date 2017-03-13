#!/usr/bin/env python
#encoding:utf-8

import requests
import sys

def get_id(listname,org):
	pass
#cookies header payload 	
url = 'http://string-db.org'
files = {'file': open('payload.txt', 'rb')}
r = requests.post(url, files=files)
r.text
with open('hehe.txt','w')as heh:
	heh.write(r.text)
	ppiid = re.findall(r'task_id: \'(.*?)\',',r.text)[1]
需要在选择一次continue	
	
	return ppiid

def get_result(ppiid,listname):
	ppiid = str(ppiid)
	listid = str(listname).split('\.DE\.list')[0]
	con_png_url = 'http://string-db.org/cgi/generate_task_specific_download_file.pl?taskId=%s&download_data_format=highres_image&download_file_name=string_hires_image.png' %ppiid
	con_svg_url = 'http://string-db.org/cgi/generate_task_specific_download_file.pl?taskId=%s&download_data_format=svg&download_file_name=string_vector_graphic.svg' %ppiid
	interaction_url = 'http://string-db.org/cgi/generate_task_specific_download_file.pl?taskId=%s&download_data_format=tsv&download_file_name=string_interactions.tsv' %ppiid
	annotation_url = 'http://string-db.org/cgi/generate_task_specific_download_file.pl?taskId=%s&download_data_format=annotations&download_file_name=string_protein_annotations.tsv' %ppiid

	with open('%s.confidence.png' %listid,'w') as con_png:
		con_png_link = requests.get(con_png_url)
		con_png.write(con_png_link.content)
		
	with open('%s.confidence.svg' %listid,'w') as con_svg:
		con_svg_link = requests.get(con_svg_url)
		con_svg.write(con_svg_link.content)
		
	with open('%s.interaction.tsv' %listid,'w') as interaction:
		interaction_link = requests.get(interaction_url)
		interaction.write(interaction_link.content)

	with open('%s.annotation.tsv' %listid,'w') as annotation:
		annotation_link = requests.get(annotation_url)
		annotation.write(annotation_link.content)	


def adj_result():
	pass
	
if __name__ == '__main__':
	ppi_id = get_id(listname)
	get_result(ppiid,listname)
	adj_result(listname)