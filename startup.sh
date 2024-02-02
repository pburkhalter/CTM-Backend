#!/bin/bash
gunicorn -w 8 /usr/local/bin/CapmoTicketMaster/src/app.py:app