import memcache

mc = memcache.Client(['127.0.0.1:11211','129.28.158.195:11211'],debug=True)

mc.set('username','hello world',time=60*5)

print(mc.get('13364089479'))



