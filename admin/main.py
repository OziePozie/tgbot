from starlette.applications import Starlette
from starlette_admin.contrib.sqla import Admin, ModelView
from config import engine
from data.models import Auth, Auto, Chats, Object, Workers, Transports, Travel_orders, PerformanceReport

app = Starlette()


admin = Admin(engine, title="Admin: SQLAlchemy")


admin.add_view(ModelView(Auth))
admin.add_view(ModelView(Auto))
admin.add_view(ModelView(Object))
admin.add_view(ModelView(Workers))
admin.add_view(ModelView(Transports))
admin.add_view(ModelView(Travel_orders))
admin.add_view(ModelView(PerformanceReport))

admin.mount_to(app)
