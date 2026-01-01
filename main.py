'''
Finalpass v1.0.0

Author: MrDerpus

Python 3.12.3
Ubuntu 24.03.3 LTS

A wrapper for scanimage that works around HP DeskJet 2823e eSCL firmware job-state issues.
This program assumes you are using this to scan images and save them to you computer.
'''

from sys import exit as kill
import subprocess
import re

import click


@click.group()
def cli(): pass


@click.command(context_settings=dict(ignore_unknown_options=True))
@click.argument('targs', nargs=-1)
def pyscan(targs:tuple) -> None:

	args:list = list(targs)
	output_flag:bool = False
	output_file:str  = ''
	xml:str   = ''
	jobs:list = []

	# Get printer's scanner status XML
	result = subprocess.run(
		['curl', '-s', 'http://localhost:60000/eSCL/ScannerStatus'],
		capture_output=True,
		check=True,
		text=True
	)
	xml = result.stdout

	# Extract ScanJob paths
	jobs = re.findall(r'/eSCL/ScanJobs/[^<]*', xml)

	print(' Cleaning up . . .')
	# Delete each job
	for job in jobs:
		subprocess.run(
			['curl', '-X', 'DELETE', f'http://localhost:60000{job}'],
			stdout=subprocess.DEVNULL,
			stderr=subprocess.DEVNULL,
			check=True
		)


	# Run scan command
	scan_command:list = ['scanimage', '-d', 'escl:http://localhost:60000', '--format=png', '--mode', 'color', '--resolution', '300']


	args_iter = iter(args)
	for arg in args_iter:

		arg = str(arg).strip()

		if arg.lower()   == 'grey':   arg = 'gray'
		elif arg.lower() == 'colour': arg = 'color'
		
		if arg == '-o':
			output_file = next(args_iter, '')
			scan_command.extend([arg, output_file])
		else:
			scan_command.append(arg)


	print(' Running scan . . .')
	subprocess.run(
		scan_command,
		stderr=subprocess.DEVNULL,
		check=True
	)

	print(' Complete!')
cli.add_command(pyscan)



if __name__ == '__main__':
	cli()