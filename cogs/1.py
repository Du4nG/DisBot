import redis

r = redis.Redis(
    host='redis.cngthnh.io.vn',
    port=6379,
    username='queostn',
    password='B0HNbCgY5j9u7s6Vz',
)

r.set('queo:alert', 'ai xoa db lam con cho.')

keys = r.keys()

for key in keys:
    value = r.get(key)
    print(f'Key: {key}, Value: {value}')