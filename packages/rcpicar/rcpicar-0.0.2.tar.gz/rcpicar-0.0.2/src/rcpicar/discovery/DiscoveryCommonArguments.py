from ..constants import default_discovery_port
from ..util.argument import AnyArguments, create_value_argument, IArguments
from ..util.Lazy import Lazy


class DiscoveryCommonArguments(IArguments):
    def __init__(self) -> None:
        self.port = Lazy(lambda store: default_discovery_port)

    def get_arguments(self) -> AnyArguments:
        return [create_value_argument(self.port, '--discovery-port', int, 'Discovery broadcast port.')]
