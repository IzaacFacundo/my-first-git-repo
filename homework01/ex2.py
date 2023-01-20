import names

count = 0
while count < 5:
	sample = names.get_full_name()
	if len(sample) == 9:
		print(sample)
		count = count + 1
