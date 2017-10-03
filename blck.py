#!/usr/bin/env python3
# copyleft (c) 2017 - parazyd
# see LICENSE file for details

import flask
import random
import os
import string


app = flask.Flask(__name__)

pastebin = False


@app.route("/", methods=['GET', 'POST'])
def main():
    try:
        url = flask.request.form['url']
        return s(url)
    except:
        return flask.render_template("index.html", pastebin=pastebin)


@app.route("/<urlshort>")
def u(urlshort):
    try:
        with open('uris/' + urlshort, 'r') as f:
            realurl = f.readline()
        os.remove('uris/' + urlshort)
    except:
        return "could not find paste\n"

    cliagents = ['curl', 'Wget']
    if flask.request.headers.get('User-Agent').split('/')[0] not in cliagents \
            and not pastebin:
        return flask.redirect(realurl.rstrip('\n'), code=301)
    else:
        return realurl


def s(url):
    if not pastebin:
        # taken from django
        import re
        regex = re.compile(
            r'^(?:http|ftp)s?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

        if len(url) > 1024 or not regex.match(url):
            return "invalid url\n"

    if not url:
        return "invalid paste\n"

    urlshort = genid()
    try:
        with open('uris/' + urlshort, 'w') as f:
            f.write(url + '\n')
    except:
        return "could not save paste\n"

    if flask.request.headers.get('X-Forwarded-Proto') == 'https':
        return flask.request.url_root.replace('http://', 'https://') \
            + urlshort + '\n'

    return flask.request.url_root + urlshort + '\n'


def genid(size=4, chars=string.ascii_uppercase + string.ascii_lowercase):
    return ''.join(random.choice(chars) for i in range(size))


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000)
