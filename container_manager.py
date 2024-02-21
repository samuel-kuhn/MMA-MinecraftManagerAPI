import docker, shutil, os, json
import container_information as CI
client = docker.from_env()
containers_path = os.getcwd() + "/containers/"
import logging

logger = logging.getLogger('exception_logging')
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler('errors.log')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter('[%(asctime)s] %(message)s', datefmt='%d/%b/%Y %H:%M:%S'))
logger.addHandler(file_handler)



def start(username, server_name):
    try: 
        container = client.containers.get(f'{username}.{server_name}')
        container.start()
    except Exception as exception:
        logger.exception(exception)
        return "something went wrong here"


def stop(username, server_name):
    try: 
        container = client.containers.get(f'{username}.{server_name}')
        container.stop()
    except Exception as exception:
        logger.exception(exception)
        return "something went wrong here"

    

def create(mc_server: CI.MinecraftServer):
    try: 
        create_config(mc_server)
        client.containers.create(image=mc_server.image, name=mc_server.full_name, ports=mc_server.port_config,
                environment=mc_server.environment, volumes=mc_server.volume)
    except Exception as exception:
        logger.exception(exception)
        return "something went wrong here"


    
def create_config(mc_server: CI.MinecraftServer): #creates a config file of the container
    try: 
        config = mc_server.config
        if not os.path.exists(mc_server.full_path):
            os.makedirs(mc_server.full_path)
        with open(mc_server.config_file, 'w') as file:
            json.dump(config, file)
    except Exception as exception:
        logger.exception(exception)
        return "something went wrong here"


def edit(username, server_name, new_server: CI.MinecraftServer):
    try: 
        container = client.containers.get(f'{username}.{server_name}')
        container.stop()
        container.remove()
        create(new_server)
    except Exception as exception:
        logger.exception(exception)
        return "something went wrong here"


def reset(username, server_name):
    stop(username, server_name)
    path = CI.full_path(username, server_name)
    try:
        shutil.rmtree(f"{path}/world")
        shutil.rmtree(f"{path}/world_nether")
        shutil.rmtree(f"{path}/world_the_end")
    except Exception as exception:
        logger.exception(exception)
        pass


def delete(username, server_name):
    try: 
        stop(username, server_name)
        container = client.containers.get(f'{username}.{server_name}')
        container.remove()
        shutil.rmtree(CI.full_path(username, server_name))
    except Exception as exception:
        logger.exception(exception)
        return "something went wrong here"


def exec(username, server_name, command):
    try: 
        container = client.containers.get(f'{username}.{server_name}')
        container.exec_run("mc-send-to-console " + command)
    except Exception as exception:
        logger.exception(exception)
        return "something went wrong here"


