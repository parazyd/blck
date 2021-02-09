#!/usr/bin/env python3
# copyleft (c) 2017-2021 parazyd <parazyd@dyne.org>
# see LICENSE file for copyright and license details.

from random import choice
from os import remove
from string import ascii_uppercase, ascii_lowercase

from flask import Flask, Blueprint, render_template, redirect, request

bp = Blueprint('blck', __name__, template_folder='templates')

@bp.route("/", methods=['GET', 'POST'])
def main():
    """ main routine """
    try:
        return short(request.form['url'])
    except:
        return render_template("index.html", pastebin=PASTEBIN, root=args.r)


@bp.route("/<urlshort>")
def urlget(urlshort):
    """ returns a paste if it exists """
    try:
        with open('uris/' + urlshort, 'r') as paste:
            realurl = paste.readline()
        if EPHEMERAL:
            remove('uris/' + urlshort)
    except FileNotFoundError:
        return "could not find paste\n"

    cliagents = ['curl', 'Wget', '']
    if request.headers.get('User-Agent').split('/')[0] not in cliagents \
            and not PASTEBIN:
        return redirect(realurl.rstrip('\n'), code=301)

    return realurl


def short(url):
    """ pasting logic """
    if not PASTEBIN:
        # taken from django
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

    if request.headers.get('X-Forwarded-Proto') == 'https':
        return request.url_root.replace('http://', 'https://') + args.r.lstrip('/') + urlshort + '\n'

    return request.url_root + args.r.lstrip('/') + urlshort + '\n'


def genid(size=4, chars=ascii_uppercase + ascii_lowercase):
    """ returns a random id for a paste """
    return ''.join(choice(chars) for i in range(size))


if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('--pastebin', default=False, action='store_true',
                        help='Use as pastebin rather than URL shortener')
    parser.add_argument('--noephemeral', default=False, action='store_true',
                        help='Do not run in ephemeral mode')
    parser.add_argument('-r', default='/', help='Application root')
    parser.add_argument('-l', default='localhost', help='Listen host')
    parser.add_argument('-p', default=5000, help='Listen port')
    parser.add_argument('-d', default=False, action='store_true', help='Debug')
    args = parser.parse_args()

    EPHEMERAL = not args.noephemeral
    PASTEBIN = args.pastebin
    if not PASTEBIN:
        import re

    app = Flask(__name__)
    app.register_blueprint(bp, url_prefix=args.r)

    if args.d:
        app.run(host=args.l, port=args.p, threaded=True, debug=args.d)
    else:
        from bjoern import run
        run(app, args.l, int(args.p))
