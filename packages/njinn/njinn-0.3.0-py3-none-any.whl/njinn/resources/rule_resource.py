from ..base import *
from ..models import *
from ..njinn_client import NjinnClient
from .mixins import *


class RuleResource(
    GetResourceMixin,
    SaveResourceMixin,
    CreateResourceMixin,
    DeleteResouceMixin,
    BaseResource,
):
    def __init__(self, client: NjinnClient):
        super().__init__("api/v1/scheduling_rules", Rule, client)

    def duplicate(self, **kwargs) -> Rule:
        return self.operation("duplicate", Rule).post(**kwargs)


Mapping.register(Rule, RuleResource)
