# SearchEngine
Search engine using Python 3, Flask, Psycopg and Beautiful Soup, along with PostgreSQL databse.

## Installs
*update for Windows CMD*

For Beautiful Soup, run `pip3 install -U beautifulsoup4`

For Flask, run `pip3 install -U Flask`

For Psycopg, run `pip3 install -U psycopg2`

For PostgreSQL, run `brew install postgresql`

## Setup the Database

run the bash script `init_py.sh`

## Running the Code

Go into main project folder and use the following commands every time you resart the app:

### MacOS/Terminal

`export FLASK_APP=app.py`

`flask run`

Can optionally turn on the debugger in dev mode:

`export FLASK_APP=app.py`

`export FLASK_APP=development`

`flask run`

### Windows
#### Command Line (CMD)

`set FLASK_APP=app.py`

`flask run`

#### PowerShell (PWS)

`$env:FLASK_APP = "app.py"`

`flask run`

