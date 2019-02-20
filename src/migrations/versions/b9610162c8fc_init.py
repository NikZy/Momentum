"""init

Revision ID: b9610162c8fc
Revises: 
Create Date: 2019-02-20 13:09:52.114726

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b9610162c8fc'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admin_user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=120), nullable=False),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_admin_user_username'), 'admin_user', ['username'], unique=True)
    op.create_table('jobbsøker',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=False),
    sa.Column('email', sa.String(length=50), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_jobbsøker_name'), 'jobbsøker', ['name'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_jobbsøker_name'), table_name='jobbsøker')
    op.drop_table('jobbsøker')
    op.drop_index(op.f('ix_admin_user_username'), table_name='admin_user')
    op.drop_table('admin_user')
    # ### end Alembic commands ###
