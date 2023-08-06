from ..base import *
from ..models import *
from ..njinn_client import NjinnClient
from .mixins import *


class ConfigResource(
    GetResourceMixin,
    SaveResourceMixin,
    CreateResourceMixin,
    DeleteResouceMixin,
    BaseResource,
):
    def __init__(self, client: NjinnClient):
        super().__init__("api/v1/configs", Config, client)

    def duplicate(self, **kwargs) -> Config:
        return self.operation("duplicate", Config).post(**kwargs)


Mapping.register(Config, ConfigResource)
