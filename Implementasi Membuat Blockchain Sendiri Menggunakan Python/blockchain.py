import sys                                # untuk mengakses objek dan fungsi sistem python
import hashlib                            # untuk melakukan hasing data
import json                               # untuk mengubah data pyhton ke json

from time import time                     # untuk mengambil waktu sekarang
from uuid import uuid4                    # untuk membuat id unik random

from flask import Flask                   # untuk mengimpor objek utama Flask
from flask.globals import request         # untuk mengakses data request yang masuk ke APIku
from flask.json import jsonify            # untuk mengubah data python ke json yang bisa dikirim liwat client

import requests                           # untuk mengirim HTTP request (GET, POST, dsb)
from urllib.parse import urlparse         # untuk memecah URL jadi bagian-bagian: protokol, domain, path, dll.
