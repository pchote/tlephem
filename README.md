A Flask + Bootstrap + jQuery frontend for calculating sky coordinates from two-line elements (TLEs) using pyephem.

Run locally using:
```
export FLASK_APP=tlephem
python -m flask run
```
or see INSTALL.md for some (far too) brief notes on how to install as a permanent service.

Depends on the `flask` and `ephem` python modules, which can be installed using `pip`.