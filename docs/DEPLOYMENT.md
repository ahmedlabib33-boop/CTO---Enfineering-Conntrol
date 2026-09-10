# Deployment

## Windows local
Double-click `run_app.bat`.

It creates `.venv`, installs Python requirements when the manifest changes, installs frontend packages when needed, starts the API and UI, performs a health check, and opens the browser.

## Docker
A minimal Docker Compose definition is included as an alternative. Direct Windows startup remains the primary MVP path.
