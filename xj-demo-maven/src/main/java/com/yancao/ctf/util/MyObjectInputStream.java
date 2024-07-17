package com.yancao.ctf.util;

import java.io.*;

public class MyObjectInputStream extends ObjectInputStream {
    public MyObjectInputStream(InputStream in) throws IOException {
        super(in);
    }

    protected Class<?> resolveClass(ObjectStreamClass desc) throws IOException, ClassNotFoundException {
        String className = desc.getName();
        System.out.println( className );
        String[] denyClasses = { "java.net.InetAddress", "org.apache.commons.collections.Transformer", "org.apache.commons.collections.functors", "com.yancao.ctf.bean.URLVisiter", "com.yancao.ctf.bean.URLHelper" };
        for (String denyClass : denyClasses) {
            if (className.startsWith(denyClass))
                throw new InvalidClassException("Unauthorized deserialization attempt", className);
        }
        return super.resolveClass(desc);
    }
}
