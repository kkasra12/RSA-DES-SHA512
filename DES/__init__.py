from base64 import b64encode
EB_map=[int(i)-1 for i in open("EB.conf").readline()[:-1].split(" ")] #expantion box
PB_map=[int(i)-1 for i in open("PB.conf").readline()[:-1].split(" ")]
PC1_left=[int(i)-1 for i in open("PC1_left.conf").readline()[:-1].split(" ")]
PC1_right=[int(i)-1 for i in open("PC1_right.conf").readline()[:-1].split(" ")]
PC2=[int(i)-1 for i in open("PC2.conf").readline()[:-1].split(" ")]
placement = lambda vector,__map: [vector[i] for i in __map]
# def placement(vector,__map):
#     return [vector[i] for i in __map]
placement.__doc__=='''converts vector using __map'''
XOR=lambda v0,v1: [i^j for i,j in zip(v0,v1)]
#load SBOX
Sbox=[]
for i in range(1,9):
    Sbox.append([[int(k) for k in j.split(",")] for j in open("S_BOX/S{}.conf".format(i)).read().split("\n")[0:-1]])
def convert_sbox(code,sbox):
    tmp=[int(i) for i in bin(sbox[code[0]*2+code[5]][code[1]*8+code[2]*4+code[3]*2+code[4]])[2:]]
    tmp=[0]*(4-len(tmp))+tmp
    return tmp
def turn_function(code,turn_key):
    t0=XOR(placement(code,EB_map),turn_key)
    t1=[]
    for i in range(8):
        tt=convert_sbox(t0[i*6:i*6+6],Sbox[i])
        t1+=tt

    return placement(t1,PB_map)

def key_generation(main_key):
    if main_key in [0x0101010101010101,0xFEFEFEFEFEFEFEFE,0xE0E0E0E0F1F1F1F1,0x1F1F1F1F0E0E0E0E]:
        print("# WARNING: used key is too weak we recommend to change your key")
    left_part=placement(main_key,PC1_left)
    right_part=placement(main_key,PC1_right)
    for i in range(16):
        if i in [0,1,8,15]:
            left_part.append(left_part.pop(0))
            right_part.append(right_part.pop(0))
        else:
            left_part.append(left_part.pop(0))
            left_part.append(left_part.pop(0))
            right_part.append(right_part.pop(0))
            right_part.append(right_part.pop(0))
        turn_key=placement(left_part+right_part,PC2)
        # print("kg:",turn_key)
        yield turn_key

turn_encrypte=lambda code,turn_key: code[32:]+XOR(code[:32],turn_function(code[32:],turn_key))
turn_decrypte=lambda code,turn_key: XOR(code[32:],turn_function(code[:32],turn_key))+code[:32]

def encrypt(code,main_key):
    for key in key_generation(main_key):
        # print("key",key)
        code=turn_encrypte(code,key)
        # print("=="*50)
    return code

def decrypt(code,main_key):
    key_list=[k for k in key_generation(main_key)]
    for key in key_list[::-1]:
        code=turn_decrypte(code,key)
    return code

def text_encoder(text,key):
    if len(key)!=64:
        raise Exception("key must be 64bit vector")
    for index,val in enumerate(key):
        if val in [0,1]:
            continue
        elif val in ['0','1']:
            key[index]=int(val)
        else:
            raise Exception("index {}th is {} ,which is nor valid".format(index,val))
    ans=[]
    i=0
    tmp=[]
    text+="0"*(8-len(text)%8)
    print(text)
    for c in text:
        print(c)
        t=[int(j) for j in bin(ord(c))[2:]] # converts each char into its binat
        t=[0]*(8-len(t))+t
        tmp+=t
        i+=1
        if i==8:
            if len(tmp)!=64:
                raise Exception("u r somewhere in hell :)")
            tmp=encrypt(tmp,key)
            for i in range(8):
                ans+=chr(int(''.join([str(i) for i in tmp[i:i+8]]),base=2))
            i=0
            tmp=[]
    print(ans)
    ans=b64encode(bytes(''.join(ans),encoding='utf8'))
    return str(ans)[2:-1]

if __name__=="__main__":
    sample_data=2**63+546
    sd=[int(i) for i in bin(sample_data)[2:]]
    #tmp_key=[1,1,0,0,1,0,0,0,0,0,0,1,0,1,1,1,1,0,0,1,1,1,0,0,0,1,0,0,1,0,1,0,0,0,0,1,0,0,0,1,0,0,0,0,1,1,1,0]#48bits
    main_key=13254409010586280507

    mk=[int(i) for i in bin(main_key)[2:]]
    print("len(sd):",len(sd))
    print("len(mk):",len(mk))

    # print(sd)
    # print(EB(sd))
    # print(Sbox)
    # print(convert_sbox([0,1,1,0,0,1],Sbox[0]))
    # print(turn_function(sd[:32],tmp_key))
    # print(turn_function(sd[32:],tmp_key))
    # print("sd:",sd)
    # encripted=turn_encripte(sd,tmp_key)
    # print("encripted:",encripted)
    # decripted=turn_decrypte(encripted,tmp_key)
    # print("decripted:",decripted)
    # print(sd==decripted)
    encrypted=encrypt(sd,mk)
    decrypted=decrypt(encrypted,mk)
    print(decrypted==sd)
    m=input("Enter your text: ")
    print(text_encoder(m,mk))
