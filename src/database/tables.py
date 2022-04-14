import sqlalchemy as sa

metadata = sa.MetaData()

users = sa.Table(
    'user',
    metadata,
    sa.Column('id', sa.BigInteger, primary_key=True),
    sa.Column('login', sa.String, nullable=False),
    sa.Column('name', sa.String, nullable=False)
)

stats = sa.Table(
    'stats',
    metadata,
    sa.Column('user_id', sa.BigInteger, sa.ForeignKey('user.id'), nullable=False),
    sa.Column('repo_id', sa.BigInteger, primary_key=True),
    sa.Column('date', sa.Date, nullable=False, primary_key=True),
    sa.Column('stargazers', sa.Integer, nullable=False),
    sa.Column('forks', sa.Integer, nullable=False),
    sa.Column('watchers', sa.Integer, nullable=False)
)
