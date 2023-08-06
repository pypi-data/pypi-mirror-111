from ..base import *
from ..models import *
from ..njinn_client import NjinnClient
from .mixins import *


class ScheduleResource(
    GetResourceMixin,
    SaveResourceMixin,
    CreateResourceMixin,
    DeleteResouceMixin,
    BaseResource,
):
    def __init__(self, client: NjinnClient):
        super().__init__("api/v1/schedules", Schedule, client)

    def duplicate(self, **kwargs) -> Schedule:
        return self.operation("duplicate", Schedule).post(**kwargs)


Mapping.register(Schedule, ScheduleResource)
