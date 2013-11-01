from datetime import date

from boundaryservice import utils

SHAPEFILES = {
    # This key should be the plural name of the boundaries in this set
    'Counties': {
        # Path to a shapefile, relative to /data/shapefiles
        'file': 'co/counties.shp',
        # Generic singular name for an boundary of from this set
        'singular': 'County',
        # Should the singular name come first when creating canonical identifiers for this set?
        'kind_first': False,
        # Function which each feature wall be passed to in order to extract its "external_id" property
        # The utils module contains several generic functions for doing this
        'ider': utils.simple_namer(['FIPS']),
        # Function which each feature will be passed to in order to extract its "name" property
        'namer': utils.simple_namer(['COUNTY']),
        # Authority that is responsible for the accuracy of this data
        'authority': 'US Census Bureau',
        # Geographic extents which the boundary set encompasses
        'domain': 'Colorado',
        # Last time the source was checked for new data
        'last_updated': date(2013, 11, 1),
        # A url to the source of the data
        'href': 'http://www.nationalatlas.gov/atlasftp-1m.html',
        # Notes identifying any pecularities about the data, such as columns that were deleted or files which were merged
        'notes': '',
        # Encoding of the text fields in the shapefile, i.e. 'utf-8'. If this is left empty 'ascii' is assumed
        'encoding': '',
        # SRID of the geometry data in the shapefile if it can not be inferred from an accompanying .prj file
        # This is normally not necessary and can be left undefined or set to an empty string to maintain the default behavior
        'srid': ''
    },

    'States': {
        'file': 'co/states.shp',
        'singular': 'State',
        'kind_first': False,
        'ider': utils.simple_namer(['STATE_FIPS']),
        'namer': utils.simple_namer(['STATE']),
        'authority': 'US Census Bureau',
        # Geographic extents which the boundary set encompasses
        'domain': 'Colorado',
        # Last time the source was checked for new data
        'last_updated': date(2013, 11, 1),
        # A url to the source of the data
        'href': 'http://www.nationalatlas.gov/atlasftp-1m.html',
        # Notes identifying any pecularities about the data, such as columns that were deleted or files which were merged
        'notes': '',
        # Encoding of the text fields in the shapefile, i.e. 'utf-8'. If this is left empty 'ascii' is assumed
        'encoding': '',
        # SRID of the geometry data in the shapefile if it can not be inferred from an accompanying .prj file
        # This is normally not necessary and can be left undefined or set to an empty string to maintain the default behavior
        'srid': ''
    }
}
