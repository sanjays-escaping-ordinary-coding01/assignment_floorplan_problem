roomFile = open("floorplan01.txt", mode="r")

maxcolumn = 0

#Read file
data = roomFile.readlines()
for i in range(len(data)):
    data[i] = data[i].replace('\n', '')
    data[i] = data[i].replace('\t', '     ')
    print(data[i])
    data[i] = [ c for c in data[i]] 
    maxcolumn = max(maxcolumn, len(data[i]))

visited = set()
row = len(data)
i = 0
j = 0

#Boarders characters
borders = ["-", "/", "\\", "+", "|"]
namePointDict = {}

#Find out coordinate point of name within brackets ()
while(i < row):
    j = 0
    while(j < len(data[i])):
        if(data[i][j] == "+"):
            visited.add((i, j))
        elif(data[i][j] == "("):
            pair = (i, j)
            j = j + 1 
            name = ""
            while(data[i][j] != ")"):
                name = name + data[i][j]
                j = j + 1
            
            namePointDict[name] = pair
        j = j + 1
        
    i = i + 1

nameAllPointDict = []
total = [0, 0, 0, 0]

newRow = [0, 0, -1, 1 ]
newColumn = [-1, 1, 0, 0]

crossRow = [1, 1, -1, -1 ]
crossColumn = [-1, 1, -1, 1]

cornerRow = [1, 1, -1, -1, 2, 2, -2, -2]
cornerColumn = [-2, 2, -2, 2, -1, 1, -1, 1 ]

for name, pair in namePointDict.items():
    points = [0, 0, 0, 0]
    coordinates = []
    
    queue = []
    visited = set()
    queue.append(pair)
    visited.add(pair)
    
    #Breadth First Search
    while queue:
        s = queue.pop(0)
        x = s[0]
        y = s[1]
        
        #Count W, P, S and C
        if(data[x][y] == "W"):
            points[0] = points[0] + 1
        elif(data[x][y] == "P"):
            points[1] = points[1] + 1
        elif(data[x][y] == "S"):
            points[2] = points[2] + 1
        elif(data[x][y] == "C"):
            points[3] = points[3] + 1 
        
        #Neighbour node up, left, right and down 
        for i in range(len(newRow)):
            newX = x + newRow[i]
            newY = y + newColumn[i]
            
            #Add neighbour node if it is not visited before and It is not border character
            if(0 <= newX < row and 0 <= newY < len(data[newX]) and (newX, newY) not in visited):
                if(data[newX][newY] not in borders):
                    queue.append((newX, newY))
                    visited.add((newX, newY))
            
            #Add coordinate if it is border corner character '+'
            if(0 <= newX < row and 0 <= newY < len(data[newX])  and (newX, newY) not in coordinates):
                if(data[newX][newY] == '+'):
                    coordinates.append((newX, newY))
        
        #neighbour node up-left, up-right, down-left, and down-right
        for i in range(len(crossRow)):
            newX = x + crossRow[i]
            newY = y + crossColumn[i]
            
            #Add coordinate if it is border corner character '+'
            if(0 <= newX < row and 0 <= newY < len(data[newX]) and (newX, newY) not in coordinates):
                if(data[newX][newY] == '+'):
                    coordinates.append((newX, newY))
                    
        #neighbour node up-left-left, up-right-right, down-left-left, and down-right-right
        #down-down-left, down-down-right, up-up-left, up-up-right
        for i in range(len(crossRow)):
            newX = x + cornerRow[i]
            newY = y + cornerRow[i]
            
            #Add coordinate if it is border corner character '+'
            if(0 <= newX < row and 0 <= newY < len(data[newX]) and (newX, newY) not in coordinates):
                if(data[newX][newY] == '+'):
                    coordinates.append((newX, newY))
        # print(coordinates)     
    total = [sum(i) for i in zip(total, points)]
    nameAllPointDict.append([name, points, coordinates])

nameAllPointDict.sort(key=lambda x: x[0], reverse=False)

print("Total :")
print("W:", total[0], end=" ")
print("P:", total[1], end=" ")
print("S:", total[2], end=" ")
print("C:", total[3])
print()

for value in nameAllPointDict: 
    print(value[0], ":")
    print("W:", value[1][0], end=" ")
    print("P:", value[1][1], end=" ")
    print("S:", value[1][2], end=" ")
    print("C:", value[1][3])
    
    print("Coordinates of ", value[0], ": ", value[2])
    print()
