#!/usr/bin/env python3
# copyleft (c) 2017 - parazyd
# see LICENSE file for details
"""
main blck module
"""

import random
import os
import string
import flask


PASTEBIN = False
APP = flask.Flask(__name__)


@APP.route("/", methods=['GET', 'POST'])
def main():
    """ main routine """
    try:
        return short(flask.request.form['url'])
    except:
        return flask.render_template("index.html", pastebin=PASTEBIN)


@APP.route("/<urlshort>")
def urlget(urlshort):
    """ returns a paste if it exists """
    try:
        with open('uris/' + urlshort, 'r') as paste:
            realurl = paste.readline()
        os.remove('uris/' + urlshort)
    except FileNotFoundError:
        return "could not find paste\n"

    cliagents = ['curl', 'Wget']
    if flask.request.headers.get('User-Agent').split('/')[0] not in cliagents \
            and not PASTEBIN:
        return flask.redirect(realurl.rstrip('\n'), code=301)

    return realurl


def short(url):
    """ pasting logic """
    if not PASTEBIN:
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
    with open('uris/' + urlshort, 'w') as paste:
        paste.write(url + '\n')

    if flask.request.headers.get('X-Forwarded-Proto') == 'https':
        return flask.request.url_root.replace('http://', 'https://') \
            + urlshort + '\n'

    return flask.request.url_root + urlshort + '\n'


def genid(size=4, chars=string.ascii_uppercase + string.ascii_lowercase):
    """ returns a random id for a paste """
    return ''.join(random.choice(chars) for i in range(size))


if __name__ == '__main__':
    APP.run(host="127.0.0.1", port=5000)
