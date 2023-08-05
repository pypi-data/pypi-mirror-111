from sqlalchemy.orm import Session

from gita_api import crud
from gita_api.config import settings
from gita_api.db.base_class import Base
from gita_api.db.session import engine
from gita_api.models import user


def init_db(db: Session) -> None:
    # add test user
    user_in = crud.get_user(db, user_id=1)
    if not user_in:
        user_in = user.User(
            id=1,
            full_name="Radha Krishna",
            email="admin@bhagavadgita.io",
            app_name="BhagavadGita.io",
            app_description="BhagavadGita.io is a modern Bhagavad Gita app with a simple, beautiful and easy to use interface, helping you focus on reading. It is an app built for Bhagavad Gita readers, by Bhagavad Gita readers.",
            app_link="https://bhagavadgita.io",
            api_key=settings.TESTER_API_KEY,
            is_active=True,
        )

        db.add(user_in)
        db.commit()

    Base.metadata.create_all(engine)
