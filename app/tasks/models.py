from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.infrastructure.database.database import Base


class Tasks(Base):
    __tablename__ = "Tasks"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column()
    pomodoro_count: Mapped[int] = mapped_column()
    category_id: Mapped[int] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('UserProfile.id'), nullable=False)


class Categories(Base):
    __tablename__ = "Categories"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column()
