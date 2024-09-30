from uuid import UUID

from sqlalchemy.orm import Session

from models import engine

from shared.infrastructure.alchemy_repository import AlchemyRepository
from shared.infrastructure.alchemy_unit_of_work import AlchemyUnitOfWork
from modules.accounts.domain.entities.user import User
from modules.document_types.domain.entities.document_type import DocumentType

session = Session(engine)
me_id = UUID("dd52d71a-0e00-48d5-8e2b-c12e5b2ed9e1")
ticket_type_id = UUID("a9e39cc9-1749-4da6-b271-cd71cd0481df")
user_repo = AlchemyRepository[User](User, session)
me = user_repo.get(me_id)
document_type_repo = AlchemyRepository[DocumentType](DocumentType, session)
document_type_repo.get(ticket_type_id)

ruben_id = UUID("0f957722-6beb-4c0b-a9b3-0e2bfcc14aee")
ruben_user = User(id=ruben_id, email="ruben@gmail.com")

with AlchemyUnitOfWork(lambda: session) as uow:
    user_repo = AlchemyRepository[User](User, uow.session)
    user_repo.add(ruben_user)
    uow.commit()
