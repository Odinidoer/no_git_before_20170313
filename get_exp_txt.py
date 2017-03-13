import pandas as pd
df = pd.read_excel('MJ.xlsx')
columns = [x for x in df.columns if 'Abundance Ratio' in x]

with open('expp.txt','w') as cols:
	cols.write('Accession\t113\t'+'\t'.join(columns)+'\n')
	for i in range(df.shape[0]):
		line = []
		line.append(df['Accession'][i])
		line.append('1')
		for col in range(len(columns)):
			guance = df[columns[col]][i]
			
			line.append(str(df[columns[col]][i]))
		cols.write('\t'.join(line)+'\n')