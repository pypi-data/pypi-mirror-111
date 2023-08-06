import logging
from typing import Any, Callable, Dict, Generic, List, Mapping, Optional, Set, Tuple, Type, TypeVar

from flask import Blueprint, Flask, Request, Response, current_app, jsonify, request
from flask.testing import FlaskClient
from flask.views import MethodView
from werkzeug.datastructures import EnvironHeaders, ImmutableMultiDict
from werkzeug.exceptions import NotFound

from pait.api_doc.html import get_redoc_html as _get_redoc_html
from pait.api_doc.html import get_swagger_ui_html as _get_swagger_ui_html
from pait.api_doc.open_api import PaitOpenApi
from pait.app.base import BaseAppHelper, BaseTestHelper
from pait.core import pait as _pait
from pait.g import pait_data
from pait.model.core import PaitCoreModel
from pait.model.response import PaitResponseModel
from pait.model.status import PaitStatus
from pait.util import LazyProperty, gen_example_json_from_schema


class AppHelper(BaseAppHelper):
    RequestType = Request
    FormType = ImmutableMultiDict
    FileType = Request.files
    HeaderType = EnvironHeaders
    app_name = "flask"

    def __init__(self, class_: Any, args: Tuple[Any, ...], kwargs: Mapping[str, Any]):
        super().__init__(class_, args, kwargs)

        self.request = request

    def body(self) -> dict:
        return request.json

    def cookie(self) -> dict:
        return request.cookies

    def file(self) -> Request.files:  # type: ignore
        return request.files

    def form(self) -> Request.form:  # type: ignore
        return request.form

    def header(self) -> EnvironHeaders:
        return request.headers

    def path(self) -> Mapping[str, Any]:
        return self.request_kwargs

    def query(self) -> Dict[str, Any]:
        return request.args

    @LazyProperty(is_class_func=True)
    def multiform(self) -> Dict[str, List[Any]]:
        return {key: request.form.getlist(key) for key, _ in request.form.items()}

    @LazyProperty(is_class_func=True)
    def multiquery(self) -> Dict[str, List[Any]]:
        return {key: request.args.getlist(key) for key, _ in request.args.items()}

    @staticmethod
    def make_mock_response(pait_response: Type[PaitResponseModel]) -> Response:
        if pait_response.media_type == "application/json" and pait_response.response_data:
            resp: Response = jsonify(gen_example_json_from_schema(pait_response.response_data.schema()))
            resp.status_code = pait_response.status_code[0]
            if pait_response.header:
                resp.headers.update(pait_response.header)  # type: ignore
            return resp
        else:
            raise NotImplementedError()


def load_app(app: Flask, project_name: str = "") -> Dict[str, PaitCoreModel]:
    """Read data from the route that has been registered to `pait`"""
    _pait_data: Dict[str, PaitCoreModel] = {}
    if not project_name:
        project_name = app.import_name.split(".")[0]
    for route in app.url_map.iter_rules():
        path: str = route.rule
        method_set: Set[str] = route.methods
        route_name: str = route.endpoint
        endpoint: Callable = app.view_functions[route_name]
        pait_id: Optional[str] = getattr(endpoint, "_pait_id", None)
        if not pait_id:
            if route_name == "static":
                continue
            view_class_endpoint = getattr(endpoint, "view_class", None)
            if not view_class_endpoint or not issubclass(view_class_endpoint, MethodView):
                logging.warning(f"loan path:{path} fail, endpoint:{endpoint} not `view_class` attributes")
                continue
            for method in view_class_endpoint.methods:
                method = method.lower()
                method_set = {method}
                endpoint = getattr(view_class_endpoint, method, None)
                if not endpoint:
                    continue
                pait_id = getattr(endpoint, "_pait_id", None)
                if not pait_id:
                    continue
                pait_data.add_route_info(
                    AppHelper.app_name, pait_id, path, method_set, f"{route_name}.{method}", project_name
                )
                _pait_data[pait_id] = pait_data.get_pait_data(AppHelper.app_name, pait_id)
        else:
            pait_data.add_route_info(AppHelper.app_name, pait_id, path, method_set, route_name, project_name)
            _pait_data[pait_id] = pait_data.get_pait_data(AppHelper.app_name, pait_id)
    return _pait_data


_T = TypeVar("_T", bound=Response)


class FlaskTestHelper(BaseTestHelper, Generic[_T]):
    client: FlaskClient

    def _app_init_field(self) -> None:
        if self.file_dict:
            if self.form_dict:
                self.form_dict.update(self.file_dict)
            else:
                self.form_dict = self.file_dict

        if self.cookie_dict:
            for key, value in self.cookie_dict.items():
                self.client.set_cookie("localhost", key, value)

    def _gen_pait_dict(self) -> Dict[str, PaitCoreModel]:
        return load_app(self.client.application)

    def _assert_response(self, resp: Response) -> None:
        response_model: Type[PaitResponseModel] = self.pait_core_model.response_model_list[0]
        assert resp.status_code in response_model.status_code
        assert resp.mimetype == response_model.media_type
        if response_model.response_data:
            assert response_model.response_data(**resp.get_json())

    def _replace_path(self, path_str: str) -> Optional[str]:
        if self.path_dict and path_str[0] == "<" and path_str[-1] == ">":
            return self.path_dict[path_str[1:-1]]
        return None

    def _make_response(self, method: str) -> Response:
        return self.client.open(
            self.path, data=self.form_dict, json=self.body_dict, headers=self.header_dict, method=method
        )


def pait(
    author: Optional[Tuple[str]] = None,
    desc: Optional[str] = None,
    summary: Optional[str] = None,
    name: Optional[str] = None,
    status: Optional[PaitStatus] = None,
    group: Optional[str] = None,
    tag: Optional[Tuple[str, ...]] = None,
    response_model_list: List[Type[PaitResponseModel]] = None,
) -> Callable:
    """Help flask provide parameter checks and type conversions for each routing function/cbv class"""
    return _pait(
        AppHelper,
        author=author,
        desc=desc,
        name=name,
        summary=summary,
        status=status,
        group=group,
        tag=tag,
        response_model_list=response_model_list,
    )


def add_doc_route(
    app: Flask,
    prefix: str = "/",
    pin_code: str = "",
    title: str = "Pait Doc",
    open_api_tag_list: Optional[List[Dict[str, Any]]] = None,
) -> None:
    if pin_code:
        logging.info(f"doc route start pin code:{pin_code}")

    def _get_request_pin_code() -> Optional[str]:
        r_pin_code: Optional[str] = request.args.to_dict().get("pin_code", None)
        if pin_code:
            if r_pin_code != pin_code:
                raise NotFound
        return r_pin_code

    def _get_open_json_url() -> str:
        r_pin_code: Optional[str] = _get_request_pin_code()
        openapi_json_url: str = f"http://{request.host}{'/'.join(request.path.split('/')[:-1])}/openapi.json"
        if r_pin_code:
            openapi_json_url += f"?pin_code={r_pin_code}"
        return openapi_json_url

    def get_redoc_html() -> str:
        return _get_redoc_html(_get_open_json_url(), title)

    def get_swagger_ui_html() -> str:
        return _get_swagger_ui_html(_get_open_json_url(), title)

    def openapi_route() -> dict:
        _get_request_pin_code()
        pait_dict: Dict[str, PaitCoreModel] = load_app(current_app)
        pait_openapi: PaitOpenApi = PaitOpenApi(
            pait_dict,
            title=title,
            open_api_server_list=[{"url": f"http://{request.host}", "description": ""}],
            open_api_tag_list=open_api_tag_list,
        )
        return pait_openapi.open_api_dict

    blueprint: Blueprint = Blueprint("api doc", __name__, url_prefix=prefix)
    blueprint.add_url_rule("/redoc", view_func=get_redoc_html, methods=["GET"])
    blueprint.add_url_rule("/swagger", view_func=get_swagger_ui_html, methods=["GET"])
    blueprint.add_url_rule("/openapi.json", view_func=openapi_route, methods=["GET"])
    app.register_blueprint(blueprint)
