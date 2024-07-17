# 根据 SQLMAP 盲注日志，恢复数据

# 示例数据：
# 172.21.0.2:80 172.21.0.1 - - [25/Apr/2024:10:14:25 +0000] "GET /cgi-bin/customerdetail.py?name=admin' AND SUBSTR((SELECT COALESCE(username,CHAR(32)) FROM secrets LIMIT 20,1),6,1)>CHAR(96) AND 'jffp'='jffp HTTP/1.1" 200 341 "-" "sqlmap/1.8.4.5#dev (https://sqlmap.org)" "-"

# 有效部分：
# SUBSTR((SELECT COALESCE(username,CHAR(32)) FROM secrets LIMIT 20,1),6,1)>CHAR(96) 

# 整理正则表达式
# 将有效字符串中的变量修改为匹配类型提取
# Tips: 
#   1. python 中，字符串中原本的括号需要使用 \ 进行转义，保留原本意义
#   2. python 中，小括号（非转义）包裹起来的匹配内容，会被返回。如下： (\w+) 意为在此处匹配多个字符，并返回，这里的返回意味着可以用 group(n) 来提取.
#   3. 如下： 
#       第一个 \w+ 提取匹配的字段；
#       第二个 \w+ 提取表名； 
#       第三个 \d 提取第几条记录（\d 意为匹配数字）； 
#       第四个 \d 提取字符位置； 
#       第五个 \d 提取比对的字符 ASCII
import re
from collections import defaultdict

pattern = r'SUBSTR\(\(SELECT COALESCE\((\w+),CHAR\(32\)\) FROM (\w+) LIMIT (\d+),1\),(\d+),1\)>CHAR\((\d+)\)'
regex = re.compile(pattern)

in_file_name = 'access_unquote.log'
out_file_name = 'data.txt'

# 初始化字典存储结果，三个表我初始化两个字典存储吧（因为我感觉第三个表好像貌似没用）
# secrets: id/datetime/passphrase/username
# user_flag: username/flagvalue/id/note/encrypted/flagname/datetime
# customers: city/state/username/contract/address/id/phone/zip

dict_secrets = defaultdict(lambda:{
    "id": defaultdict(int),
    "datetime": defaultdict(int),
    "username": defaultdict(int),
    "passphrase": defaultdict(int)
})

dict_flag = defaultdict(lambda:{
    "id": defaultdict(int),
    "username": defaultdict(int),
    "flagname": defaultdict(int),
    "flagvalue": defaultdict(int),
    "note": defaultdict(int),
    "encrypted": defaultdict(int),
    "datetime": defaultdict(int)
})

with open(in_file_name, 'r') as in_file:
    for line in in_file:
        # 只看正确日志就足够了
        if '200' in line and '341' in line:
            match = regex.search(line)
            if match:
                field = match.group(1)
                table = match.group(2)
                record_number = int(match.group(3))
                position = int(match.group(4))
                char_value = int(match.group(5))
                # 记录字符的最大位置
                if table == "secrets":
                    if dict_secrets[record_number][field][position] < char_value:
                        dict_secrets[record_number][field][position] = char_value
                    
                if table == "user_flag":
                    if dict_flag[record_number][field][position] < char_value:
                        dict_flag[record_number][field][position] = char_value
                    
# 整理要输出的值
def reconstruct_value(dict):
    value = ''
    for i in sorted(dict.keys()):
        # 因为日志是 ">" 比较，所以加1得到实际字符
        value += chr(dict[i] + 1) 
    return value

# 输出到文档保存
def save_to_file():
    with open(out_file_name, 'a') as file:
        for record_number, data in dict_secrets.items():
            id = reconstruct_value(data['id'])
            datetime = reconstruct_value(data['datetime'])
            username = reconstruct_value(data['username'])
            passphrase = reconstruct_value(data['passphrase'])
            
            file.write(f"Record {record_number} - id: {id} - datetime: {datetime} - username: {username} - passphrase: {passphrase} \n")
            
        
        for record_number, data in dict_flag.items():
            id = reconstruct_value(data['id'])
            username = reconstruct_value(data['username'])
            flagname = reconstruct_value(data['flagname'])
            flagvalue = reconstruct_value(data['flagvalue'])
            note = reconstruct_value(data['note'])
            encrypted = reconstruct_value(data['encrypted'])
            datetime = reconstruct_value(data['datetime'])
            
            file.write(f"Record {record_number} - id: {id} - datetime: {datetime} - username: {username} - flagname: {flagname} - flagvalue: {flagvalue} - note: {note} - encrypted: {encrypted} \n")

save_to_file()