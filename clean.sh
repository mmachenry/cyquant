#!/bin/sh

pip uninstall csiquant
rm -r dist/
rm -r csiquant.egg-info/
rm -r build/
rm csiquant/*.c
