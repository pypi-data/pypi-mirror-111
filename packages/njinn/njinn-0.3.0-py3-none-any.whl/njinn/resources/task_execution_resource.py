from ..base import *
from ..models import *
from .mixins import *


class TaskExecutionResource(
    GetResourceMixin, BaseResource,
):
    def __init__(self, parent: BaseResource):
        super().__init__("tasks", TaskExecution, parent.client)
        self.parent = parent

    def cancel(self, **kwargs) -> None:
        return self.operation("cancel").post(**kwargs)

    def log(self, **kwargs) -> str:
        return self.operation("log", result_class=str).get(**kwargs)


Mapping.register(TaskExecution, TaskExecutionResource)
