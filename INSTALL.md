##### Notes for deploying on CentOS 7

Add the `epel` repository and install the `nginx`, `uwsgi`, `uwsgi-python36` packages.
Install the python dependencies `python36-astropy`, `python36-skyfield`.

Clone the repository to a useful location and edit `tlephem.service` to point to it
Copy `tlephem.service` to `/usr/lib/systemd/system/`

Create directories `/srv/sockets`, `/srv/data/` and `chown nginx:nginx` them.

Enable and start the `tlephem` service.

Add to the nginx config
```
location = /tlephem { rewrite ^ /tlephem/; }

location /tlephem/static {
    alias {{PROJECT_PATH}}/static;
}

location /tlephem/ {
    uwsgi_pass unix:/srv/sockets/tlephem.sock;
    uwsgi_param SCRIPT_NAME /tlephem;
    include uwsgi_params;
}
```

Enable and start the `nginx` service.
Open the firewall if needed `sudo firewall-cmd --permanent --zone=public --add-service=http && sudo firewall-cmd --reload`
