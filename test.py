import flask
import sqlalchemy as sa
import flask_sa_logger

app = flask.Flask(__name__)
app.config.from_mapping({
    'FLASK_SA_LOGGER': 'log'
})

flask_sa_logger.init_logging(app)

engine = sa.create_engine('sqlite:///:memory:', echo=False)
metadata = sa.MetaData()
users = sa.Table('users', metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('name', sa.String)
)
metadata.create_all(engine)
conn = engine.connect()
conn.execute(users.insert().values(name='Иван Говно'))

app.run()
