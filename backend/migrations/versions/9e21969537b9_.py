"""empty message

Revision ID: 9e21969537b9
Revises: ba62e09f66cb
Create Date: 2018-01-04 13:24:05.761339

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9e21969537b9'
down_revision = 'ba62e09f66cb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('email_log', sa.Column('workshop_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'email_log', 'workshop', ['workshop_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'email_log', type_='foreignkey')
    op.drop_column('email_log', 'workshop_id')
    # ### end Alembic commands ###
