import copy

from office365.runtime.client_value import ClientValue
from office365.runtime.odata.json_light_format import JsonLightFormat
from office365.runtime.odata.odata_query_options import QueryOptions


class ClientObject(object):

    def __init__(self, context, resource_path=None, parent_collection=None, namespace=None):
        """
        Base client object which define named properties and relationships of an entity

        :type parent_collection: office365.runtime.client_object_collection.ClientObjectCollection or None
        :type resource_path: office365.runtime.resource_path.ResourcePath or None
        :type context: office365.runtime.client_runtime_context.ClientRuntimeContext
        :type namespace: str
        """
        self._properties = {}
        self._changed_properties = []
        self._entity_type_name = None
        self._query_options = QueryOptions()
        self._parent_collection = parent_collection
        self._context = context
        self._resource_path = resource_path
        self._namespace = namespace

    def clear(self):
        self._changed_properties = []

    def execute_query(self):
        self.context.execute_query()
        return self

    def execute_query_retry(self, max_retry=5, timeout_secs=5, success_callback=None, failure_callback=None):
        self.context.execute_query_retry(max_retry=max_retry,
                                         timeout_secs=timeout_secs,
                                         success_callback=success_callback,
                                         failure_callback=failure_callback)
        return self

    def build_request(self):
        return self.context.build_request()

    def get(self):
        self.context.load(self)
        return self

    def is_property_available(self, name):
        """Returns a Boolean value that indicates whether the specified property has been retrieved or set.

        :param str name: A Property name
        """
        if name in self.properties:
            return True
        return False

    def expand(self, names):
        """

        :type names: list[str]
        """
        self.query_options.expand = names
        return self

    def select(self, names):
        """

        :param list[str] names:
        :return:
        """
        self.query_options.select = names
        return self

    def remove_from_parent_collection(self):
        if self._parent_collection is None:
            return
        self._parent_collection.remove_child(self)

    def get_property(self, name):
        """
        Gets property value

        :param str name: property name
        """
        normalized_name = name[0].lower() + name[1:]
        return getattr(self, normalized_name, self._properties.get(name, None))

    def set_property(self, name, value, persist_changes=True):
        """Sets property value

        :param str name: Property name
        :param any value: Property value
        :param bool persist_changes: Persist changes
        """
        if persist_changes:
            self._changed_properties.append(name)

        prop_type = self.get_property(name)
        if isinstance(prop_type, ClientObject) or isinstance(prop_type, ClientValue) and value is not None:
            if isinstance(value, list):
                [prop_type.set_property(i, v, persist_changes) for i, v in enumerate(value)]
                self._properties[name] = prop_type
            elif isinstance(value, dict):
                [prop_type.set_property(k, v, persist_changes) for k, v in value.items()]
                self._properties[name] = prop_type
            else:
                self._properties[name] = value
        else:
            self._properties[name] = value
        return self

    def ensure_property(self, name, action=None):
        """
        Ensures if property is loaded

        :type action: () -> None
        :type name: str
        """
        return self.ensure_properties([name], action)

    def ensure_properties(self, names, action):
        """
        Ensure if list of properties are loaded

        :type action: () -> None
        :type names: str or list[str]
        """
        def _exec_action():
            if callable(action):
                action()

        names_to_include = [n for n in names if not self.is_property_available(n)]
        if len(names_to_include) > 0:
            qry = self.context.load(self, names_to_include)
            self.context.execute_after_query(qry, _exec_action)
        else:
            _exec_action()
        return self

    def clone_object(self):
        result = copy.deepcopy(self)
        result._context = self.context
        return result

    @property
    def entity_type_name(self):
        if self._entity_type_name is None:
            if self._namespace is None:
                self._entity_type_name = type(self).__name__
            else:
                self._entity_type_name = ".".join([self._namespace, type(self).__name__])
        return self._entity_type_name

    @property
    def resource_url(self):
        """Generate resource Url

        :rtype: str or None
        """
        if self.resource_path:
            url = self.context.service_root_url() + self.resource_path.to_url()
            if not self.query_options.is_empty:
                url = url + "?" + self._query_options.to_url()
            return url
        return None

    @property
    def context(self):
        return self._context

    @property
    def resource_path(self):
        return self._resource_path

    @property
    def query_options(self):
        return self._query_options

    @property
    def properties(self):
        return self._properties

    @property
    def parent_collection(self):
        return self._parent_collection

    def to_json(self, json_format=None):
        """
        :type json_format: office365.runtime.odata.odata_json_format.ODataJsonFormat or None
        """
        json = dict((k, self.get_property(k)) for k in self.properties if k in self._changed_properties)
        for k, v in json.items():
            if isinstance(v, ClientObject) or isinstance(v, ClientValue):
                json[k] = v.to_json(json_format)

        if isinstance(json_format, JsonLightFormat) and json_format.is_verbose and self.entity_type_name is not None:
            json[json_format.metadata_type_tag_name] = {'type': self.entity_type_name}
        return json
