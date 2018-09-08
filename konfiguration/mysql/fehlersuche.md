---
title: MySQL unter FreeBSD - Fehlersuche
author: Simon Biewald
description: Mal eben "kurz" MySQL installieren, doch es funktioniert nicht? Einige Ansätze für Problemlösungen.
subject: MySQL, FreeBSD, Fehlersuche, MariaDB
date: 2018-09-08T17:00
---


# MySQL unter FreeBSD: Fehlersuche

Mal eben "kurz" MySQL installieren, doch es funktioniert nicht?
Einige Ansätze für Problemlösungen, besonders für Probleme direkt nach der Installation

<blockquote class="note">
    <b>MySQL unter FreeBSD</b>
    <p>
    Dieser Artikel ist der zweiter Teil einer Serie, in der die Grundlagen
    der Installation und Einrichtung des MySQL-Servers unter FreeBSD erklärt werden.<br>
    </p>
    <ol>
        <li><a href="/konfiguration/mysql/installation">Installation</a></li>
        <li><a href="/konfiguration/mysql/fehlersuche">Fehlersuche</a></li>
        <li><a href="/konfiguration/mysql/absicherung">Grundlagen Absicherung</a></li>
    </ol>
</blockquote>

<b>Inhalt:</b>

 1. [Übliche Fehlerursachen](#1)
    1. [Datenbankordner existiert nicht](#1.1)
    2. [Berechtigungen](#1.2)
 2. [Analyse der Log-Datei](#2)

<a id="1"></a>
## 1. Übliche Fehlerursachen

`/var/db/mysql` ist der Standardort für MySQL, dieser kann allerdings in der Datei
`/usr/local/etc/my.cnf` bzw. `/usr/local/etc/mysql/my.cnf` angepasst werden. 
Der Autor des Artikels geht von einem nicht geändertem Pfad aus, 
sollten Sie einen  anderen gesetzt haben verwendet Sie natürlich Ihren
im weiteren Artikelverlauf.

<a id="1.1"></a>
### 1.1 Datenbankordner existiert nicht

Sollte der Datenbankordner nicht existieren, initialisieren Sie einfach
eine neue Datenbank:

<pre class="command-line language-bash" data-user="root" data-host="freebsd" data-output="2-14">
<code class="language-bash">/usr/local/libexec/mysqld --initialize --user=mysql --basedir=/usr/local --datadir=/var/db/mysql
 100
 100 200
 100 200
2018-09-01T10:45:51.410350Z 0 [Warning] InnoDB: New log files created, LSN=45790
 100
2018-09-01T10:45:51.907105Z 0 [Warning] InnoDB: Creating foreign key constraint system tables.
mysqld: Error on delete of './auto.cnf' (Errcode: 2 - No such file or directory)
2018-09-01T10:45:52.084840Z 0 [Warning] World-writable config file './auto.cnf' has been removed.

2018-09-01T10:45:52.085079Z 0 [Warning] No existing UUID has been found, so we assume that this is the first time that this server has been started. Generating a new UUID: 32266a46-add4-11e8-a240-00163cc60565.
2018-09-01T10:45:52.102795Z 0 [Warning] Gtid table is not ready to be used. Table 'mysql.gtid_executed' cannot be opened.
2018-09-01T10:45:53.057749Z 0 [Warning] CA certificate ca.pem is self signed.
2018-09-01T10:45:53.149448Z 1 [Note] A temporary password is generated for root@localhost: ************</code></pre>

Zu beachten: Hierbei wird eine neues Passwort für das Datenbankkonto "root" vergeben.

Anschließend sollte überprüft werden ob der MySQL-Server nun started.

<a id="1.2"></a>
### 1.2 Berechtigungen

Es ist zu prüfen, ob der `mysql`-Nutzer überhaupt Zugriff auf das Datenbankverzeichnis hat:

<pre class="command-line language-bash" data-user="root" data-host="freebsd" data-output="2-27">
<code class="language-bash">ls -la /var/db/mysql
drwxr-x---   5 mysql  mysql         26  1 Sep. 13:24 .
drwxr-xr-x  17 root   wheel         25  1 Sep. 12:45 ..
-rw-r-----   1 mysql  mysql         56  1 Sep. 12:45 auto.cnf
-rw-------   1 mysql  mysql       1676  1 Sep. 12:45 ca-key.pem
-rw-r--r--   1 mysql  mysql       1112  1 Sep. 12:45 ca.pem
-rw-r--r--   1 mysql  mysql       1112  1 Sep. 12:45 client-cert.pem
-rw-------   1 mysql  mysql       1680  1 Sep. 12:45 client-key.pem
-rw-r-----   1 mysql  mysql        327  1 Sep. 13:24 ib_buffer_pool
-rw-r-----   1 mysql  mysql  268435456  1 Sep. 13:24 ib_logfile0
-rw-r-----   1 mysql  mysql  268435456  1 Sep. 12:45 ib_logfile1
-rw-r-----   1 mysql  mysql  134217728  1 Sep. 13:24 ibdata1
-rw-r-----   1 mysql  mysql  134217728  1 Sep. 13:24 ibtmp1
drwxr-x---   2 mysql  mysql         77  1 Sep. 12:45 mysql
-rw-r-----   1 mysql  mysql        177  1 Sep. 12:46 mysql-bin.000001
-rw-r-----   1 mysql  mysql        177  1 Sep. 13:24 mysql-bin.000002
-rw-r-----   1 mysql  mysql        710  1 Sep. 13:30 mysql-bin.000003
-rw-r-----   1 mysql  mysql         57  1 Sep. 13:24 mysql-bin.index
drwxr-x---   2 mysql  mysql         90  1 Sep. 12:45 performance_schema
-rw-------   1 mysql  mysql       1680  1 Sep. 12:45 private_key.pem
-rw-r--r--   1 mysql  mysql        452  1 Sep. 12:45 public_key.pem
-rw-r--r--   1 mysql  mysql       1112  1 Sep. 12:45 server-cert.pem
-rw-------   1 mysql  mysql       1676  1 Sep. 12:45 server-key.pem
drwxr-x---   2 mysql  mysql        108  1 Sep. 12:46 sys
-rw-r-----   1 mysql  mysql        519  1 Sep. 12:46 freebsd-slow.log
-rw-r-----   1 mysql  mysql      10742  1 Sep. 12:46 freebsd.log
-rw-r-----   1 mysql  mysql          9  1 Sep. 12:46 freebsd.pid</code></pre>

In der ersten Spalte stehen die Berechtigung, in der dritten und vierten Spalte benutzer und Gruppen
und zum Schluss der Dateiname. Hier ist alles in Ordnung: Der MySQL-Nutzer ist
dem Ordner selber (`/var/db/mysql`, angezeigt als `.`) und den Dateien zugeordnet und hat
Lese- und Schreibzugriff (Spalte beginnent mit `-rw-`, `-rwx` oder `drwx`).

Sollte dieses nicht der Fall sein,
können die Berechtigungen einfach wiederhergestellt werden:

<pre class="command-line language-bash" data-user="root" data-host="freebsd">
<code class="language-bash">chown -R mysql:mysql /var/db/mysql
chmod -R u+rw /var/db/mysql</code></pre>

<a id="2"></a>
## 2. Log-Dateien auswerten

Standardmäßig schreibt MySQL Logs nach `/var/db/mysql/$HOST.err`, dabei steht`$HOST` für den Hostname des Servers.

Besonders für weitergehende Probleme ist das Logfile von großer Bedeutung.

Es folgen einige Fehlermeldungen und -ursachen.

<a id="2.1"></a>
### 2.1 "Table 'mysql.user' does not exist"

**Symptome**:

<pre class="language-code">
<code class="language-code">2018-09-01T12:04:23.640875Z 0 [ERROR] Fatal error: Can't open and lock privilege tables: Table 'mysql.user' doesn't exist
2018-09-01T12:04:23.641234Z 0 [ERROR] Fatal error: Failed to initialize ACL/grant/time zones structures or failed to remove temporary table files.
2018-09-01T12:04:23.641617Z 0 [ERROR] Aborting
</code></pre>

**Ursachen**:

Bei der Erzeugung der Datenbank ist ein Fehler unterlaufen und die interne MySQL-Nutzerdatenbank ist nicht vorhanden.

**Lösung**:

<blockquote>Wichtig: Vor dem Löschen unbedingt auf den korrekten Pfad achten!</blockquote>

Initialisieren Sie die Datenbank neu. Dafür wird zunächst das Datenbankverzeichnis gelöscht und anschließend neu initialisiert:

<pre class="command-line language-bash" data-user="root" data-host="freebsd" data-output="3-15">
<code class="language-bash">rm -r /var/db/mysql
/usr/local/libexec/mysqld --initialize --user=mysql --basedir=/usr/local --datadir=/var/db/mysql
 100
 100 200
 100 200
2018-09-01T10:45:51.410350Z 0 [Warning] InnoDB: New log files created, LSN=45790
 100
2018-09-01T10:45:51.907105Z 0 [Warning] InnoDB: Creating foreign key constraint system tables.
mysqld: Error on delete of './auto.cnf' (Errcode: 2 - No such file or directory)
2018-09-01T10:45:52.084840Z 0 [Warning] World-writable config file './auto.cnf' has been removed.

2018-09-01T10:45:52.085079Z 0 [Warning] No existing UUID has been found, so we assume that this is the first time that this server has been started. Generating a new UUID: 32266a46-add4-11e8-a240-00163cc60565.
2018-09-01T10:45:52.102795Z 0 [Warning] Gtid table is not ready to be used. Table 'mysql.gtid_executed' cannot be opened.
2018-09-01T10:45:53.057749Z 0 [Warning] CA certificate ca.pem is self signed.
2018-09-01T10:45:53.149448Z 1 [Note] A temporary password is generated for root@localhost: ************</code></pre>

Zu beachten: Hierbei wird ein neues Passwort für das Datenbankkonto "root" vergeben.

<a id="2.2"></a>
### "Can't find file: ... (errno 13 - Persmission denied)"

**Symptome**:

<pre class="language-code">
<code class="language-code">2018-09-01T10:21:49.245373Z 0 [ERROR] /usr/local/libexec/mysqld: Can't find file: './mysql/user.frm' (errno: 13 - Permission denied)
2018-09-01T10:21:49.245767Z 0 [ERROR] Fatal error: Can't open and lock privilege tables: Can't find file: './mysql/user.frm' (errno: 13 - Permission denied)
2018-09-01T10:21:49.246057Z 0 [ERROR] Fatal error: Failed to initialize ACL/grant/time zones structures or failed to remove temporary table files.
2018-09-01T10:21:49.247191Z 0 [ERROR] Aborting
</code></pre>

**Problem**:

MySQL darf nicht auf die Daten zugreifen, die Berechtigungen könnten falsch gesetzt sein.

**Lösung**:

Überprüfen Sie die Berechtigungen und stellen Sie diese im Zweifel wieder her (s. [1.1 Berechtigungen](#1.1)").
