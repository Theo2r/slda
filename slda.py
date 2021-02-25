import os
import re
from urllib.parse import quote

import redis
from hashids import Hashids
from yhttp import Application, json, statuses, validate, statuscode


__version__ = '0.1.0-dev'


hashids = Hashids()


redis = redis.Redis()
app = Application()
app.settings.merge('''
blacklist: []
''')


def getfreshid():
    randomint = int.from_bytes(os.urandom(6), 'big')
    return hashids.encode(randomint)


@app.when
def ready(app):
    app.blacklist = set(re.compile(i) for i in app.settings.blacklist)


def blacklist(value, container, field):
    for r in app.blacklist:
        if r.match(value):
            raise statuses.conflict()

    return value


@app.route('/apiv1/urls')
@validate(fields=dict(url=dict(
    required='400 Field missing: url',
    pattern=(r'^https?://.*', '400 Invalid URL'),
)))
@json
@statuscode('201 Created')
def post(req):
    url = req.form['url'].encode()
    url = quote(url, safe=':/#')
    while True:
        freshid = getfreshid()
        if redis.setnx(freshid, url):
            break

    return {'id': freshid}


@app.route('/(.*)')
def get(req, key):
    longurl = redis.get(key)
    if not longurl:
        raise statuses.notfound()

    raise statuses.found(longurl.decode())
