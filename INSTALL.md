##### Notes for deploying on CentOS 8

1. Install dependencies: `nginx`, `uwsgi` (python), `flask` (python), `github-flask` (python), `astropy` (python), `skyfield` (python)
2. Clone the repository to a useful location
3. Edit `tlephem.ini` to set `uid = ` your username
4. Edit `tlephem.service` to point to set
   * `User=` your username
   * `WorkingDirectory=` project location

5. Copy `tlephem.service` to `/usr/lib/systemd/system/`
6. Add user to the `nginx` group: `sudo usermod -a -G <user> nginx`
7. `chmod g+x` each directory in the path to the project
8. Enable and start the service
   ```
   sudo systemctl start tlephem
   sudo systemctl enable tlephem
   ```
9. Create / update nginx config to include:
   ```
    location /tlephem/static {
        alias <project path>/static;
    }

    location /tlephem/ {
        uwsgi_pass unix:<project path>/tlephem.sock;
        uwsgi_param SCRIPT_NAME /tlephem;
        include uwsgi_params;
    }
   ```
10. Enable and start the `nginx` service.
11. Open the firewall if needed
   ```
   sudo firewall-cmd --permanent --zone=public --add-service=http
   sudo firewall-cmd --reload`
   ```