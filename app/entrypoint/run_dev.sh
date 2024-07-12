#!/bin/sh

exec uvicorn --reload --host 127.0.0.1 --port 8000 wishvault.asgi:application