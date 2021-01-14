from flask import Flask, redirect, request
from flask_caching import Cache
import logging
import os

logger = logging.getLogger("run.py")

app = Flask(__name__)

@app.route("/readiness")
def ready():
    return 'ready'

if __name__ == '__main__':
    app.run()