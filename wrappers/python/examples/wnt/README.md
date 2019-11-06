# WNT API Examples

This folder contains the Wirepas Network Tool API Examples. These examples show how to interact with
the server using authentication, metadata and real time situation connections.

Please note that these examples should not be taken as production quality, but more
as the examples about the message flow and content.

## Requirements

Before running the examples please ensure that the
[wirepas_messaging](https://github.com/wirepas/backend-apis/tree/master/wrappers/python)
package is installed.

## WNT backend settings

For running the examples, WNT backend connection parameters must be given by creating settings.yml
file to the same folder from where the examples are run.

### Example settings file

```yaml
username: "username"
password: "password"
hostname: "wntbackend.mydomain.com"
```

## Examples

-   [applicationconfiguration.py][applicationconfiguration.py_link]
    -   Wirepas mesh application configuration and diagnostics interval setting \*

-   [authentication.py][authentication.py_link]
    -   Authentication and user querying, creation, updating and deletion.

-   [building.py][building.py_link]
    -   Building querying, creation, updating and deletion

-   [componentsinformation.py][componentsinformation.py_link]
    -   Component information querying

-   [floorplan.py][floorplan.py_link]
    -   Floor plan querying, creation, updating, deletion. Getting and setting of floor plan image and thumbnail.

-   [floorplanarea.py][floorplanarea.py_link]
    -   Floor plan area querying, creation, updating and deletion

-   [network.py][network.py_link]
    -   Network name querying, creation, updating and deletion

-   [node.py][node.py_link]
    -   Setting node metadata and adding node to floor plan

-   [nodedatamessage.py][nodedatamessage.py_link]
    -   Sending Wirepas mesh data message to node \*

-   [realtimedata.py][realtimedata.py_link]
    -   Connecting to the real time situation service and decoding protocol buffers messages \*

-   [scratchpadstatus.py][scratchpadstatus.py_link]
    -   Querying scratchpad status from the nodes \*

\*) Requires working Wirepas mesh network connected to the WNT backend

## Running an example

```shell
    # Run from folder where settings.yml resides
    python3 backend-apis/wrappers/python/examples/wnt/authentication.py
```

## License

Licensed under the Apache License, Version 2.0. See LICENSE for the full
license text.

[applicationconfiguration.py_link]: https://github.com/wirepas/backend-apis/tree/master/wrappers/python/examples/wnt/applicationconfiguration.py

[authentication.py_link]: https://github.com/wirepas/backend-apis/tree/master/wrappers/python/examples/wnt/authentication.py

[building.py_link]: https://github.com/wirepas/backend-apis/tree/master/wrappers/python/examples/wnt/building.py

[componentsinformation.py_link]: https://github.com/wirepas/backend-apis/tree/master/wrappers/python/examples/wnt/componentsinformation.py

[floorplan.py_link]: https://github.com/wirepas/backend-apis/tree/master/wrappers/python/examples/wnt/floorplan.py

[floorplanarea.py_link]: https://github.com/wirepas/backend-apis/tree/master/wrappers/python/examples/wnt/floorplanarea.py

[network.py_link]: https://github.com/wirepas/backend-apis/tree/master/wrappers/python/examples/wnt/network.py

[node.py_link]: https://github.com/wirepas/backend-apis/tree/master/wrappers/python/examples/wnt/node.py

[nodedatamessage.py_link]: https://github.com/wirepas/backend-apis/tree/master/wrappers/python/examples/wnt/nodedatamessage.py

[realtimedata.py_link]: https://github.com/wirepas/backend-apis/tree/master/wrappers/python/examples/wnt/realtimedata.py

[scratchpadstatus.py_link]: https://github.com/wirepas/backend-apis/tree/master/wrappers/python/examples/wnt/scratchpadstatus.py
