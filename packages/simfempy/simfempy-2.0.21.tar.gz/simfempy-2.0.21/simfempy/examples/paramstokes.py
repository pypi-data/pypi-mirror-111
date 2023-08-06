assert __name__ == '__main__'
# in shell
import os, sys
simfempypath = os.path.abspath(os.path.join(__file__, os.path.pardir, os.path.pardir, os.path.pardir, os.path.pardir,'simfempy'))
sys.path.insert(0,simfempypath)

import numpy as np
import simfempy.meshes.testmeshes as testmeshes
from simfempy.applications.stokes import Stokes
from simfempy.applications.problemdata import ProblemData
from simfempy.tools.comparemethods import CompareMethods

#----------------------------------------------------------------#
def test(exactsolution, **kwargs):
    dim = len(exactsolution[0])
    data = ProblemData()
    data.params.scal_glob['mu'] = kwargs.pop('mu', 1)
    if dim==2:
        data.ncomp=2
        createMesh = testmeshes.unitsquare
        colorsdir = [1001,1002, 1003]
        colorsneu = [1000]
    else:
        data.ncomp=3
        createMesh = testmeshes.unitcube
        colorsdir = [100,101,102,104,105]
        colorsneu = [103]
    data.bdrycond.set("Dirichlet", colorsdir)
    data.bdrycond.set("Neumann", colorsneu)
    # applicationargs = {'problemdata': data, 'exactsolution': exactsolution, 'precond_p':'schur@diag@1'}
    # applicationargs = {'problemdata': data, 'exactsolution': exactsolution, 'precond_p':'schur@none@1'}
    applicationargs = {'problemdata': data, 'exactsolution': exactsolution}
    # paramsdict = {'hdivpenalty': np.linspace(0,2,3)}
    paramsdict = {'divdivparam': [0]}
    niter = kwargs.pop('niter', 3)
    comp =  CompareMethods(niter=niter, createMesh=createMesh, paramsdict=paramsdict, application=Stokes, applicationargs=applicationargs, **kwargs)
    return comp.compare()



#================================================================#
if __name__ == '__main__':
    test(niter=5, exactsolution=[["x**2-y","-2*x*y+x**2"],"x*y"], mu=1e-1)
    # test(niter=6, exactsolution=[["x**2-y+z**2","-2*x*y*z+x**2","x**2-y**2+z"],"x*y+x*z"])
