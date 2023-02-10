#  this is the api for teh miongodb database
# it uses fastapi and motor
# it is a simple api that allows you to view the data in the database

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from motor.motor_asyncio import AsyncIOMotorClient
import os



app = FastAPI()

# connect to the database
client = AsyncIOMotorClient('mongodb://172.17.0.1:27017')
db = client['IMDB']
collection = db['here']

# get database info
@app.get('/')
async def get_info():
    info = {
        'name': db.name,
        'collection': collection.name
    }
    return info
    
#  get number of elements in the database
@app.get('/count')
async def get_count():
    count = await collection.count_documents({})
    return count



# get a random document from the database
#  using the $sample aggregation pipeline operator
#  https://docs.mongodb.com/manual/reference/operator/aggregation/sample/
@app.get('/random')
async def get_random():
    document = await collection.aggregate([{'$sample': {'size': 1}}]).to_list(length=1)
    print("document: ", document)
    return str(document)

# get all the data in the database
@app.get('/data')
async def get_data():
    data = []
    async for document in collection.find():
        data.append(document)
    return data

# get a specific document from the database
@app.get('/data/{id}')
async def get_data(id: str):

    document = await collection.find_one({'_id': id})
    return document

class SPAStaticFiles(StaticFiles):
    async def get_response(self, path: str, scope):
        response = await super().get_response(path, scope)
        if response.status_code == 404:
            response = await super().get_response('.', scope)
        return response

app.mount('/static/', SPAStaticFiles(directory='static', html=True), name='whatever')

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)

# Path: main.py



