SKOPE Timeseries Service
=========================

This repository contains the source code for the microservice that produces
time series displayed graphically in the SKOPE web application.  The
service is implemented in Java using the Spring Boot framework and is
REST-like.  The service invokes GDAL applications on the service host and
uses GDAL-compatible data files.  A docker image is provided for running the
microservice on any platform that supports Docker without having to install
Java, GDAL, or any other applications on the host.

<!-- This README describes how to configure and run the service; how to invoke the
service using REST calls; and how to build the software, run the service
in a debugger, and perform a set of automated tests on the running service 
during development. -->

Running the Service
-------------------
The recommended way to run the Timeseries Service is using the
[openskope/timeseries-service](https://hub.docker.com/r/openskope/timeseries-service/) 
docker image via Docker Compose.  To start the service run the following command in a 
directory containing a `docker-compose.yml` file:


```
docker-compose up
```

The following is an example of a valid `docker-compose.yml` file for running the timeseries service:

```
version: '3.2'

services:

  timeseries-service:
    image: openskope/timeseries-service:latest
    command: start
    restart: always
    environment:
      TIMESERIES_DATA_PATH_TEMPLATE: /project/SKOPE/data/{datasetId}_{variableName}
      TIMESERIES_UNCERTAINTY_PATH_TEMPLATE: /project/SKOPE/data/{datasetId}_{variableName}_uncertainty
      TIMESERIES_DATA_FILE_EXTENSIONS: .tif .nc .nc4
      TIMESERIES_MAX_PROCESSING_TIME: '5000'
    ports: 
      - 8001:8000
    volumes:
      - /data:/project/SKOPE/data
```


Configuring the service
-----------------------
The timeseries service can be customized via settings in the `docker-compose.yml` file.

#### Specify the port on which the service should be exposed
The timeseries service listens on port 8001 within the running Docker container.   To expose the service outside the container map this port to a port on the host using the `ports` property of the service in the `docker-compose.yml` file as shown in the example above.  In this example the service is exposed on port 8000 of the host.

#### Provide access to data files stored on the host
To make data files on the host accessible to the service running in the docker container, use the `volumes` property in the `docker-compose.yml` file.  In the example above, the host `/data` directory is made available within the container at `/project/SKOPE/data`.

#### Declare the location and naming scheme for data files
A single data file must be provided for each variable of each data set made available via the timeseries service.  The naming convention for these files, and their location on the filesystem (as viewed from within the running container) are specified using the `TIMESERIES_DATA_PATH_TEMPLATE` environment variable.  This variable may be assigned a value in the `docker-compose.yml` file as shown in the example above.

The value given to this environment must represent a filepath template containing two variables, `datasetId` and `variableName`. Each variable must appear in curly braces in the path template, either as part of one of the directory names or in the filename portion of the template.  When a request for a time series from a particular dataset and variable is received by the service, it will expand the data path template using the requested dataset ID and variable name to locate the relevant data file.

The service first will try to find a file with a name that exactly matches the expanded data path template.  If this file does not exist then the service will try alterative file names formed by appending the data file extensions specified by the `TIMESERIES_DATA_FILE_EXTENSIONS` environment variable.  This allows the service to use a single data path template with a set of files with different extensions.  In the example above, the data files may end with `.tif`, `.nc`, or `nc4.`

#### Optionally declare the location of data uncertainties
If the the `TIMESERIES_UNCERTAINTY_PATH_TEMPLATE` variable is assigned a value, the service will use this value as a file path template for finding data files containing the uncertainties associated with each value in the main data file for that variable.  The `datasetId` and `variableName` template variables must be used in this template as well, and the extensions declared via the `TIMESERIES_DATA_FILE_EXTENSIONS` environment variable will be used when matching these files.

#### Specify the timeout value for querying data files
The service invokes GDAL applications to read data files.  The `TIMESERIES_MAX_PROCESSING_TIME` environment variable sets the maximum time allowed, in milliseconds, for executions of these applications.  The service will kill any process that takes longer than this timeout value and return an error to the client.  The default value is 5000 ms.


Using the service
-----------------
A timeseries may be requested from the service either using a GET or a POST request.  

#### GET requests
A GET request must include the dataset ID and variable name as path variables.  If the base URL for timeseries service endpoints is `https://app.openskope.org/timeseries-service/api/v1/` then an example of a valid GET request for the `growing_degree_days` variable of the `paleocar_2` dataset is:

```
GET https://app.openskope.org/timeseries-service/api/v1/timeseries/paleocar_2/growing_degree_days/?longitude=-106.0&latitude=41.0
```

The above request returns the entire 2000-year time series in this dataset at the specified coordinates.  Only time series at single points are supported by GET requests, and the `longitude` and `latitude` query parameters are therefore required.  The full set of supported query parameters for GET requests are summarized in the **Table 1** and described more fully below.

**Table 1** Query line parameters applicable to both GET and POST requests.

Parameter       | Description                                                            | Values 
----------------|------------------------------------------------------------------------|-------
`longitude`     | The longitude of a POINT at which the time series is requested.        |
`latitude`      | The latitude of a POINT at which the time series is requested.         |
`timeResolution`| The units used to refer to time points in the dataset.                 | `index` (default), `band`, or `year`
`timeZero`      | The first (earliest) time point in the data set (in `timeResolution` units).| defaults to 0 (`index`) or 1 (`band` or `year`)
`start`         | First time point in requested time series (in `timeResolution` units). | Defaults to `timeZero`.
`end`           | Last time point in requested time series (in `timeResolution` units).  | Defaults to last time point in data set.
`array`         | Whether to return timeseries as a JSON array in the JSON response body.| `true` (default) or `false` 
`csv`           | Whether to return timeseries as a CSV-formatted string in the JSON response body.| `true` (default) or `false`
`nodata`        | The pixel value to be interpreted to indicate missing data.            |
`timeout`       | The maximum time allowed for producing the time series (milliseconds). |

#### POST requests

All of the query parameters supported by GET requests may be used in the query line of POST requests, in the body of a POST requests, or both.  When query line and POST request body parameter values conflict, the values specified in the body take precedence.

Specifying the dataset ID and variable name as path variables is optional for POST requests. The alternative is assign values to the `datasetID` and `variableName` properties in the POST body.  Thus, the following POST request that includes the dataset ID and variable name in the URL...

```
POST https://app.openskope.org/timeseries-service/api/v1/timeseries/paleocar_2/growing_degree_days
{
    'longitude': -106.0,
    'latitude': 41.0
}
```
...is equivalent to this POST request specifying the dataset and variable in the body:

```
POST https://app.openskope.org/timeseries-service/api/v1/timeseries/
{
    'datasetId': 'paleocar_2',
    'variableName': 'growing_degree_days',
    'longitude': -106.0,
    'latitude': 41.0
}
```

POST requests support the `BoundaryGeometry` property which both provides an alternative method for specifying the coordinates for a point for which a point is requested, and a way to specify a polgyonal region over which to compute an average value of the variable for each time point.

A POST request equivalent to the previous two examples, but using the `BoundaryGeometry` property is:

```
POST https://app.openskope.org/timeseries-service/api/v1/timeseries/
{
    'datasetId': 'paleocar_2',
    'variableName': 'growing_degree_days',
    'boundaryGeometry': {
        'type': 'Point',
        'coordinates': [-106.0, 41.0]
    }
}
```

A POST request for a time series averaged over a 1-degree x 1-degree area is 
```
POST https://app.openskope.org/timeseries-service/api/v1/timeseries/
{
    'datasetId': 'paleocar_2',
    'variableName': 'growing_degree_days',
    'boundaryGeometry': {
        'type': 'Polygon',
        'coordinates': [[
            [-106.0,41.0],
            [-106.0,42.0],
            [-105.0,42.0],
            [-105.0,42.0],
            [-106.0,41.0]
        ]]
    }
}
```

**Table 2** POST body properties.  All of the query parameters in **Table 1** also may be specified as JSON properties in a POST body.

Property                       | Description                                                            | Values 
-------------------------------|------------------------------------------------------------------------|-------
`datasetId`                    | The identifier of the data set for which a time series is requested.   |
`variableName`                 | The identifier of the variable in the data set for which a time series is requested. |
`boundaryGeometry.type`        | Indicates whether the time series is over a point or a region.    | `Point` (default) or `Polygon`.
`boundaryGeometry.coordinates` | For a point an array of the form `[longitude, latitude]`.  For a polygon an array of such points representing the vertices of the polygon. |

