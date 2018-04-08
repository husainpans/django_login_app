
from rest_framework.routers import Route,  SimpleRouter,DynamicRoute


#Custom Router Class
class CustomReadOnlyRouter(SimpleRouter):
    """
    A router for read-only APIs, which doesn't use trailing slashes.
    """
    routes = [
        Route(
            url=r'^{prefix}/$',
            mapping={
                'get': 'list',
                'post': 'create'
            },
            detail=False,
            name='{basename}-list',
            initkwargs={'suffix': 'List'}
        ),
        DynamicRoute(
            url=r'^{prefix}/{url_path}/$',
            name='{basename}-{url_name}',
            detail=False,
            initkwargs={}
        ),
        Route(
            url=r'^{prefix}/{lookup}/$',
            mapping={
                'get': 'retrieve',
                'put': 'update',
                'patch': 'partial_update',
                'delete': 'destroy'
            },
            name='{basename}-detail',
            detail=True,
            initkwargs={'suffix': 'Detail'}
        ),
     
        DynamicRoute(
            url=r'^{prefix}/{url_path}/{lookup}/$',
            name='{basename}-{url_name}',
            detail=True,
            initkwargs={}
        )
    ]