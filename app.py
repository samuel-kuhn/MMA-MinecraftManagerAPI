from flask import Flask, request
import docker
import container_manager as manager
import container_information as CI
app = Flask(__name__)

client = docker.from_env()

@app.route('/ping', methods=['GET'])
def ping():
    return ('online', 200)

@app.route('/containers', methods=['GET'])
def containers():
    username = request.args.get('username')
    return ("no username", 500) if username == "" else (CI.get_servers(username), 200)

@app.route('/get-config', methods=['GET'])
def get_config():
    username = request.args.get('username')
    server_name = request.args.get('server_name')
    return ("get config error", 500) if (username == "" or server_name == "") else (CI.get_config(username, server_name), 200)

@app.route('/create', methods=['POST'])
def create():
    request_data = eval(request.get_json())
    mc_server = CI.MinecraftServer(**request_data)
    message = manager.create(mc_server)
    return ("ok", 200) if message is None else (message, 500)

@app.route('/edit', methods=['POST'])
def edit():
    request_data = eval(request.get_json())
    username=request_data['username']
    server_name=request_data['server_name']
    config = CI.get_config(username=username, server_name=server_name)
    for key, value in request_data.items():
        config[key] = value
    new_server = CI.MinecraftServer(**config)
    message = manager.edit(username=username, server_name=server_name, new_server=new_server)
    return ("ok", 200) if message is None else (message, 500)

@app.route('/start', methods=['POST'])
def start():
    request_data = request.get_json()
    message = manager.start(**request_data)
    return ("ok", 200) if message is None else (message, 500)

@app.route('/stop', methods=['POST'])
def stop():
    request_data = request.get_json()
    message = manager.stop(**request_data)
    return ("ok", 200) if message is None else (message, 500)

@app.route('/reset', methods=['POST'])
def reset():
    request_data = request.get_json()
    message = manager.reset(**request_data)
    return ("ok", 200) if message is None else (message, 500)
    
@app.route('/delete', methods=['POST'])
def delete():
    request_data = request.get_json()
    message = manager.delete(**request_data)
    return ("ok", 200) if message is None else (message, 500)

@app.route('/exec', methods=['POST'])
def exec():
    request_data = eval(request.get_json())
    message = manager.exec(**request_data)
    return ("ok", 200) if message is None else (message, 500)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
