##### Notes for deploying on OpenSUSE

Install nginx, uwsgi, uwsgi-python3 packages (need server repo enabled).

Clone the repository to /srv/tlephem/appdata/ and chown -R nginx:nginx
Move config/tlephem.ini to /etc/uwsgi/vassals/ (uWSGI Emperor config file)
Move config/tlephem.conf to /etc/nginx/conf.d/ (nginx config file)

Open port 80 in the firewall by setting `FW_SERVICES_EXT_TCP="80"` in /etc/sysconfig/SuSEfirewall2

Enable and start services

```
systemctl enable nginx uwsgi
systemctl start nginx uwsgi
systemctl restart SuSEfirewall2
```

