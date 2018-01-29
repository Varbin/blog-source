---
title: SNTP in Python
author: Simon Biewald
description: Zeit mit Python aus dem Internet abrufen.
subject: Python, SNTP, Zeit
date: 2016-09-18
---


# SNTP in Python

*Zeit mit Python aus dem Internet abrufen!*

- - -

In Python werden eine Reihe Protokolle standardmäßig unterstützt - 
NNTP, SMTP, POP3, HTTP(S), IMAP, Telnet, FTP, SSL/TLS und XML-RPC.
Ein wichtiges Protokoll fehlt jedoch: NTP, ein Protokoll um die Zeit aus 
dem Internet abzurufen. Dieses Modul stellt deswegen die grundsätzliche
Funktion, Zeit aus dem Internet abzurufen, bereit.

<pre class="language-python line-numbers">
<code>import socket, struct
__copyright__ = "Copyright 2016, Simon Biewald"

DELTA = 2208988800
PACKET = b"\x13" + b"\00"*47

def sntp(server="pool.ntp.org", port=123, timeout=5):
    sock = socket.socket(type=socket.SOCK_DGRAM)
    sock.settimeout(timeout)
    sock.sendto(PACKET, (server, port))
    data = struct.unpack(">3Bb11I", sock.recv(48))
    sock.close()
    return data[11] + float(data[12]) / 2**32 - DELTA</code></pre>

[sntp.py](sntp.py); *Die verlinkte Version steht unter 3-Klausel-BSD-Lizenz und 
gegebenenfalls neuer.*

### Beispiel

```python
>>> import sntp
>>> sntp.sntp()
1464350897.2846684
```
