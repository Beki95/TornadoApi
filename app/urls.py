from app.handlers import (
    CreateApiHandler,
    GetApiHandler,
    DeleteApiHandler,
    UpdateApiHandler,
    GetStatisticHandler
)

urls = [
    ('/api/add/', CreateApiHandler),
    ('/api/get/', GetApiHandler),
    ('/api/remove/', DeleteApiHandler),
    ('/api/update/', UpdateApiHandler),
    ('/api/statistic/', GetStatisticHandler),
]
