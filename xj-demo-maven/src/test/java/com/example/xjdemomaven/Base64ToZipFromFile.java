package com.example.xjdemomaven;

import java.io.FileOutputStream;
import java.io.IOException;
import java.util.Base64;

import java.io.BufferedReader;
import java.io.FileReader;

public class Base64ToZipFromFile {

    public static void main(String[] args) {
        // 输入文件路径，包含Base64编码的字符串
        String inputFilePath = "D:\\Home\\玄机\\第七章 常见攻击事件分析 钓鱼邮件\\钓鱼邮件\\file_base64.txt";

        // 输出文件路径
        String outputPath = "output.zip";

        StringBuilder base64EncodedZipBuilder = new StringBuilder();

        // 分块读取文件内容
        try (BufferedReader br = new BufferedReader(new FileReader(inputFilePath))) {
            String line;
            while ((line = br.readLine()) != null) {
                base64EncodedZipBuilder.append(line);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }

        String base64EncodedZip = base64EncodedZipBuilder.toString();

        // 将Base64编码的字符串解码为字节数组
        byte[] decodedBytes = Base64.getDecoder().decode(base64EncodedZip);

        // 将字节数组写入文件
        try (FileOutputStream fos = new FileOutputStream(outputPath)) {
            fos.write(decodedBytes);
            System.out.println("Zip file has been created successfully at: " + outputPath);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
