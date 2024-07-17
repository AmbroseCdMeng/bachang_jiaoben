package com.yancao.ctf.controller;

import com.fasterxml.jackson.databind.node.POJONode;
import com.yancao.ctf.bean.URLHelper;
import com.yancao.ctf.bean.URLVisiter;
import com.yancao.ctf.util.MyObjectInputStream;
import javassist.ClassPool;
import javassist.CtClass;
import javassist.CtMethod;
import org.springframework.web.bind.annotation.*;

import javax.management.BadAttributeValueExpException;
import java.io.*;
import java.lang.reflect.Field;
import java.nio.charset.StandardCharsets;
import java.security.*;
import java.util.Base64;

@RestController
public class IndexController {
    @RequestMapping({"/"})
    public String index() {
        return "Hello World";
    }

    @GetMapping({"/hack"})
    public String hack(@RequestParam String payload)  {

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
            return e.toString();
        }
        return "ok!";
    }

    @RequestMapping({"/file"})
    public String file() throws IOException {
        File file = new File("/tmp/file");
//        File file = new File("D:\\Tools\\file");
        if (!file.exists())
            file.createNewFile();
        FileInputStream fis = new FileInputStream(file);
        byte[] bytes = new byte[1024];
        fis.read(bytes);
        String s = new String(bytes);
        System.out.println(s);
        return s;
    }
}