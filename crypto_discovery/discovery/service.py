from dataclasses import dataclass

from .adapters import CompositeDiscovery
from .models import DiscoveredPool


@dataclass
class DiscoveryResult:
    pools: list[DiscoveredPool]
    errors: list[dict]


class DiscoveryService:
    def __init__(self, discovery: CompositeDiscovery):
        self.discovery = discovery

    def run(self) -> DiscoveryResult:
        pools, errors = self.discovery.discover()
        return DiscoveryResult(pools=pools, errors=errors)
