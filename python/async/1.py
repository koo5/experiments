import asyncio

async def probe(mycounter):
	print("Entered probe", mycounter)
	if mycounter == 5:
		raise Exception(123)
	await asyncio.sleep(0.5)
	print("Leaving probe", mycounter)
	return mycounter

async def main():
	print("Calling async function")
	counter = 1
	task1 = asyncio.create_task(probe(counter), name='mytask'+str(counter))
	counter += 1
	task2 = asyncio.create_task(probe(counter), name='mytask'+str(counter))
	counter += 1
	task3 = asyncio.create_task(probe(counter), name='mytask'+str(counter))
	counter += 1
	task4 = asyncio.create_task(probe(counter), name='mytask'+str(counter))
	counter += 1
	task5 = asyncio.create_task(probe(counter), name='mytask'+str(counter))
	counter += 1
	task6 = asyncio.create_task(probe(counter), name='mytask'+str(counter))
	print("Done calling async function")
	#await asyncio.gather(task1, task2, task3)
	print([await www(x) for x in [task1, task2, task3, task4, task5, task6]])
	try:
		pass
		#print(await asyncio.gather(probe(), probe(), probe(), probe(), probe(), probe(), probe()))
		#print(await asyncio.gather(task1, task2, task3, task4, task5, task6))
	except:
		print('okbye')

async def www(x):
	result = None
	try:
		result = (await asyncio.gather(x))[0]
	except Exception as e:
		print('died:', x)
		return e
	else:
		print('ok:', x)
	return result

# Simply run the main coroutine
asyncio.run(main())
