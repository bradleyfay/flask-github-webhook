import logging
import subprocess

from github_webhook import Webhook
from flask import Flask
from git import Repo

app = Flask(__name__)  # Standard Flask app
webhook = Webhook(app) # Defines '/postreceive' endpoint

repo = Repo("/home/ubuntu/airflow/dags/")

restart_webserver = ['sudo', 'initctl', 'restart', 'airflow-webserver']
restart_scheduler = ['sudo', 'initctl', 'restart', 'airflow-scheduler']

@app.route("/")        # Standard Flask endpoint
def hello_world():
    return "Hello, World!"

@webhook.hook()        # Defines a handler for the 'push' event
def on_push(data):
    if data['ref'].lstrip('refs/heads/') == 'master':
        logging.info("Checking out master")
        repo.heads.master.checkout()

        logging.info("Pulling updates to master")
        repo.git.pull()

        logging.info("Restarting Webserver")
        subprocess.check_call(restart_webserver)

        logging.info("Restarting Scheduler")
        subprocess.check_call(restart_scheduler)
    else:
        logging.info('Received Push from {0}'.format(data['ref'].lstrip('refs/heads/')))



logging.getLogger(__name__).addHandler(logging.StreamHandler())
logging.basicConfig(filename='githooks.log', 
                    format='%(asctime)s - %(levelname)s:%(message)s',
                    datefmt='%m-%d-%Y %I:%M:%S %p',
                    level=logging.INFO)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

