"""Start API without Docker, e.g. for interactive debugging."""

import uvicorn

from signal_cli_rest_api.main import app

uvicorn.run(app, host="127.0.0.1", port=8000)
