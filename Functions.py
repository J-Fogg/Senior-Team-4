from queue import Queue
q = Queue(maxsize=6)

def add (x,y):
    z = x+y
    return z

def main():
    value_x = 5
    value_y = 6
    answer = add(value_x,value_y)
    print(answer)git 

if __name__=="__main__":
    main()

