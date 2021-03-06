"""empty message

Revision ID: 9adc0e883fc8
Revises: f827b930eb92
Create Date: 2017-08-28 09:22:12.919913

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9adc0e883fc8'
down_revision = 'f827b930eb92'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('participant',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('display_name', sa.String(), nullable=True),
    sa.Column('email_address', sa.String(), nullable=True),
    sa.Column('phone_number', sa.String(), nullable=True),
    sa.Column('bio', sa.TEXT(), nullable=True),
    sa.Column('image_file', sa.String(), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('session',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date_time', sa.DateTime(), nullable=True),
    sa.Column('duration_minutes', sa.Integer(), nullable=True),
    sa.Column('instructor_notes', sa.TEXT(), nullable=True),
    sa.Column('workshop_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['workshop_id'], ['workshop.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('participant_session',
    sa.Column('participant_id', sa.Integer(), nullable=False),
    sa.Column('session_id', sa.Integer(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('review_score', sa.Integer(), nullable=True),
    sa.Column('review_comment', sa.TEXT(), nullable=True),
    sa.Column('attended', sa.Boolean(), nullable=True),
    sa.Column('is_instructor', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['participant_id'], ['participant.id'], ),
    sa.ForeignKeyConstraint(['session_id'], ['session.id'], ),
    sa.PrimaryKeyConstraint('participant_id', 'session_id')
    )
    op.drop_column('track_workshop', 'id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('track_workshop', sa.Column('id', sa.INTEGER(), nullable=False))
    op.drop_table('participant_session')
    op.drop_table('session')
    op.drop_table('participant')
    # ### end Alembic commands ###
