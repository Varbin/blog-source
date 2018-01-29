#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
This module is a simple interface to query time from (S)NTP servers using
Python.

Example:

    >>> import sntp
    >>> sntp.sntp()
    1464348344.7562184

"""

from __future__ import print_function

import socket
import struct

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

__version__ = "1.0"
__status__ = "Production"

DELTA = 2208988800
PACKET = b"\x13" + b"\00"*47

POOLS = [
    "",
    "africa.",
    "asia.",
    "europe.",
    "north-america.",
    "oceania.",
    "south-america."]


def sntp(server="pool.ntp.org", port=123, timeout=5):
    """Request time from remote server using NTP.

    Keyword arguments:
    server  -- the remote server to ask from (default pool.ntp.org)
    port    -- the port number of remote server (default 123)
    timeout -- the timout in seconds for the used socket (default 5),

    For the timeout argument, see socket.settimeout.

    Return the time in seconds since the epoch as a floating point number.
    """
    sock = socket.socket(type=socket.SOCK_DGRAM)
    sock.settimeout(timeout)
    sock.sendto(PACKET, (server, port))
    data = struct.unpack(">3Bb11I", sock.recv(48))
    sock.close()
    return data[11] + float(data[12]) / 2**32 - DELTA


if __name__ == "__main__":
    import time

    for pool in POOLS:
        pool += "pool.ntp.org"
        print("Server:", pool)
        print()

        print("| System\t\t| Remote\t\t| Diff\t\t\t|")

        g = 0

        for i in range(5):

            s = sntp()
            t = time.time()

            print("| {0: <18}\t| {1: <18}\t| {2: <18}\t|".format(t, s, t-s))
            time.sleep(.1)

            g += t-s

        print("|\t\t\t|\t\t\t \t\t\t|")
        print("|\t\t\t|\tMean\t\t~ {0: <18}\t|".format(g/5))

        print()
