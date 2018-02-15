class ReadResourceMixin:
    @classmethod
    def _get_by_id(cls, _id):
        community = cls.model.get_id(_id)
        return cls.translator(community)

    @classmethod
    def _get_all(cls):
        communities = cls.model.get_all()
        return [cls.translator(c) for c in communities]

    def on_get(self, req, resp, _id=None):
        resp.media = self._get_by_id(_id) if _id else self._get_all()

