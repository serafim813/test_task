"""
Create database

Revision ID: 33235f55faab
Revises: 
Create Date: 2022-04-12 11:39:29.055650
"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '33235f55faab'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'user',
        sa.Column('id', sa.BigInteger(), nullable=False),
        sa.Column('login', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'stats',
        sa.Column('user_id', sa.BigInteger(), nullable=False),
        sa.Column('repo_id', sa.BigInteger(), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('stargazers', sa.Integer(), nullable=False),
        sa.Column('forks', sa.Integer(), nullable=False),
        sa.Column('watchers', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['user.id']),
        sa.PrimaryKeyConstraint('repo_id', 'date')
    )


def downgrade():
    op.drop_table('stats')
    op.drop_table('user')