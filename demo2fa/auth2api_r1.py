# Source code provided under FreeBSD License as described below. 
# If you need any other type please write us at lic@auth2.com
"""
Copyright (c) 2012 Auth2.
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met: 

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer. 
2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution. 

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

The views and conclusions contained in the software and documentation are those
of the authors and should not be interpreted as representing official policies, 
either expressed or implied, of the FreeBSD Project.
"""

import urllib
import urllib2
import uuid
import logging

logger = logging.getLogger(__name__)

# returns something like '[{"call_id_guid": "41e9ebe2-b289-449d-b24b-86a1d14c7ba9", "status": "Pending", "api_key": "<your api key>", "valid":"true"}]'
def send_key_api_client(api_key, api_secret, phone_0, phone_1, phone_2 , key):
    # Make sure the key and secret are valid UUIDs. 
    # Server will check but sending invalid values does not make sense.
    uuid.UUID(api_key)
    uuid.UUID(api_secret)

    if key<10 or key > 9999999999:
        raise ValueError("key must be between 2 to 10 digits long number.")
    if len(phone_0) != 3:
        raise ValueError("phone_0 must be exactly 3 digits long area code.")
    if len(phone_1) != 3:
        raise ValueError("phone_1 must be exactly 3 digits long.")
    if len(phone_2) != 4:
        raise ValueError("phone_2 must be exactly 4 digits long.")

    url = "http://auth2.com/api/r1/sendkey/"

    req = urllib2.Request(url)
    req.add_header('User-agent', 'Auth2 Python Client API v1.0')
    req.add_data(urllib.urlencode({'api_key':api_key , 'api_secret':api_secret , 'phone_0':phone_0 , 'phone_1':phone_1 , 'phone_2':phone_2 ,'key': key}))
    resp = urllib2.urlopen(req)
    resp_json = resp.read()
    resp.close()
    return resp_json

def send_key(api_key, api_secret, phone_number, key): 
    # Make sure the key and secret are valid UUIDs. 
    # Server will check but sending invalid values does not make sense.
    uuid.UUID(api_key)
    uuid.UUID(api_secret)
       
    if key<10 or key > 9999999999:
        raise ValueError("key must be between 2 to 10 digits long number.")

    if len(phone_number) != 10:
        raise ValueError("Phone number must be exactly 10 digits long.")

    if len(str(int(phone_number))) != 10:
        raise ValueError("Phone number must be exactly 10 digits long.")

    phone_0 = phone_number[0:3]
    phone_1 = phone_number[3:6]
    phone_2 = phone_number[6:10]

    return send_key_api_client(api_key, api_secret, phone_0, phone_1, phone_2 , key)