"""empty message

Revision ID: 5007b5f4af73
Revises: f31f4ef9b425
Create Date: 2017-12-21 15:11:25.976532

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5007b5f4af73'
down_revision = 'f31f4ef9b425'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('email_log', sa.Column('date_opened', sa.DateTime(), nullable=True))
    op.alter_column('email_log', 'email_message_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('email_log', 'email_message_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.drop_column('email_log', 'date_opened')
    # ### end Alembic commands ###
