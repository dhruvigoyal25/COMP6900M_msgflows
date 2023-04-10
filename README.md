# Real-Time Visualization Tool

This is a Python-based tool for real-time visualization of the sequence and data flow diagrams of software systems. It uses Aspect-Oriented Programming (AOP) to dynamically intercept function calls and generate diagrams in real time. The tool is designed to help developers and system architects better understand the behavior of complex software systems and diagnose performance and reliability issues.

# Installation

- Clone the repository: `git clone https://github.com/your_username/real-time-visualization.git`
- Apply the tool to any pthon project:

  `from logger import log_calls`
  
  Apply `@log_calls` to any function in your project.
  

## Setup [InfluxDB](https://www.influxdata.com/blog/start-python-influxdb/)

- Connect to the client library:
  If you have Docker installed on your computer, you can simply run InfluxDB’s Docker Image using the following command:

    `docker run --name influxdb -p 8086:8086 influxdb:2.1.0`  
- Setup and create InfluxDB account for storing the data.
- Now, you’ll have to set up a Python virtual environment. Create a new folder for the tutorial:
  
  `mkdir influxDB-Tutorial`
- Then change your directory into the new folder:
  
  `cd influxDB-Tutorial`
- Create a virtual environment:

  `python3 -m venv venv`
- Activate it.

  `source venv/bin/activate`
- Finally, install InfluxDB’s client library:
  
  `pip install influxdb-client`
- Create a new file named `__init.py__`, then go back to the InfluxDB UI:

  Select the appropriate token and bucket, then copy the code snippet under Initialize the Client and paste it in your Python file. The code snippet will be automatically updated if you change your token/bucket selection.
  Next, run your Python file:

  `python3 __init__.py`

## Start Flask server

- To install Flask, run the following command:
  
  `pip install flask`
- activate the environment:
 
  `mkdir flask-env`
  
  `cd flask-env`
  
  `source env/bin/activate`
  
  `cd ../Logger` 
- Start the rendering:

  `python sequence_diagram.py`

# Usage

- Start the Flask server.
- Navigate to http://localhost:5001 in your web browser.
- Select the project you want to visualize from the list of available projects.
- Choose the type of diagram you want to view: sequence diagram or data flow diagram.
- The diagram will be generated in real time as the software system executes.

# Supported Projects

Thsi tool is compatibale with any kind of python project. The Real-Time Visualization Tool has been tested with the following open-source projects:
- University Recommendation System
- Classic Tic-Tac-Toe Game in Python

# Contributing
Contributions are welcome! If you find a bug or have a feature request, please open an issue. If you want to contribute code, please fork the repository and submit a pull request.

