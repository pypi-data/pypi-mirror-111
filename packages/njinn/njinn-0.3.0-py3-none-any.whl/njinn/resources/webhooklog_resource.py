from ..base import *
from ..models import *
from .mixins import *


class WebhookLogResource(
    GetResourceMixin, BaseResource,
):
    def __init__(self, parent: BaseResource):
        super().__init__("log", WebhookLog, parent.client)
        self.parent = parent


Mapping.register(WebhookLog, WebhookLogResource)
