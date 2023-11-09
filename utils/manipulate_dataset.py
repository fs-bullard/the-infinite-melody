import numpy as np

# ds = np.load("dataset.npy", allow_pickle=True)

# f = open("dataset_maestro.txt", "r").read()
# ds = eval(f)

ds = np.load("dataset_maestro.npy", allow_pickle=True)

print(len(ds))

# combine songs
dataset = []
for i in ds:

    for pos in range(0, len(i) - (len(i) % 21) ):
        dataset.append(i[pos])

print(len(dataset))

# no long rests
dataset2 = []
i = 0
while i < len(dataset) - 2:
    val = dataset[i]
    if val[0] == "rest":
        dur = val[1]
        j = 1
        while i+j < len(dataset) and dataset[i+j][0] == "rest":
            dur += dataset[i+j][1]
            j += 1
            i += 1
        dataset2.append([val[0], dur, val[2]])
    else:
        dataset2.append(val)
    i += 1

print(len(dataset2))

# Most common chords
chords = {}
for i in dataset2:
    if len(i[0]) > 1 and i[0] != "rest":
        for note in i[0]:
            if note in chords.keys():
                chords[note] += 1
            else:
                chords[note] = 1

s = sum(chords.values())
for key in chords:
    chords[key] /= s

chordvals = []
for i in dataset2:
    if len(i[0]) > 1 and i[0] != "rest":
        chordvals.append(i)

np.save("chords_vals.npy", np.array(chordvals, dtype=object))
np.save("chords_consts.npy", chords)

# add between note rests
dataset3 = []
for i in range(len(dataset2)-1):
    dataset3.append([dataset2[i][0], dataset2[i][1]])
    if dataset2[i+1][2] - dataset2[i][2] > dataset2[i][1] + 0.075:
        dataset3.append(['rest', dataset2[i+1][2] - dataset2[i][2] - dataset2[i][1]])

print(len(dataset3))

# str to ints
dataset4 = []
mapping = {}
count = 0
for i in range(len(dataset3)):
    val = str(dataset3[i][0])
    if val not in mapping.keys() and (len(val) == 2 or val == "rest"):
        mapping[val] = count
        count += 1
print("count: ",count)
for i in dataset3:
    if (len(str(i[0])) == 2 or str(i[0]) == "rest"):
        dataset4.append([mapping[str(i[0])], i[1]])

print(len(dataset4))

# clip values 0.25 - 3
dataset5 = []
tem = []
for i in dataset4:
    dataset5.append([i[0], round(np.clip((20/3) * i[1], 1, 12)) - 1])
    tem.append( int(np.clip((20/3) * i[1], 1, 12) - 1))

print(len(dataset5))

# Count durations
u, count = np.unique(tem, return_counts=True)
count_sort_ind = np.argsort(-count) 
print(u[count_sort_ind])
print(count[count_sort_ind])


np.save("mapping.npy", mapping)
np.save("dataset2.npy", dataset5)