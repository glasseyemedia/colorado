"""
Settings related to assets, which are managed via Pipeline.
"""
PIPELINE_CSS = {
    'bootstrap': {
        'source_filenames': (
            'bootstrap/css/bootstrap.css',
            'bootstrap/css/bootstrap-responsive.css',
        ),
        'output_filename': 'css/bootstrap.css'
    }
}