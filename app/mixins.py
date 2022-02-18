import json
from json import JSONDecodeError
from typing import Dict


class Mixins:

    async def get_and_validate_json(self) -> Dict:
        try:
            body = json.loads(self.request.body)
        except JSONDecodeError:
            return {"error": 400}
        return body

    async def count_request(self) -> None:
        db = self.settings.get('db').statistic
        statistic = await db.find_one({})
        if not statistic:
            await db.insert_one({"query": 1})
        else:
            await db.update_one({}, {"$inc": {"query": 1}})
        return


async def get_new_key(body):
    key = ''.join([i[0] + str(i[1]) for i in dict(body).items()])
    return key
