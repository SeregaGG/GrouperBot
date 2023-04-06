import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://mongo:27017')


def get_db():
    db = client['sampleDB']
    return db
