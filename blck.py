#!/usr/bin/env python2
# copyleft (c) 2017 - parazyd
# see LICENSE file for details

import flask
import random
import re
import os
import string
import sys

app = flask.Flask(__name__)

@app.route("/")
def main():
    return flask.render_template("index.html")


@app.route("/u/<urlshort>")
def u(urlshort):
    try:
        f = open('uris/' + urlshort, 'r')
        realurl = f.readline()
        f.close()
        os.remove('uris/' + urlshort)
    except:
        return "could not find url\n"

    if "curl" not in flask.request.headers.get('User-Agent'):
        return flask.redirect(realurl.rstrip('\n'), code=301)
    else:
        return realurl

@app.route("/s", methods=['POST'])
def s():
    url = flask.request.form['url']

    if not url:
        return "invalid data\n"

    if len(url) > 1024:
        return "url too long\n"

    ## taken from django
    regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    if not regex.match(url):
        return "invalid url\n"

    urlshort = genid()
    try:
        f = open('uris/' + urlshort, 'w')
        f.write(url + '\n')
        f.close()
    except:
        return "could not save url\n"

    return flask.request.url_root + 'u/' + urlshort + '\n'


def genid(size=4, chars=string.ascii_uppercase + string.ascii_lowercase):
    return ''.join(random.choice(chars) for i in range(size))

if __name__ == "__main__":
    try:
        if sys.argv[1] == '-p':
            _port = sys.argv2
    except:
        _port = 5000

    app.run(host="127.0.0.1", port=int(_port))
