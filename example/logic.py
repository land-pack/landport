import bisect
def ckp(lst, point):
    lst.sort()
    p=bisect.bisect(lst, point)
    distance = lst[p] if p < len(lst) else -1
    distance = (distance -point) if distance != -1 else -1
    return distance


if __name__ == '__main__':
	a=[12,33,44,55]
	b=16
	print(ckp(a, b))
	b=31
	print(ckp(a, b))
	b=52
	print(ckp(a, b))
