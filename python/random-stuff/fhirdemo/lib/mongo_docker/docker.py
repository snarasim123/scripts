import docker as _docker
import time
import pymongo

try:
    _docker_client = _docker.from_env()
except:
    _docker_client = None

DEFAULT_MONGO_IMAGE = 'mongo:4'
MONGO_PORT = 27017


def client():
    return _docker_client


def is_mongo_running(container):
    try:
        mongo_host = "mongodb://%s:%d/" % (container.attrs['NetworkSettings']['IPAddress'], MONGO_PORT)
        mongo_client = pymongo.MongoClient(mongo_host)
        mongo_client.s
        # mongo_client.server_info()
        return True
    except Exception as e:
        return False


def mongo_instance(instance_name, data_path=None, restart=True, create=True, mongo_image=DEFAULT_MONGO_IMAGE):
    try:
        mongo_container = _docker_client.containers.get(instance_name)
    except:
        mongo_container = None

    if restart and mongo_container is not None and mongo_container.status == 'exited':
        mongo_container.start()
    elif create and (mongo_container is None or mongo_container.status == 'exited'):
        volumes = None if data_path is None else {data_path: {'bind': '/data/db', 'mode': 'rw'}}
        mongo_container = _docker_client.containers.run(mongo_image, name=instance_name, volumes_from=volumes,
                                                        detach=True)

    tries = 0
    while tries < 5:
        if mongo_container.status == 'running' and is_mongo_running(mongo_container):
            break
        tries += 1
        time.sleep(2)
        mongo_container = _docker_client.containers.get(instance_name)

    if mongo_container is not None and mongo_container.status == 'running' and is_mongo_running(mongo_container):
        return mongo_container, "mongodb://%s:%d/" % (mongo_container.attrs['NetworkSettings']['IPAddress'], MONGO_PORT)
    return None, None


def stop_container(container):
    container.stop()


def create_mongo_instance(instance_name, data_path=None, create=True, mongo_image=DEFAULT_MONGO_IMAGE):
    try:
        mongo_container = _docker_client.containers.get(instance_name)
    except:
        mongo_container = None

    if mongo_container is None or mongo_container.status == 'exited':
        try:
            volumes = None if data_path is None else {data_path: {'bind': '/data/db', 'mode': 'rw'}}
            mongo_container = _docker_client.containers.run(mongo_image, name=instance_name, volumes_from=volumes,
                                                            detach=True)
        except Exception as e:
            return None, None

    tries = 0
    while tries < 5:
        if mongo_container.status == 'running':
            break

    if mongo_container is not None and mongo_container.status == 'running':
        return mongo_container, "mongodb://%s:%d/" % (mongo_container.attrs['NetworkSettings']['IPAddress'], MONGO_PORT)
    return None, None


def start_mongo_instance(instance_name, data_path=None, create=True, mongo_image=DEFAULT_MONGO_IMAGE):
    try:
        mongo_container = _docker_client.containers.run(mongo_image,detach=True)
    except Exception as e:
        return None, None

    if mongo_container is None or mongo_container.status == 'exited':
        try:
            volumes = None if data_path is None else {data_path: {'bind': '/data/db', 'mode': 'rw'}}
            mongo_container = _docker_client.containers.get(mongo_image, name=instance_name, volumes_from=volumes,
                                                              detach=True)
        except Exception as e:
            return None, None

    if mongo_container is not None :
        return mongo_container, "mongodb://%s:%d/" % (mongo_container.attrs['NetworkSettings']['IPAddress'], MONGO_PORT)
    return None, None
