from ..base import *
from ..models import *
from ..njinn_client import NjinnClient
from .mixins import *


class WebhookResource(
    GetResourceMixin,
    SaveResourceMixin,
    CreateResourceMixin,
    DeleteResouceMixin,
    BaseResource,
):
    def __init__(self, client: NjinnClient):
        super().__init__("api/v1/hooks", Webhook, client)

    def duplicate(self, **kwargs) -> Webhook:
        return self.operation("duplicate", Webhook).post(**kwargs)


Mapping.register(Webhook, WebhookResource)
