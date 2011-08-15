.. _config_logging:

``[Logging]``
~~~~~~~~~~~~~~

Logging related configuration.

+--------------+-----------+-------------+-----------------------------+
| Key Name     |   Type    |   Default   |  Description                |
+==============+===========+=============+=============================+
| level        |   String  | ``WARNING`` | log warning msgs or higher  |
+--------------+-----------+-------------+-----------------------------+
| logfile      |   String  |    NONE     | log file path (mandatory)   |
+--------------+-----------+-------------+-----------------------------+
| loghistory   |   String  | ``7``       | log file history to keep    |
+--------------+-----------+-------------+-----------------------------+
| loghost      |   String  |  NONE       | syslog hostname (mandatory) |
+--------------+-----------+-------------+-----------------------------+
| logport      |   String  | NONE        | syslog port (mandatory)     |
+--------------+-----------+-------------+-----------------------------+

In order to turn on file logging, a valid path to a logfile must
be specified in the configuration file.  If this key is absent
from the configuration file, no logging will be done to log files.

In order to turn on syslog logging, a valid hostname and port number
must be specified in the configuration file.  If either key is
absent from the configuration file, no logging to syslog will be
performed.

File logs are rotated daily.  By default, seven days of history are
retained.  The length of the retained history may be overridden in
the configuration file by specifying the loghistory key with a
numeric string value of the history depth in days.

By default, logging is performed at the WARNING level of severity
or higher.  This may be overridden using the level key in the
configuration file.  Valid values, from least to most severe are
DEBUG INFO WARNING ERROR CRITICAL.
