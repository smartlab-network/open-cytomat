Welcome to the open-cytomat documentation!
=============================================

.. toctree::
   :maxdepth: 2

This module is an unofficial Python interface for Thermo Fisher Scientific Cytomat devices.

Usage
-----

To control the Cytomat, use the :py:class:`cytomat.Cytomat` class.

The Cytomat class
------------------

.. autoclass:: cytomat.Cytomat

Components
----------

.. autoclass:: cytomat.plate_handler.PlateHandler

.. autoclass:: cytomat.climate_controller.ClimateController

.. autoclass:: cytomat.shaker_controller.ShakerController

.. autoclass:: cytomat.maintenance_controller.MaintenanceController

.. autoclass:: cytomat.barcode_scanner.BarcodeScanner

.. autoclass:: cytomat.swap_station.SwapStation

Status classes
--------------

.. autoclass:: cytomat.status.OverviewStatus
    :exclude-members: index, count

.. autoclass:: cytomat.status.ActionStatus
    :exclude-members: index, count

.. autoclass:: cytomat.status.ActionTarget
    :undoc-members:

.. autoclass:: cytomat.status.ActionType
    :undoc-members:

.. autoclass:: cytomat.status.WarningStatus
    :undoc-members:

.. autoclass:: cytomat.status.ErrorStatus
    :undoc-members:

.. autoclass:: cytomat.status.SwapStationStatus
    :exclude-members: index, count

Serial Port
-----------

.. autoclass:: cytomat.serial_port.SerialPort

Errors
------

.. automodule:: cytomat.errors
    :exclude-members: with_traceback
