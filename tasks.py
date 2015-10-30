import os
from invoke import task, run

@task
def server():
	run('python main.py')

@task
def populate():
	grid()
	ipeds()

@task
def grid():
	import main
	from sources import grid
	main.main()
	grid.populate()

@task
def ipeds():
	import main
	from sources import ipeds
	main.main()
	ipeds.populate()