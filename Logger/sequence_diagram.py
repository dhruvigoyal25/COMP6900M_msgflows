from flask import Flask, request, jsonify, render_template
from influxdb_client import InfluxDBClient
from datetime import datetime, timedelta
from flask_cors import CORS

app = Flask(__name__, static_folder='../static', template_folder='../static')
CORS(app)

# Set up the InfluxDB client with your credentials
token = "<your token>"
org = "<your org name>"

# Set up the InfluxDB client with your credentials
client = InfluxDBClient(url="http://localhost:8086", token=token, org=org)


@app.route('/')
def index():
    return render_template('sequence.html')


# Endpoint for querying data from a specific bucket
@app.route('/sequence-diagram/query', methods=['GET'])
def query_bucket():
    # Get the query parameters from the request
    measurement = request.args.get('measurement', "function_calls")
    duration = request.args.get('duration')

    if measurement is None or duration is None:
        return jsonify({'error': 'measurement and duration parameters are required'})

    end_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    start_time = (datetime.utcnow() - timedelta(seconds=int(duration))).strftime('%Y-%m-%dT%H:%M:%SZ')

    # Construct a Flux query to retrieve the data
    query = f'from(bucket: "<bucket_name>") \
              |> range(start: {start_time}, stop: {end_time}) \
              |> filter(fn: (r) => r["_measurement"] == "function_calls") \
              |> filter(fn: (r) => r["_field"] == "callee_func" or r["_field"] == "caller_func" or \
              r["_field"] == "output")'

    # Use the query API to execute the query
    query_api = client.query_api()
    result = query_api.query(query)

    # Return the results as JSON
    output = []
    for table in result:
        for record in table.records:
            output.append(record.values)

    # Generate a Mermaid sequence diagram from the query result
    diagram = "sequenceDiagram \n "
    logs = ""
    for table in result:
        for record in table.records:
            source = record.values['caller_func']
            target = record.values['callee_func']
            if record.values['output'] != None:
                output = record.values['output']
            else:
                output = " "
            source = source.replace("<", "(")
            source = source.replace(">", ")")
            target = target.replace("<", "(")
            target = target.replace(">", ")")
            logs = f"Note over {source}, {target}: {record.values['_time']}ms \n" +\
                   f"{source}->>{target}: {output} \n " + logs

    diagram += logs
    return jsonify({'data': diagram})


# Endpoint for creating a dataflow diagram
@app.route('/dataflow-diagram/query', methods=['GET'])
def create_dataflow_diagram():
    # Get the query parameters from the request
    measurement = request.args.get('measurement', "function_calls")
    duration = request.args.get('duration')

    if measurement is None or duration is None:
        return jsonify({'error': 'measurement and duration parameters are required'})

    end_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    start_time = (datetime.utcnow() - timedelta(seconds=int(duration))).strftime('%Y-%m-%dT%H:%M:%SZ')

    # Construct a Flux query to retrieve the data
    query = f'from(bucket: "<bucket_name>") \
              |> range(start: {start_time}, stop: {end_time}) \
              |> filter(fn: (r) => r["_measurement"] == "function_calls") \
              |> filter(fn: (r) => r["_field"] == "callee_func" or r["_field"] == "caller_func")'

    # Use the query API to execute the query
    query_api = client.query_api()
    result = query_api.query(query)

    # Create a map of source to destination functions and their respective interaction counts
    interactions_map = {}
    for table in result:
        for record in table.records:
            source = record.values['caller_func']
            target = record.values['callee_func']
            if source not in interactions_map:
                interactions_map[source] = {}
                if target not in interactions_map[source]:
                    interactions_map[source][target] = 1
                else:
                    interactions_map[source][target] += 1
            else:
                if target not in interactions_map[source]:
                    interactions_map[source][target] = 1
                else:
                    interactions_map[source][target] += 1

    # Generate a Mermaid dataflow diagram from the interactions map
    diagram = "graph TD \n"
    for source, targets in interactions_map.items():
        for target, count in targets.items():
            source = source.replace("<", " ")
            source = source.replace(">", " ")
            target = target.replace("<", " ")
            target = target.replace(">", " ")
            diagram += f"{source} -->|{count}| {target} \n"

    return jsonify({'data': diagram})


if __name__ == '__main__':
    app.run(host="localhost", port=5001)
