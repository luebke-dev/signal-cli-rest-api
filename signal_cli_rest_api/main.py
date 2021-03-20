from fastapi import FastAPI

from signal_cli_rest_api.api import block, groups, messages, profile, register

app = FastAPI(title="signal-cli-rest-api", version="0.1.97")

app.include_router(block.router, prefix="/block", tags=["block"])
app.include_router(groups.router, prefix="/groups", tags=["groups"])
app.include_router(messages.router, prefix="/messages", tags=["messages"])
app.include_router(profile.router, prefix="/profile", tags=["profile"])
app.include_router(register.router, prefix="/register", tags=["register"])
