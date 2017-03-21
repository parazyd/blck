#!/usr/bin/env python2
# copyleft (c) 2017 - parazyd
# see LICENSE file for details

import flask
import random
import re
import os
import string

app = flask.Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def main():
    try:
        url = flask.request.form['url']
        return s(url)
    except:
        return flask.render_template("index.html")

@app.route("/<urlshort>")
def u(urlshort):
    try:
        with open('uris/' + urlshort, 'r') as f:
            realurl = f.readline()
        os.remove('uris/' + urlshort)
    except:
        return "could not find url\n"

    if "curl" not in flask.request.headers.get('User-Agent'):
        return flask.redirect(realurl.rstrip('\n'), code=301)
    else:
        return realurl


def s(url):
    ## taken from django
    regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    if not url or len(url) > 1024 or not regex.match(url):
        return "invalid url\n"

    urlshort = genid()
    try:
        with open('uris/' + urlshort, 'w') as f:
            f.write(url + '\n')
    except:
        return "could not save url\n"

    if flask.request.headers.get('X-Forwarded-Proto') == 'https':
        return flask.request.url_root.replace('http://', 'https://') + urlshort + '\n'

    return flask.request.url_root + urlshort + '\n'


def genid(size=4, chars=string.ascii_uppercase + string.ascii_lowercase):
    return ''.join(random.choice(chars) for i in range(size))


app.run(host="127.0.0.1", port=5000)
