import sqlite3
import os
import random
import base64
from Crypto.Cipher import AES  
from Crypto.Util.Padding import pad, unpad  
import hashlib  

def md5_hash(input_rawstring):  
    # 创建一个md5 hash对象  
    m = hashlib.md5()  
      
    # 更新hash对象  
    m.update(input_rawstring)  
      
    # 获取散列值的16进制字符串表示（32个字节长度）
    hexdigest =  m.hexdigest()
    #将16进制字符串转换为16字节的字节串
    byte_digest = bytes.fromhex(hexdigest)
    return byte_digest
    #return (hex_dig)

def genpassphrase(username,number):
    passphrase = ""
    accvalue = 0
    
    # 这里省略了计算随机数种子的部分代码。其余代码都是okay的。

    random.seed(accvalue)
    total = random.randint(4,7)
    for i in range(total):
        str4bytes = base64.b64encode(os.urandom(3))
        passphrase = passphrase + str4bytes.decode("utf-8")
    
    return passphrase

def genflagstr(username,number):
    flagstr = f"flag{number}" + "{"
    
    accvalue = 0
    # 这里省略了计算随机数种子的部分代码。其余代码都是okay的。
    
    random.seed(accvalue)
    
    total = random.randint(7,15)
    base64str = base64.b64encode(os.urandom(total))

    return base64str

# 迭代次数，增加这个值会提高安全性，但也会降低性能  
iterations = 10000  
  
# 密钥长度（可以是16、24或32字节，对应AES-128、AES-192或AES-256）  
key_length = 16  
  
# 简化版的PBKDF2实现，这里仅使用HMAC-SHA256作为伪随机函数  
def pbkdf2(passphrase, salt, iterations, key_length):  
    h = hashlib.sha256()  
    u = passphrase.encode("utf-8") + salt  
    for _ in range(iterations):  
        h.update(u)  
        u = h.digest()
      
    return h.digest()[:key_length]  

conn = sqlite3.connect('customers.db')
cursor = conn.cursor() 

# 先清除现有数据。
cursor.execute("delete from secrets")
conn.commit()

cursor.execute("delete from user_flag")
conn.commit()

sqlcmd = "SELECT username FROM customers"
cursor.execute(sqlcmd)
rows = cursor.fetchall()
usernames = [row[0] for row in rows]
count = len(usernames)
for username in usernames:
    passphrase = genpassphrase(username, count)

    insertsecretcmd = f"insert into secrets(username,passphrase) values('{username}','{passphrase}')"
    print(insertsecretcmd)
    
    flagname  = f"flag{count}"

    # AES加密用的salt从passphrase派生
    salt = md5_hash(passphrase.encode("utf-8") + b"saltseed")
    # 使用passphrase和salt通过PBKDF2派生密钥
    key = pbkdf2(passphrase, salt, iterations, key_length)
    # 初始化向量也从passphrase派生
    iv =  md5_hash(passphrase.encode("utf-8") + b"IVseed") 

    # 创建Cipher对象
    cipher = AES.new(key, AES.MODE_CBC, iv)  

    # 需要加密的数据
    original_flagdata = genflagstr(username,count)

    # 对数据进行填充，以符合AES的块大小（128位/16字节）
    padded_flagdata = pad(original_flagdata, AES.block_size)  

    # 加密数据 
    encrypted_flagdata = cipher.encrypt(padded_flagdata)

    # 使用相同的salt和passphrase通过PBKDF2派生密钥  
    key_decrypt = pbkdf2(passphrase, salt, iterations, key_length)  
  
    # 创建解密器对象  
    decipher = AES.new(key_decrypt, AES.MODE_CBC, iv)  
  
    # 解密数据  
    decrypted_padded_data = decipher.decrypt(encrypted_flagdata)  
  
    # 去除填充  
    decrypted_flagdata = unpad(decrypted_padded_data, AES.block_size)
    #decrypted_flagdatastr = decrypted_flagdata.decode("utf-8")
    if  original_flagdata == decrypted_flagdata:
        print(f"\r\n   congrutulations: {original_flagdata} matchs {decrypted_flagdata}\r\n")  
    
    flagvalue = base64.b64encode(encrypted_flagdata)
    base64flagdata = flagvalue.decode("utf-8")
    notestr = "encrypted with aes128. associated key, iv & salt are derived from passphrase."
    
    insertuser_flagcmd = f"insert into user_flag(username,flagname,flagvalue,note) values('{username}','{flagname}','{base64flagdata}','{notestr}')"
    print(insertuser_flagcmd)
    print("")
    count = count - 1
    
    cursor.execute(insertsecretcmd)
    cursor.execute(insertuser_flagcmd)
    conn.commit()

cursor.close()
conn.commit()
conn.close()

