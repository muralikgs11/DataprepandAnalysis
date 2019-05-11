import matplotlib.pyplot as plt 
import numpy as np 

lines = list()
with open('./data/gt.txt', 'r') as f:
	for line in f:
		lines.append(line.rstrip())
#		print(line.rstrip())
print('File has been parsed')

class_frames = dict()
for key in range(43):
	class_frames[key] = list()

for line in lines:
	l = line.split(';')
	class_no = int(l[5])
	class_frames[class_no].append(l[0])

num_elems = list()
for key in class_frames:
	num_elems.append(len(class_frames[key]))
	if len(class_frames[key]) > 35:
		print(key, len(class_frames[key]))

index = np.argsort(num_elems)

plt.bar(range(43), height=np.array(num_elems)[index], tick_label=index)
plt.xlabel('Class Number')
plt.ylabel('#frames')
plt.show()
