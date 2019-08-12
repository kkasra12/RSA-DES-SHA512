padding=lambda num,m_len:"0"*(m_len-len(num))+num
H=[0x6a09e667f3bcc908, 0xbb67ae8584caa73b, 0x3c6ef372fe94f82b, 0xa54ff53a5f1d36f1,
   0x510e527fade682d1, 0x9b05688c2b3e6c1f, 0x1f83d9abfb41bd6b, 0x5be0cd19137e2179]
H=[padding(bin(i)[2:],64) for i in H]
k=[0x428a2f98d728ae22, 0x7137449123ef65cd, 0xb5c0fbcfec4d3b2f, 0xe9b5dba58189dbbc, 0x3956c25bf348b538,
   0x59f111f1b605d019, 0x923f82a4af194f9b, 0xab1c5ed5da6d8118, 0xd807aa98a3030242, 0x12835b0145706fbe,
   0x243185be4ee4b28c, 0x550c7dc3d5ffb4e2, 0x72be5d74f27b896f, 0x80deb1fe3b1696b1, 0x9bdc06a725c71235,
   0xc19bf174cf692694, 0xe49b69c19ef14ad2, 0xefbe4786384f25e3, 0x0fc19dc68b8cd5b5, 0x240ca1cc77ac9c65,
   0x2de92c6f592b0275, 0x4a7484aa6ea6e483, 0x5cb0a9dcbd41fbd4, 0x76f988da831153b5, 0x983e5152ee66dfab,
   0xa831c66d2db43210, 0xb00327c898fb213f, 0xbf597fc7beef0ee4, 0xc6e00bf33da88fc2, 0xd5a79147930aa725,
   0x06ca6351e003826f, 0x142929670a0e6e70, 0x27b70a8546d22ffc, 0x2e1b21385c26c926, 0x4d2c6dfc5ac42aed,
   0x53380d139d95b3df, 0x650a73548baf63de, 0x766a0abb3c77b2a8, 0x81c2c92e47edaee6, 0x92722c851482353b,
   0xa2bfe8a14cf10364, 0xa81a664bbc423001, 0xc24b8b70d0f89791, 0xc76c51a30654be30, 0xd192e819d6ef5218,
   0xd69906245565a910, 0xf40e35855771202a, 0x106aa07032bbd1b8, 0x19a4c116b8d2d0c8, 0x1e376c085141ab53,
   0x2748774cdf8eeb99, 0x34b0bcb5e19b48a8, 0x391c0cb3c5c95a63, 0x4ed8aa4ae3418acb, 0x5b9cca4f7763e373,
   0x682e6ff3d6b2b8a3, 0x748f82ee5defb2fc, 0x78a5636f43172f60, 0x84c87814a1f0ab72, 0x8cc702081a6439ec,
   0x90befffa23631e28, 0xa4506cebde82bde9, 0xbef9a3f7b2c67915, 0xc67178f2e372532b, 0xca273eceea26619c,
   0xd186b8c721c0c207, 0xeada7dd6cde0eb1e, 0xf57d4f7fee6ed178, 0x06f067aa72176fba, 0x0a637dc5a2c898a6,
   0x113f9804bef90dae, 0x1b710b35131c471b, 0x28db77f523047d84, 0x32caab7b40c72493, 0x3c9ebe0a15c9bebc,
   0x431d67c49c100d4c, 0x4cc5d4becb3e42b6, 0x597f299cfc657e2a, 0x5fcb6fab3ad6faec, 0x6c44198c4a475817]
k=[padding(bin(i)[2:],64) for i in k]

def to_ascii(string):
    ans=""
    for char in string:
        tmp=bin(ord(char))[2:]
        tmp="0"*(8-len(tmp))+tmp
        ans+=tmp
    return ans

def rightRotate(num,count):
    while count:
        num=num[-1]+num[:-1]
        count-=1
    return num

XOR=lambda a,b: ''.join(str(int(i)^int(j)) for i,j in zip(a,b))
AND=lambda a,b: ''.join(str(int(i)&int(j)) for i,j in zip(a,b))
OR =lambda a,b: ''.join(str(int(i)|int(j)) for i,j in zip(a,b))
NOT=lambda a: ''.join(str((not int(i))&1) for i in a)

def add(*args):
    for i in args:
        assert len(i)==len(args[0])
    ans=''
    i=len(args[0])
    c=0
    while i:
        i-=1
        c=sum(int(num[i]) for num in args)+c
        ans=str(c%2)+ans
        c>>=1
    return ans

if __name__=="__main__":
    code=input("please enter ur text:")
    #code="kasra"

    code=to_ascii(code)
    code_len=bin(len(code))[2:]
    code+="1"
    if len(code_len)>(1<<128):
        raise Exception("Tooooo Long :[")
    # assert code_len<2**128

    tmp=896-len(code)&0x3ff # tmp=896-len(code)%1024
    if tmp<0:
        code+="0"*(tmp+896)
    else:
        code+="0"*(tmp)
    # assert len(code)%1024==896
    # print(code_len)
    code+="0"*(128-len(code_len))+code_len #128+896=1024
    # assert len(code)==1024
    # code = initialMessage + 1 + 0*(...) + messageLenIn128bit
    tmp=[]
    block_size=1024
    while code:
        tmp+=[code[:block_size]]
        code=code[block_size:]
    word_size=64
    for block in tmp:
        w=[] # the words will store here
        # each word is 64 bit size
        assert len(block)==1024
        # the block must break up into 16 words and goes into w[0] through w[15]
        while block:
            w.append(block[:word_size])
            block=block[word_size:]
        assert len(w)==16 # 1024/64=16
        w_count=80
        for i in range(16,w_count+1): # i : 16,17,18,...,80
            s0=XOR(rightRotate(w[i-15],28),rightRotate(w[i-15],8))
            s0=XOR(s0,rightRotate(w[i-15],7))
            s1=XOR(rightRotate(w[i-2],19),rightRotate(w[i-2],61))
            s1=XOR(s0,rightRotate(w[i-2],6))
            w.append(add(w[i-16],s0,w[i-7],s1))
        a=H[0]
        b=H[1]
        c=H[2]
        d=H[3]
        e=H[4]
        f=H[5]
        g=H[6]
        h=H[7]
        for i in range(w_count):
            s1=XOR(rightRotate(e,14),rightRotate(e,18))
            s1=XOR(s1,rightRotate(e,41))
            ch=XOR(AND(e,f),AND(NOT(e),g))
            #print("_"*10)
            temp1=add(h,s1,ch,k[i],w[i])
            s0=XOR(rightRotate(a,28),rightRotate(a,34))
            s0=XOR(s0,rightRotate(a,39))
            maj=XOR(AND(a,b),AND(a,c))
            maj=XOR(maj,AND(b,c))
            temp2=add(s0,maj)

            h=g
            g=f
            f=e
            e=add(d,temp1)
            d=c
            c=b
            b=a
            a=add(temp1,temp2)
        H[0]=add(H[0],a)
        H[1]=add(H[1],b)
        H[2]=add(H[2],c)
        H[3]=add(H[3],d)
        H[4]=add(H[4],e)
        H[5]=add(H[5],f)
        H[6]=add(H[6],g)
        H[7]=add(H[7],h)
    # print(H)
    code="".join(H)
    print(hex(int(code,base=2)))
