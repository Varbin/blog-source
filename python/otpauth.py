#!/usr/bin/python3
# -*- coding: UTF-8 -*-

"""
Simple library for generation of Initiative for Open Authentication
HOTP and TOTP tokens.

Example:

    >>> import otpauth
    >>> secret = otpauth.secret()
    >>> otpauth.encode_secret(secret)
    'VVYCP65QRJM54UMM'
    >>> otpauth.hotp(secret, counter=65537)
    '869007'

"""

import base64
import hashlib
import hmac
import os
import struct
import time

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


def hotp(secret, counter, digits=6, algorithm=hashlib.sha1):
    """
    Generate a HOTP-token at counter counter, with the length digits
    and the algorithm algorithm.
    """
    counter_bytes = struct.pack('>Q', int(counter))
    hs = hmac.new(secret, counter_bytes, algorithm).digest()
    o = hs[19] & 15
    numbers = str(int.from_bytes(hs[o:o+4], 'big') & 2147483647)
    return numbers[-digits:].rjust(digits, '0')


def totp(secret, period=30, digits=6, algorithm=hashlib.sha1):
    """
    Generate a TOTP-token at from the current time and the period period,
    with the length digits and the algorithm algorithm.
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
    return hashlib.md5(seed).hexdigest()[:length]
