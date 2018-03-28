---
title: Hurricane Electric 6in4-Tunnel unter FreeBSD einrichten
author: Simon Biewald
description: Mit HE kann einfach eine IPv6 Anbindung in IPv4 Netzen erfolgen - wie wird ein permanenter Tunnel dafür korrekt eingerichtet?
subject: HE, Tunnel, FreeBSD, 6in4, tunnelbroker
date: 2018-04-28T19:18
---

# Hurricane Electric 6in4-Tunnel unter FreeBSD einrichten

Besitzt ein Server keine IPv6-Anbindung kann hierfür ein 6in4-Tunnel eingesetzt werden,
dabei werden IPv6-Pakete über IPv4 verschickt werden.


**Inhalt**

 1. [Einmalige Einrichtung](#einmal)
 2. [Dauerhafte Einrichtung](#dauerhaft)
 3. [Keepalive-Dienst](#keepalive)


Ein Anbieter dafür ist der amerikanische ISP Hurricane Electric (HE) mit dem kostenlosen Dienst
[tunnelbroker.net](https://tunnelbroker.net/ "Hurricane Electric Free IPv6 Tunnel Broker") können nach
der [Registrierung](https://tunnelbroker.net/register.php "IPv6 Tunnel Broker Registration") bis zu
5 Tunnel erzeugt werden.
Zwar stellt HE Konfigurationsbeispiele für die meisten Betriebssysteme bereit,
jedoch sind diese nicht permanent und müssen somit nach jedem Neustart neu angewandt werden.

<a id="einmal">
## Einmalige Einrichtung
</a>

Zur einmaligen Einrichtung (für FreeBSD) stellt HE ein Skript bereit,
dabei werden die in Großbuchstaben geschriebenen Namen durch die jeweiligen IP-Adressen
ersetzt, die in den Tunneldetails unter "IPv6 Tunnel Endpoints" steht.

<pre class="line-numbers language-bash">
<code>#!/bin/sh

ifconfig gif0 create
ifconfig gif0 tunnel CLIENT_IPV4 SERVER_IPV4
ifconfig gif0 inet6 CLIENT_IPV6 SERVER_IPV6
route -n add -inet6 default SERVER_IPV6
ifconfig gif0 up
</code></pre>

Durch das Skript wird ein generisches Tunnelinterface (`gif0`) zuerst angelegt und konfiguriert,
anschließend die IPv6-Serveradresse von HE zur Routingtabelle hinzugefügt. Schließlich wird der Tunnel
aktiviert.

<a id="dauerhaft">
## Dauerhafte Einrichtung
</a>

Zur dauerhaften Einrichtung müssen die Netzwerkeinstellungen in die
 `/etc/rc.conf` bzw. in die  `/etc/rc.conf.local` eingetragen werden:
 
<pre class="line-numbers language-bash">
<code>cloned_interfaces="gif0"
ifconfig_gif0="tunnel CLIENT_IPV4 SERVER_IPV4 mtu 1480"
ifconfig_gif0_ipv6="inet6 CLIENT_IPV6 SERVER_IPV6 prefixlen 128"

# vtnet0 durch das Hauptnetzwerkinterface ersetzen
ifconfig_vtnet0_ipv6="inet6 SERVER_IPV6"

ipv6_defaultrouter="SERVER_IPV6"
ipv6_gateway_enable="YES"

rtadvd_enable="YES"</code></pre>

**Dabei muss *vtnet0* durch das eigentlich verwendete Hauptnetzwerkinterface ersetzt werden!**
Die <abbr title="Maximum Transmission Unit">MTU</abbr> kann bei HE netzwerkabhängig auf einen 
kleineren Wert eingestellt werden.

Nach einem Neustart sollten die Einstellungen angewendet sein. Die Ausgabe von `ifconfig` sollte
dann ähnlich aussehen:

<pre class="command-line language-bash" data-output="2-25" data-prompt="[user@freebsd] %">
<code>ifconfig
vtnet0: flags=8843&lt;UP,BROADCAST,RUNNING,SIMPLEX,MULTICAST&gt; metric 0 mtu 1500
	options=6c07bb&lt;RXCSUM,TXCSUM,VLAN_MTU,VLAN_HWTAGGING,JUMBO_MTU,VLAN_HWCSUM,TSO4,TSO6,LRO,VLAN_HWTSO,LINKSTATE,RXCSUM_IPV6,TXCSUM_IPV6&gt;
	ether 11:22:33:44:55:66
	hwaddr 11:22:33:44:55:66
	inet6 2001:DB8:0:1::1 prefixlen 64
	inet6 fe80::11:22:33ff:fe:44:55:66%vtnet0 prefixlen 64 scopeid 0x1
	inet 1.2.3.4 netmask 0xffffffc0 broadcast 79.133.35.127
	nd6 options=21&lt;PERFORMNUD,AUTO_LINKLOCAL&gt;
	media: Ethernet 10Gbase-T &lt;full-duplex&gt;
	status: active
lo0: flags=8049&lt;UP,LOOPBACK,RUNNING,MULTICAST&gt; metric 0 mtu 16384
	options=600003&lt;RXCSUM,TXCSUM,RXCSUM_IPV6,TXCSUM_IPV6&gt;
	inet6 ::1 prefixlen 128
	inet6 fe80::1%lo0 prefixlen 64 scopeid 0x2
	inet 127.0.0.1 netmask 0xff000000
	nd6 options=21&lt;PERFORMNUD,AUTO_LINKLOCAL&gt;
	groups: lo
gif0: flags=8051&lt;UP,POINTOPOINT,RUNNING,MULTICAST&gt; metric 0 mtu 1480
	options=80000&lt;LINKSTATE&gt;
	tunnel inet 1.2.3.4 --&gt; 216.0.0.0
	inet6 2001:DB8:0:1::2 --&gt; 2001:DB8:0:1::1  prefixlen 128
    inet6 fe80::11:22:33ff:fe:44:55:66%gif0 prefixlen 64 scopeid 0x1
	nd6 options=21&lt;PERFORMNUD,AUTO_LINKLOCAL&gt;
	groups: gif</code></pre>

<a id="keepalive">
## Keepalive-Dienst
</a>

Der 6in4-Tunnel wird automatisch getrennt, wenn dieser nicht mehr genutzt wird.
Als Keepalive-Dienst kann ein im Hintergrund laufender Ping-Prozess über IPv6
verwendet werden.

Damit der Hintergrundprozess verwaltbar bleibt wird ein Dienst eingerichtet (`ping6keepalive`):

`/usr/local/etc/rc.d/ping6keepalive`:

<pre class="line-numbers language-bash">
<code>#!/bin/sh
#
# PROVIDE: ping6keepalive
# REQUIRE: networking

. /etc/rc.subr

name="ping6keepalive"
desc="Ping6 daemon for keepalive"
rcvar="${name}_enable"

load_rc_config ${name}

: ${ping6keepalive_enable:="NO"}

pidfile="/var/run/${name}.pid"
procname="/sbin/ping6"
command="/usr/sbin/daemon"
command_args="-u nobody -p ${pidfile} ${procname} -i 30 freebsd.org < /dev/null >> /dev/null 2>&1"

run_rc_command "$1"</code></pre>

Download:
<a href="ping6keepalive" title="Ping6 daemon for keepalive" download>ping6keepalive</a>

Der Dienst wird unter `/etc/rc.conf` bzw. `/etc/rc.conf.local` aktiviert:

<pre class="line-numbers language-bash">
<code>ping6keepalive_enable="yes"</code></pre>

Anschließend wird der Dienst ausführbar gemacht und gestartet:

<pre class="command-line language-bash" data-user="root" data-host="freebsd" data-output="3,5">
<code>chmod +x /usr/local/etc/rc.d/ping6keepalive
service ping6keepalive start
Starting ping6keepalive.
service ping6keepalive status
ping6keepalive is running as pid 16649</code></pre>
