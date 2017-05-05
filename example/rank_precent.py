def pp(rank, entryAmount):
        die_one = entryAmount - int(rank)
        die_one = float(die_one)
        entryAmount = float(entryAmount - 1) if int(entryAmount) > 1 else -1
        f_rank = "%.f%%" % (die_one / entryAmount * 100) if entryAmount > 0 else "100%"
        return f_rank


if __name__ == '__main__':
	total = 10
	for i in range(1,total+1):
		print(" Total:%s\tRank:%s\tPrecent:%s" % (total, i, pp(i, total)))
	total = 2
	print("="*30)
	for i in range(1,total+1):
		print(" Total:%s\tRank:%s\tPrecent:%s" % (total, i, pp(i, total)))
	print("="*30)
	total = 1
	for i in range(1,total+1):
		print(" Total:%s\tRank:%s\tPrecent:%s" % (total, i, pp(i, total)))
