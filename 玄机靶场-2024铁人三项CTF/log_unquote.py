import urllib.parse

in_file_name = 'access_access.log'
out_file_name = 'access_unquote.log'

# 打开两个文件： in_file_name 是源日志文件， r 为读取模式
# out_file_name 是过滤完成后的输出文件， a 为写入模式（如果文件不存在则创建）
with open(in_file_name, 'r') as in_file, open(out_file_name, 'a') as out_file:
    for line in in_file:
        try:
            # 对日志行进行 HTML 解码
            decode_line = urllib.parse.unquote(line)
            # 将过滤并解码后的日志写入新文件中
            out_file.write(decode_line)
        except:
            ...