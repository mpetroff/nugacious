#!/usr/bin/env python3

# Query DBpedia quantity data
# (c) 2014, Matthew Petroff (http://mpetroff.net/)

import os
import csv
from SPARQLWrapper import SPARQLWrapper, JSON

sparql = SPARQLWrapper('http://dbpedia.org/sparql')
sparql.setReturnFormat(JSON)

properties = [
    ['area', 'area'],
    ['area', 'floorArea'],
    ['area', 'surfaceArea'],
    ['area', 'areaLand'],
    ['area', 'watershed'],
    ['area', 'areaMetro'],
    ['area', 'areaOfCatchment'],
    ['area', 'areaTotal'],
    ['area', 'areaWater'],
    ['area', 'areaUrban'],
    ['area', 'campusSize'],
    ['area', 'areaRural'],
    ['density', 'density'],
    ['frequency', 'frequency'],
    ['length', 'maximumBoatLength'],
    ['length', 'waistSize'],
    ['length', 'wheelbase'],
    ['length', 'course'],
    ['length', 'mouthElevation'],
    ['length', 'hipSize'],
    ['length', 'meanRadius'],
    ['length', 'originalMaximumBoatBeam'],
    #['length', 'governmentElevation'],
    ['length', 'height'],
    ['length', 'originalMaximumBoatLength'],
    ['length', 'periapsis'],
    ['length', 'distanceTraveled'],
    #['length', 'managementElevation'],
    ['length', 'bustSize'],
    ['length', 'shipDraft'],
    ['length', 'pistonStroke'],
    ['length', 'trackLength'],
    ['length', 'capitalElevation'],
    ['length', 'prominence'],
    ['length', 'minimumElevation'],
    ['length', 'shoreLength'],
    ['length', 'elevation'],
    ['length', 'runwayLength'],
    ['length', 'sourceConfluenceElevation'],
    ['length', 'maximumElevation'],
    ['length', 'cylinderBore'],
    ['length', 'railGauge'],
    ['length', 'diameter'],
    ['length', 'maximumBoatBeam'],
    ['length', 'depth'],
    ['length', 'length'],
    ['length', 'shipBeam'],
    ['length', 'wavelength'],
    ['length', 'sourceElevation'],
    ['length', 'lineLength'],
    ['length', 'apoapsis'],
    ['length', 'width'],
    ['length', 'distance'],
    ['length', 'heightAboveAverageTerrain'],
    ['length', 'mainspan'],
    ['length', 'originalMaximumBoatLength'],
    ['length', 'maximumBoatLength'],
    ['mass', 'mass'],
    ['mass', 'loadLimit'],
    ['mass', 'weight'],
    ['mass', 'shipDisplacement'],
    ['mass', 'lowerEarthOrbitPayload'],
    ['power', 'effectiveRadiatedPower'],
    ['power', 'powerOutput'],
    ['power', 'installedCapacity'],
    ['voltage', 'voltageOfElectrification'],
    ['speed', 'topSpeed'],
    ['speed', 'averageSpeed'],
    ['speed', 'escapeVelocity'],
    ['temperature', 'minimumTemperature'],
    ['temperature', 'maximumTemperature'],
    ['temperature', 'temperature'],
    ['temperature', 'meanTemperature'],
    ['time', 'missionDuration'],
    ['time', 'orbitalPeriod'],
    ['time', 'rotationPeriod'],
    ['time', 'timeInSpace'],
    ['time', 'runtime'],
    ['torque', 'torqueOutput'],
    ['volume', 'volume'],
    ['volume', 'fuelCapacity'],
    ['volume', 'displacement']
]

os.mkdir('data')

for p in properties:
    print('querying', p[0] + '.' + p[1])
    
    sparql.setQuery('''
        PREFIX : <http://dbpedia.org/resource/>
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX dbp: <http://dbpedia.org/property/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        
        SELECT ?label, ?wiki, ?value WHERE {
            ?p dbo:''' + p[1] + ''' ?value .
            ?p foaf:isPrimaryTopicOf ?wiki .  
            ?p rdfs:label ?label .
            FILTER (lang(?label) = "en")
        }
    ''')
    
    results = sparql.query().convert()
    array = []
    
    with open('data/' + p[0] + '.' + p[1] + '.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        for result in results['results']['bindings']:
            writer.writerow([result['label']['value'], result['wiki']['value'],
                result['value']['value']])
