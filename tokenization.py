import re

DELIMITERS = '/""\',()?!:;&<>='
INDEL = '/""\',():;&<>=' #tanda baca tanya dan seru gabung dengan kata yang mengikuti jd ga perlu dipisah
sentenceMatcher = re.compile(r"(?<!\..)([\?\!\.]+)\s(?!.\.)")
refMatcher = re.compile(r"(\[)\d+(\])")

def isabbrev(s): #tanda titik bukan sebagai akhir kalimat (sebagai nama singkatan)
    abbrev = ['H', 'Hj', 'Ir', 'Jend', 'Purn', 'Prof', 'rer', 'nat', 'Brig', 'Ny', 'Nn', 'Drs', 'Dra', 'dr', 'Dr']
    last = s[:s.find('.')]
    return (last in abbrev) or ((len(last)<3) and (last == last.upper()))
    
def cek_inner_delimiter(buf): #memisahkan delimiter dari kata yang mengikuti daftar delimiter ada di INDEL (hal ini dilakukan buat pengenalan kelas kata)
    if len(buf)>1:
        out = []
        for cdel in INDEL:
            if cdel in buf:
                buf = buf.replace(cdel, " "+cdel+" ")
        if " " in buf:
            return buf.split(" ")
        else:
            return [buf]
    else:
        return [buf]
    
def tokenisasi_kalimat(line):
    out = []
    tok = line.split(" ")                                       #split kalimat menjadi list kata
    for t in tok:
        buf = t                                                     #per kata dari list tok
        i = 0
        while i<len(buf) and buf[i] in DELIMITERS:                      #cek huruf dari tiap kata
            out += [buf[i]]                                             #buat gabung titik/delimiters dengan kata sebelumnya
            i += 1
        if i < len(t):
            buf = buf[i:]                                                   #dari i sampai akhir
        i = -1
        akhir = []
        while i>=-len(buf) and buf[i] in DELIMITERS:
            akhir += [buf[i]]
            i -= 1
        if -i <= len(buf):
            buf = buf[:len(buf)+i+1]
        akhir.reverse()
        out = out + cek_inner_delimiter(buf) + akhir                                    #menggabungkan semua kata dalam satu kalimat
    if len(out[-1])>1:                                          #untuk kata terakhir dari kalimat
        buf = out[-1]
        i = -1
        akhir = []
        while i>=-len(buf) and buf[i] in DELIMITERS+'.':                        #tanda titik sebagai akhir kalimat berita
            akhir += [buf[i]]
            i -= 1
        if -i <= len(buf):
            buf = buf[:len(buf)+i+1]
        if i < -1:
            out[-1] = buf
            akhir.reverse()
            out += akhir
    return out
    
def sentence_extraction(line):                                                  #untuk memisahkan antar kalimat (misal dalam satu paragraf)
    out = []
    sent = sentenceMatcher.split(line)
    tmp = ''
    pre = []
    for l in sent:
        s = l.strip()
        if len(s)==0: continue
        tmp += s.strip()
        if (s[-1] in "?!.") or (len(s)==1 and s[0] in "?!."):
            pre += [tmp]                                                             #untuk menggabung dengan token ?!. dg token sebelumnya misal kabar?kamu.
            tmp = ''
    if len(tmp)>0:
        pre += [tmp]
        tmp = ''
    for s in pre:
        tmp += s.strip()
        if not isabbrev(s[s.rfind(' ')+1:]):
            out += [tmp]  
            tmp = ''
        else:
            tmp += ' '
    if len(tmp)>0:
        out += [tmp]
        tmp = ''
    return out
    
def cleaning(line): #untuk menghilangkan semua digit dlm kurung siku kyk buat kutipan ex: [2]
    return refMatcher.sub("", line.strip())
    
if __name__=='__main__':
    l = 'response.content_type . acdef . '
    out = sentence_extraction(cleaning(l))
    for o in out:
        print " ".join(tokenisasi_kalimat(o))