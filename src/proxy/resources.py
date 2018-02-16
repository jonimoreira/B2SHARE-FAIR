from fair.models import WebAppModel, CommunityModel, RecordModel, FileModel
from fair.translators import translate_fdp, translate_catalog, translate_dataset, translate_distribution

from proxy.mixins import ReadResourceMixin, ReadResource

class WebAppResource(ReadResource):
    model = WebAppModel
    translator = translate_fdp


class CommnunityResource(ReadResourceMixin):
    model = CommunityModel
    translator = translate_catalog


class RecordResource(ReadResourceMixin):
    model = RecordModel
    translator = translate_dataset


class FileResource(ReadResourceMixin):
    model = FileModel
    translator = translate_distribution
