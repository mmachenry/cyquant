#!/bin/sh

pip uninstall cyquant
rm -r dist/
rm -r cyquant.egg-info/
rm -r build/
rm cyquant/*.cpp
rm cyquant/*.so
