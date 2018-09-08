---
title: MySQL unter FreeBSD - Grundlagen Absicherung
author: Simon Biewald
description: Mal eben "kurz" MySQL installiert, doch ist das alles so sicher? Eigentlich ganz einfach.
subject: MySQL, FreeBSD, Sicherheit, MariaDB
date: 2018-09-08T17:00
---

# MySQL unter FreeBSD: Fehlersuche

Mal eben "kurz" MySQL installieren, doch ist das alles so sicher? Eigentlich ganz einfach.

<blockquote class="note">
    <b>MySQL unter FreeBSD</b>
    <p>
    Dieser Artikel ist der dritte Teil einer Serie, in der die Grundlagen
    der Installation und Einrichtung des MySQL-Servers unter FreeBSD erklärt werden.<br>
    </p>
    <ol>
        <li><a href="/konfiguration/mysql/installation">Installation</a></li>
        <li><a href="/konfiguration/mysql/fehlersuche">Fehlersuche</a></li>
        <li><a href="/konfiguration/mysql/absicherung">Grundlagen Absicherung</a></li>
    </ol>
</blockquote>

<b>Inhalt:</b>

 1. [Zugriffsrechte des Datenbankordners](#1)
 2. [Deaktivierung des Fernzugriffs](#2)
    1. [Deaktivierung des Fernzugriffs auf den Datenbank-`root`-Nutzer](#2.1)
 3. [Verbindung zur Datenbank verschlüsseln](#3)
 2. [`mysql_secure_installation`](#2)

<a id="1"></a>
# 1. Zugriffsrechte des Datenbankordners
 
Auch wenn es die Quelle, die richtigien Zugriffsrechte auf den Datenbankordner sich unabdingbar.

Der Datenbankordner - meist `/var/db/mysql` - sollte als Besitzer bzw Gruppe den speziell dafür
angelegten Nutzer bzw. Gruppe `mysql` zugeordnet haben. Niemand anderes sollte darauf Zugriff haben.

Um die richtigen Berechtigungen zu setzen kann als `root` einfach folgendes durchgeführt werden:

<pre class="command-line language-bash" data-user="root" data-host="freebsd">
<code>chown -R mysql:mysql /var/db/mysql
find /var/db/mysql -type d | xargs chmod 700
find /var/db/mysql -type f | xargs chmod 600</code></pre>

<a id="2"></a>
# 2. Deaktivierung des Fernzugriffs

Wenn nicht unbedingt erforderlich, sollte der Fernzugriff auf den MySQL-Server deaktiviert werden.
Bei den meisten Installationen ist dies bereits voreingestellt.

Dazu ist in der `my.cnf` (bei FreeBSD unter `/usr/local/etc/mysql/` zu finden) im Abschnitt 
`mysqld` die `bind-address` auf eine *link-lokale* Adresse zu setzen (z.B. `127.0.0.1` bzw. `::1`).

<pre class="language-config line-numbers" data-start="12">
<code>[mysqld]
user                            = mysql
port                            = 3306
socket                          = /tmp/mysql.sock
bind-address                    = 127.0.0.1</code></pre>

Sollte nun ein Fernzugriff erforderlich sein, kann zum Beispiel eine SSH-Portweiterleitung
oder eine Verbindung mittels VPN-Software verwendet werden. 

Soll der Zugriff über TCP/IP komplett deaktiviert werden (sodass z.B. auch über einen
SSH-Tunnel unmöglich ist), kann die Option `skip-networking` verwendet werden. Der lokale
Zugriff ist dann nur noch über den Unix-Domain-Socket möglich:

<pre class="language-config line-numbers" data-start="12">
<code>[mysqld]
user                            = mysql
socket                          = /tmp/mysql.sock
skip-networking</code></pre>

<a id="2.1"></a>
## 2.1 Deaktivierung des Fernzugriffs auf den Datenbank-`root`-Nutzer

Sollte eine Datenverbindung von außen unbedingt nötig seien, sei hier eine Möglichkeit
präsentiert wie zumindest dem Datenbank-`root`-Nutzer der Fernzugriff verboten wird.

Dazu wird in der MySQL-Shell folgendes ausgeführt:

<pre class="command-line language-sql" data-prompt="root@localhost ([none]) >">
<code>DELETE FROM mysql.user WHERE User='root' AND Host NOT IN ('localhost', '127.0.0.1', '::1');
FLUSH PRIVILEGES;</code></pre>

<a id="3></a>
# 3. Verbindungen verschlüsseln

MySQL unterstützt grundsätzlich verschlüsselte Verbindungen. Besonders dann, wenn über einen
Fernzugriff auf MySQL zugegriffen wird, ist eine Verschlüsselung erforderlich.

Bei den meisten Installationen wird automatisch eine lokale Zertifikatsautorität erzeugt,
sodass die Verbindungen ohne weitere Konfiguration zumindest grundsätzlich gegen passives
Belauschen geschützt ist. Im *Client* kann mit `mysql -h 127.1 -p --ssl-mode=force` lokal
die Verschlüsselung getestet werden. Der Befehl `\s` zeigt dann den aktuellen 
Verschlüsselungsstatus.
Um auch gegen aktives Abhören gesichert zu sein, 
muss die entsprechende Zertifikatsautorität auf den jeweiligen Clients installiert werden.

Sollten bei der Installation des Server die, für die Verschlüsselung benötigten,
Dateien erzeugt worden sein, können diese einfach neu generiert werden:

<pre class="command-line language-bash" data-host="freebsd" data-user="root" data-output="2-16">
<code>mysql_ssl_rsa_setup --datadir /var/db/mysql
Generating a 2048 bit RSA private key
..........+++
.......................................+++
writing new private key to 'ca-key.pem'
-----
Generating a 2048 bit RSA private key
..........+++
...+++
writing new private key to 'server-key.pem'
-----
Generating a 2048 bit RSA private key
.........................................................+++
..+++
writing new private key to 'client-key.pem'
-----
</code></pre>

Ist der Server bereits für Verschlüsselung eingerichtet,
bricht `mysql_ssl_rsa_setup` ohne Fehlermeldung ab.

<a id="4"></a>
# 4. `mysql_secure_installation`

Bei jeder Installation des MySQL-Servers (auch bei MariaDB) liegt das Script 
`mysql_secure_installation` bei. Das interaktive Programm ermöglicht unter anderem:

 - Ändern des Datenbank-`root`-Passworts
 - Verbot der Verwendung des Datenbank-`root`-Nutzers über externe Netzwerkverbindungen
 - Erzwingen von sicheren Passwörtern
 - Entfernern der Testdatenbank und des anonymen Nutzers

<pre class="command-line language-sql" data-user="root" data-host="freebsd" data-output="2-28">
<code>mysql_secure_installation 

Securing the MySQL server deployment.

Enter password for user root: 

VALIDATE PASSWORD PLUGIN can be used to test passwords
and improve security. It checks the strength of password
and allows the users to set only those passwords which are
secure enough. Would you like to setup VALIDATE PASSWORD plugin?

Press y|Y for Yes, any other key for No: y
[...]
Change the password for root ? ((Press y|Y for Yes, any other key for No) : y

New password:
 
Re-enter new password: 
[...]
Remove anonymous users? (Press y|Y for Yes, any other key for No) :  y
[...]
Disallow root login remotely? (Press y|Y for Yes, any other key for No) : y
[...]
Remove test database and access to it? (Press y|Y for Yes, any other key for No) : y
[...]
Reload privilege tables now? (Press y|Y for Yes, any other key for No) : y
[...]
All done!
</code></pre>