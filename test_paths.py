
import csv

feasible_paths = list()

with open('paths.csv', 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
        
        x = 0
        y = 0
        z = 0
        
        for l in row:
	  l = l.replace(" ","")
	  
	  if l == "nocjmp7":
	    z = z + 1
	  
	  if l == "0x8048423":
	    x = x + 1
	  if l == "0x804845d":
	    y = y + 1
        
        if (x > 0 and 2*x == y and z == 1):
          feasible_paths.append(str(row))
          

    for path in feasible_paths:
      print path
        