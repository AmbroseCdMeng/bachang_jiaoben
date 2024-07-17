package com.yancao.ctf.bean;

import java.io.File;
import java.io.FileOutputStream;
import java.io.ObjectInputStream;
import java.io.Serializable;

public class URLHelper implements Serializable {
    public String url;

    public URLVisiter visiter = null;

    private static final long serialVersionUID = 1L;

    public URLHelper(String url) {
        this.url = url;
    }

    private void readObject(ObjectInputStream in) throws Exception {
        System.out.println("URLHelper running");
        // 查看堆栈信息
        // new Exception("Stack trace").printStackTrace();
        in.defaultReadObject();
        if (this.visiter != null) {
            String result = this.visiter.visitUrl(this.url);
            File file = new File("/tmp/file");
            // windows 环境用来测试，测完记得改回去
//            File file = new File("D:\\Tools\\file");
            if (!file.exists())
                file.createNewFile();
            FileOutputStream fos = new FileOutputStream(file);
            fos.write(result.getBytes());
            fos.close();
        }
    }
}
