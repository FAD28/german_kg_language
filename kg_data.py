import spacy
import time
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import csv

testdaten = ['Erste Migranten machen sich offenbar von der Türkei Richtung EU-Grenze auf',' In Mugla hätten einige Gummiboote mitgebracht.','Die staatliche Nachrichtenagentur Anadolu berichtete dass sich Migranten in den Städten Izmir Mugla und Canakkale sammelten für die Reise Richtung EU.','Zuvor hatte die türkische Regierung erklärt sie wolle syrische Flüchtlinge auf dem Weg nach Europa nicht mehr aufhalten.','Eskaliert war die Lage nach einem syrischen Luftangriff in Idlib in der Nacht auf Freitag bei dem mindestens 33 türkische Soldaten getötet worden waren.','Die Türkei die in dem Konflikt islamistische Rebellen unterstützt hat dort Beobachtungsposten.']
nlp = spacy.load('de')
def get_relations(data):
	"""
	Die Daten kommen als Liste mit einzelnen Sätzen als Items
	"""
	# Ziel:			Einheiten in einem Satz erkennen und als dict ausgeben
	
	data_dict = {}
	for item in data:
		print("------>",item, "<------")
		doc = nlp(item)

		fieldnames = ['subjekt', 'prädikat', 'objekt']
		with open('data.csv', 'w') as csv_file:
			csv_writer = csv.DictWriter(csv_file, fieldnames = fieldnames)
			csv_writer.writeheader()
		x = 0
		while x < len(data):
			# with open('data.csv','a') as csv_file:
			# 	csv_writer = csv.DictWriter(csv_file, fieldnames = fieldnames)
				subjekt_liste = []
				prädikat_liste = []
				objekt_liste = []
			# 	info = {
			# 		"subjekt": subjekt,
			# 		"prädikat": prädikat,
			# 		"objekt": objekt
			# 	}
				for tok in doc: 

					if tok.pos_ == 'NOUN':
						if tok.dep_.startswith("o") == True:
							# print("Objekt + NOUN:",tok.text)	
							objekt = tok.text+"-"+tok.dep_
							print(objekt)
							objekt_liste.append(tok.text+"-"+tok.dep_)				# <---- Objekt 1
						if tok.dep_.startswith("s") == True:
							# print("Subjekt + NOUN:", tok.text)
							subjekt = tok.text+"-"+tok.dep_
							print(subjekt)
							subjekt_liste.append(tok.text+"-"+tok.dep_)				# <---- Subjekt 1
						if tok.dep_ == "nk":
							# print("Objekt + NOUN (nk):", tok.text)
							objekt = tok.text+"-"+tok.dep_
							print(objekt)
							objekt_liste.append(tok.text+"-"+tok.dep_)					 # <--- Objekt 2
					if tok.pos_ == 'PROPN':
						if tok.dep_.startswith("o") == True:
							# print("Objekt + PROPN:",tok.text)
							objekt = tok.text+"-"+tok.dep_
							print(objekt)
							objekt_liste.append(tok.text+"-"+tok.dep_)					# <--- Objekt 3
						if tok.dep_.startswith("s") == True:
							# print("Subjekt + PROPN:", tok.text)
							subjekt = tok.text+"-"+tok.dep_
							print(subjekt)
							subjekt_liste.append(tok.text+"-"+tok.dep_)				# <---- Subjekt 2
						if tok.dep_ == "pnc":
							# print("Subjekt + PROPN (pnc):", tok.text)
							subjekt = tok.text+"-"+tok.dep_
							print(subjekt)
							subjekt_liste.append(tok.text+"-"+tok.dep_)				# <---- Subjekt 3
						if tok.dep_ == "nk":
							# print("Objekt + PROPN (nk):", tok.text)
							objekt = tok.text+"-"+tok.dep_
							print(objekt)
							objekt_liste.append(tok.text +"-" +tok.dep_)				# <--- Objekt 4
					if tok.pos_ == 'VERB':
						# print("VERB:",tok.text)
						prädikat = tok.text+"-"+tok.dep_
						print(prädikat)
						prädikat_liste.append(tok.text+"-"+tok.dep_)					# <----  Prädikat 1
						if tok.dep_ == 'ROOT':
							# print("VERB+ ROOT:", tok.text)
							prädikat = tok.text+"-"+tok.dep_
							print(prädikat)
							prädikat_liste.append(tok.text+"-"+tok.dep_)			# <----  Prädikat 2

					try:
						Dingsbums = zip(subjekt_liste, objekt_liste)
						print("ZIP: ", list(Dingsbums))
					except:
						print("Geht ned")



				# csv_writer.writerow(info)
					# print(subjekt, prädikat, objekt)
					time.sleep(2)
					x +=1
					print("__________")


		print(len(objekt))
		print(len(subjekt))
		print(len(prädikat))
		data_dict = {'subjekt': subjekt, 'prädikat': prädikat,'objekt':objekt}
		# kg_df = pd.DataFrame({'source':subjekt, 'target':objekt, 'edge':prädikat})
	return data_dict

def show_phrase(data):
	for item in data:
		doc = nlp(item)
		for tok in doc:
			print(tok.text,"------",tok.dep_, "-------",tok.pos_)

def plot_network(data):
	# create a directed-graph from a dataframe
	# G=nx.from_pandas_edgelist(kg_df, "source", "target", 
                          # edge_attr=True, create_using=nx.MultiDiGraph())
	g = nx.DiGraph(data)
	g.add_nodes_from(data.keys())
	for k,v in data.items():
		# print(k, "--", v)

		# print("----...----")
		for t in v:
			if k == 'subjekt':
				print(t, "SUBJEKT")
				try_2 = (t)
			if k == 'prädikat':
				print(t, "PRÄDIKAT")
				try_2 = (t)
			if k == 'objekt':
				print(t, "OBJEKT")	
				try_2 = (t)
		print(try_2)
			# printS(t)
		# test = [(s,o,p) for t in v]
		# print(test)
	# print(data.items())
	# [(k,t) for t in v]
	# for i, item in enumerate(data.values()):
		# print(i)
		# print(item[i])
	for k,v in data.items():
		g.add_edges_from(([(k,t) for t in v]))
	# g.add_edges_from([(subjekt, objekt, prädikat)])
	nx.draw(g,with_labels=True)
	plt.draw()
	plt.show()





data_dict = get_relations(testdaten)
print("____________________________________")
time.sleep(2)
print(data_dict)
print("____________________________________")
# show_phrase(testdaten)
plot_network(data_dict)

