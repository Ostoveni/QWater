# -*- coding: utf-8 -*-
"""
/***************************************************************************
 QWater_00Common
                                 A QGIS plugin
 Plugin for Water network design
                              -------------------
        begin                : 2016-03-15
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Jorge Almerio
        email                : jorgealmerio@yahoo.com.br
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from builtins import object
from qgis.core import *
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtCore import *
from qgis.PyQt.QtWidgets import QProgressBar
from qgis.utils import *
import os.path
#        from qgis.gui import QgsMessageBar

class QWater_00Common(object):
    # Store all configuration data under this key
    SETTINGS = 'QWater'
    def CompRealGeom(self,vLayer):
        totAcum=0
        geoAcum=0
        for feat in vLayer.getFeatures():
            ext=feat['LENGTH']
            geo=feat.geometry().length()
            if ext!= NULL:
                totAcum+=ext
            geoAcum+=geo
        return totAcum,geoAcum
    def startProgressBar(self, iniMsg):
        #iniMsg ="Disabling Snapping to Layer: "
        #iface=self.iface
        progressMessageBar = iface.messageBar().createMessage(self.SETTINGS,iniMsg)
        progress = QProgressBar()
        progress.setMaximum(100)
        progress.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        #pass the progress bar to the message Bar
        progressMessageBar.layout().addWidget(progress)
        iface.messageBar().pushWidget(progressMessageBar)
        return progress,progressMessageBar
    def PegaQWaterLayer(self, aForma):
        proj = QgsProject.instance()
        #aForma='PIPES'
        ProjVar=proj.readEntry(self.SETTINGS, aForma)[0]
        if ProjVar=='':
            msgTxt=QCoreApplication.translate('QWater','Undefined Layer: ') +aForma
            #QMessageBox.warning(None,'QEsg',msgTxt)
            iface.messageBar().pushMessage("QWater", msgTxt, level=Qgis.Warning, duration=10)
            return False
        LayerLst=proj.mapLayersByName(ProjVar)
        if LayerLst:
            layer = proj.mapLayersByName(ProjVar)[0]
            return layer
        else:
            msgTxt=aForma+'='+ProjVar+QCoreApplication.translate('QWater',u' (Layer not found)')
            #QMessageBox.warning(None,'QEsg',msgTxt)
            iface.messageBar().pushMessage("QWater:", msgTxt, level=Qgis.Warning, duration=10)
            return False