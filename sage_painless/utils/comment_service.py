class CommentService:
    # help comments using in gunicorn-conf.py template
    GUNICORN_CONFIG_COMMENTS = {
        'bind': 'bind - The server socket to bind',
        'backlog': 'backlog - The maximum number of pending connections (Generally in range 64-2048)',
        'workers': 'workers - The number of worker processes for handling requests (A positive integer generally in '
                   'the 2-4 x $(NUM_CORES) range)',
        'worker_class': 'worker_class - The type of workers to use. A string referring to one of the following '
                        'bundled classes 1. sync 2. eventlet - Requires eventlet >= 0.9.7 3. gevent - Requires '
                        'gevent >= 0.13 4. tornado - Requires tornado >= 0.2 5. gthread - Python 2 requires the '
                        'futures package to be installed 6. uvicorn - uvicorn.workers.UvicornWorker ',
        'threads': 'threads - The number of worker threads for handling requests. This will run each worker with the '
                   'specified number of threads. A positive integer generally in the 2-4 x $(NUM_CORES) range ',
        'worker_connections': 'worker_connections - The maximum number of simultaneous clients.This setting only '
                              'affects the Eventlet and Gevent worker types.',
        'max_requests': 'max_requests - The maximum number of requests a worker will process. Any value greater than '
                        'zero will limit the number of requests a work will process before automatically restarting. '
                        'This is a simple method to help limit the damage of memory leaks ',
        'max_requests_jitter': 'max_requests_jitter - The maximum jitter to add to the max-requests setting',
        'timeout': 'timeout - Workers silent for more than this many seconds are killed and restarted',
        'graceful_timeout': 'graceful_timeout - Timeout for graceful workers restart. How max time worker can handle '
                            'request after got restart signal. If the time is up worker will be force killed. ',
        'keep_alive': 'keep_alive - The number of seconds to wait for requests on a Keep-Alive connection (Generally '
                      'set in the 1-5 seconds range.) ',
        'limit_request_line': 'limit_request_line - The maximum size of HTTP request line in bytes. Value is a number '
                              'from 0 (unlimited) to 8190. This parameter can be used to prevent any DDOS attack. ',
        'limit_request_fields': 'limit_request_fields - Limit the number of HTTP headers fields in a request. This '
                                'parameter is used to limit the number of headers in a request to prevent DDOS '
                                'attack. Used with the limit_request_field_size it allows more safety. By default '
                                'this value is 100 and can’t be larger than 32768. ',
        'reload': 'reload - Restart workers when code changes',
        'reload_engine': 'reload_engine - The implementation that should be used to power reload.',
        'reload_extra_files': 'reload_extra_files - Extends reload option to also watch and reload on additional '
                              'files (e.g., templates, configurations, specifications, etc.) ',
        'spew': 'spew - Install a trace function that spews every line executed by the server',
        'check_config': 'check_config - Check the configuration',
        'preload_app': 'preload_app - Load application code before the worker processes are forked',
        'sendfile': 'sendfile - Enables or disables the use of sendfile()',
        'reuse_port': 'reuse_port - Set the SO_REUSEPORT flag on the listening socket.',
        'chdir': 'chdir - Chdir to specified directory before apps loading',
        'daemon': 'daemon - Daemonize the Gunicorn process.',
        'raw_env': 'raw_env - Set environment variable (key=value)',
        'pidfile': 'pidfile - A filename to use for the PID file. If not set, no PID file will be written.',
        'worker_tmp_dir': 'worker_tmp_dir - A directory to use for the worker heartbeat temporary file. If not set, '
                          'the default temporary directory will be used.',
        'user': 'user - Switch worker processes to run as this user. A valid user id (as an integer) or the name of a '
                'user that can be retrieved.',
        'group': 'group - Switch worker process to run as this group.',
        'umask': 'umask - A bit mask for the file mode on files written by Gunicorn. Note that this affects unix '
                 'socket permissions.',
        'initgroups': 'initgroups - If true, set the worker process’s group access list with all of the groups of '
                      'which the specified username is a member, plus the specified group id.',
        'tmp_upload_dir': 'tmp_upload_dir - Directory to store temporary request data as they are read. This path '
                          'should be writable by the process permissions set for Gunicorn.',
        'secure_scheme_headers': 'secure_scheme_headers - A dictionary containing headers and values that the '
                                 'front-end proxy uses to indicate HTTPS requests. These tell gunicorn to set '
                                 'wsgi.url_scheme to “https”, so your application can tell that the request is '
                                 'secure.',
        'forwarded_allow_ips': 'forwarded_allow_ips - Front-end’s IPs from which allowed to handle set secure headers '
                               '(comma separate).',
        'pythonpath': 'pythonpath - A comma-separated list of directories to add to the Python path.',
        'paste': 'paste - Load a PasteDeploy config file.',
        'proxy_protocol': 'proxy_protocol - Enable detect PROXY protocol (PROXY mode).',
        'proxy_allow_ips': 'proxy_allow_ips - Front-end’s IPs from which allowed accept proxy requests (comma '
                           'separate).',
        'accesslog': 'accesslog - The Access log file to write to. “-” means log to stdout.',
        'access_log_format': 'access_log_format - The access log format.',
        'disable_redirect_access_to_syslog': 'disable_redirect_access_to_syslog - Disable redirect access logs to '
                                             'syslog.',
        'errorlog': 'errorlog - The Error log file to write to. “-” means log to stderr.',
        'loglevel': 'loglevel - The granularity of Error log outputs. Valid level names are: 1. debug 2. info 3. '
                    'warning 4. error 5. critical',
        'capture_output': 'capture_output - Redirect stdout/stderr to specified file in errorlog.',
        'logger_class': 'logger_class - The logger you want to use to log events in gunicorn.',
        'logconfig': 'logconfig - The log config file to use. Gunicorn uses the standard Python logging module’s '
                     'Configuration file format.',
        'logconfig_dict': 'logconfig_dict - The log config dictionary to use, using the standard Python logging '
                          'module’s dictionary configuration format.',
        'proc_name': 'proc_name - A base to use with setproctitle for process naming.'
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
