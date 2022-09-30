# Twitter-Lite

## Requirements

* Neo4j 3.5.2 Community Edition
* Flask 1.0.2
* Neo4j Bolt Driver 1.7 for Python
* Python 3

## How to run the Website in NARGA
### Database stuff
1.  Download Neo4j for Linux [here](https://neo4j.com/download-thanks/?edition=community&release=3.5.4&flavour=unix)
2.  Update the `neo4j.conf` file as specified below
3.  run `$ ./neo4j console` to start the database server

### Flask and the Neo4j python driver
1. `$ pip install --user neo4j` to install the neo4j Python driver
2. `$ pip install --user flask` to install flask
2. `$ python server.py` Will prompt you for the database credentials (username:neo4j, password:neo4j by default)

The website should be accessible on `localhost:5000`

## Neo4j Configs:
The default ports have been changed to prevent port conflicts in NARGA:

`dbms.connector.http.listen_address=:7469`

`dbms.connector.bolt.listen_address=:7420`

`dbms.connector.https.listen_address=:7455`

## Database generation

## Running the server

## TODO

* Remove ugly from the frontend
* Complete last few DB queries
* ????
