# coding: utf-8
#from Bulk_Generate_Heisig.py import translateToHeisig


def translateToHeisig(text, heisigLookupFunction, heisigFormatString=u"{0}"):
    result = u""
    for c in text:
        value = heisigLookupFunction(c)
        if value != None:
            result += heisigFormatString.format(value)
        else:
            result += c
    return result


############################
# tests
############################

def hf(char):
    data = {'神': 'God', '六': 'Six', '千': 'Thousand'};
    return data.get(char, None)

def test_hfmock():
    assert hf("2") == None
    assert hf("六") == 'Six'

def test_translatePassThrough():
    assert translateToHeisig("",hf) == "" 
    assert translateToHeisig("123",hf) == "123" 
    assert translateToHeisig(u"百三十使Aた。",hf) == "百三十使Aた。" 
    
def test_translateKnownHeisigKanji():
    assert translateToHeisig("神",hf) == "God" 
    assert translateToHeisig("神六",hf) == "GodSix" 

def test_translateKanjiWithFormat():
    assert translateToHeisig("神六",hf,"<{0}>") == "<God><Six>" 

def test_translateMixedHeisigKanji():
    assert translateToHeisig(u"百六三十使A神た。",hf, "<{0}>") == "百<Six>三十使A<God>た。" 



