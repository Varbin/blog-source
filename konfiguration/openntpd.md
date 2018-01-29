---
title: OpenNTPD einrichten
author: Simon Biewald
description: OpenNTPD unter FreeBSD und Debian/Ubuntu einrichten.
subject: OpenNTPD, Zeit, Sicherheit
date: 2016-09-18
---

# OpenNTPD einrichten

Um die Systemzeit auf Computersystemen aktuell zu halten wird auf das *Network Time Protocol* (NTP) gesetzt.
Bei vielen Betriebssystemen wird dafür die NTP-Referenz-Implementation (ntpd) verwendet, die jedoch 
[wiederholt][3] [Sicherheitslücken][4] [aufwies][5]. Es sollte daher in betracht gezogen werden ntpd, 
wenn möglich, durch [OpenNTPD][2] zu ersetzen. 

OpenNTPD gehört zum OpenBSD-Projekt und soll folgende Ziele erfüllen:

OpenNTPD soll folgende Ziele erfüllen:

 - Sicherheit
 - Einfachheit in der Bedienung
 - Performance
 
*Quelle:* [OpenNTPD - Design Goals][6]
 
<blockquote class="note">
    Die OpenNTPD erfragte Zeit kann um 50-200ms abweichen, <strong>dieses reicht 
    jedoch für die meisten Anwendungen (z.B. Web-/Mailserver) volkommen aus.</strong>
    Außerdem ignoriert OpenNTPD Schaltsekungen und sollte daher nur zum Empfang von Uhrzeit, und nicht
    als Zeitserver für andere Computer, verwendet werden. Wenn höhere Präzision erforderlich ist, kann 
    <a href="https://chrony.tuxfamily.org/" title="Homepage von Chrony">Chrony</a> 
    eingesetzt werden.
</blockquote>

 [2]: http://www.openntpd.org/ "Seite von OpenNTPD"
 [3]: https://support.ntp.org/bin/view/Main/SecurityNotice#Recent_Vulnerabilities "Offizielle Auflistung"
 [4]: https://www.cvedetails.com/vulnerability-list/vendor_id-2153/NTP.html "Auszug zugewiesener CVEs für ntpd"
 [5]: https://www.heise.de/security/meldung/Kommt-Zeit-kommt-DDoS-Angriff-2087846.html "DDoS über ntpd"
 [6]: https://www.openbsd.org/papers/ntpd_sucon04/mgp00003.html "OpenNTPD - Design Goals"

## Installation

Debian / Ubuntu:

<pre class="command-line language-bash" data-user="root">
<code class="language-bash">apt install openntpd</code>
</pre>

FreeBSD:

<pre class="command-line language-bash" data-user="root">
<code class="language-bash">pkg install openntpd</code>
</pre>

oder

<pre class="command-line language-bash" data-user="root">
<code class="language-bash">cd /usr/ports/net/openntpd
make
make install</code>
</pre>

## Konfiguration von OpenNTPD

OpenNTPD ist bereits grundsätzlich eingerichtet und kann zur Zeitsynchronisation verwendet 
werden. Standardmäßig (FreeBSD) sollte der Serverpool pool.ntp.org eingestellt sein.

Die Konfigurationsdatei ist unter FreeBSD `/usr/local/etc/ntpd.conf` und `/etc/openntpd/ntpd.conf` unter Debian.

Minimalkonfiguration:

<pre class="language-config line-numbers">
<code>servers pool.ntp.org
constraint from "https://freebsd.org"</code></pre>

Beispielkonfiguration:

<pre class="language-config line-numbers">
<code># Als Server 
#listen on 127.0.0.1
#listen on 81.35.21.0

# Als Server auf allen Interfaces
#listen on *

# ggf. nähere Server auswählen (http://www.pool.ntp.org/zone/@)
servers de.pool.ntp.org

# Alternative:
#server 0.de.pool.ntp.org
#server 1.de.pool.ntp.org
#server 2.de.pool.ntp.org
#server 3.de.pool.ntp.org	

# Zeit auch von HTTPS-Servern abrufen (Kontrolle)
constraints from "https://google.com"
constraint from "https://freebsd.org"</code></pre>

Siehe auch: [Offizielle OpenNTPD Dokumentation][7]

 [7]: http://www.openntpd.org/manual.html "OpenNTPD Dokumentation"

### Einzelne Konfigurationsdirektiven

```config
listen on 81.35.21.0
```

**listen on *Adresse*:** Stellt einen NTP-Server auf der IP-Adresse *Adresse* bereit. 
OpenNTPD öffnet standardmäßig keine Ports. *\** ist ein Platzhalter 
für alle Interfaces. Alternativ können dafür auch *0.0.0.0* für IPv4 und *::* 
für IPv6 verwendet werden.

```config
servers de.pool.ntp.org

server 0.de.pool.ntp.org
server 1.de.pool.ntp.org
```

**server(s) *Adresse*:** Legt einen einzelnen Server oder einen Serverpool als Zeitquelle fest.

```config
constraints from "https://google.com"
constraint from "https://freebsd.org"
```

**constraint(s) from *URL*:** Überprüft die von NTP-Servern empfangene Daten durch den "Date"-Header von einem
HTTPS-Server(-pool). Darduch kann eine Manipulation der (meist) nicht abgesicherten NTP-Daten verhindert 
werden. Der Plural bedeutet auch hier wieder einen Pool an Servern.



## Aktivierung von OpenNTPD

Unter Debian/Ubuntu sollte OpenNTPD automatisch aktiviert werden. Unter FreeBSD muss nocht die `/etc/rc.conf` 
geändert werden:

<pre class="language-config line-numbers" data-start="15">
<code># ntpd deaktivieren
ntpd_enable="NO"
# OpenNTPD aktivieren
openntpd_enable="YES"
# Zeit bei Start synchronisieren
openntpd_flags="-s"</code></pre>
