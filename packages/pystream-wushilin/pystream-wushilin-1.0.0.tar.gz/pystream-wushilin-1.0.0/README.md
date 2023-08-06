stream = Stream([1,2,3,4,5])

stream.map(lambda x: x+1).sum() # 20
stream.count() #0, as stream is consumed already


