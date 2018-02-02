---
title: Zwei-Faktor-Authentifizierung in Python
author: Simon Biewald
description: Einführung einer Pythonbibliothek ohne externe Abhängigkeiten für Zwei-Faktor-Authentifizierung
  mit den Verfahren TOTP, HOTP und mOTP.
subject: Python, Kryptographie
date: 2016-09-18
---

# Zwei-Faktor-Authentifizierung in Python

**Einführung einer Pythonbibliothek ohne externe Abhängigkeiten für Zwei-Faktor-Authentifizierung
mit den Verfahren TOTP, HOTP und mOTP.**

- - -

## 2FA leicht gemacht

Heutzutage spielt die Anmeldung mit einem zweiten Faktor zusätzlich zu einem Passwort bereits bei 
[vielen][1] [Diensten][2] [eine][3] [Rolle][4]. Am häufigsten wird das ["TOTP"-Verfahren][5] verwendet, welches u.a. von der
[Initiative For Open Authentication (OATH)][6] [empfohlen][7] wird.
 Deswegen hier eine Implementation in Python ohne externe Abhängigkeiten.

## Was ist Zwei-Faktor-Authentifizierung?

Was ist ein solcher "zweiter Faktor"? Man unterscheidet zwischen drei Faktoren, die die eigene 
Identität beweisen sollen:

 - Wissen (Passwörter, PINs)
 - Besitz (Mobiltelefon, Schlüssel, Hardware-Tokens)
 - Seien (Fingerabdruck, Iris)

*Quelle:* vgl. [Wikipedia/Zwei-Faktor-Authentifizierung][8]
 
Anstelle nur eines Faktors (i.d.R. Passwort) wird nun zusätzlich mindestens ein Zweiter verlangt, idealerweise ein anderer (z.B. PIN+Fingerabdruck oder Passwort+Mobilbenachrichtigung).

Zur Kontrolle des Faktors "Besitzes" werden häufig Einmalkennwörter auf Basis eines vorher ausgetauschten Schlüssel und 
entweder auf Basis der aktuellen Zeit oder eines Zählers erzeugt. Die Verfahren werden TOTP (zeitbasiert) oder 
HOTP (zählerbasiert) genannt. Der Benutzer verwendet dann ein Hardware-Token (Beispielsweise [RSA SecurID][9] oder den 
[Battle.net Authenticator][1]) oder
eine Anwendung auf einem Mobilgerät (Beispielsweise [FreeOTP][10], [Google][11] [Authenticator][12], [Authy][13] 
oder das proprietäre ["Symantec Validation and ID Protection Service (VIP)"][14]). Bei den letzteren 
Möglichkeiten wird der Schlüssel meist über einen einzuscannenden QR-Code verteilt.


 [1]: https://eu.battle.net/support/de/article/battle-net-authenticator-faq
 [2]: https://support.google.com/accounts/answer/185839?hl=de
 [3]: https://www.heise.de/security/meldung/Amazon-startet-Zwei-Faktor-Authentifizierung-2965600.html
 [4]: https://twofactorauth.org/
 [5]: https://tools.ietf.org/html/rfc6238
 [6]: https://openauthentication.org/
 [7]: https://openauthentication.org/specifications-technical-resources/
 [8]: https://de.wikipedia.org/wiki/Zwei-Faktor-Authentifizierung
 [9]: https://www.rsa.com/de-de/products-services/identity-access-management/securid/hardware-tokens
 [10]: https://fedorahosted.org/freeotp/
 [11]: https://github.com/google/google-authenticator
 [12]: https://github.com/google/google-authenticator-android
 [14]: https://www.symantec.com/de/de/vip-authentication-service/
 [13]: https://www.authy.com/

## Beschreibung der Algorithmen

### [HOTP][15]

HOTP basiert auf einem geheimen, aber geteiltem Schlüssel ("schared secret") und einem synchronisiertem Zähler ("counter").
Zuerst wird der Zähler um einen erhöht, anschließend der HMAC des Zählers mit dem ausgetauschten Schlüssel als HMAC-Schlüssel.
Die letzten vier Bits des Ergebnises sind der sogenannte "Offset" und bestimmen, wo im Ergebnis der eigentlich Wert steht.

Vier Bytes ab dem Offset+1 (programmiertechnisch ab Offset) werden als Ergebnis in Dezimalform verwendet und auf die 
nötigen Stellen gekürzt. Sollte dieses Ergebnis nicht die nötige Anzahl stellen haben werden von links Nullen aufgefüllt.

Die Mindestlänge des Einmalkennworts beträgt sechs Dezimalstellen, [empfohlen wird die Länge sieben oder acht][16].
Da der Code sich nur durch die Erhöhung des Zählers ändert, wird auf Grund der kurzen Länge
empfohlen, [die Anzahl der Loginversuche zu begrenzen][17] (s. unten).
Außerdem ist es schwierig die Zähler von Client und Server synchron 
zu halten, als Lösung dazu werden meistens die nächsten Einmalpasswörter auf dem Server miterzeugt und 
mit dem abgegebenen verglichen, passt eins, ist der Zähler für dieses der neue Zählerstand auf dem Server.
 
 [15]: https://tools.ietf.org/html/rfc4226
 [16]: https://tools.ietf.org/html/rfc4226#page-6
 [17]: https://cryptography.io/en/latest/hazmat/primitives/twofactor/#throttling
 
### [TOTP][18]

Der TOTP-Algorithmus basiert auf dem HOTP-Algorithmus, jedoch wird anstelle des Zählers ein Bruchteil des 
Unix-Timestamps genommen. Dazu wird der aktuelle Unix-Timestamp durch einen ausgehandelten werden geteilt 
("period", üblicherweise 30). Dardurch sind die so erzeugten Tokens eine begrenzte Zeit lang gültig. Dieser geteilte
Wert tritt an die Stelle des Counters des HOTP-Algorithmus', alle anderen Parameter bleiben gleich.

Um leichte Differenzen bei Hard- und Software auszugleichen, sind Zeitunterschiede von ±30s erlaubt.

 [18]: https://tools.ietf.org/html/rfc6238
 
### [mOTP][19]

mOTP ist ein Algorithmus des Entwicklers "matts1972". Zur berechnung des Einmalpasswortes wird der MD5-Hash aus:

 - dem Unix-Timestamp / 10 (in Zahlenform)
 - einem PIN
 - und einem ausgehandeltem Schlüssel (zwischen 64 - 128bit, hexcodiert)
 
Als Einmalkennwort werden die ersten sechs Zeichen der Hexadezimaldarstellung des Hashes verwendet.

Server sollen laut [offizieller Webseite](http://motp.sourceforge.net/#1) 
Werte +/- 3 Minuten akzeptieren und nach 8 aufeinanderfolgenden, fehlgeschlagenen Loginversuchen den Nutzer sperren.

 [19]: http://motp.sourceforge.net/
 
## Pythonbibliothek

Es gibt bereits mehrere Pythonimplementationen der Protokolle TOTP und HOTP, diese besticht jedoch mit Einfachheit und Kürze.
Außerdem müssen keine zusätzlichen Bibliotheken installiert werden (keine Abhängigkeiten).
 
<pre class="language-python line-numbers">
<code>import base64
import hashlib
import hmac
import os
import struct
import time


def hotp(secret, counter, digits=6, algorithm=hashlib.sha1):
    """
    Generate a HOTP-token at counter "counter", with the length "digits"
    and the algorithm "algorithm".
    """
    counter_bytes = struct.pack('>Q', int(counter))
    hs = hmac.new(secret, counter_bytes, algorithm).digest()
    o = hs[-1] & 15 # 0x0f = 0b00001111
    numbers = str(int.from_bytes(hs[o:o+4], 'big') & 2147483647)
    return numbers[-digits:].rjust(digits, '0')


def totp(secret, period=30, digits=6, algorithm=hashlib.sha1):
    """
    Generate a TOTP-token at from the current time and the period "period",
    with the length "digits" and the algorithm "algorithm".
    """
    return hotp(secret, counter=time.time()//period,
                digits=digits, algorithm=algorithm)


def motp(pin, secret, offset=0):
    """
    Generate a "Mobile One Time Password". "offset" is in 10 seconds from now.
    """
    if isinstance(pin, str):
        pin = pin.encode()
    if isinstance(secret, str):
        secret = secret.encode()
    lc = str(int(time.time()//10+offset)).encode()
    se = pin + secret
    tg = lc+se
    return hashlib.md5(tg).hexdigest()[:6]


# Helper functions

def oath_secret(length=10):
    """Generate a valid secret with a length length"""
    return os.urandom(length)


def encode_oath_secret(secret):
    """base32-encode a secret"""
    return base64.b32encode(secret).decode()


def decode_oath_secret(secret):
    """base32-decode an encoded secret"""
    return base64.b32decode(secret)


def motp_secret(seed=None, length=16):
    """Generate a mOTP-secret based on seed, random if no seed is given (recommended)"""
    if seed is None:
        seed = os.urandom(32)
    if isinstance(seed, str):
        seed = seed.encode()
    return hashlib.md5(seed).hexdigest()[:length]</code>
</pre>

[otpauth.py](otpauth.py); *Die verlinkte Version steht unter 3-Klausel-BSD-Lizenz 
und ist gegebenenfalls neuer.*

## Beispiel

```python
>>> import otpauth
>>> secret = otpauth.decode_secret('VVYCP65QRJM54UMM')
>>> otpauth.hotp(secret, counter=65537)
'869007'
>>> otpauth.totp(secret)  # Zeitabhängig
'739702'
```

## Empfehlungen

<blockquote class="note">
    Die Empfehlungen sind zwar sinnvoll, jedoch nicht immer praktisch umzusetzen.
</blockquote>

Allgemein wird empfolhen eine möglichst große Schlüsssellänge zu verwenden. Bei HOTP/TOTP werden anstelle der
standardmäßigen 80-Bit (10 Bytes; 16 Zeichen in Base32) eine Länge von 128-Bit (16 Bytes; 26 Zeichen ohne Padding in 
Base32) empfohlen.

Die Länge der Einmalpasswörter sollte von 6 auf das Maximum 8 erhöht werden.

Da HOTP bis zu einer Serverseitigen Erhöhung des Zählers das gültige Token gleich bleibt, ist es sinnvoll die 
Zugriffsversuche zu beschränken. Bei einer Länge von 6 empfiehlt das Bundesamt für Sicherheit in der 
Informationstechnik in der Richtlinie [TR-02102-1][20] in Abschnitt 6.3.1 (Stand 2018-01) eine Beschränkung 
auf 3 Zugriffsversuche vor Sperrung.

Bei mOTP sollten kürzere Zeitintervalle als vorgeschlagen verwendet werden, sonst liegt die Sicherheit unterhalb der 
i.d.R. sechsstelligen Codes von TOTP/HOTP. Auch acht mögliche Versuche scheinen unverhältnismäßig groß.
Besonders kann die Gesamtlänge des ausgetauschten Schlüssels erhöht werden, beispielsweise auf 128-bits.

Weiterhin sollte auf Grund möglichen Verlustes des Hardware-Tokens / Mobilgeräts eine Möglichkeit vorhanden seien, den zweiten
Faktor im Notfall zu entfernen / zu ersetzen. Das kann durch eine Liste von Einmalpasswörtern (TANs) oder einem 
einzigen, nur zur Wiederherstellung verwendbaren, langem Schlüssel bestehen.

 [20]: https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Publikationen/TechnischeRichtlinien/TR02102/BSI-TR-02102.pdf

