from enum import Enum
from typing import Dict, Optional, Tuple, Union

import attr

try:
    import docker.errors
    from docker.models.containers import Container
except ImportError:
    docker = None
    Container = None

from scone.common.chanpro import Channel
from scone.sous import Utensil
from scone.sous.utensils import Worktop

_docker_client_instance = None


def _docker_client():
    if not docker:
        # check docker is actually installed and give a message with the resolution
        # when it isn't.
        raise RuntimeError(
            "You need to install docker from PyPI to use these utensils!"
        )

    global _docker_client_instance
    if not _docker_client_instance:
        _docker_client_instance = docker.from_env()
    return _docker_client_instance


class ContainerState(Enum):
    NOTFOUND = 0
    RUNNING = 1
    EXITED = 2
    RESTARTING = 3


@attr.s(auto_attribs=True)
class DockerContainerState(Utensil):
    # Name of the container to check the existence of.
    name: str

    async def execute(self, channel: Channel, worktop: Worktop):
        client = _docker_client()
        # this is essentially `docker ps -a`
        # TODO(perf) run this in a threaded executor since docker can be slow.
        for container in client.containers.list(all=True):
            # container: Container
            if self.name == container.name:
                if container.status == "running":
                    await channel.send(ContainerState.RUNNING.value)
                elif container.status == "exited":
                    await channel.send(ContainerState.EXITED.value)
                elif container.status == "restarting":
                    await channel.send(ContainerState.RESTARTING.value)
                else:
                    raise ValueError(f"Unknown container status: {container.status}")
                break
        else:
            await channel.send(ContainerState.NOTFOUND.value)


@attr.s(auto_attribs=True)
class DockerContainerRun(Utensil):
    # Name of the image to use to create the container.
    image: str
    # Command to create the container with. Optional.
    command: Optional[str]
    # Custom name to give the container.
    name: str
    # Ports to bind inside the container
    # {'2222/tcp': ('127.0.0.1', 3333)} will expose port 2222 inside as 3333 outside.
    ports: Dict[str, Tuple[str, int]]
    # Volumes to mount inside the container.
    # Key is either a host path or a container name.
    # Value is a dictionary with the keys of:
    #   bind = path to bind inside the container
    #   mode = 'rw' or 'ro'
    volumes: Dict[str, Dict[str, str]]
    # Environment variables
    environment: Dict[str, str]
    # Restart policy
    restart_policy: str

    @attr.s(auto_attribs=True)
    class Result:
        name: str

    async def execute(self, channel: Channel, worktop: Worktop):
        restart_policy: Dict[str, Union[int, str]] = {
            "Name": self.restart_policy,
        }
        if self.restart_policy == "on-failure":
            restart_policy["MaximumRetryCount"] = 5

        container = _docker_client().containers.run(
            self.image,
            self.command,
            detach=True,
            name=self.name,
            ports=self.ports,
            volumes=self.volumes,
            environment=self.environment,
            restart_policy=restart_policy,
        )

        await channel.send(DockerContainerRun.Result(name=container.name))


@attr.s(auto_attribs=True)
class DockerImagePull(Utensil):
    repository: str
    tag: str

    @attr.s(auto_attribs=True)
    class Result:
        id: str

    async def execute(self, channel: Channel, worktop: Worktop):
        try:
            image = _docker_client().images.pull(self.repository, self.tag)
        except docker.errors.APIError:
            # the docker server returned an error
            await channel.send(None)
            return

        await channel.send(DockerImagePull.Result(id=image.id))


@attr.s(auto_attribs=True)
class DockerVolumeCreate(Utensil):
    name: str

    @attr.s(auto_attribs=True)
    class Result:
        name: str

    async def execute(self, channel: Channel, worktop: Worktop):
        try:
            volume = _docker_client().volume.create(self.name)
        except docker.errors.APIError:
            # the docker server returned an error
            await channel.send(None)
            return

        await channel.send(DockerVolumeCreate.Result(name=volume.name))


@attr.s(auto_attribs=True)
class DockerNetworkCreate(Utensil):
    name: str
    check_duplicate: Optional[bool]
    internal: Optional[bool]
    enable_ipv6: Optional[bool]
    attachable: Optional[bool]
    ingress: Optional[bool]

    @attr.s(auto_attribs=True)
    class Result:
        name: str

    async def execute(self, channel: Channel, worktop: Worktop):
        try:
            network = _docker_client().networks.create(
                self.name,
                check_duplicate=self.check_duplicate,
                internal=self.internal,
                enable_ipv6=self.enable_ipv6,
                attachable=self.attachable,
                ingress=self.ingress,
            )
        except docker.errors.APIError:
            # the docker server returned an error
            await channel.send(None)
            return

        await channel.send(DockerContainerRun.Result(name=network.name))
