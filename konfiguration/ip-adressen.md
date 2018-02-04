---
title: IP-Adressen in Webserverlogs datenschutzgemäß anonymisieren
author: Simon Biewald
description: IP-Adressen sind persönliche Daten - doch können häufig nicht korrekt gespeichert werden. Dieses Problem kann schnell mit einem Skript behoben werden.
subject: IP-Adressem, Anonymität, Webserver, Datenschutz
date: 2018-02-04
---

# IP-Adressen in Webserverlogs datenschutzgemäß anonymisieren

<blockquote class="note">
    Dieser Abschnitt über die gesetzliche Lage ist nur einen Überblick 
    und möglicherweise ungenau. Im Zweifel kontaktieren Sie bitte einen 
    Rechtsanwalt.
</blockquote>

IP-Adressen sind persönliche Daten - als solche sind diese zu schützen und nur bei Notwendigkeit und 
besonderem Interesse zu erheben. Um z.B. für statistische Auswertungen doch 
Logdateien anzulegen zu dürfen, sollten bzw. müssen daher (wenn diese nicht unbedingt 
erforderlich sind) IP-Adressen anonymisert (maskiert) oder ganz entfernt werden.

Unter der Maskierung von IP-Adressen wird das Entfernen eindeutig zuordnebarer
Bestandteile verstanden. Bei IPv4-Adressen sind dies meist die letzten beiden 
Oktetts (`79.133.35.120` → `79.133.x.x`). Bei IPv6-Adresse sollten stattdessen 
[mindestens die letzten 64 bis 80 Bits entfernt werden][0].

 [0]: https://stackoverflow.com/a/6098698
      "Antwort auf Stack Overflow zur Problemstellung: "Anonymizing IPv6 addresses""

## Status quo

Die meisten Webserver legen Logs im [(NCSA) Common log][1] Format an: 

```highlight
{remote} - {user} [{when}] "{method} {uri} {proto}" {status} {size}
```

 - remote: IP-Adresse bzw. Hostname des Clients, z.B. 79.133.35.120
 - user: Nutzername, wenn [HTTP-Authentifizierung][3] verwendet wird, 
   sonst "-" (ohne Anführungszeichen)
 - when: Zeitstempel
 - method: HTTP-Methode, z.B. GET
 - uri: Angefragte <abbr title="Uniform Resource Identifier">URI</abbr>, z.B. /
 - proto: Protokoll der Anfrage, z.B. HTTP/1.1
 - status: [HTTP-Statuscode][4] der Antwort
 - size: Antwortlänge

Einige Webserver ergänzen:

```highlight
"{Referer}" "{User-Agent}
```

 - Referer: Die Webseite, die auf die angefragte Seite führte
 - User-Agent: Der [HTTP-User-Agent-String][5]

So ergibt sich dann Beispielhaft:

```code
79.133.35.120 - - [03/Feb/2018:17:10:35 +0100] "GET / HTTP/1.1" 200 1024 "-" "Mozilla/5.0"
```

Quelle: [http.log - Caddy User Guide][2]

 [1]: https://en.wikipedia.org/wiki/Common_Log_Format "Common Log Format - Wikipedia (Englisch)"
 [2]: https://caddyserver.com/docs/log#log-format "http.log - Caddy User Guide"
 [3]: https://de.wikipedia.org/wiki/HTTP-Authentifizierung "HTTP-Authentifizierung - Wikipedia"
 [4]: https://de.wikipedia.org/wiki/HTTP-Statuscode "HTTP-Statuscode - Wikipedia"
 [5]: https://de.wikipedia.org/wiki/User_Agent#Webbrowser "User Agent - Wikipedia"

Viele Webserver bieten die Option an, dieses Logformat zu ändern - viele Anwendung
zur Auswertung der Logs benötigen allerdings dieses Format. Meist können IP-Adressen 
zwar vollständig (und damit auch datenschutzkonform) enfernt werden - häufig jedoch 
nicht einfach "nur" anonymisiert.

## Lösung

Anstelle, dass der Webserver seine Logs in eine "echte" Datei schreibt, werden diese
in eine [benannten Pipe][10] geleitet und von einem zusätzlichem Skript 
"nachbearbeitet". Die originalen Logdaten werden so nicht gespeichert.

 [10]: https://en.wikipedia.org/wiki/Named_pipe "Named pipe - Wikipedia (Englisch)"

Folgendes Skript liest Daten von `/var/log/access.fifo` und schreibt diese bereinigt
in `/var/log/access.log`:

<pre class="language-python line-numbers">
<code>import os
import ipaddress

from daemonize import Daemonize

UNKNOWN_IP = "0.0.0.0"
MASK_IPV4 = int(os.environ.get("MASK_IPV4", 16))
MASK_IPV6 = int(os.environ.get("MASK_IPV6", 48))


def mask(line):
    ip, rest = line.split(maxsplit=1)
    if "[" in ip: ip = ip.replace("[", "")
    if "]" in ip: ip = ip.replace("]", "")

    try:
        parsed_ip = ipaddress.ip_address(ip)
    except ValueError:
        fixed_ip = UNKNOWN_IP
    else:
        if isinstance(parsed_ip, ipaddress.IPv4Address):
            network_width = MASK_IPV4
        else:
            network_width = MASK_IPV6
        fixed_ip = str(ipaddress.ip_network(
            '{}/{}'.format(ip, network_width), False)[0])

    return ' '.join((fixed_ip, rest))


def main():
    with open("/var/log/access.fifo") as fifo:
        with open("/var/log/access.log") as logfile:
            while True:
                line = fifo.readline()
                logfile.write(mask(line))            


if __name__ == "__main__":
    daemon = Daemonize(app="ipclear", pid="/var/run/ipclear.pid", action=main,
                       foreground="-f" in sys.argv)
    daemon.start()</code></pre>
    
[ipclear.py](ipclear.py); *Die verlinkte Version steht unter 3-Klausel-BSD-Lizenz und 
ist gegebenenfalls neuer.*
    
<blockquote class="note">
    Das Skript hat folgende Abhängigkeit:
    
    <ul>
    <li><a href="https://pypi.python.org/pypi/daemonize">daemonize</a> 
    (pip: <code>daemonize</code>; apt: <code>python3-daemonize</code>; pkg: <code>py36-daemonize-2.4.7</code>; ports: <code>devel/daemonize</code>)</li>
    </ul>
</blockquote>

Angelegt werden kann die Named Pipe mit dem Befehl:

<pre class="command-line language-bash" data-user="root">
<code class="language-bash">mkfifo /var/log/access.fifo</code>
</pre>

Da eine benannte Pipe (fast) wie eine normale Datei behandelt wird, 
sollten die Berechtigungen korrekt gesetzt werden:

<pre class="command-line language-bash" data-user="root">
<code class="language-bash">chown www:www /var/log/access.fifo
chmod 700 /var/log/access.fifo</code></pre>

## Resultat

Aus dem obrigen Beispiel

```code
79.133.35.120 - - [03/Feb/2018:17:10:35 +0100] "GET / HTTP/1.1" 200 1024 "-" "Mozilla/5.0"
```

wird durch das Skript

```code
79.133.0.0 - - [03/Feb/2018:17:10:35 +0100] "GET / HTTP/1.1" 200 1024 "-" "Mozilla/5.0"
```

