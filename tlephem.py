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

import argparse
import base64
import datetime
import io
import math
import urllib.request
import os
import sys
import ephem

from flask import abort
from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request

def sexagesimal(angle):
    """Formats a decimal number in sexagesimal format"""
    # TODO: Replace with astropy Angle.to_string(sep=':')
    negative = angle < 0
    angle = abs(angle)

    degrees = int(angle)
    angle = (angle - degrees) * 60
    minutes = int(angle)
    seconds = (angle - minutes) * 60

    if negative:
        degrees *= -1

    return '{:d}:{:02d}:{:05.2f}'.format(degrees, minutes, seconds)

# TODO: Generalize this to support other sites
SITE_LATITUDE = 28.7603135
SITE_LONGITUDE = -17.8796168
SITE_ELEVATION = 2387

def generate_ephemeris(name, tle1, tle2, date_str):
    date = datetime.datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S')
    print('name', name)
    print('tle1', tle1)
    print('tle2', tle2)
    print('date', date)
    obs = ephem.Observer()
    # pylint: disable=assigning-non-slot
    obs.lat = SITE_LATITUDE*ephem.degree
    obs.lon = SITE_LONGITUDE*ephem.degree
    obs.elev = SITE_ELEVATION
    obs.date = date
    # pylint: enable=assigning-non-slot

    target = ephem.readtle(name, tle1, tle2)
    target.compute(obs.date)

    return {
        'name': name,
        'date': date.strftime('%Y-%m-%dT%H:%M:%S'),
        'ra': sexagesimal(target.ra * 12 / math.pi),
        'dec': sexagesimal(target.dec * 180 / math.pi),
        'latitude': sexagesimal(target.sublat * 180 / math.pi),
        'longitude': sexagesimal(target.sublong * 180 / math.pi)
    }

def process_input(targets):
    results = []
    for target in targets:
        results.append(generate_ephemeris(target['name'], target['tle1'], target['tle2'], target['date']))
    return jsonify(results)

app = Flask(__name__)

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
