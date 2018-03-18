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

 - PHP-Backdoors: Azrail, CasuS, Cybershell, KAdot, Lolipop, lostpassworddc, Spammailer, MyShell, NShell, s72
 - Exploits: Umgehungsversuche des PHP-Safemodes
 - Weitere Backdoors: Gamma Webshell (Perl) sowie eine CGI-Backdoor in Python
 
Außerdem ist eine einfache Heuristik zur Erkennung von PHP-Backdoors mit dabei, 
die erkennt ob `$_`-Variablen (`$_GET`, `$_POST`, `$_REQUEST`) als Argument für 
`eval` / `system` / `passthru` / `exec` / `popen` / `proc_open` verwendet werden.

## Download

```python
# Heuristik
PHP.Webshell.Generic:0:*:(6576616c|73797374656d|7061737374687275|65786563|706f70656e|70726f635f6f70656e)28245f
PHP.Webshell.Generic:0:*:24636d64{-5}245f{-250}(73797374656d|7061737374687275|65786563|706f70656e|70726f635f6f70656e)2824636d64
PHP.Webshell.Generic:0:*:65787472616374{-3}245f
# Webshells
PHP.Webshell.Azrail:3:*:617a7261696c20312e3020627920632d772d6d3c
PHP.Webshell.CasuS:3:*:73797374656D2822246B6F6422293B*3C623E3C753E736F6674776172653C2F753E3A20247365727665725F736F6674776172653C2F623E3C62723E*6D61666961626F7927
PHP.Webshell.Cybershell:3:*:73656c663f643d24642664697a2674*73656c663f643d24642664697a2674*73656c663f643d24642664697a2674*73656c663f643d24642664697a2674*73656c663f643d24642664697a2674
PHP.Webshell.KAdot:3:*:2473656c663f61633d6576616c3e*706173737468727528245f706f73745b27
PHP.Webshell.Lolipop:3:*:3d3d6c6f6c69706f7020706870626220696e6465782e3d3d
PHP.Webshell.lostpassworddc:3:*:6c6f737470617373776f72642c20643376696c633064652063726577*7368656c6c
PHP.Webshell.Spammailer:3:*:6d61696c2824746f{32}227370616d6564273e3c62723e22
PHP.Webshell.MyShell:0:*:6d797368656c6c*73797374656d2824636f6d6d616e64202e202220313e202f746d702f6f75747075742e74787420323e26313b
PHP.Webshell.s72:7:*:3c3f7068702040246f75747075743d73797374656d28245f706f73745b22636f6d6d616e64225d293b203f3e
PHP.Webshell.NShell:0:*:66756e6374696f6e2065782824636f6d64*657865632824636f6d64
PHP.Backdoor.ReverseShell:0:*:24736f636b203d2066736f636b6f70656e{-150}6172726179282270697065222c2022722229{-75}6172726179282270697065222c2022772229{-75}6172726179282270697065222c2022772229{-75}70726f635f6f70656e
# PHP Exploits
PHP.Exploit.Safemode:3:*:736166655f6d6f6465*636f70792822636f6d70726573732e7a6c69623a2f2f222e24
# Andere
Trojan.Webshell.Gamma:7:*:6d79202476657273696f6e203d202767616d6d6120776562207368656c6c*2473656c662d3e7b6c6f67696e7d203d203120696620637279707428247765627368656c6c3a3a636f6e66696775726174696f6e3a3a70617373776f72642c20246c6f67696e2e227878222920657120246c6f67696e3b202473656c662d3e7b6c6f67696e7d203d2031206966202470617373776f726420657120247765627368656c6c3a3a636f6e66696775726174696f6e3a3a70617373776f72643b
Trojan.Webshell.PyCGISimple:7:*:23206367692d7368656c6c2e7079202320412073696d706c6520434749207468617420657865637574657320617262697472617279
Trojan.Webshell.PyCGISimple:7:*:4d4554484f44203d202722504f53542227*64617461203d20676574666f726d285b27636d64275d2c666f726d2920746865636d64*6f732e706f70656e32
```

[sbiewald-php.ndb](sbiewald-php.ndb); 
*Die verlinkte Version steht unter 3-Klausel-BSD-Lizenz und ist gegebenenfalls neuer.*
