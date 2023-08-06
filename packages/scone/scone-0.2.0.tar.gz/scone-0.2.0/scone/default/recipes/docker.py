from scone.default.utensils.docker_utensils import (
    ContainerState,
    DockerContainerRun,
    DockerContainerState,
    DockerImagePull,
    DockerNetworkCreate,
    DockerVolumeCreate,
)
from scone.head.head import Head
from scone.head.kitchen import Kitchen, Preparation
from scone.head.recipe import Recipe, RecipeContext
from scone.head.utils import check_type, check_type_opt


class DockerContainer(Recipe):
    _NAME = "docker-container"

    def __init__(self, recipe_context: RecipeContext, args: dict, head):
        super().__init__(recipe_context, args, head)

        self.image = check_type(args.get("image"), str)
        self.command = check_type_opt(args.get("command"), str)
        self.name = check_type(args.get("name"), str)
        self.volumes = check_type(args.get("volumes", dict()), dict)
        self.ports = check_type(args.get("ports", dict()), dict)
        self.environment = check_type(args.get("environment", dict()), dict)
        self.restart_policy = check_type(args.get("restart_policy", "on-failure"), str)

    def prepare(self, preparation: Preparation, head: Head) -> None:
        super().prepare(preparation, head)
        preparation.provides("docker-container", self.name)

    async def cook(self, kitchen: Kitchen) -> None:
        kitchen.get_dependency_tracker()

        current_state = ContainerState(
            await kitchen.ut1(DockerContainerState(self.name))
        )

        if current_state == ContainerState.NOTFOUND:
            await kitchen.ut1areq(
                DockerContainerRun(
                    self.image,
                    self.command,
                    self.name,
                    {k: (v["host"], v["port"]) for k, v in self.ports.items()},
                    self.volumes,
                    {k: str(v) for k, v in self.environment.items()},
                    self.restart_policy,
                ),
                DockerContainerRun.Result,
            )


class DockerImage(Recipe):
    _NAME = "docker-image"

    def __init__(self, recipe_context: RecipeContext, args: dict, head):
        super().__init__(recipe_context, args, head)

        self.repository = check_type(args.get("repository"), str)
        self.tag = check_type(args.get("tag"), str)

    async def cook(self, kitchen: Kitchen) -> None:
        kitchen.get_dependency_tracker()
        await kitchen.ut1areq(
            DockerImagePull(self.repository, self.tag), DockerImagePull.Result
        )


class DockerVolume(Recipe):
    _NAME = "docker-volume"

    def __init__(self, recipe_context: RecipeContext, args: dict, head):
        super().__init__(recipe_context, args, head)

        self.name = check_type(args.get("name"), str)

    async def cook(self, kitchen: Kitchen) -> None:
        kitchen.get_dependency_tracker()
        await kitchen.ut1areq(DockerVolumeCreate(self.name), DockerVolumeCreate.Result)


class DockerNetwork(Recipe):
    _NAME = "docker-network"

    def __init__(self, recipe_context: RecipeContext, args: dict, head):
        super().__init__(recipe_context, args, head)

        self.name = check_type(args.get("name"), str)
        self.driver = check_type_opt(args.get("driver"), str)
        self.check_duplicate = check_type_opt(args.get("check_duplicate"), bool)
        self.internal = check_type_opt(args.get("internal"), bool)
        self.enable_ipv6 = check_type_opt(args.get("enable_ipv6"), bool)
        self.attachable = check_type_opt(args.get("attachable"), bool)
        self.scope = check_type_opt(args.get("scope"), str)
        self.ingress = check_type_opt(args.get("ingress"), bool)

    async def cook(self, kitchen: Kitchen) -> None:
        kitchen.get_dependency_tracker()
        await kitchen.ut1areq(
            DockerNetworkCreate(
                self.name,
                self.check_duplicate,
                self.internal,
                self.enable_ipv6,
                self.attachable,
                self.ingress,
            ),
            DockerNetworkCreate.Result,
        )
