import csv

# def addrests(arr):
#     for i in range(len(arr)-1):
#         if arr[i+1][2] - arr[i][2] > 0.01:
            
dataset = []

with open("test.csv", newline='\n') as f:
    reader = csv.reader(f)
    for row in reader:
        dataset.append(row)

print(dataset)