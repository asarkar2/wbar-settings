#!/usr/bin/env python3

# Lisence: GPLv3 or later version.

import os
import sys
from PyQt5.QtWidgets import (QHBoxLayout, QVBoxLayout, QFileDialog, QLabel,
    QSpinBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFontDatabase

# File Dialog with preview for images selected
# https://stackoverflow.com/questions/47599170/qfiledialog-preview
class ImageDialogPreview(QFileDialog):

    def __init__(self, imagePath = None, *args, **kwargs):

        QFileDialog.__init__(self, *args, **kwargs)

        self.setOption(QFileDialog.DontUseNativeDialog, True)

        vbox = QVBoxLayout()

        self.setFixedSize(self.width() + 250, self.height())

        self.mpPreview = QLabel("Preview", self)
        self.mpPreview.setFixedSize(250, 250)
        self.mpPreview.setAlignment(Qt.AlignCenter)
        self.mpPreview.setObjectName("labelPreview")
        vbox.addWidget(self.mpPreview)

        vbox.addStretch()

        self.layout().addLayout(vbox, 1, 3, 1, 1)

        self.currentChanged.connect(self.onChange)
        self.fileSelected.connect(self.onFileSelected)
#         self.filesSelected.connect(self.onFilesSelected)

        self._fileSelected = None
#         self._filesSelected = None

        if imagePath:
            self.onChange(imagePath)

    def onChange(self, path):

        pixmap = QPixmap(path)

        if(pixmap.isNull()):
            self.mpPreview.setText("Preview")
        else:
            self.mpPreview.setPixmap(pixmap.scaled(self.mpPreview.width(), 
                self.mpPreview.height(), Qt.KeepAspectRatio, 
                Qt.SmoothTransformation))

    def onFileSelected(self, file):
        self._fileSelected = file

    def getFileSelected(self):
        return self._fileSelected


class FontDialogPreview(QFileDialog):

    def __init__(self, fontPath, fontSize, fontSizeMin, fontSizeMax, 
                 *args, **kwargs):

        QFileDialog.__init__(self, *args, **kwargs)

        self.setOption(QFileDialog.DontUseNativeDialog, True)

        self.fontSizeMin = fontSizeMin
        self.fontSizeMax = fontSizeMax
        self.fontPath = fontPath
        self.fontSize = fontSize
        self.previewText = 'AaBbYyZz'

        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        vbox.addLayout(hbox)

        self.setFixedSize(self.width() + 250, self.height())

        fontSizeLabel = QLabel('Font Size:')
        hbox.addWidget(fontSizeLabel)

        hbox.addStretch()

        self.fontSizeSpinBoxDlg = QSpinBox()
        self.fontSizeSpinBoxDlg.setToolTip('Font size')
        self.fontSizeSpinBoxDlg.setRange(self.fontSizeMin, self.fontSizeMax)
        self.fontSizeSpinBoxDlg.setValue(self.fontSize)
        self.fontSizeSpinBoxDlg.valueChanged.connect(self.onSizeSelected)
        hbox.addWidget(self.fontSizeSpinBoxDlg)

        self.fontPreviewDlg = QLabel(self.previewText)   
        self.fontPreviewDlg.setFixedSize(250, 250)
        self.fontPreviewDlg.setAlignment(Qt.AlignCenter)
        vbox.addWidget(self.fontPreviewDlg)

        vbox.addStretch()

        self.layout().addLayout(vbox, 1, 3, 1, 1)

        self.currentChanged.connect(self.onChange)
        self.fileSelected.connect(self.onFileSelected)

        if fontPath:
            self.onChange(fontPath)

    def _getDatabaseFont(self, fntPth, size):

        db = QFontDatabase()
        fontId = db.addApplicationFont(fntPth)
        family = db.applicationFontFamilies(fontId)[0]
        styles = db.styles(family)

        # Check if the style is part of the name or not.
        # If yes, then use that style, otherwise use 'Regular'
        fontfile = os.path.basename(fntPth)
        matchFound = False
        for style in styles:
            s = style.replace(' ','')  # Delete the space in style
            if s in fontfile:
                matchFound = True
                break
        
        if matchFound:
            font = db.font(family, style, size)
        else:
            font = db.font(family, 'Regular', size)

        return font

    def onChange(self, fontPath):
        
        if os.path.isfile(fontPath):
            self.fontSize = self.fontSizeSpinBoxDlg.value()            
            self.font = self._getDatabaseFont(fontPath, self.fontSize)
            self.fontPreviewDlg.setFont(self.font)

    def onFileSelected(self, file):
        self.fontPath = file

    def onSizeSelected(self, sz):
        self.fontSize = sz

        self.font = self.fontPreviewDlg.font()
        self.font.setPointSize(self.fontSize)
        self.fontPreviewDlg.setFont(self.font)

    def getFont(self):
        return self.font, self.fontPath 

