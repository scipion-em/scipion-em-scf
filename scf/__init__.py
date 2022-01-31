# **************************************************************************
# *
# * Authors:     Federico P. de Isidro Gomez (fp.deisidro@cnb.csi.es) [1]
# *
# * [1] Centro Nacional de Biotecnologia, CSIC, Spain
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
import os

import pwem
from scipion.constants import PYTHON
from pyworkflow.gui.project.utils import OS

from scf.constants import DEFAULT_VERSION, SCF_HOME

_logo = ""
_references = []


class Plugin(pwem.Plugin):
    _homeVar = SCF_HOME
    _validationMsg = None

    @classmethod
    def _defineVariables(cls):
        cls._defineEmVar(SCF_HOME, cls._getSCFFolder(DEFAULT_VERSION))

    @classmethod
    def getEnviron(cls):
        return None

    @classmethod
    def runSCF(cls, protocol, program, args, cwd=None):
        """ Run SCF command from a given protocol. """

        #  Call python
        cmd = PYTHON + " "

        # Get the command
        cmd += Plugin.getHome("CommandLineSCF")
        cmd = os.path.join(cmd, program)

        # Run the protocol with that command
        protocol.runJob(cmd, args, env=cls.getEnviron(), cwd=cwd)

    @classmethod
    def defineBinaries(cls, env):
        SCF_INSTALLED = 'scf_%s_installed' % DEFAULT_VERSION

        if 'linux' in OS.getPlatform().lower():

            # Clone repo https://github.com/LyumkisLab/CommandLineSCF.git
            installationCmd = ' git clone git@github.com:LyumkisLab/CommandLineSCF.git \n'

            # Create installation finished flag file
            installationCmd += 'touch %s' % SCF_INSTALLED

            env.addPackage('scf',
                           version=DEFAULT_VERSION,
                           createBuildDir=True,
                           buildDir=cls._getEMFolder(DEFAULT_VERSION),
                           commands=[(installationCmd, SCF_INSTALLED)],
                           default=True)

    @classmethod
    def _getEMFolder(cls, version, *paths):
        return os.path.join("scf-%s" % version, *paths)

    @classmethod
    def _getSCFFolder(cls, version, *paths):
        return os.path.join(cls._getEMFolder(version), *paths)
