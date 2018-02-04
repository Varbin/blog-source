#!/usr/bin/env python3
"""
Usage: ipclear.py [-f]

Command line options:

 -f         Run in foreground (don't daemonize).

Reads log data in Common Log format from /var/log/access.fifo,
masks IPs and writes the modified lines to file /var/log/access.log.
"""

__author__ = "Simon Biewald"
__copyright__ = "Copyright 2016, Simon Biewald"
__license__ = """\
Copyright (c) 2016, Simon Biewald
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
this list of conditions and the following disclaimer in the documentation
and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors
may be used to endorse or promote products derived from this software without
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import os
import ipaddress

from daemonize import Daemonize

UNKNOWN_IP = "0.0.0.0"
MASK_IPV4 = int(os.environ.get("MASK_IPV4", 16))
MASK_IPV6 = int(os.environ.get("MASK_IPV6", 48))


def mask(line):
    ip, rest = line.split(maxsplit=1)
    if "[" in ip: ip = ip.replace("[", "")
    if "]" in ip: ip = ip.replace("]", "")

    try:
        parsed_ip = ipaddress.ip_address(ip)
    except ValueError:
        fixed_ip = UNKNOWN_IP
    else:
        if isinstance(parsed_ip, ipaddress.IPv4Address):
            network_width = MASK_IPV4
        else:
            network_width = MASK_IPV6
        fixed_ip = str(ipaddress.ip_network(
            '{}/{}'.format(ip, network_width), False)[0])

    return ' '.join((fixed_ip, rest))


def main():
    with open("/var/log/access.fifo") as fifo:
        with open("/var/log/access.log") as logfile:
            while True:
                line = fifo.readline()
                logfile.write(mask(line))            


if __name__ == "__main__":
    daemon = Daemonize(app="ipclear", pid="/var/run/ipclear.pid", action=main,
                       foreground="-f" in sys.argv)
    daemon.start()
