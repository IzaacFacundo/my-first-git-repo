words = []

with open('/usr/share/dict/words', 'r') as f:
    words = f.read().splitlines()
topfive = [words[0],words[1],words[2],words[3],words[4]]
smallest = 0

for word in words:
	for x in range(0,5):
		if len(topfive[x]) < len(topfive[smallest]):
			smallest = x

	if len(word) > len(topfive[smallest]):
		topfive[smallest] = word

for x in range(5):
	print(topfive[x])

	
