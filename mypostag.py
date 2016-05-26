
from hmmtagger import MainTagger
from tokenization import *
from summary import *



class postagger:
    def post(self, x):
        global result
        mt = MainTagger("resource/Lexicon.trn", "resource/Ngram.trn", 0, 3, 3, 0, 0, False, 0.2, 0, 500.0, 1)
        lines = x.strip().split("\n")
        result = []
        try:
            for l in lines:
                if len(l) == 0: continue
                out = sentence_extraction(cleaning(l))
                for o in out:
                    strtag = " ".join(tokenisasi_kalimat(o)).strip()
                    result += mt.taggingStr1(strtag)
                    
        except:
            return "exception"
        return result
        
        
    









