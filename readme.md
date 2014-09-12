# Nugacious

Nugacious compares physical quantities. Enter a quantity, and the closest
match, five other randomly chosen close matches, and five completely random
matches are returned. Want more random comparisons? Just reload the page or
click the "Get more comparisons" button.

## Name

Nugacious [noo-**gey**-sh*uh* s] is a synonym of trivial and refers to
the insignificant nature of the quantity comparisons provided.

## Requirements

* Python 3
* Django 1.7

### Python Packages

* numpy
* pint
* simpleeval
* smartypants
* markdown

## Data

Comparisons are made against a set of roughly 700,000 physical quantities
extracted from [DBpedia](http://dbpedia.org/), an ontology created from
Wikipedia infoboxes. Length, area, volume, time, speed, mass, temperature,
power, voltage, frequency, density, and torque are covered to varying degrees.

## License

Nugacious is distributed under the MIT License. For more information, read the
file `COPYING`.

## Credits

Nugacious was built by [Matthew Petroff](//mpetroff.net/) using
[Python](//www.python.org/), [Django](//www.djangoproject.com/),
[Pint](//pint.readthedocs.org/), and [Bootstrap](http://getbootstrap.com/).
The information icon and the more comparisons icon are from
[Font Awesome](http://fontawesome.io/).
