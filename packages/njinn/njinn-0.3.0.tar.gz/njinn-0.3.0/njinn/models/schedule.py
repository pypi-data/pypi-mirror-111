from typing import TypeVar

from ..base import *
from .mixins import *

T = TypeVar("T")


class Schedule(SaveModelMixin, DeleteModelMixin, BaseModel):
    def __init__(
        self,
        id=None,
        name=None,
        created_at=None,
        updated_at=None,
        is_active=None,
        schedule_type=None,
        cron=None,
        time=None,
        interval_minutes=None,
        between_start=None,
        between_end=None,
        rule=None,
        filter_parameters=None,
        timezone=None,
        inputs=None,
        workflow=None,
        title=None,
        labels=None,
        next_execution=None,
        last_execution=None,
        version=None,
        updated_by=None,
        description=None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.id = id
        self.name = name
        self.created_at = created_at
        self.updated_at = updated_at
        self.is_active = is_active
        self.schedule_type = schedule_type
        self.cron = cron
        self.time = time
        self.interval_minutes = interval_minutes
        self.between_start = between_start
        self.between_end = between_end
        self.rule = rule
        self.filter_parameters = filter_parameters
        self.timezone = timezone
        self.inputs = inputs
        self.workflow = workflow
        self.title = title
        self.labels = labels
        self.next_execution = next_execution
        self.last_execution = last_execution
        self.version = version
        self.updated_by = updated_by
        self.description = description

    _read_only = [
        "id",
        "version",
        "updated_by",
        "updated_at",
        "created_at",
        "last_execution",
    ]

    @operation
    def duplicate(self: T, name=None, title=None) -> T:
        pass
