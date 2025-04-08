def char_to_uni(a):
    z = ord(a) - 13
    if z < 65:
        y = 64 - z
        z = 90 - y
    x = chr(z)
    return x
    
def rot13_crypt(secretkey):
    res = "\nDeine geheime Botschaft:\n"
    for i in secretkey: 
        res += char_to_uni(i)    
    print(res)
        
secret = input("Gib hier deinen zu Text zum Ver/Entschlüsseln ein\n>>> Bitte nur in GROßBUCHSTABEN <<<\n")
rot13_crypt(secret)
 
 
 

    


    
 