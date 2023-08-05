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


def lazy_import():
    from satnogsnetworkapiclient.model.demod_data import DemodData
    globals()['DemodData'] = DemodData


class PatchedObservation(ModelNormal):
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
        ('client_version',): {
            'max_length': 255,
        },
    }

    @cached_property
    def additional_properties_type():
        """
        This must be a method because a model may have properties that are
        of type self, this must run after the class is loaded
        """
        lazy_import()
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
        lazy_import()
        return {
            'id': (int,),  # noqa: E501
            'start': (datetime,),  # noqa: E501
            'end': (datetime,),  # noqa: E501
            'ground_station': (int,),  # noqa: E501
            'transmitter': (str,),  # noqa: E501
            'norad_cat_id': (str,),  # noqa: E501
            'payload': (str, none_type,),  # noqa: E501
            'waterfall': (str, none_type,),  # noqa: E501
            'demoddata': ([DemodData],),  # noqa: E501
            'station_name': (str,),  # noqa: E501
            'station_lat': (str,),  # noqa: E501
            'station_lng': (str,),  # noqa: E501
            'station_alt': (str,),  # noqa: E501
            'vetted_status': (str,),  # noqa: E501
            'vetted_user': (str,),  # noqa: E501
            'vetted_datetime': (str,),  # noqa: E501
            'archived': (bool,),  # noqa: E501
            'archive_url': (str,),  # noqa: E501
            'client_version': (str,),  # noqa: E501
            'client_metadata': (str,),  # noqa: E501
            'status': (str,),  # noqa: E501
            'waterfall_status': (str,),  # noqa: E501
            'waterfall_status_user': (int,),  # noqa: E501
            'waterfall_status_datetime': (datetime,),  # noqa: E501
            'rise_azimuth': (float,),  # noqa: E501
            'set_azimuth': (float,),  # noqa: E501
            'max_altitude': (float,),  # noqa: E501
            'transmitter_uuid': (str,),  # noqa: E501
            'transmitter_description': (str,),  # noqa: E501
            'transmitter_type': (dict,),  # noqa: E501
            'transmitter_uplink_low': (int,),  # noqa: E501
            'transmitter_uplink_high': (int,),  # noqa: E501
            'transmitter_uplink_drift': (int,),  # noqa: E501
            'transmitter_downlink_low': (int,),  # noqa: E501
            'transmitter_downlink_high': (int,),  # noqa: E501
            'transmitter_downlink_drift': (int,),  # noqa: E501
            'transmitter_mode': (str,),  # noqa: E501
            'transmitter_invert': (bool,),  # noqa: E501
            'transmitter_baud': (float,),  # noqa: E501
            'transmitter_updated': (str,),  # noqa: E501
            'tle0': (str,),  # noqa: E501
            'tle1': (str,),  # noqa: E501
            'tle2': (str,),  # noqa: E501
        }

    @cached_property
    def discriminator():
        return None


    attribute_map = {
        'id': 'id',  # noqa: E501
        'start': 'start',  # noqa: E501
        'end': 'end',  # noqa: E501
        'ground_station': 'ground_station',  # noqa: E501
        'transmitter': 'transmitter',  # noqa: E501
        'norad_cat_id': 'norad_cat_id',  # noqa: E501
        'payload': 'payload',  # noqa: E501
        'waterfall': 'waterfall',  # noqa: E501
        'demoddata': 'demoddata',  # noqa: E501
        'station_name': 'station_name',  # noqa: E501
        'station_lat': 'station_lat',  # noqa: E501
        'station_lng': 'station_lng',  # noqa: E501
        'station_alt': 'station_alt',  # noqa: E501
        'vetted_status': 'vetted_status',  # noqa: E501
        'vetted_user': 'vetted_user',  # noqa: E501
        'vetted_datetime': 'vetted_datetime',  # noqa: E501
        'archived': 'archived',  # noqa: E501
        'archive_url': 'archive_url',  # noqa: E501
        'client_version': 'client_version',  # noqa: E501
        'client_metadata': 'client_metadata',  # noqa: E501
        'status': 'status',  # noqa: E501
        'waterfall_status': 'waterfall_status',  # noqa: E501
        'waterfall_status_user': 'waterfall_status_user',  # noqa: E501
        'waterfall_status_datetime': 'waterfall_status_datetime',  # noqa: E501
        'rise_azimuth': 'rise_azimuth',  # noqa: E501
        'set_azimuth': 'set_azimuth',  # noqa: E501
        'max_altitude': 'max_altitude',  # noqa: E501
        'transmitter_uuid': 'transmitter_uuid',  # noqa: E501
        'transmitter_description': 'transmitter_description',  # noqa: E501
        'transmitter_type': 'transmitter_type',  # noqa: E501
        'transmitter_uplink_low': 'transmitter_uplink_low',  # noqa: E501
        'transmitter_uplink_high': 'transmitter_uplink_high',  # noqa: E501
        'transmitter_uplink_drift': 'transmitter_uplink_drift',  # noqa: E501
        'transmitter_downlink_low': 'transmitter_downlink_low',  # noqa: E501
        'transmitter_downlink_high': 'transmitter_downlink_high',  # noqa: E501
        'transmitter_downlink_drift': 'transmitter_downlink_drift',  # noqa: E501
        'transmitter_mode': 'transmitter_mode',  # noqa: E501
        'transmitter_invert': 'transmitter_invert',  # noqa: E501
        'transmitter_baud': 'transmitter_baud',  # noqa: E501
        'transmitter_updated': 'transmitter_updated',  # noqa: E501
        'tle0': 'tle0',  # noqa: E501
        'tle1': 'tle1',  # noqa: E501
        'tle2': 'tle2',  # noqa: E501
    }

    read_only_vars = {
        'id',  # noqa: E501
        'start',  # noqa: E501
        'end',  # noqa: E501
        'ground_station',  # noqa: E501
        'transmitter',  # noqa: E501
        'norad_cat_id',  # noqa: E501
        'station_name',  # noqa: E501
        'station_lat',  # noqa: E501
        'station_lng',  # noqa: E501
        'station_alt',  # noqa: E501
        'vetted_status',  # noqa: E501
        'vetted_user',  # noqa: E501
        'vetted_datetime',  # noqa: E501
        'archived',  # noqa: E501
        'archive_url',  # noqa: E501
        'status',  # noqa: E501
        'waterfall_status',  # noqa: E501
        'waterfall_status_user',  # noqa: E501
        'waterfall_status_datetime',  # noqa: E501
        'rise_azimuth',  # noqa: E501
        'set_azimuth',  # noqa: E501
        'max_altitude',  # noqa: E501
        'transmitter_uuid',  # noqa: E501
        'transmitter_description',  # noqa: E501
        'transmitter_type',  # noqa: E501
        'transmitter_uplink_low',  # noqa: E501
        'transmitter_uplink_high',  # noqa: E501
        'transmitter_uplink_drift',  # noqa: E501
        'transmitter_downlink_low',  # noqa: E501
        'transmitter_downlink_high',  # noqa: E501
        'transmitter_downlink_drift',  # noqa: E501
        'transmitter_mode',  # noqa: E501
        'transmitter_invert',  # noqa: E501
        'transmitter_baud',  # noqa: E501
        'transmitter_updated',  # noqa: E501
        'tle0',  # noqa: E501
        'tle1',  # noqa: E501
        'tle2',  # noqa: E501
    }

    _composed_schemas = {}

    @classmethod
    @convert_js_args_to_python_args
    def _from_openapi_data(cls, *args, **kwargs):  # noqa: E501
        """PatchedObservation - a model defined in OpenAPI

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
            id (int): [optional]  # noqa: E501
            start (datetime): [optional]  # noqa: E501
            end (datetime): [optional]  # noqa: E501
            ground_station (int): [optional]  # noqa: E501
            transmitter (str): [optional]  # noqa: E501
            norad_cat_id (str): [optional]  # noqa: E501
            payload (str, none_type): [optional]  # noqa: E501
            waterfall (str, none_type): [optional]  # noqa: E501
            demoddata ([DemodData]): [optional]  # noqa: E501
            station_name (str): [optional]  # noqa: E501
            station_lat (str): [optional]  # noqa: E501
            station_lng (str): [optional]  # noqa: E501
            station_alt (str): [optional]  # noqa: E501
            vetted_status (str): [optional]  # noqa: E501
            vetted_user (str): [optional]  # noqa: E501
            vetted_datetime (str): [optional]  # noqa: E501
            archived (bool): [optional]  # noqa: E501
            archive_url (str): [optional]  # noqa: E501
            client_version (str): [optional]  # noqa: E501
            client_metadata (str): [optional]  # noqa: E501
            status (str): [optional]  # noqa: E501
            waterfall_status (str): [optional]  # noqa: E501
            waterfall_status_user (int): [optional]  # noqa: E501
            waterfall_status_datetime (datetime): [optional]  # noqa: E501
            rise_azimuth (float): [optional]  # noqa: E501
            set_azimuth (float): [optional]  # noqa: E501
            max_altitude (float): [optional]  # noqa: E501
            transmitter_uuid (str): [optional]  # noqa: E501
            transmitter_description (str): [optional]  # noqa: E501
            transmitter_type (dict): [optional]  # noqa: E501
            transmitter_uplink_low (int): [optional]  # noqa: E501
            transmitter_uplink_high (int): [optional]  # noqa: E501
            transmitter_uplink_drift (int): [optional]  # noqa: E501
            transmitter_downlink_low (int): [optional]  # noqa: E501
            transmitter_downlink_high (int): [optional]  # noqa: E501
            transmitter_downlink_drift (int): [optional]  # noqa: E501
            transmitter_mode (str): [optional]  # noqa: E501
            transmitter_invert (bool): [optional]  # noqa: E501
            transmitter_baud (float): [optional]  # noqa: E501
            transmitter_updated (str): [optional]  # noqa: E501
            tle0 (str): [optional]  # noqa: E501
            tle1 (str): [optional]  # noqa: E501
            tle2 (str): [optional]  # noqa: E501
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
    def __init__(self, *args, **kwargs):  # noqa: E501
        """PatchedObservation - a model defined in OpenAPI

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
            id (int): [optional]  # noqa: E501
            start (datetime): [optional]  # noqa: E501
            end (datetime): [optional]  # noqa: E501
            ground_station (int): [optional]  # noqa: E501
            transmitter (str): [optional]  # noqa: E501
            norad_cat_id (str): [optional]  # noqa: E501
            payload (str, none_type): [optional]  # noqa: E501
            waterfall (str, none_type): [optional]  # noqa: E501
            demoddata ([DemodData]): [optional]  # noqa: E501
            station_name (str): [optional]  # noqa: E501
            station_lat (str): [optional]  # noqa: E501
            station_lng (str): [optional]  # noqa: E501
            station_alt (str): [optional]  # noqa: E501
            vetted_status (str): [optional]  # noqa: E501
            vetted_user (str): [optional]  # noqa: E501
            vetted_datetime (str): [optional]  # noqa: E501
            archived (bool): [optional]  # noqa: E501
            archive_url (str): [optional]  # noqa: E501
            client_version (str): [optional]  # noqa: E501
            client_metadata (str): [optional]  # noqa: E501
            status (str): [optional]  # noqa: E501
            waterfall_status (str): [optional]  # noqa: E501
            waterfall_status_user (int): [optional]  # noqa: E501
            waterfall_status_datetime (datetime): [optional]  # noqa: E501
            rise_azimuth (float): [optional]  # noqa: E501
            set_azimuth (float): [optional]  # noqa: E501
            max_altitude (float): [optional]  # noqa: E501
            transmitter_uuid (str): [optional]  # noqa: E501
            transmitter_description (str): [optional]  # noqa: E501
            transmitter_type (dict): [optional]  # noqa: E501
            transmitter_uplink_low (int): [optional]  # noqa: E501
            transmitter_uplink_high (int): [optional]  # noqa: E501
            transmitter_uplink_drift (int): [optional]  # noqa: E501
            transmitter_downlink_low (int): [optional]  # noqa: E501
            transmitter_downlink_high (int): [optional]  # noqa: E501
            transmitter_downlink_drift (int): [optional]  # noqa: E501
            transmitter_mode (str): [optional]  # noqa: E501
            transmitter_invert (bool): [optional]  # noqa: E501
            transmitter_baud (float): [optional]  # noqa: E501
            transmitter_updated (str): [optional]  # noqa: E501
            tle0 (str): [optional]  # noqa: E501
            tle1 (str): [optional]  # noqa: E501
            tle2 (str): [optional]  # noqa: E501
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
