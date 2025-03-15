from auth import hash_password
from models import Right, Role, Session, User


async def create_admin_user(
    session: Session,
    username: str,
    password: str,
) -> None:
    write_rights = [
        Right(
            model=model.__name__,
            write=True,
            read=False,
            only_own=False,
        )
        for model in (Right, Role, User)
    ]
    read_rights = [
        Right(
            model=model.__name__,
            write=False,
            read=True,
            only_own=False,
        )
        for model in (Right, Role, User)
    ]
    rights = [*write_rights, *read_rights]
    role = Role(name="admin", rights=rights)
    user = User(name=username, password=hash_password(password), roles=[role])
    session.add_all([*rights, role, user])
    await session.commit()


async def create_user_role(session: Session) -> None:
    rights = []
    for wr in True, False:
        for model in (User,):
            rights.append(
                Right(
                    model=model.__name__,
                    write=wr,
                    read=not wr,
                    only_own=True,
                )
            )
    role = Role(name="user", rights=rights)
    session.add_all([*rights, role])
    await session.commit()
