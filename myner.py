import itertools

f = open('organisasiprefiks')
organisasi = [w.strip() for w in f.readlines()]
f.close()
f1 = open('preposisilokasi')
lokasi = [w.strip() for w in f1.readlines()]
f1.close()
f2 = open('preposisiperson')
person = [w.strip() for w in f2.readlines()]
f2.close()
f3 = open('date')
datee = [w.strip() for w in f3.readlines()]
f3.close()
f4 = open('suffixperson')
suffixper = [w.strip() for w in f4.readlines()]
f4.close()
f5 = open('suffixorganisasi')
suffixorg = [w.strip() for w in f5.readlines()]
f5.close()
f6 = open('organisasi')
organisasii = [w.strip() for w in f6.readlines()]
f6.close()
f7 = open('predate')
predate = [w.strip() for w in f7.readlines()]
f7.close()
f8 = open('lokasi')
lokasii = [w.strip() for w in f8.readlines()]
f8.close()


class entitas:
	def pilih(self,kalimat): #fungsi untuk menyatukan calon entitas (token dg kelas kata NN/NNP)
		global ner
		temp =[]
		ner = []
		i = 0
		j = 0
		while i < len(kalimat):
			word = kalimat [i][0]
			pos = kalimat [i][1]
			if word in organisasi or word in lokasi or word in person :
				if len(temp) != 0:
					ner.append([(temp, "entitas")])
				else:
					pass
				temp = temp[:0]
				temp.append(kalimat[i])
				ner.append(temp)
				temp = temp[:0]
			elif word in suffixper:
				temp.append(word)
				ner.append([(temp, "suffiksperson")])
				temp = temp[:0]
			elif word in suffixorg:
				if len(temp) != 0:
					ner.append([(temp, "entitas")])
					temp = temp[:0]
					temp.append(word)
					ner.append([(temp, "suffixorg")])
					temp = temp[:0]
				else :
					temp.append(word)
					ner.append([(temp, "suffixorg")])
					temp = temp[:0]
			elif word in datee:
				temp.append(word)
				ner.append([(temp, "tanggal")])
				temp = temp[:0]
			elif pos in ["NNP", "NN"] and word.istitle(): #mengumpulkan kata dg kelas kata NN/NNP berturut2
				if i == (len(kalimat)-1): #menandai kata sebagai calon entitas yaitu kelas kata NN/NNP dan mempunya diawali huruf besar
					temp.append(word)
					ner.append([(temp, "entitas")])
					temp = temp[:0]
				elif i < (len(kalimat)-1): #dikurangin satu biar tidak out of range
					if kalimat[i+1][1] in ["NNP", "NN"] and kalimat[i+1][0].istitle() :
						temp.append(word)
					elif kalimat[i+1][1] in ["NNP", "NN"] and kalimat[i+1][0].isupper() :
						temp.append(word)
					elif kalimat[i+1][1] in ["NNP", "NN"]: #cek kata setelahnya
						temp.append(word)
						ner.append([(temp, "entitas")])
						temp = temp[:0]
					else:
						temp.append(word)
						ner.append([(temp, "entitas")])
						temp = temp[:0]
			elif word.isupper(): #aturna 6 organisasi
				temp.append(word)
				ner.append([(temp, "ORGANIZATION")])
				temp = temp[:0]
			else:
				if len(temp) != 0:
					ner.append(temp)
				else:
					temp.append(kalimat[i])
					ner.append(temp)
				temp = temp[:0]
			i += 1
		ner = itertools.chain(*ner)
		ner = (list(ner))
		while j < len(ner): #menggabungkan beberapa kata yg berkelas kata NN/NNP dalam satu list 
			if isinstance(ner[j][0], list):
				x = " ".join(ner[j][0])
				ner[j] = (x, ner[j][1])
			else:
				pass
			j += 1
		return ner #hasi akhir list of list

	def tanggal(self): #fungsi untuk menentukan tanggal format (2/4)
		global tanggal
		temp =[]
		tanggal = []
		i=0
		j=0
		while i < len(ner):	#menyatukan tanggal format (2/4) dalam satu tuple
			word = ner [i][0]
			pos = ner [i][1]
			if word in datee: #menyatukan hari kedalam satu tuple untuk aturan 3 tanggal
				if i<(len(ner)-1):
					if ner[i+1][1]=="OP" and ner[i+2][1]=="CDP":
						temp.append(word+" ")
					else:
						tanggal.append(ner[i])
				else:
					tanggal.append(ner[i])
			elif word =="(":
				if i < (len(ner)-1): #dikurangin satu biar tidak out of range
					if ner[i+1][1]=="CDP" and ner[i+2][1]=="GM": #cek kata setelahnya apakah format tanggal bukan
						temp.append(word)
					else :
						tanggal.append(ner[i])
				else:
					pass
			elif pos=="CDP" and ner[i-1][0]=="(": 
				if i < (len(ner)-1):
					if ner[i+1][1]=="GM": #klo bukan format tanggal akan dikembalikan spt semula misal (28 tahun)
						temp.append(word)
					else:
						tanggal.append(ner[i])
				else:
					pass
			elif pos=="GM" and ner[i-1][1]=="CDP":
				temp.append(word)
			elif pos=="CDP" and ner[i-1][1]=="GM":
				temp.append(word)
			elif pos=="CP" and ner[i-1][1]=="CDP" and ner[i-2][1]=="GM":
				temp.append(word)		
				tanggal.append((temp, "tanggal")) #aturan 2 tanggal
				temp = temp[:0]
			else:
				if len(temp) != 0:
					tanggal.append((temp, "tanggal"))
					temp=temp[:0]
					tanggal.append(ner[i])
				else:
					tanggal.append(ner[i])
			i+=1
		while j < len(tanggal): #menghilangkan list dalam tuple
			if isinstance(tanggal[j][0], list):
				x = "".join(tanggal[j][0])
				tanggal[j] = (x, tanggal[j][1])
			else:
				pass
			j += 1
		return tanggal

	def tanggall(self):
		global tanggall
		temp =[]
		tanggall = []
		j=0
		k=0
		while k<len(tanggal):
			word = tanggal[k][0]
			pos = tanggal[k][1]
			if pos=="CDP" and tanggal[k-1][1]=="tanggal":
					temp.append(word+" ")
					tanggall.append((temp, "tanggal"))
					temp=temp[:0]
			elif pos=="CDP":
				if k<(len(tanggal)-1):
					if tanggal[k+1][1]=="tanggal":
						temp.append(word+" ")
					else:
						tanggall.append(tanggal[k])
				else:
					tanggall.append(tanggal[k])
			elif pos=="tanggal" and tanggal[k-1][1]=="CDP":
					temp.append(word+" ")
			else:
				if len(temp) != 0:
					tanggall.append((temp, "tanggal"))
					temp=temp[:0]
					tanggall.append(tanggal[k])
				else:
					tanggall.append(tanggal[k])
			k+=1
		while j < len(tanggall): #menghilangkan list dalam tuple
			if isinstance(tanggall[j][0], list):
				x = "".join(tanggall[j][0])
				tanggall[j] = (x, tanggall[j][1])
			else:
				pass
			j += 1
		return tanggall

	def aturan(self):
		global hasil
		hasil=[]
		i=0
		j=0
		while i<len(tanggall): #aturan 1 semua
			word = tanggall[i][0]
			if word in organisasii:
				hasil.append((word, "ORGANIZATION"))
			elif word in lokasii:
				hasil.append((word, "LOCATION"))
			elif tanggall[i-1][0] in organisasi and tanggall[i][1] =="entitas":
				hasil.append((word, "ORGANIZATION"))
			elif tanggall[i-1][0] in lokasi and tanggall[i][1] =="entitas":
				hasil.append((word,"LOCATION"))
			elif tanggall[i-1][0] in person and tanggall[i][1] =="entitas":
				hasil.append((word,"PERSON"))
			elif tanggall[i][1]=="tanggal":
				hasil.append((word,"DATE"))
			elif tanggall[i][1]=="CDP" and tanggall[i-1][0] in predate:
				hasil.append((word,"DATE")) 												#aturan tanggal 6
			else:
				hasil.append((word, tanggall[i][1])) 										#list hasil 'entitas' secara umum sudah dispesifikan
			i+=1
		while j<len(hasil):																	 #aturan 3 semua
			word = hasil[j][0] 																				#buat mengubah 'entitas' yg umum menjadi spesifik melihat dr list hasil
			if hasil[j][1] == "entitas":
				if hasil[j-1][1] == "CC" and hasil[j-2][1] == "ORGANIZATION":
					hasil[j] = (word, "ORGANIZATION")
				elif hasil[j-1][1] == "CC" and hasil[j-2][1] == "LOCATION":
					hasil[j] = (word, "LOCATION")
				elif hasil[j-1][1] == "-" and hasil[j-2][1] == "LOCATION":								#aturan 5 lokasi
					hasil[j] = (word, "LOCATION")
				elif hasil[j-1][1] == "CC" and hasil[j-2][1] == "PERSON":
					hasil[j] = (word, "PERSON")
				 #aturan 2 semua
				elif hasil[j-1][1] == "," and hasil[j-2][1] == "ORGANIZATION": #n09
					hasil[j] = (word, "ORGANIZATION")
				elif hasil[j-1][1] == "," and hasil[j-2][1] == "LOCATION":
					hasil[j] = (word, "LOCATION")
				elif hasil[j-1][1] == "," and hasil[j-2][1] == "PERSON": #n015
					hasil[j] = (word, "PERSON")
					#aturan 4 semua
				elif hasil[j-1][1] == "CC" and hasil[j-2][1] == "," and hasil[j-3][1] == "ORGANIZATION":
					hasil[j] = (word, "ORGANIZATION")
				elif hasil[j-1][1] == "CC" and hasil[j-2][1] == "," and hasil[j-3][1] == "LOCATION":
					hasil[j] = (word, "LOCATION")
				elif hasil[j-1][1] == "CC" and hasil[j-2][1] == "," and hasil[j-3][1] == "PERSON":
					hasil[j] = (word, "PERSON")
				elif hasil[j-1][1] == "JJ" and hasil[j-2][0] in person: #aturan 6 person
					hasil[j] = (word, "PERSON")
				elif hasil[j-1][1] in ["VBT", "VBI"]: #aturan 8 person
					hasil[j] = (word, "PERSON")	
				elif j < (len(hasil)-1):
					if hasil[j+1][1]=="suffiksperson":
						hasil[j] = (word, "PERSON")
					elif hasil[j+1][0]=="," and hasil[j+2][1]=="suffiksperson":
						hasil[j] = (word, "PERSON")
					elif hasil[j][1]=="entitas" and hasil[j+1][1]=="OP":                                      #aturan 7person
						hasil[j] = (word, "PERSON")
					elif hasil[j+1][1]=="suffixorg":
						hasil[j] = (word, "ORGANIZATION") 
					elif hasil[j+1][1] in ["VBT", "VBI"]: #aturan 8 person
						hasil[j] = (word, "PERSON")	
					else:
						pass
			else:
				pass
			j += 1
		return hasil

	def akhir (self): #memberi tag pada entitas sesuai aturan
		global resultt
		resultt = []
		i=0
		while i < len(hasil):
			word = hasil[i][0]
			if hasil[i][1]=="ORGANIZATION":
				resultt.append("&ltORGANIZATION&gt"+word+"&lt/ORGANIZATION&gt")
			elif hasil[i][1]=="LOCATION":
				resultt.append("&ltLOCATION&gt"+word+"&lt/LOCATION&gt")
			elif hasil[i][1]=="PERSON":
				resultt.append("&ltPERSON&gt"+word+"&lt/PERSON&gt")
			elif hasil[i][1]=="DATE":
				resultt.append("&ltDATE&gt"+word+"&lt/DATE&gt")
			else:
				resultt.append(word)
			i+=1
		return " ".join(resultt)


	

















	















