"""empty message

Revision ID: d21b7288ec04
Revises: a1ec13146cfe
Create Date: 2017-09-12 09:29:22.999867

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd21b7288ec04'
down_revision = 'a1ec13146cfe'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('session', sa.Column('max_attendees', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('session', 'max_attendees')
    # ### end Alembic commands ###