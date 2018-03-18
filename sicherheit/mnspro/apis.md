---
title: Api-Endpunkte im MNSpro Schulnetzwerk
author: Simon Biewald
description: Für jede Funktion ein Api-Endpunkt beim MNSpro Schulnetzwerk - welcher Endpunkt macht was von wo?
subject: Sicherheit, MNSpro, REST, Api
date: 2018-03-18T20:30
---

# Api-Endpunkte im MNSpro Schulnetzwerk

*Für jede Funktion ein Api-Endpunkt beim MNSpro Schulnetzwerk - welcher Endpunkt macht was von wo?*

Die meisten [Sicherheitslücken im  MNSpro Schulnetzwerk][0] entstehen durch mangelnde Absicherung von aus dem Netzwerk
abrufbaren Apis.

Zu unterscheiden sind: 

 - Unterrichtszentralendienst-Apis: Diese sind auf den Clients aktiv und erlauben die Fernsteuerung von Computern durch Lehrer
   mit der sogenannten Unterrichtszentrale. Ist diese Api nicht korrekt abgesichert hat dieses schwerwiegende Konsequenzen.
 - Serverdienst-Apis: Diese ist auf dem Domain Controller aktiv und dient zur Informationserlangung der 
   Unterrichtszentrale (z.B. Wer ist an welchem Computer angemeldet, etc.), ist allerdings auch eine Abstraktion von
   Netzwerkfunktionen (Wake on Lan). Zur Verwendung wird i.d.R. keine bzw. eine zu vernachlässigende Authentifizierung 
   benötigt.

 [0]: /sicherheit/mnspro/ "Sicherheitslücken in der Software MNSpro Schulnetzwerk"

## Unterrichtszentralendienst-Apis

Der Unterrichtszentralendienst stellt, wie bereits erwähnt, Funktionen für die Lehrersoftware "Unterrichtszentrale" zur 
Verfügung. Gelauscht wird auf einem zufälligem Port im ungefähren Bereich `49000` - `63000`, es muss sich
authentifiziert werden, [auch wenn die Sicherheit der Authentifizierungsmethode häufig mangelhaft ist][0].

Es gibt folgende Endpunkte (unter `/Api/`):

 - VNC-Passwort: `getRemotingCredentials`
 - Screenshot (löst Warnung aus): `GetScreenshot?width=[Breite]&height=[Höhe]&user=[Nutzer]&machine=[Computername]`
 - Sperrt Bildschirm: `LockDesktop`
 - Entsperrt Bildschirm: `UnlockDesktop`
 - Sperrt-/Entsperrt optische Laufwerke: `SetCdRomState?enable=[False/True]`
 - Sperrt-/Entsperrt USB: `SetUsbState?enable=[False/True]`
 - Sperrt-/Entsperrt Internetzugang (schaltet installierten Filtertreiber (!) an oder aus): 
   `SetInternetState?enable=[False/True]`
 - Setzt Ton: `SetVolumeInformation?ismute=[True/False]&volume=[Lautstärke]`
 - Meldet aktuellen Nutzer ab: `LogOffUser`
 - Meldet Nutzer an (nur im Anmeldebildschirm sinnvoll): `LogOnUser?username=[Nutzername]&password=[Passwort]`
   - Aktion: `Strg`+`Alt`+`Entf`, anschließend `Strg`+`A`, Eingabe des Nutzername, `Tab`, Eingabe des Passworts
 - URL für Chatserver (i.d.R. URL für die allgemeinen Serverdienst-Apis): `GetChatServiceUrl`
 - Herunterfahren des Computers: `Shutdown`
 - Neustart des Computers: `Restart`
 - Eine komplizierterer Endpunkt für Starten einer Bildschirmübertragung.
 - Bildschirmübertragung an den angesprochenen Computer unterbinden: `CloseRemoteDesktop`
 - Deaktiviert das Menü unter `Strg`+`Alt`+`Entf` (verwendet bei `LockDesktop`): `SetPolicies`
 - Aktiviert das Menü unter `Strg`+`Alt`+`Entf`: `ResetPolicies`
 - Führt ein Programm aus: `StartApplication?executable=[Pfad]&arguments=[Argumente]`

### Weitere Api

Außerdem lauscht auf dem Port 8001 ein weiterer Server (als HTTP-Host muss `localhost:8001` gesendet werden):

 - Liefert das Bild für die Fehlermeldung aus, die angezeigt wird, falls durch den Internetfiltertreiber (!) 
   der Internetzugang blockiert wurde: `InternetBlockedImage`

## Serverservice-Apis

Auf dem Domain Controller laucht eine Api zur Abfrage von Informationen als auch als Abstraktion von Netzwerkfunktionen.
Der Port ist auf der Registry des Servers abgelegt (wenn nicht ist es Port `8001`).

- `AllowedApps`
   - GET: Zeigt Erlaubte Apps für an (`?targetname=[Raum- oder Computername]`).
   - POST: Setzt neue Apps (Parameter `AppList` (`\n` getrennt) und `TargetName`)
 - Liefert JSON-formattierte AD-Daten (Räume, Gruppen, Nutzer): `GetAdStructures`
 - Listet alle aktive MNSpro-Sitzungen auf (inkl. "Service-URL"): `GetClientSessions`
 - Startet einen Computer über Wake-on-Lan: `WakeOnLan?MachineName=[Computername]`
 - Überprüft, ob einem Nutzer Computer außerhalb des Raumes angezeigt werden dürfen: `IsUserAllowedToSeeAllStructures?username=[Nutzername]&domainName=[Domainname]` 
 - Überprüft, ob ein Nutzer ein Lehrer ist (funktionierte in vorliegender Installation nicht): `IsTeacher?username=[Nutzername]&domainName=[Domainname]`
 - Zeigt (GET) bzw. setzt (POST) "Optionen" (genaue Funktion unklar): `Options`

Raummodelle haben folgende Aufrufe (genaue Funktionen unklar):

 - Erzeugt / aktualiesiert Raummodelle (genaue Verwendung unklar):
   `AddOrUpdateViewLayout?targetname=[Raum?]&layoutName=[Name]&layoutDescription=[Beschreibung]&id=.[GUID]&kind=[GUID]`
 - Zeigt Modelle von Räumen an (falls eingerichtet), in alten Version werden alle Raumauflistungen angezeigt:
   `GetViewLayouts`
 - Löscht Raummodelle: `DeleteViewLayout?id=[GUID]`

### Weitere Apis

Außerdem existiert auch folgende Api (unter `https://mnsserver.[Domainname]:8735/Api/`, Domainname ist):

 - Überprüft ob das MNSpro eigene Startmenü aktiv ist:  `DashboardEnable`
 - Überprüft ob der eigene Maildienst eingerichtet ist: `TreeConfiguration?name=[UPN, optional]` 
   (bei den zurückgegebenen JSON-Daten muss "Result" "2" entsprechen.)
 - Ruft ungelesene Nachrichten ab (*ungetestet*): `MailManagerGetUnreadMails?name=[UPN]`

Authentifiziert wird sich mit dem URL-Parameter `Api_key=aachen0815`. UPN ist `Nutzername@domain`
