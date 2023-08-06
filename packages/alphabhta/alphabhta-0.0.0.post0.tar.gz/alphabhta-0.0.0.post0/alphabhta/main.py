#!/usr/bin/env python3

import os
import argparse
import subprocess

if __name__ == '__main__':
	from . import __version__
else:
	from . import __version__


def command(cmd):
	"""Run a shell command"""

	subprocess.call(cmd, shell=True)

	"""
	cmd_split = cmd.split()

	process = subprocess.Popen(cmd_split,
		shell=True,
		stdout=subprocess.PIPE,
		stderr=subprocess.PIPE,
	universal_newlines=True)
	stdout, stderr = process.communicate()

	return stdout, stderr
	"""


def main():

	absFilePath = os.path.dirname(os.path.abspath(__file__))
	cwdPath = os.path.abspath(os.getcwd())

	parser = argparse.ArgumentParser(
		prog="owl",
		description="Assembly/C/C++ utility to build embedded systems",
		epilog="Author: Kanelis Elias",
		fromfile_prefix_chars='@')

	# parser.add_argument('-v', '--verbose',
	#                       action='store_true',
	#                       help='an optional argument')

	"""
	parser.add_argument('Path',
	metavar='path',
	type=str,
	default=cwdPath,
	help='the config filepath')
	"""

	parser.add_argument(
		'-d', '--directory',
		type=str,
		default=cwdPath,
		help='the config filepath')

	parser.add_argument(
		'-v', '--version',
		action='store_true',
		help='get the version of the build system')

	# parser.add_argument(
	# 	'-f',
	# 	'--file',
	# 	help='A readable file',
	# 	metavar='FILE',
	# 	type=argparse.FileType('r'),
	# 	default=None)

	cmd_parser = parser.add_subparsers(dest='cmd', description="")

	parser_build = cmd_parser.add_parser(
		'build',
		help="build the project")
	parser_get_version = cmd_parser.add_parser(
		'get_version',
		help="try to get the version from git")
	# parser_get_version.add_argument(
	# 	'-a', '--alpha',
	# 	dest='alpha',
	# 	help='try to get the version')

	# Execute parse_args()
	args = parser.parse_args()

	subcommand = parser.parse_args().cmd

	if args.version is True:
		print(f"version: {__version__}")
		exit(0)

	# if subcommand is None or subcommand == "build":
	if subcommand == "build":
		makefilePath = os.path.join(absFilePath, "conf/make/Makefile")
		command(f"make -f {makefilePath}")
	elif subcommand == "get_version":
		print("version")
	else:
		print(f"Version: {__version__}")

	return

	# Working directory
	wd = os.path.abspath(args.directory)

	print(f"File:              {absFilePath}")
	print(F"CWD:               {cwdPath}")
	print(F"Working directory: {wd}")
	print(F"makefile path:     {makefilePath}")
	print()

	command(f"make -f {makefilePath}")


if __name__ == '__main__':
	main()
