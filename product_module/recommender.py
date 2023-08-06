from jahanbakhshiEshop.settings import REDIS_DB, REDIS_PORT, REDIS_HOST
import redis
from django.conf import settings
from .models import Product

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)


class Recommender(object):
    def get_product_key(self, id):
        return f"product:{id}:bought_with"  # product:1:bought_with

    def products_bought(self, *args):
        product_ids = [p.id for p in args]
        for product_id in product_ids:  # [1,2,3]
            for with_id in product_ids:
                if product_id != with_id:
                    r.zincrby(self.get_product_key(product_id), 1, with_id)

    def suggest_products_for(self, products, max_results=6):
        if len(products) == 1:
            suggestions = r.zrange(self.get_product_key(products[0].id), 0, -1, desc=True)[:max_results]
            suggested_products_ids = [int(id) for id in suggestions]
            suggested_products = Product.objects.filter(id__in=suggested_products_ids)
            return suggested_products
        else:
            product_ids = [p.id for p in products]
            flat_ids = ''.join([str(id) for id in product_ids])  # [1,2,3] => "123"
            tmp_key = f"tmp_{flat_ids}"  # "123" => tmp_123
            keys = [self.get_product_key(id) for id in product_ids]
            r.zunionstore(tmp_key, keys)
            r.zrem(tmp_key, *product_ids)
            suggestions = r.zrange(tmp_key, 0, -1, desc=True)[:max_results]
            r.delete(tmp_key)
            suggested_products_ids = [int(id) for id in suggestions]
            suggested_products = Product.objects.filter(id__in=suggested_products_ids)
            return suggested_products
