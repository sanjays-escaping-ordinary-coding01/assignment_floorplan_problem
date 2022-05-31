#!/usr/bin/env python3.9.4

'''
__version__ = 2.0
__status__ = complete

__purpose__ = 
command line tool that process floor plan in text file and extract the following information: 
- Number of different chair types for the floor plan
- Number of different chair types per room

__output__ =
Total : 
W: 0, P: 0, S: 0, C: 0

room :
W: 0, P: 0, S: 0, C: 0
Boundary: [(0, 0)]
'''

import argparse

def check_file(files: str):
    '''
    purpose: To check if text file
    
    input: file path
    
    output: 
    if True: Open file for reading
    else False
    '''
    if files[-3:] == "txt":
        return open(files, mode="r")

def process_file(input_file):
    '''
    purpose: process input file
    
    input: file object
    
    output: 
    1. total count of individual chairs (list)
    2. Room, count of chairs, coordinates of construction points
    '''
    
    maxcolumn = 0
   
    # Read file content
    data = input_file.readlines()

    # Scan through each line
    for line in range(len(data)):
        data[line] = data[line].replace('\n', '')
        data[line] = data[line].replace('\t', '     ')
        data[line] = [ char for char in data[line]] # split each line
        maxcolumn = max(maxcolumn, len(data[line])) # max length of each line

    visited = set()
    row = len(data)
    i = 0
    j = 0

    # Boarder characters
    borders = ["-", "/", "\\", "+", "|"]
    room_point_dict = {}

    # Find out coordinate point of name within brackets ()
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
                room_point_dict[name] = pair
            j = j + 1
        i = i + 1

    room_all_point_dict = []

    # Count total chairs (W,P,S,C)
    total = [0, 0, 0, 0]

    # Neighbour up, left, right, down
    new_row = [0, 0, -1, 1 ]
    new_column = [-1, 1, 0, 0]

    cross_row = [1, 1, -1, -1 ]
    cross_column = [-1, 1, -1, 1]

    corner_row = [1, 1, -1, -1, 2, 2, -2, -2]

    for name, pair in room_point_dict.items():
        points = [0, 0, 0, 0]
        coordinates = []
        
        queue = []
        visited = set()
        queue.append(pair)
        visited.add(pair)
        
        #Breadth First Search
        while queue:
            position = queue.pop(0)
            x = position[0]
            y = position[1]
            
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
            for node in range(len(new_row)):
                new_x = x + new_row[node]
                new_y = y + new_column[node]
                
                #Add neighbour node if it is not visited before and It is not border character
                if(0 <= new_x < row and 0 <= new_y < len(data[new_x]) and (new_x, new_y) not in visited):
                    if(data[new_x][new_y] not in borders):
                        queue.append((new_x, new_y))
                        visited.add((new_x, new_y))
                
                #Add coordinate if it is border corner character '+'
                if(0 <= new_x < row and 0 <= new_y < len(data[new_x])  and (new_x, new_y) not in coordinates):
                    if(data[new_x][new_y] == '+'):
                        coordinates.append((new_x, new_y))
            
            #neighbour node up-left, up-right, down-left, and down-right
            for node in range(len(cross_row)):
                new_x = x + cross_row[node]
                new_y = y + cross_column[node]
                
                #Add coordinate if it is border corner character '+'
                if(0 <= new_x < row and 0 <= new_y < len(data[new_x]) and (new_x, new_y) not in coordinates):
                    if(data[new_x][new_y] == '+'):
                        coordinates.append((new_x, new_y))
                        
            #neighbour node up-left-left, up-right-right, down-left-left, and down-right-right
            #down-down-left, down-down-right, up-up-left, up-up-right
            for node in range(len(cross_row)):
                new_x = x + corner_row[node]
                new_y = y + corner_row[node]
                
                #Add coordinate if it is border corner character '+'
                if(0 <= new_x < row and 0 <= new_y < len(data[new_x]) and (new_x, new_y) not in coordinates):
                    if(data[new_x][new_y] == '+'):
                        coordinates.append((new_x, new_y))
            
        total = [sum(i) for i in zip(total, points)]
        room_all_point_dict.append([name, points, coordinates])

    room_all_point_dict.sort(key=lambda x: x[0], reverse=False)
    
    return total, room_all_point_dict

def print_output(*args):
    '''
    purpose: Print Output in the required format
    input: 
    1. total count of individual chairs (list)
    2. Room, count of chairs, coordinates of construction points
    
    output: String
    
        Total: 
        W: 0, P: 0, S: 0, C: 0
    
        room :
        W: 0, P: 0, S: 0, C: 0
        Boundary: [(0, 0)]
    
    '''
    
    total, room_all_point_dict = args[0][0], args[0][1]
    
    print("\nTotal :")
    print("W: {0}, P: {1}, S: {2}, C: {3}".format(total[0], total[1], total[2], total[3]))

    for value in room_all_point_dict: 
        print()
        print(value[0], ":")
        print("W: {0}, P: {1}, S: {2}, C: {3}".format(value[1][0], value[1][1], value[1][2], value[1][3]))
        
        print("Boundary: {0}".format(value[2]))

def main():
  
    # Creating argument parser to load file
    parser = argparse.ArgumentParser(description='Kindly load an input file')
    parser.add_argument('Path', metavar='path', type=str, nargs='+',
                        help='file path to text file')
            
    args = parser.parse_args()  
    filename = args.Path[0] 
    input_file = check_file(filename) 
    if input_file:
        print_output(process_file(input_file))
    else:
        print("Problem processing the file")
        
if __name__ == "__main__":
    try:
        main()        
    except:
        print("Problem processing the file")
          
    
