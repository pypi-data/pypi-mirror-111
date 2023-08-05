"""

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: 0.0.0
    Generated by: https://openapi-generator.tech
"""


import re  # noqa: F401
import sys  # noqa: F401

from satnogsnetworkapiclient.model_utils import (  # noqa: F401
    ApiTypeError,
    ModelComposed,
    ModelNormal,
    ModelSimple,
    cached_property,
    change_keys_js_to_python,
    convert_js_args_to_python_args,
    date,
    datetime,
    file_type,
    none_type,
    validate_get_composed_info,
)
from ..model_utils import OpenApiModel
from satnogsnetworkapiclient.exceptions import ApiAttributeError



class Station(ModelNormal):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.

    Attributes:
      allowed_values (dict): The key is the tuple path to the attribute
          and the for var_name this is (var_name,). The value is a dict
          with a capitalized key describing the allowed value and an allowed
          value. These dicts store the allowed enum values.
      attribute_map (dict): The key is attribute name
          and the value is json key in definition.
      discriminator_value_class_map (dict): A dict to go from the discriminator
          variable value to the discriminator class name.
      validations (dict): The key is the tuple path to the attribute
          and the for var_name this is (var_name,). The value is a dict
          that stores validations for max_length, min_length, max_items,
          min_items, exclusive_maximum, inclusive_maximum, exclusive_minimum,
          inclusive_minimum, and regex.
      additional_properties_type (tuple): A tuple of classes accepted
          as additional properties values.
    """

    allowed_values = {
    }

    validations = {
        ('name',): {
            'max_length': 45,
        },
        ('lat',): {
            'inclusive_maximum': 90,
            'inclusive_minimum': -90,
        },
        ('lng',): {
            'inclusive_maximum': 180,
            'inclusive_minimum': -180,
        },
        ('qthlocator',): {
            'max_length': 8,
        },
        ('description',): {
            'max_length': 500,
        },
        ('client_version',): {
            'max_length': 45,
        },
        ('target_utilization',): {
            'inclusive_maximum': 100,
            'inclusive_minimum': 0,
        },
    }

    @cached_property
    def additional_properties_type():
        """
        This must be a method because a model may have properties that are
        of type self, this must run after the class is loaded
        """
        return (bool, date, datetime, dict, float, int, list, str, none_type,)  # noqa: E501

    _nullable = False

    @cached_property
    def openapi_types():
        """
        This must be a method because a model may have properties that are
        of type self, this must run after the class is loaded

        Returns
            openapi_types (dict): The key is attribute name
                and the value is attribute type.
        """
        return {
            'id': (int,),  # noqa: E501
            'name': (str,),  # noqa: E501
            'altitude': (str,),  # noqa: E501
            'min_horizon': (str,),  # noqa: E501
            'lat': (float,),  # noqa: E501
            'lng': (float,),  # noqa: E501
            'antenna': (str,),  # noqa: E501
            'created': (datetime,),  # noqa: E501
            'status': (str,),  # noqa: E501
            'observations': (str,),  # noqa: E501
            'qthlocator': (str,),  # noqa: E501
            'last_seen': (datetime, none_type,),  # noqa: E501
            'description': (str,),  # noqa: E501
            'client_version': (str,),  # noqa: E501
            'target_utilization': (int, none_type,),  # noqa: E501
        }

    @cached_property
    def discriminator():
        return None


    attribute_map = {
        'id': 'id',  # noqa: E501
        'name': 'name',  # noqa: E501
        'altitude': 'altitude',  # noqa: E501
        'min_horizon': 'min_horizon',  # noqa: E501
        'lat': 'lat',  # noqa: E501
        'lng': 'lng',  # noqa: E501
        'antenna': 'antenna',  # noqa: E501
        'created': 'created',  # noqa: E501
        'status': 'status',  # noqa: E501
        'observations': 'observations',  # noqa: E501
        'qthlocator': 'qthlocator',  # noqa: E501
        'last_seen': 'last_seen',  # noqa: E501
        'description': 'description',  # noqa: E501
        'client_version': 'client_version',  # noqa: E501
        'target_utilization': 'target_utilization',  # noqa: E501
    }

    read_only_vars = {
        'id',  # noqa: E501
        'altitude',  # noqa: E501
        'min_horizon',  # noqa: E501
        'antenna',  # noqa: E501
        'created',  # noqa: E501
        'status',  # noqa: E501
        'observations',  # noqa: E501
    }

    _composed_schemas = {}

    @classmethod
    @convert_js_args_to_python_args
    def _from_openapi_data(cls, id, name, altitude, min_horizon, lat, lng, antenna, created, status, observations, *args, **kwargs):  # noqa: E501
        """Station - a model defined in OpenAPI

        Args:
            id (int):
            name (str):
            altitude (str):
            min_horizon (str):
            lat (float): eg. 38.01697
            lng (float): eg. 23.7314
            antenna (str):
            created (datetime):
            status (str):
            observations (str):

        Keyword Args:
            _check_type (bool): if True, values for parameters in openapi_types
                                will be type checked and a TypeError will be
                                raised if the wrong type is input.
                                Defaults to True
            _path_to_item (tuple/list): This is a list of keys or values to
                                drill down to the model in received_data
                                when deserializing a response
            _spec_property_naming (bool): True if the variable names in the input data
                                are serialized names, as specified in the OpenAPI document.
                                False if the variable names in the input data
                                are pythonic names, e.g. snake case (default)
            _configuration (Configuration): the instance to use when
                                deserializing a file_type parameter.
                                If passed, type conversion is attempted
                                If omitted no type conversion is done.
            _visited_composed_classes (tuple): This stores a tuple of
                                classes that we have traveled through so that
                                if we see that class again we will not use its
                                discriminator again.
                                When traveling through a discriminator, the
                                composed schema that is
                                is traveled through is added to this set.
                                For example if Animal has a discriminator
                                petType and we pass in "Dog", and the class Dog
                                allOf includes Animal, we move through Animal
                                once using the discriminator, and pick Dog.
                                Then in Dog, we will make an instance of the
                                Animal class but this time we won't travel
                                through its discriminator because we passed in
                                _visited_composed_classes = (Animal,)
            qthlocator (str): [optional]  # noqa: E501
            last_seen (datetime, none_type): [optional]  # noqa: E501
            description (str): Max 500 characters. [optional]  # noqa: E501
            client_version (str): [optional]  # noqa: E501
            target_utilization (int, none_type): Target utilization factor for your station. [optional]  # noqa: E501
        """

        _check_type = kwargs.pop('_check_type', True)
        _spec_property_naming = kwargs.pop('_spec_property_naming', False)
        _path_to_item = kwargs.pop('_path_to_item', ())
        _configuration = kwargs.pop('_configuration', None)
        _visited_composed_classes = kwargs.pop('_visited_composed_classes', ())

        self = super(OpenApiModel, cls).__new__(cls)

        if args:
            raise ApiTypeError(
                "Invalid positional arguments=%s passed to %s. Remove those invalid positional arguments." % (
                    args,
                    self.__class__.__name__,
                ),
                path_to_item=_path_to_item,
                valid_classes=(self.__class__,),
            )

        self._data_store = {}
        self._check_type = _check_type
        self._spec_property_naming = _spec_property_naming
        self._path_to_item = _path_to_item
        self._configuration = _configuration
        self._visited_composed_classes = _visited_composed_classes + (self.__class__,)

        self.id = id
        self.name = name
        self.altitude = altitude
        self.min_horizon = min_horizon
        self.lat = lat
        self.lng = lng
        self.antenna = antenna
        self.created = created
        self.status = status
        self.observations = observations
        for var_name, var_value in kwargs.items():
            if var_name not in self.attribute_map and \
                        self._configuration is not None and \
                        self._configuration.discard_unknown_keys and \
                        self.additional_properties_type is None:
                # discard variable.
                continue
            setattr(self, var_name, var_value)
        return self

    required_properties = set([
        '_data_store',
        '_check_type',
        '_spec_property_naming',
        '_path_to_item',
        '_configuration',
        '_visited_composed_classes',
    ])

    @convert_js_args_to_python_args
    def __init__(self, name, lat, lng, *args, **kwargs):  # noqa: E501
        """Station - a model defined in OpenAPI

            name (str):
            lat (float): eg. 38.01697
            lng (float): eg. 23.7314
        Keyword Args:
            _check_type (bool): if True, values for parameters in openapi_types
                                will be type checked and a TypeError will be
                                raised if the wrong type is input.
                                Defaults to True
            _path_to_item (tuple/list): This is a list of keys or values to
                                drill down to the model in received_data
                                when deserializing a response
            _spec_property_naming (bool): True if the variable names in the input data
                                are serialized names, as specified in the OpenAPI document.
                                False if the variable names in the input data
                                are pythonic names, e.g. snake case (default)
            _configuration (Configuration): the instance to use when
                                deserializing a file_type parameter.
                                If passed, type conversion is attempted
                                If omitted no type conversion is done.
            _visited_composed_classes (tuple): This stores a tuple of
                                classes that we have traveled through so that
                                if we see that class again we will not use its
                                discriminator again.
                                When traveling through a discriminator, the
                                composed schema that is
                                is traveled through is added to this set.
                                For example if Animal has a discriminator
                                petType and we pass in "Dog", and the class Dog
                                allOf includes Animal, we move through Animal
                                once using the discriminator, and pick Dog.
                                Then in Dog, we will make an instance of the
                                Animal class but this time we won't travel
                                through its discriminator because we passed in
                                _visited_composed_classes = (Animal,)
            qthlocator (str): [optional]  # noqa: E501
            last_seen (datetime, none_type): [optional]  # noqa: E501
            description (str): Max 500 characters. [optional]  # noqa: E501
            client_version (str): [optional]  # noqa: E501
            target_utilization (int, none_type): Target utilization factor for your station. [optional]  # noqa: E501
        """

        _check_type = kwargs.pop('_check_type', True)
        _spec_property_naming = kwargs.pop('_spec_property_naming', False)
        _path_to_item = kwargs.pop('_path_to_item', ())
        _configuration = kwargs.pop('_configuration', None)
        _visited_composed_classes = kwargs.pop('_visited_composed_classes', ())

        if args:
            raise ApiTypeError(
                "Invalid positional arguments=%s passed to %s. Remove those invalid positional arguments." % (
                    args,
                    self.__class__.__name__,
                ),
                path_to_item=_path_to_item,
                valid_classes=(self.__class__,),
            )

        self._data_store = {}
        self._check_type = _check_type
        self._spec_property_naming = _spec_property_naming
        self._path_to_item = _path_to_item
        self._configuration = _configuration
        self._visited_composed_classes = _visited_composed_classes + (self.__class__,)

        self.name = name
        self.lat = lat
        self.lng = lng
        for var_name, var_value in kwargs.items():
            if var_name not in self.attribute_map and \
                        self._configuration is not None and \
                        self._configuration.discard_unknown_keys and \
                        self.additional_properties_type is None:
                # discard variable.
                continue
            setattr(self, var_name, var_value)
            if var_name in self.read_only_vars:
                raise ApiAttributeError(f"`{var_name}` is a read-only attribute. Use `from_openapi_data` to instantiate "
                                     f"class with read only attributes.")
