import redis

r = redis.Redis(
    host='redis.cngthnh.io.vn',
    port=6379,
    username='queostn',
    password='B0HNbCgY5j9u7s6Vz',
)

r.set('DungLe:alert', 'ai xoa db lam con cho.')

r.delete('queo:1175820556004769883')

keys = r.keys()

for key in keys:
    value = r.get(key)
    print(f'Key: {key}, Value: {value}')
