
.. |config_file| replace:: :file:`/etc/bbpgsql.ini` 


.. _configuration_file:


Configuration File
------------------

The system must contain a file named |config_file|.

This file uses a simple `INI format <http://en.wikipedia.org/wiki/INI_file>`_: ``name = value``.  Anything from ``#`` to the end of the line is a comment.

Keys (``name``) and sections are case-sensitive.  ``values`` can be continued by indenting::

  [SomeSection]
  name1=hello
  name2=The quick
    brown fox
    jumped over the lazy dog.

All values are strings.  

The file contains one or more sections, such as a "Credentials", with each section beginning with the section name on a line by itself, in square brackets (e.g., ``[Credentials]``).

.. _config_file_permissions:

Configuration File Permissions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It is important that the |config_file| file permissions be carefully set.  It should be owned by the same system account that the PostgreSQL server runs as, and should have have owner read and write permission, and no group or world permissions (e.g., octal permissions of 0600).

.. _config_file_backup:

Backing Up the Configuration File
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. todo::
    The configuration file |config_file| itself should be backed up itself.
    The values contained within are crucial for restoring a database.
    Should we back up the configuration file each time we take a snapshot?


.. _config_sections:

Configuration File Sections and Keys
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following sections detail the Sections that can appear in the
|config_file| file, along with the keys (names) for each section, their default
values, and a brief description.

.. _config_credentials:

``[Credentials]``
~~~~~~~~~~~~~~~~~

This section must contain your Amazon Web Services (AWS) Credentials:

.. literalinclude:: sample_configs/credentials.ini

These fields must contain your AWS Access Key and Secret Keys, respectively.  Please refer to the `Amazon Documention on AWS Security Credentials <http://docs.amazonwebservices.com/AWSSecurityCredentials/1.0/AboutAWSCredentials.html#AccessKeys>`_ for more information.


+---------------------+-----------+-------------+------------------+
| Key Name            |   Type    |   Default   |  Description     |
+=====================+===========+=============+==================+
| aws_access_key_id   |   String  | None        | AWS Access Key   |
+---------------------+-----------+-------------+------------------+
| aws_secret_key_id   |   String  | None        | AWS Secret Key   |
+---------------------+-----------+-------------+------------------+

.. _config_general:

``[General]``
~~~~~~~~~~~~~

General backup configuration.

+----------------------+-----------+-------------+-----------------------------+
| Key Name             |   Type    |   Default   |  Description                |
+======================+===========+=============+=============================+
| bucket               |   String  | None        | S3 Bucket to store snapshots|
|                      |           |             | and WAL files               |
+----------------------+-----------+-------------+-----------------------------+
| pgsql_data_directory | String    | None        | Absolute path to the        |
|                      |           |             | postgresql data directory   |
|                      |           |             | (e.g., value of             |
|                      |           |             | ``data_directory`` in       |
|                      |           |             | ``postgresql.conf``)        |
+----------------------+-----------+-------------+-----------------------------+
| backup_days          | Integer   | 7           | Number of days of backup    |
|                      |           |             | history                     |
|                      |           |             | to retain.  Backup data     |
|                      |           |             | (:term:`snapshots` and      |
|                      |           |             | :term:`WAL files`)          |
|                      |           |             | older                       |
|                      |           |             | than this will be           |
|                      |           |             | deleted during the cleanup  |
|                      |           |             | phase of :ref:`archivepgsql`|
+----------------------+-----------+-------------+-----------------------------+

.. _config_snapshot:

``[Snapshot]``
~~~~~~~~~~~~~~

Snapshot related configuration.

+--------------+-----------+-------------+-----------------------------+
| Key Name     |   Type    |   Default   |  Description                |
+==============+===========+=============+=============================+
| prefix       |   String  |``snapshots``| prefix for snapshots in S3  |
+--------------+-----------+-------------+-----------------------------+

.. _config_WAL:

``[WAL]``
~~~~~~~~~

WAL related configuration.


+--------------+-----------+-------------+-----------------------------+
| Key Name     |   Type    |   Default   |  Description                |
+==============+===========+=============+=============================+
| prefix       |   String  |  ``wals``   | prefix for WAL files in S3  |
+--------------+-----------+-------------+-----------------------------+


.. _config_encryption:

``[Encryption]``
~~~~~~~~~~~~~~~~

Encryption related configuration.

See :ref:`crypto` for more information.

+--------------+-----------+-----------------+---------------------------------+
| Key Name     |   Type    |   Default       |  Description                    |
+==============+===========+=================+=================================+
| cmd          |  String   | ``cat %s > %d`` | Encryption Command              |
|              |           |                 |                                 |
|              |           | (no encryption) | ``%s`` will be replaced by      |
|              |           |                 | the full path to file to encrypt|
|              |           |                 |                                 |
|              |           |                 | ``%d`` will be replaced by      |
|              |           |                 | the full path to where the      |
|              |           |                 | encrypted file should be placed |
|              |           |                 |                                 |
|              |           |                 | use ``%%`` for a literal %      |
+--------------+-----------+-----------------+---------------------------------+

``[Decryption]``
~~~~~~~~~~~~~~~~

Decryption related configuration

See :ref:`crypto` for more information.

+--------------+-----------+-----------------+---------------------------------+
| Key Name     |   Type    |   Default       |  Description                    |
+==============+===========+=================+=================================+
| cmd          |  String   | ``cat %s > %d`` | Decryption Command              |
|              |           |                 |                                 |
|              |           | (no decryption) | ``%s`` will be replaced by      |
|              |           |                 | the full path to file to decrypt|
|              |           |                 |                                 |
|              |           |                 | ``%d`` will be replaced by      |
|              |           |                 | the full path to where the      |
|              |           |                 | decrypted file should be placed |
|              |           |                 |                                 |
|              |           |                 | use ``%%`` for a literal %      |
+--------------+-----------+-----------------+---------------------------------+

