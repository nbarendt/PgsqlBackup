.. _tutorial:

Tutorial
========

.. _installation:

Installing BBPGSQL
------------------

BBPGSQL is provided in the form of a Debian package and should be
installed using sudo and dpkg:

    sudo dpkg -i bbpgsql_0.4.0-rc1-1_i386.deb

Initial Configuration and Setup
-------------------------------

bbpgsql
~~~~~~~

.. todo:: drop sample file inline in this section (try literalinclude::)

Edit the sample /etc/bbpgsql.ini (shown below) configuration file as the PostgreSQL user.

Sample Configuration File
_________________________
.. literalinclude:: sample_configs/bbpgsql.ini

At a minimum, the following options must be configured:

    1. **aws_access_key_id** should be set to your AWS access key.
    2. **aws_secret_key_id** should be set to your AWS secret key.
    3. **bucket** should be set to the string identifying the S3 bucket for the archives.
    4. **pgsql_data_directory** should be set to the same value as the data_directory in the PostgreSQL configuration file.

If logging is desired, either or both of the following two sets of options should be set:

.. todo:: reformat following two sections to be lower level in outline, unordered list, or something

.. todo:: make all configuration options (e.g., "logfile") obvious in documentation (either italics, or a reference link to the detailed doc for the option)

File Logging
````````````

    1. **logifle** should be set to the base filename for the bbpgsql log file.

Syslog Logging
``````````````

    1. **loghost** should be set to the hostname for the syslog host
    2. **logport** should be set to the proper port number for the syslog host.  Note that this will vary with the specific syslog facility and OS.

All remaining options have default values and may be set as needed by the database administrator.  The **logtcp** option is available to perform logging over TCP instead of UDP (the default).  **logfacility** exists to route log messages to the proper logging facility.  Consult your system documentation for more information.

Important:  make sure the /etc/bbpgsql.ini file is owned by the PostgreSQL user account and has permission restricting it to user access only (i.e. not group or world accessible).  It contains AWS credentials and needs to be kept private.  The bbpgsql tools check the file's permissions and will exit with an error if the permissions are incorrect.

Important:  make sure that the /etc/bbpgsql.ini file is correctly installed by running the storagestats utility as the PostgreSQL user before configuring the PostgreSQL server for continuous WAL archiving.

PostgreSQL
~~~~~~~~~~

Set up the PostgreSQL server to do Continuous Archive Backup (see the PostgreSQL documentation, Server Administration, Backup and Restore).

.. todo:: highlight postgres configuration options below (e.g., italics)

As the PostgreSQL user, edit the postgres.conf file and set the following options:

    1.  set archive_mode to on
    2.  set archive_command to the string '/usr/bin/archivewal %p'
    3.  set archive_timeout to the maximum number of seconds the server will wait before archiving the current WAL segment and starting a new one.  Values between 60 and 300 seconds (1 to 5 minutes) are reasonable.  Note that a high traffic server will archive segments more often than this.

.. note:: changing these settings will require PostgreSQL to be restarted.

Initial Snapshot
~~~~~~~~~~~~~~~~

As the PostgreSQL user, run the archivepgsql command to create an initial snapshot of the data directory.  If you configured logging in the above section, you should see the activity being reported.  If the command fails, please see :doc:`/troubleshooting`.

.. todo:: add a few of the most common errors and how to resolve them to the troubleshooting section.

Periodic Snapshots
~~~~~~~~~~~~~~~~~~

Configure your server to use the archivepgsql command to create periodic snapshots of the server data directory.  The cron utility can be used for this purpose.

Verify BBPGSQL Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Run storagestats again to verify that things are set up correctly and the snapshots and WAL files are being archived to S3.

Restoring the latest backup
---------------------------

.. todo:: format the postgres doc references so they're clearly documents and chapters (e.g., underline doc names, quote chapter names, etc.).  Maybe include links for a few major releases, e.g., 8.3, 8.4, 9.X)?

This tutorial assumes you are restoring to the production server or an exact duplicate.  Consult the PostgreSQL documentation for insights into restoring on non-identical hardware and software.

.. todo:: make these an ordered list of steps?

.. todo:: just a thought, borrow the steps in the postgres manual, and expand with our stuff?  e.g., take the exact text from postgres 8.4 restore manual, and stich in our operations in a different color text or something?

Consult the PostgreSQL documentation, Server Administration, Backup and Restore, Recovering Using a Continuous Archive Backup, for the standard procedure for preparing a server for a full restore.  This includes backing up the existing data directory or, at a minimum, any unarchived WAL files.  It may also include modifying the pg_hba.conf file to disallow ordinary users from connecting until the restore is complete.

With the server cluster data directory completely empty, run restorepgsql as the PostgreSQL user account.  This will download and restore the latest snapshot from S3.

Remove the contents of the pg_xlog directory in the server cluster data directory and then copy any unarchived WAL segments saved earlier into the now empty pg_xlog directory.

Create the recovery.conf file in the cluster data directory, setting the restore_command option to the string '/usr/bin/restorewal %f %p'.  This is the only required setting in recovery.conf.

Start the PostgreSQL server and wait until it completes recovery.

Verify that the restore worked.

.. todo:: add steps like, if you modified pg_hba.conf, restore its previous settings?

.. todo::

    Write Tutorial(s).
    Possibly: setting up a warm-standby, and taking a warm-standby live.
