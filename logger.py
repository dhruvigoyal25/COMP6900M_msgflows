import datetime
import inspect
import logging

from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

token = "<your token>"
org = "<your org name>"
bucket = "<bucket name>"

with InfluxDBClient(url="http://localhost:8086", token=token, org=org) as client:
    write_api = client.write_api(write_options=SYNCHRONOUS)


def log_calls(func):
    def advising_function_wrapper(*args, **kwargs):
        caller_frame = inspect.stack()[1]
        caller_func = caller_frame.function
        callee_func = func.__name__
        timestamp = datetime.datetime.utcnow().isoformat()
        try:
            result = func(*args, **kwargs)
            output = result
            print(output)
        except Exception as e:
            result = None
            output = str(e)
            raise e
        print(f"Callee: {callee_func}, Caller: {caller_func}")
        data = [
            {
                "measurement": "function_calls",
                "tags": {
                    "caller_func": caller_func,
                    "callee_func": callee_func,
                    "output": str(output), // configurable data
                },
                "time": timestamp,
                "fields": {
                    "args": str(args),
                    "kwargs": str(kwargs),
                    "output": str(output),
                    "time": timestamp,
                    "caller_func": caller_func,
                    "callee_func": callee_func,
                }
            }
        ]
        write_api.write(bucket, org, data)
        return result

    advising_function_wrapper.__name__ = f"{func.__name__}_wrapper"
    return advising_function_wrapper
