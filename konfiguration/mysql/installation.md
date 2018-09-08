---
title: MySQL-Server unter FreeBSD - Installation
author: Simon Biewald
description: Wie wird der meistgenutzte SQL-Server unter FreeBSD installiert? So einfach geht es!
subject: MySQL, FreeBSD, Installation, MariaDB
date: 2018-09-08T17:00
---

# MySQL-Server unter FreeBSD: Installation

MySQL ist eine der bekanntesten und meistgenutzten SQL-Implementationen überhaupt.
Sei es für Nextcloud oder Wordpress - MySQL muss oder kann benutzt werden.

<blockquote class="note">
    <b>MySQL unter FreeBSD</b>
    <p>
    Dieser Artikel üder erster Teil einer Serie, in der die Grundlagen
    der Installation und Einrichtung des MySQL-Servers unter FreeBSD erklärt werden.<br>
    </p>
    <ol>
        <li><a href="/konfiguration/mysql/installation">Installation</a></li>
        <li><a href="/konfiguration/mysql/fehlersuche">Fehlersuche</a></li>
        <li><a href="/konfiguration/mysql/absicherung">Grundlagen Absicherung</a></li>
    </ol>
</blockquote>

<b>Inhalt</b>

 1. [Installation](#1)
    1. [Installation mit `pkg`](#1.1)
    2. [Installation aus dem Portstree](#1.2)
    3. [Installation aus den Quellen von mysql.com](#1.3)
 2. [Aktivierung in `/etc/rc.conf`](#2)
 3. [Anhang: MariaDB](#3)

<a id="1"></a>
## 1. Installation

MySQL sollte entweder über `pkg` oder aus den Ports installiert werden.
Nur in Ausnahmefällen sollten die Quellen direkt von mysql.com bezogen werden.

Da der MySQL-Server in unterschiedlichen Fassungen vorliegt, sollte sich zu erst überlegt werden,
welche Version zu installieren ist.

<a id="1.1"></a>
### 1.1. Installation mit `pkg`

Zum Zeitpunkt des Verfassens des Artikels stehen folgende Pakete zur verfügung:

 - `mysql55-server`: MySQL 5.5
 - `mysql56-server`: MySQL 5.6
 - `mysql57-server`: MySQL 5.7
 - `mysql80-server`: MySQL 8.0
 - `mysqlwsrep56-server`: MySQL 5.6 mit Galera-Replikation
 - `mysqlwsrep57-server`: MySQL 5.7 mit Galera-Replikation

Während des schreibens des Artikel wurde das Paket von MySQL 8.0 (`mysql80-server`) noch
als Beta gekennzeichnet. Die `mysqlwsrep5*-server`-Pakete wurden zusätzlich um für Cluster erweitert.

Daher kann sich, sollten nicht die neuste Funktionen oder Replikation benötigt werden,
für eine der "normalen" Versionen entschieden werden:

<pre class="command-line language-bash" data-user="root" data-host="freebsd">
<code class="language-bash">pkg install mysql57-server</code></pre>

Automatisch mitinstalliert wird der Kommandozeilen-Client `mysql*-client`, passend
zu der Version des Servers.

<a id="1.2"></a>
### 1.2. Installation aus den Ports

Für die Installation aus den Ports wird GNU-make (`gmake`) vorrausgesetzt.

Zur Zeitpunkt des Artikel waren folgende Ports verfügbar:

 - `databases/mysql55-server`: MySQL 5.5
 - `databases/mysql56-server`: MySQL 5.6
 - `databases/mysql57-server`: MySQL 5.7
 - `databases/mysql80-server`: MySQL 8.0
 - `databases/mysqlwsrep56-server`: MySQL 5.6 mit Galera-Replikation
 - `databases/mysqlwsrep57-server`: MySQL 5.7 mit Galera-Replikation

Nach dem Wechsel in das entsprechende Verzeichnis wird mit

<pre class="command-line language-bash" data-user="root" data-host="freebsd">
<code class="language-bash">make config</code></pre>

die Konfiguration ermöglicht. Dort könne verschiedene "Storage Engines" direkt in
den Server integriert werden - sollten diese nicht angewählt werden, stehen diese
trotzdem zur Verfügung.

Die folgenden Befehlt kompilieren und installieren den MySQL-Server:

<pre class="command-line language-bash" data-user="root" data-host="freebsd">
<code class="language-bash">make
make install</code></pre>

<a id="1.3"></a>
## 1.3. Installation aus den Quellen von mysql.com

Natürlich ist es möglich den SQL-Server auch von dem offiziellen Quellcode zu installieren.
Sinnvoll ist dieses, sollte ein Fehler oder nur eine veraltete im Portstree bzw. bei `pkg`
vorhanden sein.

Bei der manuellen Installation wird der MySQL-Server nicht im Paketsystem registriert.

Hier sei auf die
 [Installationsanleitung auf mysql.com](https://dev.mysql.com/doc/refman/5.7/en/source-installation.html),
verwiesen.

Der FreeBSD-Dienst muss hierbei eventuell selber eingerichtet werden.

<a id="2"></a>
## 2. Aktivierung in `/etc/rc.conf`

Damit MySQL als Dienst überhaupt starten kann, muss dieser zunächst aktiviert werden:

<pre class="command-line language-bash" data-user="root" data-host="freebsd" data-output="2">
<code class="language-bash">sysrc mysql_enable=yes
mysql_enable: yes -> yes</code></pre>

Dabei wird der Eintrag `mysql_enable` in `/etc/rc.conf` auf `yes` gesetzt.

Um zu überprüfen, ob bei der Installation alles glatt lief, wird der Dienst einmal gestartet:

<pre class="command-line language-bash" data-user="root" data-host="freebsd" data-output="2">
<code class="language-bash">service mysql-server start
Starting mysql.</code></pre>

Sollte anschließend `service mysql-server status` folgendes ausgeben, ist die Installation
erfolgreich verlaufen:

<pre class="command-line language-bash" data-user="root" data-host="freebsd" data-output="2">
<code>service mysql-server status
mysql is running as pid 19512.</code></pre>

Sollte stattdessen folgendes dort stehen, ist ein Fehler aufgetreten:

<pre class="command-line language-bash" data-user="root" data-host="freebsd" data-output="2">
<code class="language-bash">service mysql-server status
mysql is not running.</code></pre>

In diesem Fall geht es [weiter mit der Fehlersuche](/konfiguration/mysql/fehlersuche).

<a id="3"></a>
## 3. Anhang: MariaDB

MariaDB ist ein Fork von MySQL: Als solcher ist dieser weitesgehend kompatibel zu MySQL und kann
fast als *drop-in-replacement* verwendet werden.
MariaDB wird jedoch als eigenständige Datenk-Engine weiterentwickelt, sodass etwa
eine Replikation über mehrere Knoten möglich ist.

Grundsätzlich kann die Anleitung auch auf MariaDB übertragen werden. Allerdings gilt zu beachten:

 * Die gleichzeitige Verwendung des MySQL-Servers und des MariaDB-Servers auf dem gleichen System 
   ist meist schwierig oder unmöglich - schon der Paketmanager verbietet dieses in der Regel.
 * MySQL und MariaDB verwenden standardmäßig den gleichen Netzwerkport.
 * Das Datenbankformat der Backends ist unterschiedlich. Sollen unter MySQL erzeugten Datenbanken
   weitergenutzt werden, muss ein SQL-Dump davon erzeugt werden und unter MariaDB wieder
   eingespielt werden. Das gleiche gilt für den Wechsel zurück.
 
 Die Pakete von MariaDB sind in bei `pkg` mit den folgenden Namen zu installieren:
 
 - `mariadb55`
 - `mariadb100`
 - `mariadb101`
 - `mariadb102`
 - `mariadb103`
 
Im Portstree ist MariaDB unter den folgenden Ordnern zu finden:

 - `databases/mariadb55`
 - `databases/mariadb100`
 - `databases/mariadb101`
 - `databases/mariadb102`
 - `databases/mariadb103`
 
Da MariaDB von sich aus die Möglichkeit für Cluster enthält, gibt es keine separaten Pakete.