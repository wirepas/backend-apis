About
-----

This wheel contains the generated code to interact with the 
Wirepas Mesh services.


Installation
------------

To install the wirepas messaging package start by cloning the repo

::

    git clone git@github.com:wirepas/backend-apis.git


Change directory to backend-apis/wrappers/python and create the wheel and tar files with

::

    ./utils/generate_whell.sh


Afterwards, install the package from the dist folder with

::

    python install dist/wirepas_messaging-*.whl

    or

    python install dist/wirepas_messaging-*.tar


For development mode installation use


::

    pip install -e .


License
------------
Licensed under the Apache License, Version 2.0. See LICENSE for the full license text.

