Command Reference
=============================================

.. _archivepgsql:

archivepgsql
------------

.. program:: archivepgsql

The :program:`archivepgsql` program archives a PostgreSQL database.  It is called like this::

    $ archivepgsql

The operation of the :program:`archivepgsql` is controlled by the
:ref:`configuration_file`.  It accepts no options.

In addition to creating :term:`snapshots` of the PostgreSQL database and uploading them to S3, :ref:`archivepgsql` is also responsible for cleanup.  After completing a snapshot upload, :ref:`archivepgsql` deletes any backup data (:term:`snapshots` and :term:`WAL files` older than ``backup_days`` (see :ref:`config_general`) from S3.

.. _restorepgsql:

restorepgsql
------------

.. program:: restorepgsql

The :program:`restorepgsql` program restores a PostgreSQL database.

The operation of the :program:`restorepgsql` program is controlled by the
:ref:`configuration_file`, but unlike the other programs provided, it is an interactive application, since restoring a PostgreSQL database is a multi-step operation that requires operator intervention and confirmations at various points.

.. _archiveWAL:

archiveWAL
------------

.. program:: archiveWAL

The :program:`archiveWAL` program archives a WAL file and is called like this::
    
    $ archiveWAL absolute_path_to_WAL

where ``absolute_path_to_WAL`` is the absolute path to the WAL file that should be archived.

  .. note::

    This is meant to be used only within the PostgreSQL configuration file
    (:file:`postgresql.conf`) with the ``archive_command`` parameter like so::

      archive_command = '/ABSOLUTE_PATH/archiveWAL %p'

    Please see :ref:`Configuring PostgreSQL for Backup` and `PostgreSQL archive_command <http://www.postgresql.org/docs/8.4/interactive/runtime-config-wal.html#GUC-ARCHIVE-MODE>`_ for more information.


The operation of the :program:`archiveWAL` program is controlled by the
:ref:`configuration_file`.

.. _restoreWAL:

restoreWAL
------------

.. program:: restoreWAL

The :program:`restoreWAL` program restores a WAL file.

The operation of the :program:`restoreWAL` program is controlled by the
:ref:`configuration_file`.


