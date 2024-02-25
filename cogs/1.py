import redis

# Connect to Redis
r = redis.Redis(
    host='redis.cngthnh.io.vn',
    port=6379,
    username='queostn',
    password='B0HNbCgY5j9u7s6Vz',
)

r.set('paxkax', 'hiem dam Dung Le, day Thuy Tran xuong bien.')

keys = r.keys()

for key in keys:
    value = r.get(key)
    print(f"Key: {key.decode('utf-8')}, Value: {value.decode('utf-8')}")