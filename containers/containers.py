from dependency_injector.containers import DeclarativeContainer
from dependency_injector.containers import WiringConfiguration
from dependency_injector.providers import Factory
from dependency_injector.providers import Configuration
from dependency_injector.providers import Resource

from shared.infrastructure.cloud.aws_storage import AWSS3
from shared.infrastructure.alchemy_unit_of_work import AlchemyUnitOfWork


class Container(DeclarativeContainer):
    """
    App dependency injector configuration.
    More info on IoC:
    https://python-dependency-injector.ets-labs.org/introduction/di_in_python.html
    """

    wiring_config = WiringConfiguration(
        packages=[
            "fastapi_app.endpoints",
            "shared.infrastructure",
            "modules",
        ]
    )

    logger_config = Configuration(yaml_files=["logging.yaml"])
    app_config = Configuration(yaml_files=["config.yaml"])

    logger: Resource = Resource("logging.config.dictConfig", logger_config)

    aws_session: Resource = Resource("boto3.session.Session")
    s3_client = Resource(
        aws_session.provided.client.call(),
        service_name="s3",
    )
    cloud_storage = Factory(
        AWSS3,
        aws_session=aws_session,
        default_bucket=app_config.aws.default_bucket_name,
    )
    unit_of_work = Factory(AlchemyUnitOfWork)
