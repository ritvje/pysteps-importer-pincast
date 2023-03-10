# -*- coding: utf-8 -*-
"""Importers for netCDF files.

Import a precipitation field from a NetCDF4 file.
The format of the files is assumed to be the same as produced by the
PINCAST `radar_composite_generator` module.

The metadata contains the following key-value pairs:

.. tabularcolumns:: |p{2cm}|L|

+------------------+----------------------------------------------------------+
|       Key        |                Value                                     |
+==================+==========================================================+
|   projection     | PROJ.4-compatible projection definition                  |
+------------------+----------------------------------------------------------+
|   x1             | x-coordinate of the lower-left corner of the data raster |
+------------------+----------------------------------------------------------+
|   y1             | y-coordinate of the lower-left corner of the data raster |
+------------------+----------------------------------------------------------+
|   x2             | x-coordinate of the upper-right corner of the data raster|
+------------------+----------------------------------------------------------+
|   y2             | y-coordinate of the upper-right corner of the data raster|
+------------------+----------------------------------------------------------+
|   xpixelsize     | grid resolution in x-direction                           |
+------------------+----------------------------------------------------------+
|   ypixelsize     | grid resolution in y-direction                           |
+------------------+----------------------------------------------------------+
|   cartesian_unit | the physical unit of the cartesian x- and y-coordinates: |
|                  | e.g. 'm' or 'km'                                         |
+------------------+----------------------------------------------------------+
|   yorigin        | a string specifying the location of the first element in |
|                  | the data raster w.r.t. y-axis:                           |
|                  | 'upper' = upper border                                   |
|                  | 'lower' = lower border                                   |
+------------------+----------------------------------------------------------+
|   institution    | name of the institution who provides the data            |
+------------------+----------------------------------------------------------+
|   unit           | the physical unit of the data: 'mm/h', 'mm' or 'dBZ'     |
+------------------+----------------------------------------------------------+
|   transform      | the transformation of the data: None, 'dB', 'Box-Cox' or |
|                  | others                                                   |
+------------------+----------------------------------------------------------+
|   threshold      | the rain/no rain threshold with the same unit,           |
|                  | transformation and accutime of the data.                 |
+------------------+----------------------------------------------------------+
|   zerovalue      | the value assigned to the no rain pixels with the same   |
|                  | unit, transformation and accutime of the data.           |
+------------------+----------------------------------------------------------+

"""

# Import the needed libraries
import numpy as np
import rioxarray
import xarray as xr

from pysteps.decorators import postprocess_import


@postprocess_import()
def importer_pincast_netcdf(
    filename, precip_field: str = "RATE", quality_field: str = None, **kwargs
):
    """Import a precipitation field from a NetCDF4 file.

    Import a precipitation field from a NetCDF4 file.
    The format of the files is assumed to be the same as produced by the
    PINCAST `radar_composite_generator` module.
    In general the NetCDF4 files should contain the following variables:

    - precipitation field with name `precip_field` (e.g. RATE)
    - optionally, quality field with name `quality_field` (e.g. QUALITY)
    - x and y coordinates
    - projection information available through ds.spatial_ref.crs_wkt

    Parameters
    ----------
    filename : str
        Name of the file to import.

    precip_field : str
        Name of the precipitation field to import from the netcdf file.

    quality_field : str
        Name of the quality field to import from the netcdf file. If None, no quality is imported.

    {extra_kwargs_doc}

    Returns
    -------
    precipitation : 2D array, float32
        Precipitation field in mm/h. The dimensions are [latitude, longitude].
    quality : 2D array or None
        If no quality information is available, set to None.
    metadata : dict
        Associated metadata (pixel sizes, map projections, etc.).

    """
    # Read dataset from netcdf file
    ds = xr.open_dataset(filename)
    ds = ds.rio.write_crs(ds.spatial_ref.crs_wkt)

    precip = ds[precip_field].data.astype(np.float32).squeeze()

    # Quality field, should have the same dimensions of the precipitation field.
    # Use None is not information is available.
    if quality_field is not None:
        quality = ds[quality_field].data.squeeze()
    else:
        quality = None

    # Adjust the metadata fields according to the file format specifications.
    # For additional information on the metadata fields, see:
    # https://pysteps.readthedocs.io/en/latest/pysteps_reference/io.html#pysteps-io-importers

    # The projection definition is an string with a PROJ.4-compatible projection
    # definition of the cartographic projection used for the data
    # More info at: https://proj.org/usage/projections.html

    # For example:
    try:
        projection_definition = ds.rio.crs.to_proj4()
        unit = ds.rio.crs.data["units"]
    except:
        projection_definition = None
        unit = None

    try:
        institute = ds.attrs["nc.institution"]
    except:
        institute = None

    metadata = dict(
        xpixelsize=np.diff(ds.coords["x"])[0],
        ypixelsize=np.diff(ds.coords["y"])[0],
        cartesian_unit=unit,
        unit="mm/h",
        transform=None,
        zerovalue=0,
        institution=institute,
        projection=projection_definition,
        yorigin="upper",
        threshold=None,
        x1=ds.x.data.min(),
        x2=ds.x.data.max(),
        y1=ds.y.data.min(),
        y2=ds.y.data.max(),
    )

    # IMPORTANT! The importers should always return the following fields:
    return precip, quality, metadata
