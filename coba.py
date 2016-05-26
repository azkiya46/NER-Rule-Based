from mypostag import postagger
from myner import *



a = postagger() 
b= entitas()      
contohf = "Golci Maneha, S.H."
contoh= "jelas Fischer"
D= a.post(contoh)
E = b.pilih(D)
C = b.tanggal()
H = b.tanggall()
F = b.aturan()
G = b.akhir()
print D
print 1
print E
print "oaofp"
print C
print 2
print "tanggall"
print H
print 4
print F
print "AKHIR"
print G



