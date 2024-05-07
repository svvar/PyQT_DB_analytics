import pymongo


class DBService:
    def __init__(self, connection_str, db_name, collection_name):
        self.client = pymongo.MongoClient(connection_str)
        self.db = self.client[db_name]
        self.goods = self.db[collection_name]

    def get_all(self):
        return self.goods.find()

    def get_limit(self, skip, limit):
        return self.goods.find().skip(skip).limit(limit)

    def insert_one(self, inv_num, name, desc, warehouse, rating, quantity, price, date_added, date_changed):
        return self.goods.insert_one({
                "inv_num": inv_num,
                "name": name,
                "desc": desc,
                "warehouse": warehouse,
                "rating": rating,
                "quantity": quantity,
                "price": price,
                "date_added": date_added,
                "date_changed": date_changed
            })

    def insert_many(self, data):
        raise NotImplementedError

    def update_one(self, inv_num, name, desc, warehouse, rating, quantity, price, date_added, date_changed):

        return self.goods.update_one({"inv_num": inv_num}, {'$set': {
            "name": name,
            "desc": desc,
            "warehouse": warehouse,
            "rating": rating,
            "quantity": quantity,
            "price": price,
            "date_added": date_added,
            "date_changed": date_changed
        }})

    def update_many(self, query, data):
        raise NotImplementedError

    def delete_one(self, inv_num):
        return self.goods.delete_one({"inv_num": inv_num})

    def delete_many(self, query):
        raise NotImplementedError

    def get_amount_by_warehouse(self):
        pipeline = [
            {
                '$group': {
                    '_id': '$warehouse',
                    'total': {'$sum': '$quantity'}
                }
            }
        ]
        return list(self.goods.aggregate(pipeline))

    def get_avg_rating_in_warehouse(self):
        pipeline = [
            {
                '$group': {
                    '_id': '$warehouse',
                    'avg_rating': {'$avg': '$rating'}
                }
            }
        ]
        return list(self.goods.aggregate(pipeline))

    def get_amount_by_date(self, start_date, end_date):
        pipeline = [
            {
                '$match': {
                    'date_added': {
                        '$gte': start_date,
                        '$lte': end_date
                    }
                }
            },
            {
                '$group': {
                    '_id': '$warehouse',
                    'total': {'$sum': '$quantity'}
                }
            }
        ]
        return list(self.goods.aggregate(pipeline))

