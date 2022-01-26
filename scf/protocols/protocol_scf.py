# -*- coding: utf-8 -*-
# **************************************************************************
# *
# * Authors:     Federico P. de Isidro-Gomez (fp.deisidro@cnb.csic.es)
# *
# * Unidad de  Bioinformatica of Centro Nacional de Biotecnologia , CSIC
# *
# * This program is free software; you can redistribute it and/or modify
# * it under the terms of the GNU General Public License as published by
# * the Free Software Foundation; either version 2 of the License, or
# * (at your option) any later version.
# *
# * This program is distributed in the hope that it will be useful,
# * but WITHOUT ANY WARRANTY; without even the implied warranty of
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# * GNU General Public License for more details.
# *
# * You should have received a copy of the GNU General Public License
# * along with this program; if not, write to the Free Software
# * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA
# * 02111-1307  USA
# *
# *  All comments concerning this program package may be sent to the
# *  e-mail address 'scipion@cnb.csic.es'
# *
# **************************************************************************

from pyworkflow.protocol.params import (FloatParam, IntParam)
from pwem.protocols import ProtAnalysis3D
from pyworkflow.object import Float
from scf.constants import VERSION_0_0_1
from scf import Plugin


MONORES_METHOD_URL = 'http://github.com/I2PC/scipion/wiki/XmippProtMonoRes'
OUTPUT_RESOLUTION_FILE = 'monoresResolutionMap.mrc'
OUTPUT_RESOLUTION_FILE_CHIMERA = 'monoresResolutionChimera.mrc'
OUTPUT_MASK_FILE = 'refinedMask.mrc'
FN_MEAN_VOL = 'meanvol'
METADATA_MASK_FILE = 'metadataresolutions'
FN_METADATA_HISTOGRAM = 'hist.xmd'
BINARY_MASK = 'binarymask'
FN_GAUSSIAN_MAP = 'gaussianfilter'


class ScfProtAnalysis(ProtAnalysis3D):
    """
    Calculate SCF parameter and make plots.
    The SCF is how much the SSNR has likely been attenuated due to projections not being distributed uniformly.
    """

    _label = 'SCF'
    _lastUpdateVersion = VERSION_0_0_1

    def __init__(self, **args):
        ProtAnalysis3D.__init__(self, **args)
        self.min_res_init = Float()
        self.max_res_init = Float()

    # --------------------------- DEFINE param functions ----------------------
    def _defineParams(self, form):
        form.addSection(label='Input')

        # --FileName, "the name of the File of Angles; Psi Theta Rot in degrees  "
        # --3DFSCMap, " the 3DFSC map, if one wants to correlate Sampling/Resolution; currently not implemented  "
        # --RootOutputName, " the root name for logging outputs. Default is SCFAnalysis "

        form.addParam('FourierRadius',
                      IntParam,
                      default=50,
                      label='Fourier radius',
                      help='Fourier radius (int) of the shell on which sampling is evaluated')

        form.addParam('NumberToUse',
                      IntParam,
                      default=1000,
                      label='Number of projections',
                      help='The number of projections to use, if you do not want to use all of them')

        form.addParam('TiltAngle',
                      FloatParam,
                      default=0.0,
                      label='Tilt angle',
                      help='Tilting of the sample in silico')

    # -------------------------- INSERT steps functions ---------------------
    def _insertAllSteps(self):
        self._insertFunctionStep(self.runScfAnalysis)

    # --------------------------- STEPS functions ----------------------------
    def runScfAnalysis(self):
        """Compute the SCF analysis"""

        # paramsScf = {
        #     'FileName': ,
        #     '3DFSCMap': ,
        #     'RootOutputName': self.getExtraPath(),
        #     'FourierRadius': self.FourierRadius.get(),
        #     'NumberToUse': self.NumberToUse.get(),
        #     'TiltAngle': self.TiltAngle.get()
        # }
        #
        # argsScf = "--FileName %(FileName)s " \
        #     "--3DFSCMap %(3DFSCMap)s " \
        #     "--RootOutputName %(RootOutputName)s " \
        #     "--FourierRadius %(FourierRadius)d" \
        #     "--NumberToUse %(FourierRadius)d " \
        #     "--TiltAngle %(TiltAngle)f "


        # Plugin.runSCF(self, 'SCFJan2022', argsScf % paramsScf)

    # --------------------------- INFO functions ----------------------------
    def _summary(self):
        summary = []

        return summary

    def _methods(self):
        methods = []

        return methods

