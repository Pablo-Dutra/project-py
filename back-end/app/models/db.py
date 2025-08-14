import sqlalchemy

metadata = sqlalchemy.MetaData()

items = sqlalchemy.Table(
    "items",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("nome", sqlalchemy.String(length=100)),
    sqlalchemy.Column("descricao", sqlalchemy.String(length=255)),
)

# Tabela valores
valores = sqlalchemy.Table(
    "valores",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("item_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("items.id", ondelete="CASCADE")),
    sqlalchemy.Column("data_cadastro", sqlalchemy.DateTime),
    sqlalchemy.Column("valor", sqlalchemy.Float),
)
