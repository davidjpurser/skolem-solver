from . import Options




class FlagManager:

	flagMapping = {
	#all
		"-r": 'reducelrs',
		"-p": 'print',
		"-sD": "skipdegeneratecheck",
		"-sM": "skipminimisation",
	#algorithmchoice
		"-L": 'Leapfrogging',
		"-B": 'BakerDavenport',
		"-P": "pAdic",
	#padic options:
		"-sP": "skipmultiplicity",
		"-oP": "primeonly",
	#BD options
		"-n": 'reverseLRS',
		"-bi": 'bidirectional',
		"-bo": 'boundonly',
		"-blist" : "listn",
	#LF options
		"-lmerge": 'mergesubcases',
		"-lmin": 'smallestm',
		"-lfastjump": 'usefastjump',
	#test rig options
		"-t": 'testoptions',
		"-1": 'runone',
	}
	numberFlagMapping = {
		"-TER" : 'terminate',
		"-TO": 'singleInstanceTimeout',
		"-c" : 'cores',
		"-fixedbound" : "fixedbound",
		# pAdic options (numeric)
		"-pApmin": "p_min", 
		"-pAHprec": "H_prec",
	}
	textFlagMapping = {
		"-ec" : 'everychild',
	}


	def setOptions(this, options,flags):

		for x in this.flagMapping:
			if x in flags:
				options.set(this.flagMapping[x], True)

		for x in this.numberFlagMapping:
			if x in flags:
				count = int([y for y in flags.split("-") if y.startswith(x[1:])][0][len(x[1:]):])
				options.set(this.numberFlagMapping[x], count)

		for x in this.textFlagMapping:
			if x in flags:
				text = ([y for y in flags.split("-") if y.startswith(x[1:])][0][len(x[1:]):])
				options.set(this.textFlagMapping[x], text)

		return options

	def getFlags(this, options,exclude =[]):
		flags = []
		for x in this.flagMapping:
			if x not in exclude and this.flagMapping[x] not in exclude and options.get(this.flagMapping[x]):
				flags.append(x)

		for x in this.numberFlagMapping:
			if x not in exclude and this.numberFlagMapping[x] not in exclude and options.get(this.numberFlagMapping[x]):
				flags.append(x + str(options.get(this.numberFlagMapping[x])))

		for x in this.textFlagMapping:
			if x not in exclude and this.textFlagMapping[x] not in exclude and options.get(this.textFlagMapping[x]):
				flags.append(x + str(options.get(this.textFlagMapping[x])))

				
		return "".join(flags)


