# ToBlender

Use an external editor with Blender 🐵.

## Installation

### 1. Blender Addon

To make this work you need to install the [corresponding addon 2blender](https://github.com/s-a/ToBlender/releases). This will start a simple tcp server to manage the synchronisation process. Since this could be a security risk you might want to keep an eye on activation state of the addon when you finished your python development.

### 2. Console Application

This application is based on Node.js so you need to install it from https://nodejs.org/en/download/.

After that you can install the application with `npm install toblender -g`. It needs to be global to make it systemwide available.

## Demo usage

![Demo](demo/demo.gif)

### Commandline arguments

See [COMMANDLINE-ARGUMENTS.md](COMMANDLINE-ARGUMENTS.md) for all details.