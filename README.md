# DW data generator
Data generator for DW subject at GUT 2024.

## Generator installation and using
**Warning**  
This setup is valid only on Windows machines!

### Create virtual environment
`python -m venv venv`

### Activate virtual environment
`venv\Scripts\acitvate`

### Install dependencies
`pip install -r requirements.txt`

### Run generator 
`python generator.py`  

It should output 3 files `cities.csv`, `shows.csv` and `tickets.csv` to `/output` directory.

### Building custom MSSQL docker image
`docker build . -t csv-mssql`

### Running instance of `csv-mssql`
`docker run
-e "ACCEPT_EULA=Y"
-e "MSSQL_SA_PASSWORD=yourStrong(!)Password"
-p 1433:1433
--name sqlserver
--hostname sqlserver
-d
csv-mssql`

After container creation you should be able to log in into your database with **SMSS**.
