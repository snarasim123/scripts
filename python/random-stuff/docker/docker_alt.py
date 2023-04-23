
import sys
import logging
import docker
# from docker import Client


class Docker(object):
    """
    Docker Client
    """

    def __init__(self, docker_server=None):
        self.log = logging.getLogger()
        # set the docker_server as base_url
        if docker_server is None:
            self.docker_server = "unix://var/run/docker.sock"
        else:
            self.docker_server = "tcp://" + docker_server + ":2375"
        # try to bind docker server
        try:
            self.docker_client = docker.Client(base_url=self.docker_server)
        except DockerException as error:
            print (error)
            sys.exit(255)

    def find_images(self, image):
        """
        check if image exists in docker server
        """
        image_name = image.split(":")[0]
        image_tag = image.split(":")[1]
        image_repo = []
        try:
            images = self.docker_client.images(image_name)
        except DockerException as error:
            # print error
            sys.exit(255)
        # check if image_name in docker server
        if not images:
            print ("Can't find docker image: %s" % image_name)
            sys.exit(255)
        else:
            image_repos = [i["RepoTags"] for i in images]
            for i in image_repos:
                for j in i:
                    image_repo.append(j)
        # check if image_tag in docker server
        if image not in image_repo:
            print ("Can't find docker image %s" % image)
        else:
            print ("Image %s exits in docker server" % image)

    def inspect_images(self, image):
        """
        get image informations, like image ID
        """
        try:
            images = self.docker_client.inspect_image(image)
        except DockerException as error:
            print (error)
            sys.exit(255)
        return images["Id"]

    def create_container(self, config):
        """
        basic function for creating container
        """
        try:
            new_container = self.docker_client.create_container_from_config(\
                            config)
        except DockerException as error:
            print (error)
            sys.exit(255)
        return new_container

    def create_storage_container(self, source, image):
        """
        create container for storage automation code
        """
        # set config for create storage: 'Volumes': source
        bind_route = '/data/:%s:rw' % source
        config = {
            'Tty': True,
            'OpenStdin': True,
            'Image': image,
            'Cmd': '/bin/bash',
            'HostConfig': {'Binds': [bind_route]}
        }
        storage_container = self.create_container(config)
        print("Create storage container", storage_container['Id'])
        return storage_container['Id']

    def create_running_container(self, source_container, image):
        """
        create container for running automation
        """
        # set config for create running: 'Volumes_from': source_container
        config = {
            'Tty': True,
            'OpenStdin': True,
            'Image': image,
            'Cmd': '/bin/bash',
            'HostConfig': {'VolumesFrom': [source_container]}
        }
        running_container = self.create_container(config)
        print ("Create running container", running_container['Id'])
        return running_container['Id']

    def remove_container(self, container, force=False):
        """
        remove container using container_Id or container_name
        """
        try:
            self.docker_client.remove_container(container)
        except DockerException as error:
            print (error)
            sys.exit(255)
        print ("Remove container: ", container)

    def start_container(self, container):
        """
        start an exist docker container
        """
        try:
            self.docker_client.start(container)
        except DockerException as error:
            print (error)
            sys.exit(255)
        print ("Start container: ", container)

    def stop_container(self, container):
        """
        stop an exist docker container
        """
        try:
            self.docker_client.stop(container)
        except DockerException as error:
            print (error)
            sys.exit(255)
        print ("Stop container: ", container)

    def restart_container(self, container):
        """
        restart an exist docker container
        """
        try:
            self.docker_client.restart(container)
        except DockerException as error:
            print (error)
            sys.exit(255)
        print ("Restart container: ", container)

    def inspect_container(self, container):
        """
        inspect container to get more information about container
        """
        try:
            container_info = self.docker_client.inspect_container(container)
        except DockerException as error:
            print (error)
            sys.exit(255)
        return container_info

    def get_container_IP(self, container):
        """
        get container IP and other infomation
        """
        container_info = self.inspect_container(container)
        container_IP = container_info['NetworkSettings']['IPAddress']
        container_Gateway = container_info['NetworkSettings']['Gateway']

    def exec_create(self, container, cmd):
        """
        create an exec instance in a running container
        """
        try:
            exec_instance = self.docker_client.exec_create(container, cmd)
        except DockerException as error:
            print (error)
            sys.exit(255)
        print ("Exec_instance created...")
        return exec_instance['Id']

    def exec_start(self, exec_id, stream=False):
        """
        start a previously create exec instance
        """
        try:
            exec_starter = self.docker_client.exec_start(exec_id, stream)
        except DockerException as error:
            print (error)
            sys.exit(255)
        print ("Exec_instance started...")


class DockerException(Exception):
    """
    General docker exception
    """
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)


# if __name__ == '__main__':

#    # Add an easy demo to show how automation run in docker by using this
#    # docker client lib
#
#    # First build a docker client connect to docker server 10.66.136.205
#    docker = Docker(docker_server="10.66.136.205")
#
#    # set basic param
#    storage_image = "storage:0.1.0"
#    running_image = "run:0.1.0"
#    source_route = "/data/"
#
#    # check if images exists
#    docker.find_images(storage_image)
#    docker.find_images(running_image)
#
#    # create storage_container and running_container
#    storage_container = docker.create_storage_container(\
#                        source_route, storage_image)
#    running_container = docker.create_running_container(\
#                         storage_container, running_image)
#    #print storage_container, "\n", running_container
#
#    # start storage_container and running_container
#    docker.start_container(storage_container)
#    docker.start_container(running_container)
#
#    # create running_container exec_instance and start this instance
#    # exec cmd "bash -c 'Xvfb :99 &'"
#    cmd = "bash -c 'Xvfb :99 &'"
#    exec_Xfvb = docker.exec_create(running_container, cmd)
#    docker.exec_start(exec_Xfvb)
#
#
#    # test run automation script
#    automation_cmd = "bash -c 'pybot \
#            tools-automation/tests/Maitai2/cases/01_BasicFunction/login.txt'"
#    exec_automation = docker.exec_create(running_container, automation_cmd)
#    run_result = docker.exec_start(exec_automation)

    # dockerC = Docker(docker_server="10.66.136.205")
    # cmd = "bash -c 'Xvfb :99'"
    # exec_Xfvb = dockerC.exec_create("run", cmd)
    # print (exec_Xfvb)
    # dockerC.exec_start(exec_Xfvb, stream=True)
    # automation_cmd = "bash -c 'pybot tools-automation/tests/Maitai2/cases/01_BasicFunction/login.txt'"
    # exec_automation = dockerC.exec_create("run", automation_cmd)
    # print (exec_automation)
    # test = dockerC.exec_start(exec_automation)