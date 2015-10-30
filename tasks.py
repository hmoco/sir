import os
from invoke import task, run

@task
def server():
	run('python main.py')

@task
def populate():
	sources = 'sources/'
	files = [file_ for file_ in os.listdir(sources) if os.path.isfile(os.path.join(sources, file_))]
	print files
	for file_ in files:
		run ('python {}'.format(os.path.join(sources, file_)))