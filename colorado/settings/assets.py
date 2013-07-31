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
        ),

        'output_filename': 'js/leaflet-plugins.js'
    }
}