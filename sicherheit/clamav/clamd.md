---
title: Mit Clamd + OpenSSH Virenscans auslagern
author: Simon Biewald
description: Antivirenscans können hohe Belastungen verursachen - mit dem mitgelieferten ClamAV-Daemon diese einfach sicher auslagern.
subject: ClamAV, Clamd, Antivirus, SSH
date: 2018-03-25T20:16
---

# Mit `clamd` + OpenSSH Virenscans auslagern

Mit ClamAV steht ein quelloffener (<abbr title="Free/Libre Open Source Software">FLOSS</abbr>) Virenscanner für die meisten
Betriebssysteme zur Verfügung (z.B. Windows, MacOS, Linux-Distributionen, *BSD, etc.). 
Viele Anwendungen starten jedoch für jeden Scanvorgang einen einzelnen Prozess, 
sodass immer wieder erneut die kompletten Virendefinitionen geladen werden müssen - ist diese ca. 400 - 600 
<abbr title="1 Mebibyte ≙ 1024³ Bytes">MiB</abbr> groß.
Zusätzlich dazu kommen möglicher noch Drittanbieter-Datenbanken,
wie sie etwa [auch diese Webseite anbietet](/sicherheit/clamav/php). 
Bei automatischen, parallelen Scanvorgängen kann es vorkommen, dass die Datenbank mehrfach im RAM liegt und so unnötig viele
Resourcen beansprucht werden, bis schließlich kein Arbeitsspeicher mehr verfügbar ist.
Dafür gibt es den ClamAV-Daemon `clamd` der die Datenbank konstant geladen hält, somit das erneute, langwierige Einlesen vermeidet und
gleichzeitig das mehrfache Vorhandensein der Definitionen im Arbeitsspeicher vermeidet.

Um den Daemon zu benutzen, kann dieser über eine Netzwerkschnittstelle angesprochen werden. 
Der Befehl <code>clam<i>d</i>scan</code> anstelle nutzt diesen Daemon,
im Gegensatz des normalerweise genutzte `clamscan`.

Die Netzwerkschnittstelle ermöglicht auch die Verwendung eines gesonderten Servers,
welcher nur für die Untersuchung von Dateien zuständig ist.

**Inhalt**

 - [Installation von `clamd`](#installation)
 - [Einfacher Remote-Scan](#einfach)
  - [Optimierung und Fehlerbehebung](#optimierung)
 - [Sicherer Remote-Scan über SSH](#ssh)
  - [Einfache Verbindung mit Schlüsseln](#ssh-schlüssel)
 - [Weblinks](#links)
 - [Anhang](#anhang)

<a id="installation">
## Installation von `clamd`
</a>

Unter Debian/Ubuntu können `clamd` und `clamdscan` wie folgt installiert werden:

<pre class="command-line language-bash" data-user="root">
<code class="language-bash">apt install clamav-daemon
apt install clamdscan</code>
</pre>

Die Konfigurationsdatei hat den Pfad `/etc/clamav/clamd.conf`.

<a id="einfach">
## Einfacher Remote-Scan
</a>

In einem einfachen Szenario soll ein Server (`server.domain.tld`) im Netzwerk eine Scanschnittstelle bereitstellen, 
welche aus dem Netzwerk (z.B. von `client.domain.tld`) genutzt wird.

Die folgende Konfiguration (`/etc/clamav/clamd.conf`) ist, sowohl auf dem Server, 
*als auch auf dem Client*, minimal:

<pre class="line-numbers language-">
<code>TcpAddr server.domain.tld
TcpPort 3310</code></pre>

Auf dem Server wird der Dienst gestartet:

<pre class="command-line language-bash" data-user="root" data-host="server.domain.tld">
<code >service clamav-daemon start</code>
</pre>

<small>Neuer Systemd-Befehl: <i>systemctl start clamav-daemon</i></small>

Der Client kann nun mit `clamdscan` Dateien untersuchen (hier der Ordner `/var/www/html`):

<pre class="command-line language-bash" data-user="user" data-host="client.domain.tld">
<code>clamdscan /var/www/html --stream</code>
</pre>

Der Parameter `--stream` kann weggelassen werden, wenn der Server, auf dem `clamd` selber läuft
überprüft wird. Dabei wird der Scan erheblich beschleunigt.

<a id="optimierung">
### Optimierung und Fehlerbehebung
</a>

Sollte `clamdscan` mit dem Fehler `lstat() failed: No such file or directory. ERROR` abbrechen, 
fehlt das Argument `--stream`. Ohne dieses wird das lokale Dateisystem des Servers, von dem
`clamd` bereitgestellt wird, überprüft.

<pre class="command-line language-bash" data-user="user" data-host="client.domain.tld">
<code>clamdscan /var/www/html --stream</code>
</pre>

Zur Beschleunigung des Scans kann das Argument `--multiscan` bzw. `-m` verwendet werden, bei der mehrere Dateien
gleichzeitig überprüft werden:

<pre class="command-line language-bash" data-user="user" data-host="client.domain.tld">
<code>clamdscan /var/www/html --stream --multiscan</code>
</pre>

Die maximale Dateigröße kann in der Konfigurationsdatei mit der Option <code>StreamMaxLength GRÖSSE</code>
festgelegt werden. Zu beachten ist, dass die benötigte Netzwerkbandbreite steigt und eine kurzfristig
höhere Belastung auf dem Scan-Server entsteht. 

<a id="ssh">
## Sicherer Remote-Scan über SSH
</a>

`clamd` überträgt Daten nicht verschlüsselt, sodass ein Angreifer möglicherweise private Daten abhören kann.
Außerdem reicht ein einfacher `SHUTDOWN`-Befehl um den Dienst zu beenden 
(einen Patch [den `SHUTDOWN`-Befehlt zu entfernen befindet sich im Anhang](#anhang)). 
Daher bietet sich die Absicherung über SSH an: Daten werden sicher verschlüsselt und der Zugriff 
ist nur nach vorheriger Authentifizierung möglich.

Dazu wird die Konfiguration entsprechend angepasst:

<pre class="line-numbers language-">
<code>TcpAddr 127.0.0.1
TcpPort 3310</code></pre>

Damit ist der Dienst nicht mehr aus dem Netzwerk erreichbar. Über SSH wird der Port weitergeleitet:

<pre class="command-line language-bash" data-user="user" data-host="client.domain.tld">
<code>ssh -nNT -L 3310:127.0.0.1:3310 nutzer@server.domain.tld</code>
</pre>

<a id="ssh-schlüssel">
### Einfache Verbindung mit Schlüsseln
</a>

SSH unterstützt neben der Anmeldung mit Passwort Public-Key-Authentifizierung, sodass
eine automatische Anmeldung möglich ist.

Auf dem Client wird, wenn nicht bereits vorhanden, ein Schlüsselpaar erzeugt. 
Damit kein Passwort beim (automatischen) Anmeldevorgang eingegeben werden muss, 
wird der private Schlüssel in diesem Fall nicht verschlüsselt.

<pre class="command-line language-bash" data-user="user" data-host="client.domain.tld" data-output="2-9">
<code>ssh-keygen -b 4096 -t rsa
Generating public/private rsa key pair.
Enter file in which to save the key (/home/user/.ssh/id_rsa): 
Enter passphrase (empty for no passphrase): 
Your identification has been saved in /home/user/.ssh/id_rsa.
Your public key has been saved in /home/user/.ssh/id_rsa.pub.
The key fingerprint is:
SHA256:...
The key's randomart image is: ...
</code>
</pre>

<small>Anstelle von `rsa` ist bei modernen System `ed25519` sinnvoll.</small>

Auf dem Server wird aus Sicherheitsgründen ein zusätzlicher Nutzer angelegt:

<pre class="command-line language-bash" data-user="root" data-host="server.domain.tld">
<code>adduser --disabled-password --shell /usr/sbin/nologin --system clamav-ssh</code>
</pre>

Der öffentliche Schlüssel wird nun in die `.ssh/authorized_keys`-Datei des neu angelgten Nutzers auf dem Server kopiert.
Eine SSH-Verbindung sollte nun möglich sein, allerdings sofort wieder beendet werden:

<pre class="command-line language-bash" data-user="user" data-host="client.domain.tld" data-output="2">
<code>ssh clamav-ssh@server.domain.tld
This account is currently not available.
</code>
</pre>

Ein Portweiterleitung erfolgt nun mit dem folgendem Befehl:

<pre class="command-line language-bash" data-user="user" data-host="client.domain.tld" data-output="2">
<code>ssh -nNT -L 3310:127.0.0.1:3310 clamav-ssh@server.domain.tld</code>
</pre>

Nun kann in einer anderen Sitzung `clamdscan` eingesetzt werden.
Nicht zu vergessen ist der Parameter `--stream`,
damit auch wirklich Daten über das Netzwerk übetragenwerden: 

<pre class="command-line language-bash" data-user="user" data-host="client.domain.tld" data-output="2">
<code>clamdscan --stream /var/www/html</code>
</pre>

<a id="links">
## Weblinks
</a>

Hilfeseiten (`manpages`):

 - [`ssh-keygen(1)`](https://manpages.debian.org/stretch/openssh-client/ssh-keygen.1.en.html "ssh-keygen — authentication key generation, management and conversion")
 - [`clamd.conf(5)`](https://manpages.debian.org/stretch/clamav-daemon/clamd.conf.85en.html "clamd.conf - Configuration file for Clam AntiVirus Daemon ")
 - [`clamd(8)`](https://manpages.debian.org/stretch/clamav-daemon/clamd.8.en.html "clamd - an anti-virus daemon")

<a id="anhang">
## Anhang
</a>

Patch zur Deaktivierung des `SHUTDOWN`-Befehls in `clamd`:

<pre class="line-numbers language-diff">
<code>--- a/clamd/session.c
+++ b/clamd/session.c
@@ -562,11 +562,13 @@ int execute_or_dispatch_command(client_conn_t *conn, enum commands cmd, const ch
     }
 
     switch (cmd) {
+    /* disable SHUTDOWN *
        case COMMAND_SHUTDOWN:
            pthread_mutex_lock(&exit_mutex);
            progexit = 1;
            pthread_mutex_unlock(&exit_mutex);
            return 1;
+       */
        case COMMAND_RELOAD:
            pthread_mutex_lock(&reload_mutex);
            reload = 1;</code></pre>

[clamd-patch.diff](clamd-patch.diff)
