#!/usr/bin/env node

const Cli = require('n-cli')
const net = require('net')
const fs = require('fs')
const client = new net.Socket()
const chokidar = require('chokidar')

client.on('data', function (data) {
	console.log('Received: ' + data)
	client.destroy()
})

client.on('close', function () {
	console.log('Connection closed')
})

Cli.prototype.showHelpHint = function () {
	this.stdout(this.color.yellow("use 'toblender help' to get detailed informations about usage.\n"))
}

Cli.prototype.error = function (msg) {
	this.stdout(this.color.red(msg))
}

Cli.prototype.msg = function (msg) {
	this.stdout(this.color.green(msg + '\n'))
}

Cli.prototype.getWatchFolder = function (rc) {
	const result = (rc.watch || this.argv.watch)
	if (typeof (result) === 'string') {
		return this.resolvePath(result)
	} else {
		return null
	}
}

Cli.prototype.watch = function (rc) {
	const self = this

	const watchFolder = this.getWatchFolder(rc)
	const watchSettings = rc.watchSettings || {
		ignored: /^\./,
		persistent: true
	}
	this.msg(`watch folder ${watchFolder}`)
	const watcher = chokidar.watch(watchFolder, watchSettings)

	watcher
		.on('add', function (path) {
			console.log('File', path, 'has been added')
		})
		.on('change', async function (path) {
			console.log('File', path, 'has been changed')
			await self.executeRemote()
		})
		.on('unlink', function (path) {
			console.log('File', path, 'has been removed')
		})
		.on('error', function (error) {
			console.error('Error happened', error)
		})
}

Cli.prototype.executeRemote = async function () {
	await client.connect(3001, '127.0.0.1')
	console.log('Connected')
	// client.write('BY-GEN');
	// client.write('c:\\git\\tcp\\test.py');
	client.write(this.argv.reload)
}

const cli = new Cli({
	silent: false,
	handleUncaughtException: true, // beautifies error output to console
	handledRejectionPromiseError: true, // beautifyies error output to console
	runcom: '.2blender'
})

cli.runcom(async function (rc) {
	const runcomSettings = rc || {}
	this.argv.notNull('reload')

	const watchFolder = this.getWatchFolder(runcomSettings)

	if (watchFolder === null) {
		await this.executeRemote()
	} else {
		// this.error('invalid arguments. ')
		// this.showHelpHint()
		if (!fs.existsSync(watchFolder)) {
			throw new this.Error(`${watchFolder} does not exist.`)
		}
		this.watch(runcomSettings)
	}
})