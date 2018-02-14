import falcon
from proxy.resources import CommnunityResource


api = falcon.API()
api.add_route('/community/', CommnunityResource())
api.add_route('/community/{_id}', CommnunityResource())
