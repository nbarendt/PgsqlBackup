.. _intro:

Introduction
======================

.. _theory_of_operation:

Theory of Operation
-------------------

The BitBacker PostgreSQL Backup and Restore Tools are a turnkey, continuous backup and restore solution for Linux PostgreSQL database clusters.  They combine periodic, full-system backups, and continuous Write Ahead Log (WAL) file "log" shipping, storing both the full-system snapshots and the WAL files in `Amazon's Simple Storage Service <http://aws.amazon.com/s3/>`_ (S3).  

.. _gettting_started:

Usage Overview
^^^^^^^^^^^^^^^

The BitBacker PostgreSQL Backup and Restore Tools are installed on a PostgreSQL database server (for Debian/Ubuntu Linux Systems a ".deb" file is provided; for other Linux distributions, please contact BitBacker), a few parameters are set in a configuration file (/etc/bbpgsql.ini), the PostgreSQL database configuration is modified to enable "archive" mode, and a periodic Unix cron task is configured to start periodic database snapshots.  That's it.

The periodic full database snaphots integrate with PostgreSQL WAL "log shipping", with the full database snapshots effectively acting as baseline backups and the WAL files as "delta" backups.

Restoring (or maintaining a Warm Standby Server) is straight-forward, as well, with the BitBacker PostgreSQL Backup and Restore Tools restoring the latest snapshot and "replaying" the WAL files from S3.

.. todo::

    Need a method to test and verify configuration (e.g., encryption, decription)
    are working properly.  Can access S3, etc.
    Maybe some command-line tools to exercise the various subsystems in a
    non-destructive manner.

.. todo::

    Need some warnings about timekeeping on the primary PostgreSQL server.
    Should use NTP or something similar to maintain a relatively accurate
    timebase.

.. todo::
        
    Need some warnings about the bucket and snapshot prefix and WAL prefix 
    being unique for all databases, otherwise data will be clobbered





