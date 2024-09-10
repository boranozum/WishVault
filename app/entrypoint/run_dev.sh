#!/bin/sh

exec uvicorn --reload --host 0.0.0.0 --port 8000 wishvault.asgi:application