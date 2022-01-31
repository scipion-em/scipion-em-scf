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
import csv

from pwem.convert.transformations import euler_from_matrix
from pyworkflow.protocol.params import FloatParam, IntParam, PointerParam
from pwem.protocols import ProtAnalysis3D
from scf import Plugin


class ScfProtAnalysis(ProtAnalysis3D):
    """
    Calculate SCF parameter and make plots.
    The SCF is how much the SSNR has likely been attenuated due to projections not being distributed uniformly.
    """

    _label = 'SCF Analysis'

    def __init__(self, **args):
        ProtAnalysis3D.__init__(self, **args)

    # --------------------------- DEFINE param functions ----------------------
    def _defineParams(self, form):
        form.addSection(label='Input')

        form.addParam('inParticles',
                      PointerParam,
                      pointerClass='SetOfParticles',
                      label='Input particles',
                      help='Input set of particles containing angle information')

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

        # not implemented yet
        # --3DFSCMap eventually we will look at correlations of the resolution and the sampling

    # -------------------------- INSERT steps functions ---------------------
    def _insertAllSteps(self):
        self._insertFunctionStep(self.generateSideInfo)
        self._insertFunctionStep(self.runScfAnalysis)

    # --------------------------- STEPS functions ----------------------------
    def generateSideInfo(self):
        """ Generates angle information of the particles to feed the SCF algorithm """
        particles = self.inParticles.get()

        angles = []

        for p in particles:
            matrix = p.getTransform().getMatrix()

            psi, theta, rot = self.getAnglesFromMatrix(matrix)

            angles.append([psi, theta, rot])

        outputAnglesFile = self._getExtraPath("particleAngles.txt")

        with open(outputAnglesFile, 'w') as f:
            csvW = csv.writer(f, delimiter='\t')
            csvW.writerows(angles)

    def runScfAnalysis(self):
        """ Compute the SCF analysis """
        paramsScf = {
            'FileName': self._getExtraPath("particleAngles.txt"),
            # '3DFSCMap': , # Not implemented yet
            'RootOutputName': self._getExtraPath(),
            'FourierRadius': self.FourierRadius.get(),
            'NumberToUse': self.NumberToUse.get(),
            'TiltAngle': self.TiltAngle.get()
        }

        argsScf = "--RootOutputName %(RootOutputName)s " \
                  "--FourierRadius %(FourierRadius)d " \
                  "--NumberToUse %(FourierRadius)d " \
                  "--TiltAngle %(TiltAngle)d " \
                  "%(FileName)s "
                  # "--3DFSCMap %(3DFSCMap)s "

        Plugin.runSCF(self, 'SCFJan2022.py', argsScf % paramsScf)

    # --------------------------- UTILS functions ----------------------------
    @staticmethod
    def getAnglesFromMatrix(matrix):
        angles = euler_from_matrix(matrix)

        return angles[0], angles[1], angles[2]

    # --------------------------- INFO functions ----------------------------
    def _summary(self):
        summary = []

        return summary

    def _methods(self):
        methods = []

        return methods
