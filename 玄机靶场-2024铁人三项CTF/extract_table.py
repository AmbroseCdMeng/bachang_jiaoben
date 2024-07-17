# 提取日志中的表名字段名

import re
from collections import defaultdict


# 示例数据：
# 172.21.0.2:80 172.21.0.1 - - [25/Apr/2024:10:14:25 +0000] "GET /cgi-bin/customerdetail.py?name=admin' AND SUBSTR((SELECT COALESCE(username,CHAR(32)) FROM secrets LIMIT 20,1),6,1)>CHAR(96) AND 'jffp'='jffp HTTP/1.1" 200 341 "-" "sqlmap/1.8.4.5#dev (https://sqlmap.org)" "-"

# 有效部分：
# SELECT COALESCE(username,CHAR(32)) FROM secrets LIMIT

# 正则表达式提取列名、表名
pattern = r'SELECT COALESCE\((\w+),CHAR\(32\)\) FROM (\w+) LIMIT'

# 定义字典存储
result = defaultdict(set)

regex = re.compile(pattern)

with open('access_filter.log', 'r') as file:
    for line in file:
        # 正则匹配
        match = regex.search(line)
        if match:
            column_name = match.group(1)
            table_name = match.group(2)
            # print(f'Table: {table_name}, Column:{column_name}')
            result[table_name].add(column_name)
            
# 输出结果
for table, column in result.items():
    columns = '/'.join(column)
    print(f"{table}: {columns}")