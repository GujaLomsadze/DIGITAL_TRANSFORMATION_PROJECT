#!/bin/bash
uvicorn app:app --host $UVICORN_HOST --port $UVICORN_PORT --workers $(($(nproc) * 2 + 1))
