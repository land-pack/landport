from collections import defaultdict

d = {}
def save(e, k):
    if e in d:
        d[e].add(k)
    else:
        d[e]=set([k])

save('hello',23)
save('hello',24)
save('hello',25)
save('hey',25)
save('hey',25)
print(d)
print(d.get('hello'))


print('-'*100)
#=======use default dict

d2 = defaultdict(set)

d2['hello'].add(23)
d2['hello'].add(24)
d2['hello'].add(25)
d2['hey'].add(25)
d2['hey'].add(25)
print(d2)
print(d2.get('hello'))
