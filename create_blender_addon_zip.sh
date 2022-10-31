#!/bin/bash

# #################################################################
# Run this sh file (without parameters) to create a Blender add-on 
# (photogrammetry_importer.zip), which can be installed in Blender.
# #################################################################

# Go to the directory where the script is located
cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd

if command -v git >/dev/null 2>&1; then
	echo "Found git executable."
else
	echo "Found NO git executable, use zip to create matrix_world.zip."
  	zip -r matrix_world.zip matrix_world
  	exit 0
fi

if git rev-parse --git-dir > /dev/null 2>&1; then
	echo "Found valid git repository, use git-archive to create zip file."
	# Use the HEAD of the current branch to create an archive of the subfolder matrix_world 
	git archive --format=zip -o matrix_world.zip HEAD matrix_world
else
  echo "Found NO valid git repository, use zip to create matrix_world.zip."
  zip -r matrix_world.zip matrix_world
fi
