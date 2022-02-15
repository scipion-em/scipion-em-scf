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
import os.path

from pwem.convert.transformations import euler_from_matrix
from pyworkflow.object import String
from pyworkflow.protocol.params import FloatParam, IntParam, PointerParam, StringParam
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
        self._outputInfoFileSCF = String("")

    # --------------------------- DEFINE param functions ----------------------
    def _defineParams(self, form):
        form.addSection(label='Input')

        form.addParam('inParticles',
                      PointerParam,
                      pointerClass='SetOfParticles',
                      label='Input particles',
                      help='Input set of particles containing angle information.')

        form.addParam('resolutionAnalysis',
                      FloatParam,
                      default=5,
                      label='Resolution analysis',
                      help='Resolution at which the SCF analysis will be performed.')

        form.addParam('sym',
                      StringParam,
                      default='',
                      label='Symmetry',
                      help='Options Icos, Oct, Tet, Cn, or Dn. If tilt specified, then Sym =C1.')

        form.addParam('numberToUse',
                      IntParam,
                      default=1000,
                      label='Number of projections',
                      help='The number of projections to use, if you do not want to use all of them. The default value '
                           'is the minimum of 10000 or the total number in the file. One can try to increase this '
                           'number. To select all the particles set to -1.')

        form.addParam('tiltAngle',
                      FloatParam,
                      default=0.0,
                      label='Tilt angle',
                      help='Tilting of the sample in silico.')

        # Not implemented yet
        # --3DFSCMap eventually we will look at correlations of the resolution and the sampling

    # -------------------------- INSERT steps functions ---------------------
    def _insertAllSteps(self):
        self._insertFunctionStep(self.generateSideInfo)
        self._insertFunctionStep(self.runScfAnalysis)

    # --------------------------- STEPS functions ----------------------------
    def generateSideInfo(self):
        """ Generates side information and input files to feed the SCF algorithm """

        # Generates the angle information file of the particles to feed the SCF algorithm
        self._outputInfoFileSCF = String(self._getExtraPath("outputInfoFileSCF.txt"))

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

        # Converts the input resolution to fourier radius
        self.fourierRadius = (self.inParticles.get().getSamplingRate() / self.resolutionAnalysis.get()) * 2 * self.inParticles.get().getFirstItem().getXDim()

        self._store()

    def runScfAnalysis(self):
        """ Compute the SCF analysis """
        paramsScf = {
            'FileName': self._getExtraPath("particleAngles.txt"),
            # '3DFSCMap': , # Not implemented yet
            'RootOutputName': self._getExtraPath(),
            'FourierRadius': self.fourierRadius,
            'TiltAngle': self.tiltAngle.get(),
            'outputInfoFileSCF': self._outputInfoFileSCF,
        }

        argsScf = "--RootOutputName %(RootOutputName)s " \
                  "--FourierRadius %(FourierRadius)d " \
                  "--TiltAngle %(TiltAngle)d " \

        if self.numberToUse.get() != -1:
            paramsScf.update({
                'NumberToUse': self.numberToUse.get(),
            })

            argsScf += "--NumberToUse %(NumberToUse)d "

        if self.sym.get() != '':
            paramsScf.update({
                'Sym': self.sym.get()
            })

            argsScf += "--Sym %(Sym)s "

        argsScf += "%(FileName)s " \
                   "2>&1 | tee %(outputInfoFileSCF)s "
                   # "--3DFSCMap %(3DFSCMap)s " # Not implemented yet

        Plugin.runSCF(self, 'SCFJan2022.py', argsScf % paramsScf)

    # --------------------------- UTILS functions ----------------------------
    @staticmethod
    def getAnglesFromMatrix(matrix):
        angles = euler_from_matrix(matrix)

        return angles[0], angles[1], angles[2]

    # --------------------------- INFO functions ----------------------------
    def _summary(self):
        summary = []

        if os.path.exists(self._outputInfoFileSCF.get()):
            summary.append("SCF analysis output summary:")

            with open(self._outputInfoFileSCF.get(), 'r') as f:
                lines = f.readlines()

            for line in lines:
                summary.append(line[:-1])

        else:
            summary.append("SCF analysis not finished yet.")

        return summary

    def _methods(self):
        methods = []

        if os.path.exists(self._outputInfoFileSCF.get()):
            methods.append('SCF analysis completed using the Baldwin and Lyumkis method. Out information contained in '
                           'summary and plot image under "Analyze results".')

        else:
            methods.append("SCF analysis not finished yet.")

        return methods
