# -*- coding: utf-8 -*-
"""
This class essentially overrides the boto3 session init, passing in
an async botocore session
"""

import copy

import aiobotocore.session
from aiobotocore.config import AioConfig

import boto3.session
import boto3.resources.base
import boto3.utils
from botocore.exceptions import DataNotFoundError, UnknownServiceError
from boto3.exceptions import ResourceNotExistsError, UnknownAPIVersionError

from aioboto3.resources.factory import AIOBoto3ResourceFactory


class Session(boto3.session.Session):
    """
    A session stores configuration state and allows you to create service
    clients and resources.

    :type aws_access_key_id: string
    :param aws_access_key_id: AWS access key ID
    :type aws_secret_access_key: string
    :param aws_secret_access_key: AWS secret access key
    :type aws_session_token: string
    :param aws_session_token: AWS temporary session token
    :type region_name: string
    :param region_name: Default region when creating new connections
    :type botocore_session: botocore.session.Session
    :param botocore_session: Use this Botocore session instead of creating
                             a new default one.
    :type profile_name: string
    :param profile_name: The name of a profile to use. If not given, then
                         the default profile is used.
    """
    def __init__(self, aws_access_key_id=None, aws_secret_access_key=None,
                 aws_session_token=None, region_name=None,
                 botocore_session=None, profile_name=None):
        if botocore_session is not None:
            self._session = botocore_session
        else:
            # Create a new default session
            self._session = aiobotocore.session.get_session()

        # Setup custom user-agent string if it isn't already customized
        if self._session.user_agent_name == 'Botocore':
            botocore_info = 'Botocore/{0}'.format(
                self._session.user_agent_version)
            if self._session.user_agent_extra:
                self._session.user_agent_extra += ' ' + botocore_info
            else:
                self._session.user_agent_extra = botocore_info
            self._session.user_agent_name = 'Boto3'
            self._session.user_agent_version = boto3.__version__

        if profile_name is not None:
            self._session.set_config_variable('profile', profile_name)

        if aws_access_key_id or aws_secret_access_key or aws_session_token:
            self._session.set_credentials(
                aws_access_key_id, aws_secret_access_key, aws_session_token)

        if region_name is not None:
            self._session.set_config_variable('region', region_name)

        self.resource_factory = AIOBoto3ResourceFactory(
            self._session.get_component('event_emitter'))
        self._setup_loader()
        self._register_default_handlers()

    def resource(self, service_name, region_name=None, api_version=None,
                       use_ssl=True, verify=None, endpoint_url=None,
                       aws_access_key_id=None, aws_secret_access_key=None,
                       aws_session_token=None, config=None):
        try:
            resource_model = self._loader.load_service_model(
                service_name, 'resources-1', api_version)
        except UnknownServiceError:
            available = self.get_available_resources()
            has_low_level_client = (
                service_name in self.get_available_services())
            raise ResourceNotExistsError(service_name, available,
                                         has_low_level_client)
        except DataNotFoundError:
            # This is because we've provided an invalid API version.
            available_api_versions = self._loader.list_api_versions(
                service_name, 'resources-1')
            raise UnknownAPIVersionError(
                service_name, api_version, ', '.join(available_api_versions))

        if api_version is None:
            # Even though botocore's load_service_model() can handle
            # using the latest api_version if not provided, we need
            # to track this api_version in boto3 in order to ensure
            # we're pairing a resource model with a client model
            # of the same API version.  It's possible for the latest
            # API version of a resource model in boto3 to not be
            # the same API version as a service model in botocore.
            # So we need to look up the api_version if one is not
            # provided to ensure we load the same API version of the
            # client.
            #
            # Note: This is relying on the fact that
            #   loader.load_service_model(..., api_version=None)
            # and loader.determine_latest_version(..., 'resources-1')
            # both load the same api version of the file.
            api_version = self._loader.determine_latest_version(
                service_name, 'resources-1')

        # Creating a new resource instance requires the low-level client
        # and service model, the resource version and resource JSON data.
        # We pass these to the factory and get back a class, which is
        # instantiated on top of the low-level client.
        if config is not None:
            if config.user_agent_extra is None:
                config = copy.deepcopy(config)
                config.user_agent_extra = 'Resource'
        else:
            config = AioConfig(user_agent_extra='Resource')

        # client = blah part has been moved into a dodgy context class
        return ResourceCreatorContext(self, service_name, region_name, api_version,
                                      use_ssl, verify, endpoint_url, aws_access_key_id,
                                      aws_secret_access_key, aws_session_token, config,
                                      resource_model)

    def _register_default_handlers(self):
        # S3 customizations
        self._session.register(
            'creating-client-class.s3',
            boto3.utils.lazy_call(
                'aioboto3.s3.inject.inject_s3_transfer_methods'))
        self._session.register(
            'creating-resource-class.s3.Bucket',
            boto3.utils.lazy_call(
                'aioboto3.s3.inject.inject_bucket_methods'))
        self._session.register(
            'creating-resource-class.s3.Object',
            boto3.utils.lazy_call(
                'boto3.s3.inject.inject_object_methods'))
        self._session.register(
            'creating-resource-class.s3.ObjectSummary',
            boto3.utils.lazy_call(
                'aioboto3.s3.inject.inject_object_summary_methods'))

        # DynamoDb customizations
        self._session.register(
            'creating-resource-class.dynamodb',
            boto3.utils.lazy_call(
                'boto3.dynamodb.transform.register_high_level_interface'),
            unique_id='high-level-dynamodb')
        self._session.register(
            'creating-resource-class.dynamodb.Table',
            boto3.utils.lazy_call(
                'aioboto3.dynamodb.table.register_table_methods'),
            unique_id='high-level-dynamodb-table')

        # EC2 Customizations
        self._session.register(
            'creating-resource-class.ec2.ServiceResource',
            boto3.utils.lazy_call(
                'boto3.ec2.createtags.inject_create_tags'))

        self._session.register(
            'creating-resource-class.ec2.Instance',
            boto3.utils.lazy_call(
                'boto3.ec2.deletetags.inject_delete_tags',
                event_emitter=self.events))


class ResourceCreatorContext(object):
    def __init__(self, session, service_name, region_name, api_version, use_ssl, verify,
                 endpoint_url, aws_access_key_id, aws_secret_access_key, aws_session_token,
                 config, resource_model):
        self.service_name = service_name
        self.resource_model = resource_model
        self.session = session
        self.api_version = api_version
        self.cls = None
        self.client = session.client(
            service_name, region_name=region_name, api_version=api_version,
            use_ssl=use_ssl, verify=verify, endpoint_url=endpoint_url,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            aws_session_token=aws_session_token, config=config)

    async def __aenter__(self):
        client = await self.client.__aenter__()
        service_model = client.meta.service_model

        # Create a ServiceContext object to serve as a reference to
        # important read-only information about the general service.
        service_context = boto3.utils.ServiceContext(
            service_name=self.service_name, service_model=service_model,
            resource_json_definitions=self.resource_model['resources'],
            service_waiter_model=boto3.utils.LazyLoadedWaiterModel(
                self.session._session, self.service_name, self.api_version)
        )

        # Create the service resource class.
        self.cls = (await self.session.resource_factory.load_from_definition(
            resource_name=self.service_name,
            single_resource_json_definition=self.resource_model['service'],
            service_context=service_context
        ))(client=client)

        return self.cls

    async def __aexit__(self, exc_type, exc, tb):
        await self.cls.close()
