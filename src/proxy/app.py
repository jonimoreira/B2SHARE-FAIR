import falcon
from proxy.resources import CommnunityResource, WebAppResource, RecordResource, FileResource


api = falcon.API()
api.add_route('/fdp/', WebAppResource())
api.add_route('/catalogs/', CommnunityResource())
api.add_route('/catalogs/{_id}', CommnunityResource())
api.add_route('/datasets/', RecordResource())
api.add_route('/datasets/{_id}', RecordResource())
api.add_route('/datasets/?q={_query}', RecordResource())
api.add_route('/datasets/?q=community:{_community_id}', RecordResource())
api.add_route('/datasets/?drafts', RecordResource())  #Requires user to be authenticated in B2SHARE
api.add_route('/distributions/{_id}', FileResource())
