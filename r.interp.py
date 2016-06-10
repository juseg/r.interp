#!/usr/bin/env python

"""
MODULE:     r.interp

AUTHOR(S):  Julien Seguinot <seguinot@vaw.baug.ethz.ch>.

PURPOSE:    Fill data holes using 2D interpolation.

COPYRIGHT:  (c) 2016 Julien Seguinot

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

# Todo:
# * (0.1)
#  - upload to GRASS repo/wiki
#  - add minimal HTML docs

#%Module
#% description: Fill data holes using 2D interpolation.
#% keywords: raster interpolation
#%End

#%option
#% key: input
#% type: string
#% gisprompt: old,cell,raster
#% description: Name of input raster map
#% required: yes
#%end
#%option
#% key: output
#% type: string
#% gisprompt: new,cell,raster
#% description: Name for output raster map
#% required: yes
#%end
#%option
#% key: method
#% type: string
#% description: Interpolation method
#% required : no
#% options: linear, nearest, cubic
#% answer: linear
#%end


import numpy as np                      # [1]
from scipy.interpolate import griddata  # [2]
import grass.script as grass
import grass.script.array as garray


def main():
    """Main function, called at execution time."""

    # parse arguments
    input = options['input']
    output = options['output']
    method = options['method']

    # read map with grass array
    a = garray.array(dtype='f4')
    a.read(input)

    # points with existing data
    points = np.nonzero(a)
    data = a[points]

    # interpolation grid
    rows, cols = a.shape
    gridx, gridy = np.mgrid[0:rows, 0:cols]  # WORKS!

    # interpolate and write map
    a[...] = griddata(points, data, (gridx, gridy), method=method)
    a.write(output)

    return


if __name__ == "__main__":
    options, flags = grass.parser()
    main()

# Links
# [1] http://numpy.scipy.org
# [2] http://www.scipy.org

