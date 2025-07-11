"""update-user-del-googletoken

Revision ID: 918c4cc4ef51
Revises: 033ae3f423c3
Create Date: 2025-06-18 15:54:24.387727

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '918c4cc4ef51'
down_revision: Union[str, None] = '033ae3f423c3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('UserProfile', 'google_access_token')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('UserProfile', sa.Column('google_access_token', sa.VARCHAR(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
