BitBacker PostgreSQL Backup and Restore Tools
=============================================

.. _archivepgsql:

archivepgsql
------------

.. program:: archivepgsql

The :program:`archivepgsql` program archives a PostgreSQL database.  It is called like this::

    $ archivepgsql

The operation of the :program:`archivepgsql` is controlled by the
:term:`configuration file`.

.. _restorepgsql:

restorepgsql
------------

.. program:: restorepgsql

The :program:`restorepgsql` program restores a PostgreSQL database.

The operation of the :program:`restorepgsql` program is controlled by the
:term:`configuration file`.

.. _archiveWAL:

archiveWAL
------------

.. program:: archiveWAL

The :program:`archiveWAL` program archives a WAL file.

The operation of the :program:`archiveWAL` program is controlled by the
:term:`configuration file`.

.. _restoreWAL:

restoreWAL
------------

.. program:: restoreWAL

The :program:`restoreWAL` program restores a WAL file.

The operation of the :program:`restoreWAL` program is controlled by the
:term:`configuration file`.


.. _configuration file:

Configuration File
------------------

The system must contain a file named :file:`/etc/bbpgsql.ini`.

This file uses a simple `INI format <http://en.wikipedia.org/wiki/INI_file>`_: ``name = value``.  Anything from ``#`` to the end of the line is a comment.

Keys (``name``) and sections are case-sensitive.  ``values`` can be continued by indenting::

  [SomeSection]
  value1=hello
  value2=The quick
    brown fox
    jumped over the lazy dog.

All values are strings.  

The file contains one or more sections, such as a "Credentials", with each section beginning with the section name on a line by itself, in square brackets (e.g., ``[Credentials]``).

.. _config_file_permissions:

Configuration File Permissions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It is important that the :file:`/etc/bbpgsql.ini` file permissions be carefully set.  It should be owned by the same system account that the PostgreSQL server runs as, and should have have owner read and write permission, and no group or world permissions (e.g., octal permissions of 0600).

.. _config_credentials:

``[Credentials]``
~~~~~~~~~~~~~~~~~

This section must contain your Amazon Web Services (AWS) Credentials:

.. literalinclude:: sample_configs/credentials.ini

These fields must contain your AWS Access Key and Secret Keys, respectively.  Please refer to the `Amazon Documention on AWS Security Credentials <http://docs.amazonwebservices.com/AWSSecurityCredentials/1.0/AboutAWSCredentials.html#AccessKeys>`_ for more information.


``[SomeOtherSection]``
~~~~~~~~~~~~~~~~~~~~~~

some other stuff

