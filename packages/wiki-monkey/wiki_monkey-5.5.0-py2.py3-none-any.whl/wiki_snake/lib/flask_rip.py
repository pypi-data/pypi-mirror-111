# This file is part of Flask RIP - Create Flask REST APIs in peace.
# Copyright (C) 2018-present Dario Giovannetti <dev@dariogiovannetti.net>
# Licensed under MIT
# https://github.com/kynikos/lib.py.flask-rip/blob/master/LICENSE

# TODO: requirements.txt, pytest, tox, Travis-CI ###############################################################

# TODO: Integrate with webargs for example to support formData and file submissions ############################
#       https://webargs.readthedocs.io/en/latest/

# TODO: Generate an OpenAPI definition and use it to generate documentation, ###################################
#       tests and web interfaces
#       https://swagger.io/swagger-codegen/
#       Use https://apispec.readthedocs.io/en/latest/

# TODO: Influences/Acknowledgements ############################################################################
#       https://flask-restful.readthedocs.io/en/latest/ (no Swagger support, unmaintained?)
#       https://flask-restplus.readthedocs.io/en/latest/ (fork of flask-restful, but no marshmallow support)

from functools import wraps, partialmethod
from collections import defaultdict, namedtuple
import inspect
import re
from flask import request, make_response
from marshmallow import post_load, UnmarshalResult, ValidationError
from flask_marshmallow import Marshmallow, Schema as MASchema
from apispec import APISpec

IMPLICIT = 0b01
EXPLICIT = 0b10

# Adapted from https://stackoverflow.com/a/1176023/645498
# Don't store in the Resource class to not pollute its namespace
_FIRST_CAP_RE = re.compile('([A-Z]+)([A-Z][a-z])')
_ALL_CAP_RE = re.compile('([a-z0-9])([A-Z])')


def camel_to_kebab(name):
    name1 = _FIRST_CAP_RE.sub(r'\1-\2', name)
    name2 = _ALL_CAP_RE.sub(r'\1-\2', name1).lower()
    return name2.replace('_', '-')


class API:
    # TODO: It would be cool if this accepted a list of packages where to ##############################
    #       look for modules with Resource-derived classes, and import them
    #       dynamically without requiring them to be imported manually in the
    #       main app

    ENDPOINT_GLUE = ':'

    def __init__(self, app, base_path=None, base_endpoint=None,
                 parent_api=None, path_from_endpoint=camel_to_kebab,
                 base_method_path=IMPLICIT, openapi_spec=None):
        self.app = app
        self.parent_api = parent_api
        self.openapi_spec = openapi_spec

        if parent_api:
            self.path_from_endpoint = (path_from_endpoint or
                                       parent_api.path_from_endpoint)
            self.base_method_path = (base_method_path or
                                     parent_api.base_method_path)

            base_endpoint = base_endpoint or self.__class__.__name__
            if parent_api.base_endpoint:
                # Do use the parent glue here
                self.base_endpoint = parent_api.ENDPOINT_GLUE.join((
                    parent_api.base_endpoint, base_endpoint))
            else:
                self.base_endpoint = base_endpoint

            # Don't try to normalize leading/trailing slashes,
            # "we're all consenting adults here"
            base_path = base_path or '/' + path_from_endpoint(
                self.__class__.__name__)
            if parent_api.base_path:
                self.base_path = ''.join((parent_api.base_path, base_path))
            else:
                self.base_path = base_path
        else:
            self.path_from_endpoint = path_from_endpoint
            self.base_method_path = base_method_path
            self.base_endpoint = base_endpoint
            # Don't try to normalize leading/trailing slashes,
            # "we're all consenting adults here"
            self.base_path = base_path

        self.ma = Marshmallow(app)

        if self.openapi_spec:
            self.openapi_spec.setup_plugin('apispec.ext.flask')
            self.openapi_spec.setup_plugin('apispec.ext.marshmallow')

        self.subapis = []
        # TODO: Keep track of the instantiated resources? ##################################################
        # self.resources = []

        self.resource_from_class = ResourceFromClass(self)
        self.delete = self.resource_from_class.delete
        self.get = self.resource_from_class.get
        self.head = self.resource_from_class.head
        self.options = self.resource_from_class.options
        self.patch = self.resource_from_class.patch
        self.post = self.resource_from_class.post
        self.put = self.resource_from_class.put

        # Convenience attributes to allow importing directly from the API
        # instance
        self.Schema = Schema
        self.MASchema = MASchema
        # No point in exporting APISpec too, because that must be already
        # instantiated when constructing this class
        # self.APISpec = APISpec

    def append_api(self, base_endpoint, base_path=None):
        subapi = self.__class__(self.app, parent_api=self, base_path=base_path,
                                base_endpoint=base_endpoint)
        self.subapis.append(subapi)
        return subapi

    # TODO: An alternative would be to accept the already-instantiated resource, #################################
    #       but that would require using the API instance twice: #################################################
    #       api.add_resource(Resource_(api)) #####################################################################
    def add_resource(self, Resource_, *args, **kwargs):
        resource = Resource_()
        self.resource_from_class.post_init(resource, *args, **kwargs)
        return resource

    def resource(self, *args, **kwargs):
        def decorator(Resource_):
            self.add_resource(Resource_, *args, **kwargs)

            @wraps(Resource_)
            def inner(*fargs, **fkwargs):
                return Resource_(*fargs, **fkwargs)
            return inner
        return decorator

    def create_resource(self, *args, **kwargs):
        return ResourceFromFunctions(self, *args, **kwargs)


class _Resource:
    REQUESTMETHOD_TO_GETDATA = {
        'DELETE': lambda: request.args,
        'GET': lambda: request.args,
        'HEAD': lambda: request.args,
        'OPTIONS': lambda: request.args,
        'PATCH': lambda: request.get_json(),
        'POST': lambda: request.get_json(),
        'PUT': lambda: request.get_json(),
    }

    # TODO: I could allow 'many' as a decorator option and use it in #################################
    #       Schema.load() and Schema.jsonify() instead of when instantiating
    #       the schemas, but it's better to recommend to do use the Schema
    #       options directly when instantiating it
    #       Document an example suggesting to use ad-hoc schemas directly in
    #       the decorator call if needed, e.g. @post(Schema(many=True), ...)

    # TODO: Allow adding multiple rules to the same endpoint ###########################################
    #       Also remind that it's still possible to use normal Flask routes ############################

    def __init__(self, api):
        self.api = api

    def post_init(self, endpoint, res_path, resvar_path):
        # TODO: Map endpoints to methods? (Flask has app.view_functions) ###################################
        # self.endpoint_to_methods = defaultdict(list)

        # Don't try to normalize leading/trailing slashes,
        # "we're all consenting adults here"
        self.baseabsrule = ''.join((self.api.base_path or '', res_path,
                                    resvar_path or ''))

        self.res_endpoint = self.api.ENDPOINT_GLUE.join(
            (self.api.base_endpoint, endpoint)
        ) if self.api.base_endpoint else endpoint

    def _route_function(self, function, var_path, http_method, action):
        action = action or function.__name__

        # Don't try to normalize leading/trailing slashes,
        # "we're all consenting adults here"
        baseabsrule = ''.join((self.baseabsrule, var_path or ''))
        # TODO: Optionally convert the underscores in the action name to dashes ###########################
        absrule = '/'.join((baseabsrule, action))

        endpoint = self.api.ENDPOINT_GLUE.join((self.res_endpoint,
                                                function.__name__))

        # TODO: Allow spelling the a default HTTP-method view name with #############################
        #       any capitalization? E.g.: ###########################################################
        #       @api.get(...)
        #       def GeT(self, indata):
        #           return {}
        #       For the moment only support full lowercase ##########################################
        if action == http_method.lower():
            if self.api.base_method_path & IMPLICIT:
                self.api.app.add_url_rule(
                    baseabsrule,
                    endpoint=endpoint,
                    view_func=function,
                    methods=(http_method, ))

            if self.api.base_method_path & EXPLICIT:
                self.api.app.add_url_rule(
                    absrule,
                    endpoint=endpoint,
                    view_func=function,
                    methods=(http_method, ))

        else:
            self.api.app.add_url_rule(
                absrule,
                endpoint=endpoint,
                view_func=function,
                methods=(http_method, ))

        if self.api.openapi_spec:
            with self.api.app.test_request_context():
                # TODO: Properly handle views associated to multiple paths, e.g. #########################
                #       the optional "/resource/get" and "/resource/" cases ##############################
                self.api.openapi_spec.add_path(view=function)

    def _route_function_hook(self, function, var_path, http_method, action):
        raise NotImplementedError()

    def _call_function(self, function, indata, *args, **kwargs):
        raise NotImplementedError()

    def _make_decorator(self, in_method, in_schema, out_schema,
                        var_path=None, action=None, in_get_data=None,
                        out_code=200):
        if in_get_data:
            get_data = in_get_data
        else:
            get_data = self.REQUESTMETHOD_TO_GETDATA[in_method]

        if in_schema:
            # TODO: Validate the data ################################################################
            unmarshal_data = lambda: in_schema.load(get_data())  # noqa
        else:
            unmarshal_data = lambda: get_data()   # noqa

        if out_schema:
            marshal_data = lambda outdata: out_schema.jsonify(outdata)  # noqa
        else:
            marshal_data = lambda outdata: outdata  # noqa

        if in_schema and self.api.openapi_spec:
            # TODO: Check that there aren't duplicated schema names ######################################
            self.api.openapi_spec.definition(in_schema.__class__.__name__,
                                             schema=in_schema.__class__)

        def decorator(function):
            # TODO: Store function.__doc__ as a description for documentation ###############################

            @wraps(function)
            def inner(*args, **kwargs):
                # This might also be a class method, i.e. the first argument
                # could be a class instance
                # def inner(inself, *args, **kwargs):

                indata = unmarshal_data()

                # TODO: Remove the following block once Marshmallow 3 is the #############################
                #       most common version around #######################################################
                if type(indata) is UnmarshalResult:
                    # Marshmallow<3
                    if indata.errors:
                        raise ValidationError(indata.errors)
                    indata = indata.data
                # else it's Marshmallow>=3, which returns the data directly

                outdata = self._call_function(function, indata, *args,
                                              **kwargs)

                return marshal_data(outdata), out_code

            self._route_function_hook(inner, var_path, in_method, action)
            inner._var_path = var_path
            inner._http_method = in_method
            inner._action = action

            return inner
        return decorator

    delete = partialmethod(_make_decorator, 'DELETE')
    get = partialmethod(_make_decorator, 'GET')
    head = partialmethod(_make_decorator, 'HEAD')
    options = partialmethod(_make_decorator, 'OPTIONS')
    patch = partialmethod(_make_decorator, 'PATCH')
    post = partialmethod(_make_decorator, 'POST')
    put = partialmethod(_make_decorator, 'PUT')

    # TODO #########################################################################################
    # An OPTIONS handler is needed to support CORS preflight requests
    # https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS#Preflighted_requests
    # When testing on localhost, the OPTIONS request isn't cached, so the
    # following instructs the browser to cache it; test what happens on a real
    # remote server
    # It would be equally effective to set a catch-all routing rule on the
    # OPTIONS method, but this method allows per-resource customization
    # NOTE: When testing manually it may look like this handler is actually not
    #       needed, but that's only due to the caching below
    # def options(self):
    #     # By default the response to a preflight request isn't cached, so set
    #     # Access-Control-Max-Age explicitly
    #     # TODO: Allow overriding/disabling or setting the max age ##################################
    #     return make_response(("", 204, {'Access-Control-Max-Age': 86400}))


class ResourceFromFunctions(_Resource):
    def __init__(self, api, endpoint, res_path=None, resvar_path=None):
        super().__init__(api)
        respath = res_path or '/' + api.path_from_endpoint(endpoint)
        super().post_init(endpoint, res_path=respath, resvar_path=resvar_path)

    def _route_function_hook(self, function, var_path, http_method, action):
        self._route_function(function, var_path, http_method, action)

    def _call_function(self, function, indata, *args, **kwargs):
        return function(indata, *args, **kwargs)


class ResourceFromClass(_Resource):
    def __init__(self, api):
        super().__init__(api)

    def post_init(self, resource, res_path=None, resvar_path=None):
        respath = res_path or '/' + self.api.path_from_endpoint(
            resource.__class__.__name__)

        super().post_init(endpoint=resource.__class__.__name__,
                          res_path=respath, resvar_path=resvar_path)

        for fname, function in inspect.getmembers(resource,
                                                  predicate=inspect.ismethod):
            try:
                func_var_path = function._var_path
                http_method = function._http_method
                action = function._action
            except AttributeError:
                continue

            self._route_function(function, func_var_path, http_method, action)

    def _route_function_hook(self, function, var_path, http_method, action):
        pass

    def _call_function(self, function, indata, *args, **kwargs):
        return function(args[0], indata, *args[1:], **kwargs)


# TODO: Document that it's still possible to use plain marshmallow schemas ###############################
#       (which simply return dicts) ######################################################################
class Schema(MASchema):
    @post_load
    def make_namedtuple(self, data):
        # Yes, the order of keys() and values() are ensured to correspond
        # https://docs.python.org/3/library/stdtypes.html#dict-views
        return namedtuple("UnmarshalNamedTuple", data.keys())(*data.values())
