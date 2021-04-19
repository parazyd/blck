#!/usr/bin/env python3
# copyleft (c) 2017-2021 parazyd <parazyd@dyne.org>
# see LICENSE file for copyright and license details.

from io import BytesIO
from os import remove, rename
from os.path import isfile
from random import choice
from string import ascii_uppercase, ascii_lowercase

from flask import (Flask, Blueprint, render_template, request, safe_join,
                   send_file, abort)
import magic

bp = Blueprint('blck', __name__, template_folder='templates')


@bp.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html', root=args.r)
    return short(request.files)


@bp.route("<urlshort>")
def urlget(urlshort):
    fp = safe_join('files', urlshort)
    if not isfile(fp):
        abort(404)
    r = BytesIO()
    mime = magic.from_file(fp, mime=True)
    with open(fp, 'rb') as fo:
        r.write(fo.read())
    r.seek(0)
    remove(fp)
    return send_file(r, mimetype=mime)


def short(c):
    if not c or not c['c']:
        return abort(400)

    s = genid()
    f = c['c']
    f.save(safe_join('files', s))

    mimetype = f.mimetype
    if not mimetype:
        mimetype = magic.from_file(safe_join('files', s), mime=True)

    if mimetype:
        t, s = s, '.'.join([s, mimetype.split('/')[1]])
        rename(safe_join('files', t), safe_join('files', s))

    if request.headers.get('X-Forwarded-Proto') == 'https':
        return ''.join([
            request.url_root.replace('http://', 'https://'),
            args.r.lstrip('/'), s, '\n'
        ])
    return ''.join([request.url_root + args.r.lstrip('/'), s, '\n'])


def genid(size=4, chars=ascii_uppercase + ascii_lowercase):
    return ''.join(choice(chars) for i in range(size))


if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-r', default='/', help='application root')
    parser.add_argument('-l', default='localhost', help='listen host')
    parser.add_argument('-p', default=13321, help='listen port')
    parser.add_argument('-d', default=False, action='store_true', help='debug')
    args = parser.parse_args()

    app = Flask(__name__)
    app.register_blueprint(bp, url_prefix=args.r)

    if args.d:
        app.run(host=args.l, port=args.p, threaded=True, debug=args.d)
    else:
        from bjoern import run
        run(app, args.l, int(args.p))
