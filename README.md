blck
====

an ephemeral pastebin/url-shortener. you can only retrieve the paste or
url once, and afterwards it's deleted from the server.


installation
------------

get `python-flask` and execute `blck.py`. by default it starts on
`localhost:5000`, but you can configure it at the bottom of the script.

if not running in debug mode, you also need `bjoern`. find it at
https://github.com/jonashaag/bjoern.

run `blck.py -h` to see usage info. 


nginx
-----

```
server {
	listen 80;
	listen [::]:80;
	server_name blck.cf;

	location /.well-known/acme-challenge/ {
		alias /tmp/blckssl/;
		try_files $uri =404;
	}

	return 301 https://$server_name$request_uri;
}

server {
	listen 443 ssl;
	listen [::]:443 ssl;
	server_name blck.cf;

	ssl_certificate     /etc/ssl/blck.cf.pem;
	ssl_certificate_key /etc/ssl/blck.cf.key;

	error_log  /var/log/nginx/blck.cf_error.log  warn;
	access_log /var/log/nginx/blck.cf_access.log combined;

	location / {
		proxy_set_header Host $host;
		proxy_set_header X-Real-IP $remote_addr;
		proxy_set_header X-Forwarded-Proto https;
		proxy_pass http://127.0.0.1:5000;
	}
}
```


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
