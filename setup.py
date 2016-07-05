#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
This file is part of OpenSesame.

OpenSesame is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

OpenSesame is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with OpenSesame.  If not, see <http://www.gnu.org/licenses/>.
"""

from setuptools import setup
import glob
import yaml

# Extract the plugin version from info.yaml
with open('media_player_mpy/info.yaml') as fd:
	d = yaml.load(fd)
version = d['version']

setup(
	name='opensesame-plugin-media_player_mpy',
	version=version,
	description='Media player plugin for OpenSesame, based on MoviePy',
	author='Daniel Schreij',
	author_email='dschreij@gmail.com',
	url='https://github.com/dschreij/opensesame-plugin-mediaplayer',
	license='MIT',
	install_requires=['mediadecoder'],
	classifiers=[
		'Intended Audience :: Developers',
		'Environment :: Console',
		'Topic :: Documentation :: Sphinx',
		'Topic :: Multimedia :: Sound/Audio',
		'Topic :: Multimedia :: Sound/Audio :: Players',
		'Topic :: Multimedia :: Video :: Display',
		'Topic :: Software Development :: Libraries :: pygame',
		'Operating System :: MacOS :: MacOS X',
		'Operating System :: Microsoft :: Windows',
		'Operating System :: POSIX',
		'License :: OSI Approved :: MIT License',
		'Programming Language :: Python',
	],
	data_files=[
		('share/opensesame_plugins/media_player_mpy', [
			'media_player_mpy/media_player_mpy.py',
			'media_player_mpy/media_player_mpy.md',
			'media_player_mpy/info.yaml',
			]),
		('share/opensesame_plugins/media_player_mpy/handlers',
			glob.glob('media_player_mpy/handlers/*.py'))
		],
	)
