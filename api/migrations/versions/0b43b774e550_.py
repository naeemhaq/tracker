"""empty message

Revision ID: 0b43b774e550
Revises: 6e9ff94fcf09
Create Date: 2020-02-15 12:22:38.261972

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0b43b774e550'
down_revision = '6e9ff94fcf09'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('tfa_validated', sa.Boolean(), nullable=True))
    op.add_column('users', sa.Column('user_role', sa.String(), nullable=True))
    op.drop_column('users', 'two_factor_auth')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('two_factor_auth', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.drop_column('users', 'user_role')
    op.drop_column('users', 'tfa_validated')
    # ### end Alembic commands ###
