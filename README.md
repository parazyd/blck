blck.cf
=======

a one-click url shortener.


installation
------------

get `python-flask` and execute `blck.py`. by default it starts on port
5000, but you can use the `-p` switch to specify a port.


usage
-----

either use the website, or curl:

```
curl -F 'url=http://blck.cf' http://blck.cf/s
```

how does it work?
-----------------

simple enough... sql sucks, so we don't keep the urls in a sqlite or
something, but we rather utilize the filesystem. the script itself is
very short and understandable so give it a look.
