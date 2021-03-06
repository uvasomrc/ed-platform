"""empty message

Revision ID: e0a08c6a0885
Revises: cfc0359a9884
Create Date: 2017-10-16 13:29:30.982961

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e0a08c6a0885'
down_revision = 'cfc0359a9884'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('code',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('desc', sa.TEXT(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('track_code',
    sa.Column('track_id', sa.Integer(), nullable=False),
    sa.Column('code_id', sa.String(), nullable=False),
    sa.Column('order', sa.Integer(), nullable=True),
    sa.Column('prereq', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['code_id'], ['code.id'], ),
    sa.ForeignKeyConstraint(['track_id'], ['track.id'], ),
    sa.PrimaryKeyConstraint('track_id', 'code_id')
    )
    op.drop_table('track_workshop')
    op.add_column('workshop', sa.Column('code_id', sa.String(), nullable=True))
    op.create_foreign_key(None, 'workshop', 'code', ['code_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'workshop', type_='foreignkey')
    op.drop_column('workshop', 'code_id')
    op.create_table('track_workshop',
    sa.Column('track_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('workshop_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('order', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['track_id'], ['track.id'], name='track_workshop_track_id_fkey'),
    sa.ForeignKeyConstraint(['workshop_id'], ['workshop.id'], name='track_workshop_workshop_id_fkey')
    )
    op.drop_table('track_code')
    op.drop_table('code')
    # ### end Alembic commands ###
