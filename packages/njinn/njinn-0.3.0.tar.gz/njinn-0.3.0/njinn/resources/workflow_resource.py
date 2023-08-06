from ..base import *
from ..models import *
from ..njinn_client import NjinnClient
from .mixins import *


class WorkflowResource(
    GetResourceMixin,
    SaveResourceMixin,
    CreateResourceMixin,
    DeleteResouceMixin,
    BaseResource,
):
    def __init__(self, client: NjinnClient):
        super().__init__("api/v1/workflows", Workflow, client)

    def run(self, **kwargs):
        return self.operation("run", Execution).post(**kwargs)

    def duplicate(self, **kwargs):
        return self.operation("duplicate", Workflow).post(**kwargs)


Mapping.register(Workflow, WorkflowResource)
