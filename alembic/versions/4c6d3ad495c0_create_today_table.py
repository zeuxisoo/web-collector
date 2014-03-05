"""create today table

Revision ID: 4c6d3ad495c0
Revises: 277bff62adde
Create Date: 2014-03-05 14:59:16.470988

"""

# revision identifiers, used by Alembic.
revision = '4c6d3ad495c0'
down_revision = '277bff62adde'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('today',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('result_id', sa.Integer(), nullable=True),
    sa.Column('result_name', sa.String(length=120), nullable=True),
    sa.Column('result_image', sa.String(length=180), nullable=True),
    sa.Column('result_width', sa.SmallInteger(), nullable=True),
    sa.Column('result_height', sa.SmallInteger(), nullable=True),
    sa.Column('result_thumbnail', sa.String(length=180), nullable=True),
    sa.Column('result_thumbnail_width', sa.SmallInteger(), nullable=True),
    sa.Column('result_thumbnail_height', sa.SmallInteger(), nullable=True),
    sa.Column('result_date', sa.Date(), nullable=True),
    sa.Column('filename', sa.String(length=80), nullable=True),
    sa.Column('create_at', sa.DateTime(), nullable=True),
    sa.Column('update_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_today_result_id', 'today', ['result_id'], unique=True)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_today_result_id', table_name='today')
    op.drop_table('today')
    ### end Alembic commands ###