"""empty message

Revision ID: 91a1129e95d5
Revises: d911d67fa2d4
Create Date: 2017-10-30 12:30:32.729849

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '91a1129e95d5'
down_revision = 'd911d67fa2d4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('participant_session', sa.Column('wait_listed', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('participant_session', 'wait_listed')
    # ### end Alembic commands ###