class ReadResourceMixin:
    @classmethod
    def _get_by_id(cls, _id):
        community = cls.model.get_id(_id)
        return cls.translator(community)

    @classmethod
    def _get_all(cls, query):
        communities = cls.model.get_all(query)
        return [cls.translator(c) for c in communities]

    def on_get(self, req, resp, _id=None):
        if _id:
            print(_id)
            resp.media = self._get_by_id(_id)
        else:
            resp.media = self._get_all(req.query_string)


class ReadResource:
    @classmethod
    def _get(cls):
        b2entity = cls.model.get('')
        return cls.translator(b2entity)

    def on_get(self, req, resp, _id=None):
        resp.media = self._get()
