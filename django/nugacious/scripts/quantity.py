# Quantity comparisons for Nugacious (http://nugacio.us/)
# (c) 2014, Matthew Petroff (http://mpetroff.net/)

import pickle
import gzip
import re
import random
import string
import fractions
import os
import itertools
import numpy as np
import pint
import simpleeval

class UnsupportedDimensionsError(Exception):
    '''
    Raised when comparator doesn't support the entered dimensions.
    '''
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return self.value

class NoDimensionsError(Exception):
    '''
    Raised when the query is dimensionless.
    '''
    def __init__(self):
        pass

class match(object):
    '''
    A quantity match returned by the comparator.
    '''
    
    def __init__(self, label, wiki, ratio, mag, unit, dimension, category):
        '''
        Sets label, Wikipedia URL, ratio, magnitude, unit, dimension,
        and category.
        '''
        self.label = label
        self.wiki = wiki
        self.ratio = ratio
        self.magnitude = mag
        self.unit = unit
        self.dimension = dimension
        self.category = category
    
    def __str__(self):
        '''
        Returns comma seperated string of match's values
        '''
        return '%s, %s, %f, %s, %s' % (self.label, self.wiki, self.ratio,
            self.magnitude, self.unit, self.dimension, self.category)
    
    def natural_language(self):
        '''
        Returns natural language string describing match.
        '''
        properties = {
            'area.area': 'the area of %s',
            'area.floorArea': 'the floor area of %s',
            'area.surfaceArea': 'the surface area of %s',
            'area.areaLand': 'the land area of %s',
            'area.watershed': 'the watershed area of %s',
            'area.areaMetro': 'the metro area of %s',
            'area.areaOfCatchment': 'the area of catchment of %s',
            'area.areaTotal': 'the total area of %s',
            'area.areaWater': 'the water area of %s',
            'area.areaUrban': 'the urban area of %s',
            'area.campusSize': 'the campus size of %s',
            'area.areaRural': 'the rural area of %s',
            'density.density': 'the density of %s',
            'frequency.frequency': 'the frequency of %s',
            'length.maximumBoatLength': 'the maximum boat length of the %s',
            'length.waistSize': 'the waist size of %s',
            'length.wheelbase': 'the wheelbase of the %s',
            'length.course': 'the course length of the %s',
            'length.mouthElevation': 'the mouth elevation of the %s',
            'length.hipSize': 'the hip size of %s',
            'length.meanRadius': 'the mean radius of %s',
            'length.originalMaximumBoatBeam':
                'the original maximum boat beam of the %s',
            'length.height': 'the height of %s',
            'length.originalMaximumBoatLength':
                'the original maximum boat length of the %s',
            'length.periapsis': 'the periapsis of %s',
            'length.distanceTraveled': 'the distance traveled by the %s',
            'length.bustSize': 'the bust size of %s',
            'length.shipDraft': 'the ship draft of the %s',
            'length.pistonStroke': 'the area of the %s',
            'length.trackLength': 'the area of the %s',
            'length.capitalElevation': 'the capital elevation of %s',
            'length.prominence': 'the topographic prominence of %s',
            'length.minimumElevation': 'the minimum elevation of %s',
            'length.shoreLength': 'the shore length of %s',
            'length.elevation': 'the elevation of %s',
            'length.runwayLength': 'the length of a runway at %s',
            'length.sourceConfluenceElevation':
                'the source confluence elevation of the %s',
            'length.maximumElevation': 'the maximum elevation of %s',
            'length.cylinderBore': 'the cylinder bore of %s',
            'length.railGauge': 'the rail gauge of the %s',
            'length.diameter': 'the diameter of %s',
            'length.maximumBoatBeam': 'the maximum boat beam of the %s',
            'length.depth': 'the depth of %s',
            'length.length': 'the length of %s',
            'length.shipBeam': 'the ship beam of the %s',
            'length.wavelength': 'the wavelength of %s',
            'length.sourceElevation': 'the source elevation of the %s',
            'length.lineLength': 'the length of the %s',
            'length.apoapsis': 'the apoapsis of %s',
            'length.width': 'the width of %s',
            'length.distance': 'the distance of the %s',
            'length.heightAboveAverageTerrain':
                'the height above average terrain of %s\'s transmitter',
            'length.mainspan': 'the mainspan of the %s',
            'length.originalMaximumBoatLength':
                'the original maximum boat length of the %s',
            'length.maximumBoatLength': 'the maximum boat length of the %s',
            'mass.mass': 'the mass of %s',
            'mass.loadLimit': 'the load limit of the %s',
            'mass.weight': 'the weight of %s',
            'mass.shipDisplacement': 'the displacement of the %s',
            'mass.lowerEarthOrbitPayload':
                'the low earth orbit payload capacity of the %s rocket',
            'power.effectiveRadiatedPower':
                'the effective radiated power of %s\'s transmitter',
            'power.powerOutput': 'the power output of the %s',
            'power.installedCapacity': 'the installed capacity of the %s',
            'voltage.voltageOfElectrification':
                'the voltage of electrification of the %s',
            'speed.topSpeed': 'the top speed of the %s',
            'speed.averageSpeed': 'the average speed of %s',
            'speed.escapeVelocity': 'the escape velocity of %s',
            'temperature.minimumTemperature': 'the minimum temperature of %s',
            'temperature.maximumTemperature': 'the maximum temperature of %s',
            'temperature.temperature': 'the temperature of %s',
            'temperature.meanTemperature': 'the mean temperature of %s',
            'time.missionDuration': 'the mission duration of the %s',
            'time.orbitalPeriod': 'the orbital period of %s',
            'time.rotationPeriod': 'the rotation period of %s',
            'time.timeInSpace': 'the time spent in space by %s',
            'time.runtime': 'the runtime of %s',
            'torque.torqueOutput': 'the torque output of the %s',
            'volume.volume': 'the volume of %s',
            'volume.fuelCapacity': 'the fuel capacity of the %s',
            'volume.displacement': 'the displacement of the %s'
        }
        
        ratio = '{:.3g}'.format(self.ratio)
        if re.search('[e]', ratio):
            a = ratio[:ratio.index('e') + 2]  # Strip leading zeros on exponent
            b = ratio[ratio.index('e') + 2:]
            b = re.sub('^(0*)', '', b)
            ratio = '<span>' + a + b + '</sup></span>'
        if self.ratio < 1:
            frac = str(fractions.Fraction(self.ratio).limit_denominator(100))
            if frac != '0':
                f = frac.split('/')
                if len(f) == 2:
                    ratio += ' (<sup>' + f[0] + '</sup>&frasl;<sub>' \
                        + f[1] + '</sub>)'
        
        label = '<a href="' + '//en.wikipedia.org/wiki/' + self.wiki + \
            '">' + self.label + '</a>'
        properties[self.dimension + '.' + self.category] = \
            properties[self.dimension + '.' \
            + self.category].replace("'", '&rsquo;')
        if re.search('[e]', ratio):
            ratio = '(' + ratio + ')'
        ratio = re.sub('(e\+)', ' &times; 10<sup>', ratio)
        ratio = re.sub('(e\-)', ' &times; 10<sup>-', ratio)
        prefix = '&#8776;&thinsp;%s &times; '
        
        mag = '{:.3g}'.format(self.magnitude)
        if re.search('[e]', mag):
            a = mag[:mag.index('e') + 2]
            b = mag[mag.index('e') + 2:]
            b = re.sub('^(0*)', '', b)
            mag = '<span>' + a + b + '</sup></span>'
        mag = re.sub('(e\+)', ' &times; 10<sup>', mag)
        mag = re.sub('(e\-)', ' &times; 10<sup>-', mag)
        suffix = ' <small><span class="text-muted">(%s %s)</span></small>'
        
        units = ''
        for k in self.unit.keys():
            units += '<span>' + k
            if self.unit[k] != 1:
                units += '<sup>' + str(int(self.unit[k])) + '</sup>'
            units += '</span> '
        units = units.strip().replace('_', '&thinsp;')
        
        return (prefix + properties[self.dimension + '.' + self.category]
            + suffix) % (ratio, label, mag, units)

class comparator(object):
    '''
    Compares quantities.
    '''
    
    def __init__(self):
        '''
        Initalizes comparator with pickled data and initalizes unit registry.
        '''
        pkl_file = gzip.open(os.path.join(os.path.dirname(
            os.path.abspath(__file__)), 'data.pkl.gz'), 'rb')
        self.data = pickle.load(pkl_file)
        pkl_file.close()
        
        self.ureg = pint.UnitRegistry()
    
    def compare(self, input_string, close_count=5, random_count=5):
        '''
        Parses quantity described by input string and compares it to other
        quantities. The number of close matches (closest 10% of database) and
        the number of random matches can be specified.
        '''
        
        # Since Pint uses eval, whitelist certain characters for security
        alphabet = string.ascii_letters + string.digits + re.escape(' */^+-.')
        escaped_string = re.sub('[^' + alphabet + ']', '', input_string)
        
        # Parse number words
        nums = {
            'zero': 0,
            'one': 1,
            'two': 2,
            'three': 3,
            'four': 4,
            'five': 5,
            'six': 6,
            'seven': 7,
            'eight': 8,
            'nine': 9,
            'ten': 10,
            'eleven': 11,
            'twelve': 12,
            'thirteen': 13,
            'fourteen': 14,
            'fifteen': 15,
            'sixteen': 16,
            'seventeen': 17,
            'eighteen': 18,
            'nineteen': 19,
            'twenty': 20,
            'thirty': 30,
            'forty': 40,
            'fifty': 50,
            'sixty': 60,
            'seventy': 70,
            'eighty': 80,
            'ninety': 90,
            'hundred': 1e2,
            'thousand': 1e3,
            'million': 1e6,
            'billion': 1e9,
            'trillion': 1e12,
            'quadrillion': 1e15,
            'quintillion': 1e18,
            'sextillion': 1e21,
            'septillion': 1e24,
            'octillion': 1e27,
            'nonillion': 1e30,
            'decillion': 1e33,
            'dozen': 12,
            'gross': 144
        }

        # Replace number words with numerals
        s = escaped_string.replace('-', ' ')
        s = s.replace('stone', 'rock')  # Escape stone unit
        for n in nums:
            r = re.compile(re.escape(n), re.IGNORECASE)
            s = r.sub('*' + '{:f}'.format(nums[n]), s)
        s = s.replace('rock', 'stone')  # Unescape stone unit
        if (s[0] == '*'):
            s = '1' + s
        
        # Allow caret power notation to work
        s = s.replace('^', '**')

        # Split at first remaining letter
        i = re.search('[^a-zA-Z]*', s).end()
        
        # Parse numerical expression
        if i != 0:
            s = s.replace(s[:i], str(simpleeval.simple_eval(s[:i])) + ' ')
        
        # Parse escaped input expression
        try:
            q = self.ureg.parse_expression(s)
        except pint.UndefinedUnitError:
            split = s.split(' ')
            length = len(split) - 1
            for i in itertools.product("_ ", repeat=length):
                joined = split[0]
                for j in range(length):
                    joined += i[j] + split[j+1]
                try:
                    q = self.ureg.parse_expression(joined)
                    break
                except pint.UndefinedUnitError:
                    pass
            if 'q' not in vars():
                self.ureg.parse_expression(s)

        if not hasattr(q, 'magnitude'):
            raise NoDimensionsError()
        
        # Input interpretation
        mag = '{:.3g}'.format(q.magnitude)
        if re.search('[e]', mag):
            a = mag[:mag.index('e') + 2]
            b = mag[mag.index('e') + 2:]
            b = re.sub('^(0*)', '', b)
            mag = '<span>' + a + b + '</sup></span>'
        mag = re.sub('(e\+)', ' &times; 10<sup>', mag)
        mag = re.sub('(e\-)', ' &times; 10<sup>-', mag)
        units = ''
        for k in q.units.keys():
            units += '<span>' + k
            if q.units[k] != 1:
                units += '<sup>' + str(int(q.units[k])) + '</sup>'
            units += '</span> '
        units = units.strip().replace('_', '&thinsp;')
        input_interp = '%s %s' % (mag, units)
        
        base_units = {
            'area': (self.ureg.meter ** 2),
            'density': (self.ureg.kilogram / self.ureg.meter ** 3),
            'frequency': (self.ureg.hertz),
            'length': (self.ureg.meter),
            'mass': (self.ureg.gram),
            'power': (self.ureg.watt),
            'voltage': (self.ureg.volt),
            'speed': (self.ureg.kph),
            'temperature': (self.ureg.kelvin),
            'time': (self.ureg.second),
            'torque': (self.ureg.newton * self.ureg.meter),
            'volume': (self.ureg.meter ** 3)
        }
        
        dimension = None
        for u in base_units:
            if hasattr(q, 'dimensionality') \
                and base_units[u].dimensionality == q.dimensionality:
                qb = q.to(base_units[u].units)
                dimension = u
                break
        if not dimension:
            raise UnsupportedDimensionsError(input_interp)
        
        # Either closest or 2nd closest value (good enough and very fast)
        index = np.searchsorted(self.data[dimension][2], qb.magnitude)
        index = min(index, len(self.data[dimension][2]) - 1)
        index = max(index, 0)
        closest_match = match(self.data[dimension][0][index],
            self.data[dimension][1][index],
            qb.magnitude / self.data[dimension][2][index],
            (self.data[dimension][2][index]
            * base_units[u]).to(q.units).magnitude,
            q.units, dimension, self.data[dimension][3][index])
        
        # Close comparisons
        close_matches = []
        for i in range(close_count):
            while True:
                length = len(self.data[dimension][2])
                dist = min(250, int(0.05 * length))
                ri = index + random.randint(-dist, dist)
                if ri >= 0 and ri < length:
                    break
            close_matches.append(match(self.data[dimension][0][ri],
                self.data[dimension][1][ri],
                qb.magnitude / self.data[dimension][2][ri],
                (self.data[dimension][2][ri]
                * base_units[u]).to(q.units).magnitude,
                q.units, dimension, self.data[dimension][3][ri]))
        
        # Random comparisons
        random_matches = []
        for i in range(random_count):
            ri = random.randint(0, len(self.data[dimension][2]) - 1)
            random_matches.append(match(self.data[dimension][0][ri],
                self.data[dimension][1][ri],
                qb.magnitude / self.data[dimension][2][ri],
                (self.data[dimension][2][ri]
                * base_units[u]).to(q.units).magnitude,
                q.units, dimension, self.data[dimension][3][ri]))
        
        return input_interp, closest_match, close_matches, random_matches

    def statistics(self):
        '''
        Returns size of quantity database.
        '''
        quantity_count = 0
        for t in self.data:
            quantity_count += len(self.data[t][2])
        return quantity_count
