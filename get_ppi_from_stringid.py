#!/usr/bin/env python
#encoding:utf-8

import requests
import sys

con_png_url = 'http://string-db.org/cgi/generate_task_specific_download_file.pl?taskId=%s&download_data_format=highres_image&download_file_name=string_hires_image.png' %str(sys.argv[1])
con_svg_url = 'http://string-db.org/cgi/generate_task_specific_download_file.pl?taskId=%s&download_data_format=svg&download_file_name=string_vector_graphic.svg' %str(sys.argv[1])
interaction_url = 'http://string-db.org/cgi/generate_task_specific_download_file.pl?taskId=%s&download_data_format=tsv&download_file_name=string_interactions.tsv' %str(sys.argv[1])
annotation_url = 'http://string-db.org/cgi/generate_task_specific_download_file.pl?taskId=%s&download_data_format=annotations&download_file_name=string_protein_annotations.tsv' %str(sys.argv[1])

with open('%s.confidence.png' %str(sys.argv[2]),'w') as con_png:
	con_png_link = requests.get(con_png_url)
	con_png.write(con_png_link.content)
	
with open('%s.confidence.svg' %str(sys.argv[2]),'w') as con_svg:
	con_svg_link = requests.get(con_svg_url)
	con_svg.write(con_svg_link.content)
	
with open('%s.interaction.tsv' %str(sys.argv[2]),'w') as interaction:
	interaction_link = requests.get(interaction_url)
	interaction.write(interaction_link.content)

with open('%s.annotation.tsv' %str(sys.argv[2]),'w') as annotation:
	annotation_link = requests.get(annotation_url)
	annotation.write(annotation_link.content)	
