# **************************************************************************
# *
# * Authors:     Federico P. de Isidro Gomez (fp.deisidro@cnb.csic.es) [1]
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
import scf
import tempfile
import os
from PIL import Image

import pyworkflow.viewer as pwviewer
import pyworkflow.protocol.params as params

from scf import Plugin
from scf.protocols import ScfProtAnalysis


class ScfViewer(pwviewer.Viewer):
    """ Wrapper to visualize the output graphs obtained by the SCF analysis
    """
    _environments = [pwviewer.DESKTOP_TKINTER, Plugin.getEnviron()]
    _targets = [
        ScfProtAnalysis
    ]

    def _visualize(self, obj, **kwargs):
        img = Image.open(self.protocol._getExtraPath("particleAnglesTilt0.jpg"))
        img.show()
