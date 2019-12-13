from .root import RootResources, RootNameResources
from .sms import SmsResources, SmsPresentResources


def setup_routes(app):
    app.add_route("/", RootResources())
    app.add_route("/{name}", RootNameResources())
    app.add_route("/sms", SmsPresentResources())
    app.add_route("/sms/{operation}", SmsResources())
