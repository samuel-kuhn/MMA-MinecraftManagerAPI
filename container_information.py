import docker, shutil, os, json
client = docker.from_env()
containers_path = os.getcwd() + "/containers/"
def full_path(username, server_name):
    return f'{containers_path}{username}/{server_name}'
def config_path(username, server_name):
    return f'{containers_path}{username}/{server_name}/config.json'

class MinecraftServer:
    def __init__(self, username, server_name, port, mode, 
        version, memory='2G', Type='VANILLA', 
        motd = 'a simple minecraft server', image_label='latest', image=None):

        #Attributes
        self.user = username
        self.name = server_name
        self.full_name = f"{username}.{server_name}"
        self.full_path = f"{containers_path}{self.user}/{self.name}"
        self.port = port
        self.port_config = {'25565/tcp': port}
        self.volume = [f'{self.full_path}:/data']
        self.mode = mode
        self.version = version
        self.memory = memory
        self.Type = Type
        self.motd = motd
        self.image_label = image_label
        self.image = f"itzg/minecraft-server:{image_label}" if image is None else image
        self.config_file = f"{self.full_path}/config.json"
        self.environment = ["EULA=TRUE", f"TYPE={Type}", f"VERSION={version}", f"MEMORY={memory}", f"MOTD={motd}", f"MODE={mode}"]
        self.config = {"username":username, "server_name":server_name, "port":port, "mode":mode, 
              "version":version, "memory":memory, "Type":Type, "motd":motd, "image": self.image}
        
    #def load from config
def get_config(username, server_name):
    config_file = config_path(username, server_name) 
    with open(config_file, 'r') as file:
        config = json.load(file)
    return config


def get_servers(username):
    running = []
    not_running = []
    containers = client.containers.list(filters={'name': f'{username}.'}, all=True)
    for container in containers:
        server_name = container.name.replace(f'{username}.', '')
        public_port = container.attrs['HostConfig']['PortBindings']['25565/tcp'][0]['HostPort']
        status = container.status
        environment_list = container.attrs['Config']['Env']
        environment = dict(item.split('=', 1) for item in environment_list)
        memory = environment['MEMORY'] if 'MEMORY' in environment else '1G'
        version = environment['VERSION']
        if status == 'running':
            running.append({
                "name": server_name,
                "status": status,
                "memory": memory,
                "port": public_port,
                "version": version
            })
        else:
            not_running.append({
                "name": server_name,
                "status": status,
                "memory": memory,
                "port": public_port,
                "version": version
            })
    
    return [running, not_running]




