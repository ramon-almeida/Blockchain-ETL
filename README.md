**Blockchain ETL Using Etherscan API**

**Project Overview**

This project is designed to extract blockchain data using the Etherscan API and automate the ETL (Extract, Transform, Load) process using Python scripts and Google Cloud Composer (Airflow). The data is extracted from the Etherscan API, transformed into a CSV format, and then loaded into Google BigQuery for further analysis.



**Repository Structure**

├── dags/
│   ├── eth_balances_dag.py
│   └── scripts/
│       └── fetch_eth_balances.py

**dags/** : This directory contains the Airflow DAG (Directed Acyclic Graph) files responsible for orchestrating the ETL process.

    •eth_balances_dag.py : The main DAG file where the tasks are defined. This file imports the Python functions from the **scripts/** directory, executes the ETL process, and manages the workflow.

    •scripts/ : This folder contains the Python scripts that perform the actual data extraction from the Etherscan API.

       •fetch_eth_balances.py: The script that interacts with the Etherscan API, extracts the required data, and prepares it for 	    loading into a CSV file.

**ETL Process**

**1.** **Data Extraction** :

    •The Python script located in**scripts/fetch_eth_balances.py** connects to the Etherscan API to retrieve blockchain data based on specific parameters.

**2.** **Data Transformation** :

    •The extracted data is transformed and organized into a structured CSV format using Pandas.

**3.** **Data Loading** :

    •The CSV file is uploaded to a Google Cloud Storage bucket.

    •Finally, the CSV file is loaded into a Google BigQuery table for storage and further analysis.

**Cloud Composer (Airflow) Setup**

    •The ETL process is orchestrated using Google Cloud Composer (which utilizes Apache Airflow).

    •The DAG file (**dag_file.py**) contains the task definitions that call the functions in the Python script, handle task dependencies, and manage scheduling.

**Usage**

Once the DAG is triggered, it will execute the following steps:

1.	Extract data from the Etherscan API.

2.Transform the data and save it as a CSV file.

3.	Upload the CSV to Google Cloud Storage.

4.	Load the CSV data into a BigQuery table.
