import falcon
from proxy.resources import CommnunityResource, WebAppResource


api = falcon.API()
api.add_route('/fdp/', WebAppResource())
api.add_route('/catalog/', CommnunityResource())
api.add_route('/catalog/{_id}', CommnunityResource())
