import logging
from logging.handlers import RotatingFileHandler
import subprocess

from github_webhook import Webhook
from flask import Flask
from git import Repo

app = Flask(__name__)  # Standard Flask app
webhook = Webhook(app) # Defines '/postreceive' endpoint

repo = Repo("/home/ubuntu/airflow/dags/")

restart_webserver = ['sudo', 'systemctl', 'restart', 'airflow-webserver']
restart_scheduler = ['sudo', 'systemctl', 'restart', 'airflow-scheduler']

@app.route("/")        # Standard Flask endpoint
def hello_world():
    return "Hello, World!"

@webhook.hook()        # Defines a handler for the 'push' event
def on_push(data):
    if data['ref'].replace('refs/heads/','') == 'master':
        logger.info("Checking out develop")
        repo.heads.master.checkout()

        logger.info("Pulling updates to develop")
        repo.git.pull()

        logger.info("Restarting Webserver")
        subprocess.check_call(restart_webserver)

        logger.info("Restarting Scheduler")
        subprocess.check_call(restart_scheduler)
    else:
        logger.info('Received Push from {0}'.format(data['ref'].replace('refs/heads/','')))



logger = logging.getLogger('sample_logger')
logger.setLevel(logging.INFO)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

fh = RotatingFileHandler('githooks.log', maxBytes=50000000, backupCount=3)
fh.setLevel(logging.INFO)

formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s:%(message)s',
                              datefmt='%Y-%m-%d %H:%M:%S')
ch.setFormatter(formatter)
fh.setFormatter(formatter)

logger.addHandler(ch)
logger.addHandler(fh)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

