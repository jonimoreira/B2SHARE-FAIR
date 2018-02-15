from fair.models import CommunityModel
from fair.translators import translate_catalog

from proxy.mixins import ReadResourceMixin


class CommnunityResource(ReadResourceMixin):
    model = CommunityModel
    translator = translate_catalog


