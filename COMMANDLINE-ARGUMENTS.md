# Syntax usage and command line parameter description

## Reload python code

Reloads a python script file or Blender addon. 
This might be your main python file for example `__init__.py` or the `BLENDER_ADDON_NAME`

Examples:
`toblender --reload C:\git\tcp\test.py;`  
`toblender --reload BY-GEN;`  

## Watch folder

Watches an existing folder for changes and reloads regarding python code defined via `--reload` command line argument.

Examples:
`toblender --watch C:\git\tcp --reload C:\git\tcp\test.py;`  

## Show version info

Get version details of this application.

Examples:
`toblender -v;`  
`toblender --version;`  

## Show this help

Examples:
`toblender help;`  
`toblender -h;`  
`toblender /?;`