---
title: Zusätzliche ClamAV-Signaturen zur Erkennung von PHP-Backdoors
author: Simon Biewald
description: Die Erkennungsrate von ClamAV bei PHP-Backdoors kann zusätzlich mit Datenbanken verbessert werden.
subject: ClamAV, Sicherheit, PHP
date: 2018-03-18T20:30
---

# Zusätzliche ClamAV-Signaturen zur Erkennung von PHP-Backdoors

Die Erkennungsrate von ClamAV bie PHP-Backdoors kann zusätzlich mit Datenbanken verbessert werden.

Die händisch erstellte Signaturdatenbank enthält Signaturen für folgende Schadprogramme:

 - PHP-Backdoors: Azrail, CasuS, Cybershell, KAdot, Lolipop, lostpassworddc, Spammailer, MyShell, NShell, s72, Ant(Sword), b374k
 - Exploits: Umgehungsversuche des PHP-Safemodes
 - Weitere Backdoors: Gamma Webshell (Perl) sowie eine CGI-Backdoor in Python
 
Außerdem ist eine einfache Heuristik zur Erkennung von PHP-Backdoors mit dabei, 
die erkennt ob `$_`-Variablen (`$_GET`, `$_POST`, `$_REQUEST`) als Argument für 
`eval` / `system` / `passthru` / `exec` / `popen` / `proc_open` verwendet werden.
Eine Extra Datei für häufig verwendete Verschleierungstaktiken ist ebenfalls vorhanden.

## Download

**Auszug sbiewald-php.ndb**

```python
# Heuristik
PHP.Webshell.Generic:0:*:(6576616c|73797374656d|7061737374687275|65786563|706f70656e|70726f635f6f70656e)28245f
...
# Webshells
PHP.Webshell.Azrail:3:*:617a7261696c20312e3020627920632d772d6d3c
...
# PHP Exploits
PHP.Exploit.Safemode:3:*:736166655f6d6f6465*636f70792822636f6d70726573732e7a6c69623a2f2f222e24
...
# Andere
Trojan.Webshell.Gamma:7:*:6d79202476657273696f6e203d202767616d6d6120776562207368656c6c
...
```

[sbiewald-php.ndb](sbiewald-php.ndb); 
*Die verlinkte Datei steht unter 3-Klausel-BSD-Lizenz.*

[sbiewald-obf.ndb](sbiewald-obf.ndb); 
*Die verlinkte Datei steht unter 3-Klausel-BSD-Lizenz.*

