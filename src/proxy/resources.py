from fair.models import CommunityModel, WebAppModel
from fair.translators import translate_catalog, translate_fdp

from proxy.mixins import ReadResourceMixin, ReadResource

class WebAppResource(ReadResource):
    model = WebAppModel
    translator = translate_fdp


class CommnunityResource(ReadResourceMixin):
    model = CommunityModel
    translator = translate_catalog
