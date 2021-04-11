**Run Locally**

Spin up mongo db and redis containers (pre-req : Docker & docker-compose)

_`make dependencies`_

Install required python dependencies (pre-req : python 3.8 and pip)

_`pip install -r requirements.txt`_

Start the flask server

_`python run.py`_

Start the worker

_`python worker.py`_