from decouple import config

import motor.motor_asyncio

cluster = motor.motor_asyncio.AsyncIOMotorClient(config("MONGODB_URL"))

db = cluster.example_db
