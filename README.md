Colorado Gun Deaths
===================

This is a structured beat covering all gun deaths in Colorado. It includes records of homicides, suicides, accidental deaths and officer-involved shootings. The project is a collaboration between the University of Colorado in Boulder and Glass Eye Media LLC.

Codebase layout
---------------

    colorado/
    ├── colorado
    │   ├── apps
    │   │   └── gundeaths
    │   │       ├── __init__.py
    │   │       ├── models.py
    │   │       ├── tests.py
    │   │       └── views.py
    │   ├── settings
    │   │   ├── __init__.py
    │   │   ├── apps.py
    │   │   ├── base.py
    │   │   ├── local.py
    │   │   └── logging.py
    │   ├── templates
    │   │   └── base.html
    │   ├── __init__.py
    │   ├── urls.py
    │   └── wsgi.py
    ├── README.md
    ├── fabfile.py
    ├── manage.py
    └── requirements.txt

All project-specific apps are stored in the `apps` folder. This isn't added to `PYTHONPATH`, so they should be referenced as `colorado.apps.gundeaths`.

Settings are split up into logical chuncks. Everything related to apps is in `apps.py` and so forth. By default, all settings are imported into `__init__.py` so `colorado.settings` just works. For deployment, set `DJANGO_SETTINGS_MODULE` environment variable to a settings file that imports `colorado.settings`.

