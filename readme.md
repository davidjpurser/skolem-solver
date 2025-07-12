# Skolem Solvers


Developed by [David Purser](https://www.davidpurser.net/) and [Joris Nieuwveld](https://www.mpi-sws.org/people/jnieuwve/).

The code is made available under the GNU Affero General Public License.

Paper on which the Leapfrogging algorithm is based. Yuri Bilu, Florian Luca, Joris Nieuwveld, Joël Ouaknine, David Purser, and James Worrell. "Skolem meets Schanuel." MFCS 2022. [doi:10.4230/LIPIcs.MFCS.2022.20](http://doi.org/10.4230/LIPIcs.MFCS.2022.20), [arxiv:2204.13417](https://arxiv.org/abs/2204.13417). 

[![DOI](https://zenodo.org/badge/1017415732.svg)](https://doi.org/10.5281/zenodo.15858619)

# Datasets

Data used in the paper: [dataset](https://github.com/davidjpurser/skolem-solver/blob/main/datasets/mfcs.tpls)

Generated using generator.py.

# Guide

This guide is aimed at using the tool, for developing and deploying the tool, see [here](developing.md)

## Getting started 

Install `sage`, at least version 10

`sage --python -m pip install -r requirements.txt`


## Running the server locally

`sage --python -m gunicorn -w 4 flask_app:app` also available as `./server.sh`

See [skolem.mpi-sws.org](https://skolem.mpi-sws.org)

## Input format

The input format is common between the following two tools.

Line 1: OrderOfLRS space separated coefficients of the recurrence
Line 2: OrderOfLRS space separated initial numbers


<code>9 -10 522 -4745 4225
-6 -12 3066 -768 -15366</code>

encodes

`u_{n} =9u_{n-1} + -10u_{n-2} + 522u_{n-3} + -4745u_{n-4} + 4225u_{n-5}`
With initial values : `[-6, -12, 3066, -768, -15366]`

## Flags
<code>
	# Global options
		"-r": 'reducelrs', (removes the gcd)
		"-p": 'print', (whether to print along the way)
		"-sD": "skipdegeneratecheck",
		"-sM": "skipminimisation",
	# Which algorithm to run (can be both)
		"-L": 'Leapfrogging',
		"-B": 'BakerDavenport',
	#BD options
		"-n": 'reverseLRS', (not to be used with -bi)
		"-bi": 'bidirectional', (otherwise only positive direction is performed)
		"-bo": 'boundonly', (doesn't compute the zeros, just the bound)
		"-blist" : "listn", (list the whole LRS up to the bound)
	# Leapfrogging options 
		"-lmerge": 'mergesubcases',
		"-lmin": 'smallestm', (otherwise smallest period is used)
		"-lfastjump": 'usefastjump', )
</code>

### These require a number
<code>
		"-fixedbound" : "fixedbound",
</code>


## Simple Skolem Solver Tool (with Sage Installed)

Solves Skolem for (nearly) all simple LRS

* Usage by file: `sage skolemtool.py flags filename`, for example `sage skolemtool.py -L fibonacci.eg`
* Usage by server, see above.

Currently hosted at `skolem.mpi-sws.org` via `flask_app.py`.








