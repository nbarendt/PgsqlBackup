.. _glossary:

Glossary
========

.. glossary::
    :sorted:

    postgresql.conf
        The top-level PostgreSQL configuration file.  Typically
        :file:`/etc/postgresql.conf`.

    configuration file
        The primary configuration file for the BitBacker PostgreSQL Backup and
        Restore Tools.  The :file:`/etc/bbpgsql.ini` file contains the
        configuration used for :ref:`archivepgsql`, :ref:`restorepgsql`,
        :ref:`archivewal`, :ref:`restorewal`.

        See :ref:`configuration_file` for details.

    PostgreSQL
        A very advanced, open-source database system.
        Please see `PostgreSQL`_ for more information.

    write ahead log
        Also known as a Write Ahead Log :term:`WAL files`.

        The on-disk log files that PostgreSQL uses to satisfy durability
        requirements.  WAL files can also be used for backup and restore
        purposes, with a proper archive and restore system, such as provided
        by the BitBacker PostgreSQL Backup and Restore Tools.

    WAL files
        See :term:`write ahead log`.

    snapshots
        Filesystem snapshots of the PostgreSQL database files (e.g.,
        ``data_directory`` of ``postgresql.conf``).

    Amazon Web Services
        A collection of "cloud" services offered by `Amazon`_, including
        :term:`S3`.

    Simple Storage Service
        An :term:`Amazon Web Services` offering that provides inexpensive,
        reliable data storage.  Also known as :term:`S3`.
        See `Amazon Simple Storage Service`_ for
        more information.

    S3
        See :term:`Simple Storage Service`.
    
.. _PostgreSQL: http://www.postgresql.org/

.. _Amazon: http://aws.amazon.com/

.. _Amazon Simple Storage Service: http://aws.amazon.com/s3/




