.. _system configuration:

System Configuration
=================================



.. _continuous wal archiving:

Configuring PostgreSQL for Continuous WAL Archiving
----------------------------------------------------------

The following configuration values in the :term:`postgresql.conf` file need to be modified to enable backup protection:

* :ref:`archive_mode`
* :ref:`archive_command`
* :ref:`archive_timeout`

  .. note:: 

     The Postgresql database server **must** be restarted after making these changes.

.. _archive_mode:

archive_mode
~~~~~~~~~~~~
The value of ``archive_mode`` must be set to ``on``::

  archive_mode=on

.. _archive_command:

archive_command
~~~~~~~~~~~~~~~
The value of ``archive_command`` must be set to point to the ``archivewal``
command and use the ``%p`` format (``%p`` is replaced with the relative path to
the WAL file to be archived at runtime)::

  archive_command="/<bbpgsql_install_path>/archivewal %p"

where ``/<bbpgsql_install_path>`` is the absolute path to where the tools are installed.

.. _archive_timeout:

archive_timeout
~~~~~~~~~~~~~~~
The value of ``archive_timeout`` should be set to limit how "old" unarchived
data can be before the server forces a switch to a new WAL segment file, 
regardless of whether the WAL segment file is full, and
archives the data.  This effectively controls the backup window -
the amount of time between changes to the database occuring and those
changes being backed up.

Values of 1-5 minutes (60-300 seconds) are reasonable::

  archive_timeout = 60

.. note::

     WAL files are compressed before being uploaded to S3, so while all WAL
     files (full and non-full) are the same size (16MB by default), non-full
     files tend to have high compression ratios, so upload bandwidth and
     storage are not unreasonable.


.. _configuring periodic snapshots:

Configuring Periodic Snapshots
------------------------------
Continuous backup coverage requires a filesystem snapshot backup of the
PostgreSQL database directories (``data_dir``), and the archiving of WAL
files.  Restoring a database requires restoring the filesytem snapshot,
followed by "replaying" WAL archive files.  To restore to the most recent
version of the database requires "replaying" all WAL files produced since
the filesystem snapshot was taken.  To minimize the restore time, periodic
snapshots should be taken.  The Unix ``Cron`` utility is the most common
way to implement periodic snapshots.

We use the :ref:`archivepgsql` command to create and archive a filesystem
snapshot, which uses the ``pg_backup_start()`` and ``pg_backup_stop()``
PostgreSQL functions.

.. note::

  Continuous WAL archiving (see :ref:`continuous wal archiving`) must be
  enabled before snapshots can be created.


For many applications, a weekly snapshot is adequate.  For other applications,
with more frequent database changes, daily snapshots would be warranted.

Please consult your local ``cron`` and ``crontab`` documentation, but the
following examples should be helpful.

.. note::

  Snapshots must be created by the Unix user that the PostgreSQL
  database server runs as (e.g., "postgres").

Crontab
~~~~~~~

To edit the crontab for the current user::

  $ crontab -e


To edit the crontab for another user, such as the ``postgres`` user::

  $ crontab -u postgres -e

Example Crontab entries
~~~~~~~~~~~~~~~~~~~~~~~

For a Daily snapshot, occuring at 2AM everyday::

    0 2 * * * /<bbpgsql_install_path>/archivepgsql

For a Weekly snapshot, occuring every Sunday at 5:00 AM::

    0 5 * * 0 /<bbpgsql_install_path>/archivepgsql

