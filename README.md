# flask-github-webhook

A simple flask app to process github webhooks based on the app written by [Bloomberg](https://github.com/bloomberg/python-github-webhook)

Specifically, when our Airflow-Dags repo is pushed to, Github sends a payload to the app. The app then parses the payload. If the push was to master, the app pulls the updates into the local repo of master and restarts the airflow webserver and schduler.
