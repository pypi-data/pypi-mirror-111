from libvarya.utils import Config
from werkzeug import Request, Response
from werkzeug.exceptions import HTTPException, abort
from werkzeug.routing import Map, Rule
from werkzeug.utils import ImportStringError, import_string
from xmlrpc.server import CGIXMLRPCRequestHandler
from .globals import _app_stack



class Server(object):
    def __init__(self,
        config: str = 'settings.ini',
        api_rule: str = '/<string:apiv>'
    ) -> None:
        self.__url_map = Map([
            Rule(api_rule, methods=['POST'])])

        self.__handler_pool = {}

        self.__config = Config()
        self.config.from_ini(
            config, associate=True)

        self.__setup_api()

        # set Application instance to local context
        _app_stack.append(self)

    def __setup_api(self) -> None:
        if self.__config.has_option('apienabled', 'default'):
            apis = self.__config['default']['apienabled']
            for api in apis.split(','):
                try:
                    service = import_string(f'api.{api}.Service')

                    handler = CGIXMLRPCRequestHandler()
                    handler.register_instance(
                        service, allow_dotted_names=True)

                    self.__handler_pool[api] = handler
                except ImportStringError:
                    print(f'Module api.{api} has not \"Service\" class.')
        else:
            print(f'No one api package enabled.')

    def __dispatch_request(self, request):
        try:
            if not self.__check_token(request.environ):
                abort(401)

            adapter = self.__url_map.bind_to_environ(request.environ)
            endpoint, values = adapter.match()
    
            apiv = values['apiv']
            if apiv not in self.__handler_pool:
                abort(404)

            handler = self.__handler_pool[apiv]
            return Response(
                handler._marshaled_dispatch(request.data), mimetype='text/xml')

        except HTTPException as e:
            return e

    def __check_token(self, environ):
        if not 'HTTP_X_CLIENT_TOKEN' in environ or not self.__config.has_option(
                'apitoken', 'default'):
            return False
    
        client_token = environ.get('HTTP_X_CLIENT_TOKEN')
        server_token = self.__config['default']['apitoken']

        print(client_token, server_token, client_token == server_token)

        return client_token == server_token

    def __wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.__dispatch_request(request)

        return response(environ, start_response)

    def __call__(self, environ, start_response):
        return self.__wsgi_app(environ, start_response)

    @property
    def config(self) -> "Config":
        return self.__config
