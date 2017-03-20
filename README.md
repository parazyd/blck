blck.cf
=======

a one-click url shortener.


installation
------------

get `python-flask` and execute `blck.py`. by default it starts on
localhost:5000, but you can configure it at the bottom of the script.


usage
-----

either use the website, or curl:

```
curl -F 'url=https://github.com/parazyd/blck.cf' http://blck.cf
```

how does it work?
-----------------

simple enough... sql sucks, so we don't keep the urls in a sqlite or
something, but we rather utilize the filesystem. the script itself is
very short and understandable so give it a look.
