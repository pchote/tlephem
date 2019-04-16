#
# tlephem is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# tlephem is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with tlephem.  If not, see <http://www.gnu.org/licenses/>.

# pylint: disable=invalid-name


import datetime
import os
from skyfield.api import load, Loader, Topos, utc
from skyfield.sgp4lib import EarthSatellite

from astropy.coordinates import Angle, EarthLocation, SkyCoord
from astropy.time import Time
import astropy.units as u

from flask import abort
from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request


app = Flask(__name__)

# Override download directory for data files
if 'TLEPHEM_DATA_DIR' in os.environ:
    load = Loader(os.environ['TLEPHEM_DATA_DIR'])

# TODO: Generalize this to support other sites
# TODO: Deduplicate with EarthLocation
SITE_LATITUDE = '28.7603135N'
SITE_LONGITUDE = '17.8796168 W'
SITE_ELEVATION = 2387
SITE_LOCATION = EarthLocation(
    lat=28.7603135*u.deg,
    lon=-17.8796168*u.deg,
    height=2387*u.m)


def generate_ephemeris(name, tle1, tle2, date_str):
    date = datetime.datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S')
    date = date.replace(tzinfo=utc)
    lst = Time(date, scale='utc', location=SITE_LOCATION).sidereal_time('apparent')

    print('name', name)
    print('tle1', tle1)
    print('tle2', tle2)
    print('date', date)

    observer = Topos(SITE_LATITUDE, SITE_LONGITUDE, elevation_m=SITE_ELEVATION)
    time = load.timescale().utc(date)
    target = EarthSatellite(tle1, tle2, name)
    ra, dec, distance = (target - observer).at(time).radec()
    alt, az, distance = (target - observer).at(time).altaz()

    subpos = target.at(time).subpoint()
    lat = subpos.latitude.degrees
    lon = subpos.longitude.degrees
    if lon > 180:
        lon -= 360

    field = SkyCoord(ra.hours, dec.degrees, unit=(u.hourangle, u.deg))

    time2 = load.timescale().utc(date + datetime.timedelta(seconds=5))
    ra2, dec2, distance2 = (target - observer).at(time2).radec()
    dra = (ra2._degrees - ra._degrees) * 3600 / 5
    ddec = (dec2.degrees - dec.degrees) * 3600 / 5

    return {
        'name': name,
        'date': date.strftime('%Y-%m-%dT%H:%M:%S'),
        'ra': ra.to(u.hourangle).to_string(sep=':'),
        'ha': (lst - field.icrs.ra).wrap_at(12 * u.hourangle).to_string(sep=':', unit=u.hourangle, precision=2),
        'dec': dec.to(u.deg).to_string(sep=':'),
        'dra': round(dra, 3),
        'ddec': round(ddec, 3),
        'alt': round(alt.degrees, 6),
        'az': round(az.degrees, 6),
        'latitude': round(lat, 3),
        'longitude': round(lon, 3)
    }


def process_input(targets):
    results = []
    for target in targets:
        results.append(generate_ephemeris(target['name'], target['tle1'], target['tle2'], target['date']))
    return jsonify(results)


@app.route('/')
def input_display():
    return render_template('input.html')


@app.route('/generate', methods=['POST'])
def generate_json():
    if not request.json:
        abort(500)
    try:
        return process_input(request.json)
    except Exception as e:
        print(e)
        abort(500)
