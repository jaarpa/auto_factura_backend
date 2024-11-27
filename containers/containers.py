from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Configuration, Factory, Resource

from modules.accounts.infrastructure.service.imple_validator import ValidateJWT
from modules.document_types.domain.entities.document_type import DocumentType
from modules.files.domain.entities.file import File
from modules.tickets.domain.entities.ticket import Ticket
from shared.infrastructure.alchemy_repository import AlchemyRepository
from shared.infrastructure.alchemy_unit_of_work import AlchemyUnitOfWork
from shared.infrastructure.cloud.aws_storage import AWSS3


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

    # JWT VALIDATOR
    jwt_validator = Factory(
        ValidateJWT,
        jwks_url=app_config.cognito.jwks_url,
        client_id=app_config.cognito.client_id,
        user_pool_id=app_config.cognito.user_pool_id,
    )

    document_type_repository = Factory(
        AlchemyRepository[DocumentType],
        DocumentType,
    )
    file_repository = Factory(
        AlchemyRepository[File],
        File,
    )
    ticket_repository = Factory(
        AlchemyRepository[Ticket],
        Ticket,
    )
