import base64
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad


###  这部分代码属于加解密全局变量与工具方法，直接从 initsecretandflagdata.py 文件中复制过来使用 ###
    
# 迭代次数，增加这个值会提高安全性，但也会降低性能  
iterations = 10000  
  
# 密钥长度（可以是16、24或32字节，对应AES-128、AES-192或AES-256）  
key_length = 16  

# md5_hash 算法
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
  
# 简化版的PBKDF2实现，这里仅使用HMAC-SHA256作为伪随机函数  
def pbkdf2(passphrase, salt, iterations, key_length):  
    h = hashlib.sha256()  
    u = passphrase.encode("utf-8") + salt  
    for _ in range(iterations):  
        h.update(u)  
        u = h.digest()
      
    return h.digest()[:key_length]  
   
###  end  ###

# 参考源文件提供的解密思路，整理解密方法
def decrypt_flag(passphrase, base64flagdata):
    try:
        # 对 base64flagdata 进行解码
        encrypted_flagdata = base64.b64decode(base64flagdata)
        
        # 源文件注释中说了，解密使用相同的 salt 和 passphrase 通过 PBKDF2 派生密钥
        # 于是将 salt 和 passphrase 拿过来，并通过 PBKDF2 派生密钥
        salt = md5_hash(passphrase.encode("utf-8") + b"saltseed")
        iv =  md5_hash(passphrase.encode("utf-8") + b"IVseed") 
        # 使用 passphrase 和 salt 通过 PBKDF2 派生密钥
        key = pbkdf2(passphrase, salt, iterations, key_length)
        # 拿到密钥 key 之后，创建解密器，进行 AES_CBC 解密
        decipher = AES.new(key, AES.MODE_CBC, iv)  
        # 解密
        decrypted_padded_data = decipher.decrypt(encrypted_flagdata)  
        # 解密完成后去除填充
        decrypted_flagdata = unpad(decrypted_padded_data, AES.block_size)
        # 返回解密后的数据
        return decrypted_flagdata
        
    except:
        ...
        

# 调用解密方法，解密并按照题目要求拼接 flag
        
flag1 = 'lTr01ZNX8R9xotVanrPtKiBjCfQD5U5dD+KLRPgjnQ4='
passphrase1 = '7xjo0DHFsoF1Jrus'

flag6 = 'PgH8ySWqsB1IJEradvOouNWEP5mpHZnu5e9ShkiS1LWLb81hRUjAZLD4zzzxO5Tn'
passphrase6 = 'TJOC6+L+vTajLOGqfJMweoLFZqvJ'


decrypted_flag1 = decrypt_flag(passphrase1, flag1)
decrypted_flag6 = decrypt_flag(passphrase6, flag6)

print(decrypted_flag1)
print(decrypted_flag6)