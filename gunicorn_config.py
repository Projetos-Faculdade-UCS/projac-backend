# gunicorn_config.py

# Bind to 0.0.0.0:8000 to listen for requests on all available IP addresses
bind = "0.0.0.0:80"

# Use a number of worker processes equal to the number of CPUs available
workers = 2

# Specify the WSGI application object (adjust "app" to your project name)
wsgi_app = "config.wsgi:application"

# Optional: Set a timeout (default is 30 seconds)
timeout = 30

# Optional: Set the log level (debug, info, warning, error, critical)
loglevel = "info"

# Optional: Access log file
accesslog = "-"

# Optional: Error log file
errorlog = "-"
