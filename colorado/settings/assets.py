"""
Settings related to assets, which are managed via Pipeline.
"""
PIPELINE_CSS = {
    'site': {
        'source_filenames': (
            #'bootstrap/css/bootstrap.css',
            'bootstrap/css/journal.css',
            'bootstrap/css/bootstrap-responsive.css',
        ),
        
        'output_filename': 'css/site.css'
    },

    'leaflet': {
        'source_filenames': (
            'components/leaflet.markerclusterer/dist/MarkerCluster.css',
            'components/leaflet.markerclusterer/dist/MarkerCluster.Default.css',
        ),

        'output_filename': 'css/leaflet.css'
    }
}

PIPELINE_JS = {
    'leaflet': {
        'source_filenames': (
            'components/leaflet.markerclusterer/dist/leaflet.markercluster.js',
            'components/underscore/underscore.js',
            'jst/*.jst',
        ),

        'output_filename': 'js/leaflet-plugins.js'
    },

    'd3': {
        'source_filenames': (
            'components/underscore/underscore.js',
            'components/d3/d3.min.js',
            'components/colorbrewer/colorbrewer.js',
            'components/nvd3/nv.d3.js'
        ),

        'output_filename': 'js/d3-components.js'
    }
}