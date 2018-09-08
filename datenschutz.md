---
title: Datenschutzerklärung
description: Angewandter Datenschutz in der Datenschutzerklärung zu sbiewald.de
---

# Datenschutzerklärung

Anstelle der leeren Formulierung

<blockquote>
Die Betreiber dieser Seiten nehmen den Schutz Ihrer persönlichen Daten sehr ernst.
</blockquote>

setze ich Datenschutz auf meiner Webseite wirklich um!

Es werden **keine** Cookies gesetzt und **nichts** von z.B. Google oder Facebook verwendet. 
Alle gesammelten Daten werden **keinen Personen zugeordnet**.

## Welche Daten werden erfasst?

Die folgenden, von Ihrem Webbrowser automatisch übertragenden,
Daten werden zur **Erbringung des Dienstes** und **anonymen** statistischen Auswertungen erhoben:

 - gekürzte IP-Adresse
 - Uhrzeit Ihres Besuchs
 - die besuchte Seite
 - ggf. die zuvor besuchte Seite ("Referer")
 - ggf. das von Ihnen verwendete Betriebssystem und Webbrowser ("User-Agent")
 
Diese Daten können nicht Personen zugeordnet werden (sie sind nicht "personenbezogen"). Diese Daten werden **nicht** für Werbezwecke genutzt oder
weitergegeben.

### Und das heißt...?

Sollte unklar sein, welche erhobenen Daten damit gemeint sind und wie diese verwendet werden können, 
hier eine Erklärung der einzelnen möglicherweise unklaren Punkte.

#### gekürzte IP-Adresse

Die IP-Adresse ist vergleichbar mit eine Telefonnummer Ihres Computers oder Internetanschlusses.
Da IP-Adressen personenbezogene Daten darstellen, wird diese selbstverständlich vor der Speicherung **gekürzt** und ist
somit nicht mehr Personen zuordnebar. 
So wird beispielsweise statt der vollständigen Adresse `79.133.35.120` nur `79.133.0.0` gespeichert.
Damit lässt sich die IP-Adresse nicht mehr einer einzelnen Person zuweisen.

Mit Hilfe der IP-Adresse lässt sich die ungefähre Besucherzahl abschätzen und es kann ungefähr 
zugeordnet werden, aus welchem Land Sie diese Seite aufrufen.

#### ggf. die zuvor besuchte Seite ("Referer")

Ihr Webbrowser sendet teilweise die Information mit, über welche Webseite Sie auf eine andere Webseite 
gekommen sind - dieses ist der sogenannte "Referer" (<abbr title="schreibt sich wirklich so">sic!</abbr>). 
So ist es beispielsweise erkennbar, ob Sie z.B. von der Google-Suche auf meine Webseite gekommen sind. 
Dabei kann möglicherweise der verwendete Suchbegriff enthalten sein.

Mit Hilfe dieser Daten kann ich beispielsweise evaluieren, wie meine Seite benutzt wird, oder welche
Seiten auf diese Seite verweisen.

Die Übetragung dieser Daten kann in den Einstellungen des benutzten Webbrowsers meist abgestellt werden.

#### ggf. das von Ihnen verwendete Betriebssystem und Webbrowser ("User-Agent")

Ihr Webbrowser sendet Informationen über sich und das Betriebssystem mit (der sogenannte "User-Agent"). 

So kann ich zum Beispiel feststelle, für welchen Webbrowser ich meine Webseite optimieren sollte.

Der gesendete "User-Agent" kann übrigens auch geändert werden.

### Beispiel

Die von einem Webseitenaufruf gesammelten Informationen sehen dann beispielsweise so aus:

```log
93.236.0.0 - - [16/Feb/2018:16:51:26 +0100] "GET /sicherheit/mnspro/ HTTP/2.0" 200 5451 "-"
```

Daraus ablesbar ist: Die IP-Adresse des Besuchers fing mit `93.236` an, 
fragte am `16. Februar 2018 um 16:51` die Webseite `/sicherheit/mnspro` mit einem modernen Webbrowser 
(`HTTP/2.0`) an. Die Seite wurde direkt aufgerufen oder es wurde kein "Referer" gesendet (`"-"`).

### An wen werden Daten weitergegeben?

Zur statistischen Auswertung wird der "User-Agent" im Rahmen von Telemetrie meiner Software
an das Caddy-Project übertragen.

Auch dabei kann kein Personenbezug hergestellt werden.

Zu der Telemetrie, siehe auch [der Dokumentation des Webservs Caddy](https://caddyserver.com/docs/telemetry).

## Sollte etwas unklar sein...

...einfach [mich kontaktieren](/impressum). Auch Verbesserungen nehme ich gerne an!
