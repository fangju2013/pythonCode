from multiprocessing import  Pool

def add(n):
    n= n+3
    return n

if __name__=="__main__":
    pool=Pool(4)
    ss=pool.map_async(add,range(10000))
    pool.close()
    pool.join()