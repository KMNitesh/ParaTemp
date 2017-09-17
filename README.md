[![DOI](https://zenodo.org/badge/64339257.svg)](https://zenodo.org/badge/latestdoi/64339257)

This is a package with many tools, functions, and some classes for
analyzing and running molecular dynamics trajectories.
It is specifically designed for working with Replica Exchange Molecular
Dynamics (Parallel Tempering, when the replicas are at different
temperatures).
It is in part specialized for analyzing trajectories of TADDOL-catalyzed
reactions, though I hope to generalize it more.

All simulations have so far been from GROMACS, but with the powerful
generality of [MDAnalysis](http://www.mdanalysis.org/), that should not
be a particular constraint for using this software.

This package depends on MDAnalysis, NumPy, pandas, panedr, and
gromacswrapper.
Most if not all should be installable with conda.