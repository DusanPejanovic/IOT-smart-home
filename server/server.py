from flask import Flask, jsonify, request
from flask_socketio import SocketIO
from flask_cors import CORS
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import paho.mqtt.client as mqtt
import json

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="http://localhost:4200")

# InfluxDB Configuration
token = "smarthometoken"
org = "smarthomeiot"
url = "http://localhost:8086"
bucket = "smarthomebucket"
influxdb_client = InfluxDBClient(url=url, token=token, org=org)

# MQTT Configuration
mqtt_client = mqtt.Client()
mqtt_client.connect("localhost", 1883, 60)
mqtt_client.loop_start()


# MQTT logic
def on_connect(client, userdata, flags, rc):
    client.subscribe("Temperature")
    client.subscribe("Humidity")
    client.subscribe("Motion")
    client.subscribe("Distance")
    client.subscribe("Button")
    client.subscribe("Led")
    client.subscribe("Buzzer")
    client.subscribe("Key")

    # Gyro
    client.subscribe("Acceleration")
    client.subscribe("Rotation")

    client.subscribe("alarm")

    # Status
    client.subscribe("clock-alarm-status")
    client.subscribe("alarm-status")


def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode('utf-8'))
    if msg.topic == "alarm":
        save_alarm_to_db(data)
    elif msg.topic == "clock-alarm-status":
        data = json.loads(msg.payload.decode('utf-8'))
        try:
            socketio.emit('clock-alarm', json.dumps({"status": data["status"]}))
        except Exception as e:
            print(str(e))
    elif msg.topic == "alarm-status":
        data = json.loads(msg.payload.decode('utf-8'))
        try:
            socketio.emit('alarm', json.dumps({"status": data["status"]}))
        except Exception as e:
            print(str(e))
    elif msg.topic == "Acceleration" or msg.topic == "Rotation":
        save_gsg_to_db(data)
    else:
        save_to_db(data)

    # Update data for that sensor
    if "new_sensor_value" in data and data["new_sensor_value"]:
        send_new_sensor_value(data)


mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message


def save_to_db(data):
    write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)
    point = (
        Point(data["measurement"])
        .tag("simulated", data["simulated"])
        .tag("runs_on", data["runs_on"])
        .tag("name", data["name"])
        .field("measurement", data["value"])
        .time(data["time"])
    )
    write_api.write(bucket=bucket, org=org, record=point)


def save_gsg_to_db(data):
    for i, coord in enumerate(['x', 'y', 'z']):
        write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)
        point = (
            Point(data["measurement"])
            .tag("simulated", data["simulated"])
            .tag("runs_on", data["runs_on"])
            .tag("name", data["name"])
            .tag("coordinate", coord)
            .field("measurement", data["value"][i])
            .time(data["time"])
        )
        write_api.write(bucket=bucket, org=org, record=point)


def save_alarm_to_db(data):
    write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)
    point = (
        Point(data["measurement"])
        .tag("type", data["type"])
        .field("reason", data["reason"])
        .time(data['time'])
    )
    write_api.write(bucket=bucket, org=org, record=point)


# Socket logic
@socketio.on('connect')
def handle_connect():
    print('Client connected successfully\n')


@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected successfully\n')


def send_new_sensor_value(data):
    try:
        socketio.emit('new-sensor-value/' + data['runs_on'], json.dumps(data))
    except Exception as e:
        print(str(e))


def send_alarm_data(data):
    try:
        socketio.emit('alarm', json.dumps(data))
    except Exception as e:
        print(str(e))


# Backend logic
@app.route('/rgb/color', methods=['PUT'])
def update_rgb_color():
    try:
        data = request.get_json()
        color = data.get('color', None)

        if color is not None:
            print(f"Received color: {color}")

            mqtt_message = {"color": color}
            mqtt_client.publish("rgb/color", payload=json.dumps(mqtt_message))

            return jsonify({'message': 'Color updated successfully'}), 200
        else:
            return jsonify({'error': 'Color not provided'}), 400

    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500


@app.route('/clock-alarm', methods=['POST'])
def post_clock_alarm():
    data = request.get_json()
    date = data.get('params').get('date')
    time = data.get('params').get('time')
    mqtt_client.publish("clock-alarm/on", json.dumps(data.get('params')))
    return jsonify({'message': f'Data received successfully. Date: {date}, Time: {time}'})


@app.route('/clock-alarm/off', methods=['PUT'])
def clock_alarm_off():
    mqtt_client.publish("clock-alarm/off", json.dumps({"action": "Off"}))
    return jsonify({'message': f'Turn clock alarm off'})


@app.route('/alarm/off', methods=['PUT'])
def alarm_off():
    write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)
    try:
        point = (
            Point("alarm")
            .tag("caused_by", "web")
            .tag("message", "Alarms turned off by web app")
            .field("status", "OFF")
        )
        alarm_data = {
            "caused_by": "web",
            "message": "Alarms turned of by web app",
            "status": "OFF"
        }

        write_api.write(bucket="events", org=org, record=point)
        mqtt_client.publish("topic/alarm/buzzer/off", json.dumps(alarm_data))

        return jsonify({'message': f'SUCCESS'}), 200

    except Exception as e:
        print(str(e))
        pass

    return jsonify({'message': "ERROR"}), 400


if __name__ == '__main__':
    socketio.run(app, debug=True, port=5001, use_reloader=False)
