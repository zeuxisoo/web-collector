"""create comment table

Revision ID: 648705e80aa
Revises: 2044f795f260
Create Date: 2014-03-17 16:58:07.061099

"""

# revision identifiers, used by Alembic.
revision = '648705e80aa'
down_revision = '2044f795f260'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('comment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('category', sa.Enum('stream', 'today'), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('result_id', sa.Integer(), nullable=False),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('create_at', sa.DateTime(), nullable=True),
    sa.Column('update_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('comment')
    ### end Alembic commands ###
