import names

def print_name_and_length(name):
	length = len(name)
	print(name,length)

count = 0
previous_names = []
while count < 5:
	
	current_name = names.get_full_name()
	if count == 0:
		print_name_and_length(current_name)
		previous_names.append(current_name)
		count = count + 1
	else:	
		for x in previous_names:
			if x == current_name:
				break
		count = count + 1
		print_name_and_length(current_name)
		previous_names.append(current_name)


