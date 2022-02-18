import base64
from tornado.web import RequestHandler, HTTPError

from app.mixins import Mixins, get_new_key


class CreateApiHandler(Mixins, RequestHandler):

    async def post(self):
        await self.count_request()
        body = await self.get_and_validate_json()
        if body.get("error"):
            raise HTTPError(status_code=400)
        db = self.settings.get('db').data
        key = await get_new_key(body)
        key = base64.b64encode(key.encode('ascii'))
        obj = await db.find_one({"_id": key})
        if obj:
            await db.update_one({'_id': key}, {"$inc": {"duplicates": 1}})
        else:
            await db.insert_one({"_id": key, "body": body})
        return self.write({"key": key.decode()})


class GetApiHandler(Mixins, RequestHandler):

    async def get(self, **kwargs):
        await self.count_request()
        key = self.request.query_arguments.get('key', False)
        if not key:
            raise HTTPError(status_code=400)
        db = self.settings.get('db').data
        result = await db.find_one({"_id": key[0]})
        if result:
            result['_id'] = result['_id'].decode()
        return self.write({"data": result})


class DeleteApiHandler(Mixins, RequestHandler):

    async def delete(self, **kwargs):
        await self.count_request()
        body = await self.get_and_validate_json()
        key = body.get('key', None)
        if not key:
            raise HTTPError(status_code=400)
        db = self.settings.get('db').data
        await db.delete_one({'_id': key.encode("ascii")})
        return self.write({"message": "The object has been deleted"})


class UpdateApiHandler(Mixins, RequestHandler):

    async def put(self, **kwargs):
        await self.count_request()
        body = await self.get_and_validate_json()
        key = body.pop('key', None)
        if not key:
            raise HTTPError(status_code=400)
        db = self.settings.get('db').data
        key = await get_new_key(body)
        key = base64.b64encode(key.encode('ascii'))
        await db.update_one({'_id': key},
                            {"$set": {"body": body}})
        return self.write({"key": key})


class GetStatisticHandler(RequestHandler):

    async def get(self, **kwargs):
        db = self.settings.get('db')
        # get duplicates count
        duplicates = db.data.find({"duplicates": {"$gte": 1}})
        duplicates_count = [i.get('duplicates') for i in
                            await duplicates.to_list(length=100)]
        # get query count
        query = await db.statistic.find_one()

        result = (query['query'] * (sum(duplicates_count) / 100)) * 10
        return self.write({"result": f"{round(result, 2)} %"})
