#!/usr/bin/env python3

# Lisence: GPLv3 or later version.

import re
import os
import sys
from PyQt5.QtWidgets import (QApplication, QDialog, QWidget, QVBoxLayout, 
    QHBoxLayout, QPushButton, QTabWidget, QTableWidget, QTableWidgetItem, 
    QFormLayout, QComboBox, QSpinBox, QDoubleSpinBox, QCheckBox,
    QFrame, QColorDialog, QLabel, QLineEdit, QFileDialog, QMessageBox, 
    QStatusBar, QDialogButtonBox)
from PyQt5.QtCore import QSettings, Qt
from PyQt5.QtGui import (QIcon, QPixmap, QColor, QPalette)
from filedialogpreview import FontDialogPreview, ImageDialogPreview

class SelectIcon(QDialog):
    """Main Window."""

    def __init__(self, window_icon_path, inputDict = None, *args, **kwargs):

        """Initializer."""
        super(SelectIcon, self).__init__(*args, **kwargs)

        self.window_title = 'Select Icon'
        self.setWindowTitle(self.window_title)
        
        self.window_icon_path = window_icon_path
        self.setWindowIcon(QIcon(self.window_icon_path))

        self.inputDict = inputDict
        self.iconsDirecDefault = '/usr/share/icons'

        self.minWidth = 300
        self.minHeight = 135

        self.setMinimumWidth(self.minWidth)
        self.setMinimumHeight(self.minHeight)

        self.vbox = QVBoxLayout()
        self.setLayout(self.vbox)

        self._createForm()
        self._createButtons()

    def _createForm(self):

        form = QFormLayout()
        self.vbox.addLayout(form)

        # Title
        self.titleEdit = QLineEdit()
        if self.inputDict:
            self.titleEdit.setText(self.inputDict['title'])
            self.titleEdit.setCursorPosition(0)
        form.addRow('Title:', self.titleEdit)
        # Title

        # Icon
        iconHBox = QHBoxLayout()

        self.iconEdit = QLineEdit()
        if self.inputDict:
            self.iconEdit.setText(self.inputDict['icon'])
            self.iconEdit.setCursorPosition(0)
        iconHBox.addWidget(self.iconEdit)

        iconBtn = QPushButton('...')
        iconBtn.setToolTip('Select icon')
        iconBtn.setFixedSize(24,24)
        iconBtn.clicked.connect(self.iconBtnClicked)
        iconHBox.addWidget(iconBtn)

        form.addRow('Icon:', iconHBox)
        # Icon

        # Command
        commandHBox = QHBoxLayout()

        self.commandEdit = QLineEdit()
        if self.inputDict:
            self.commandEdit.setText(self.inputDict['command'])
            self.commandEdit.setCursorPosition(0)
        commandHBox.addWidget(self.commandEdit)

        commandBtn = QPushButton('...')
        commandBtn.setToolTip('Select command')
        commandBtn.setFixedSize(24,24)
        commandBtn.clicked.connect(self.commandBtnClicked)
        commandHBox.addWidget(commandBtn)

        form.addRow('Command:', commandHBox)        
        # Command

    def iconBtnClicked(self):

        currentImage = self.iconEdit.text()
        
        imageSelectDialog = ImageDialogPreview(currentImage)
        imageSelectDialog.setWindowTitle('Select Image')
        imageSelectDialog.setDirectory(self.iconsDirecDefault)
        imageSelectDialog.setNameFilters(["Image Files (*.png *.jpg *.jpeg)"])
        
        imageSelectDialog.setFileMode(QFileDialog.ExistingFile)

        if currentImage and os.path.exists(currentImage):
            imageSelectDialog.selectFile(currentImage)

        if imageSelectDialog.exec_() == ImageDialogPreview.Accepted:
            iconSelected = imageSelectDialog.getFileSelected()
            self.iconEdit.setText(iconSelected)

        return        

    def commandBtnClicked(self):

        commandSelectDialog = QFileDialog(self, "Select Command",
            "","All Files (*.*)")
        commandSelectDialog.setFileMode(QFileDialog.ExistingFile)

        if commandSelectDialog.exec_() == QFileDialog.Accepted:
            commandSelected = commandSelectDialog.selectedFiles()[0]
            self.commandEdit.setText(commandSelected)

        return

    def _createButtons(self):
        buttonBox = QDialogButtonBox(self)
        buttonBox.setStandardButtons(QDialogButtonBox.Ok |
                                     QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.close)

        self.vbox.addWidget(buttonBox)

    def accept(self): 

        title = self.titleEdit.text()
        icon = self.iconEdit.text()
        command = self.commandEdit.text()

        if title and icon and command:    

            self._iconDict = {
                'title': title,
                'icon': icon,
                'command': command,
            }

            super(SelectIcon,self).accept()

        else:

            error_dlg = QMessageBox(QMessageBox.Critical, "Error", 
                "<b>Some fields are empty</b>", QMessageBox.Ok)
            error_dlg.setWindowIcon(QIcon(self.window_icon_path))
            error_dlg.setInformativeText("The values are not valid values.")
            error_dlg.exec_()

            return

    def get_output(self):
        return self._iconDict


# https://www.geeksforgeeks.org/pyqt5-how-to-add-separator-in-status-bar/
class HLine(QFrame):

    # A simple Horizontal line
    def __init__(self):
  
        super(HLine, self).__init__()
        self.setFrameShape(self.HLine|self.Sunken)


# https://www.geeksforgeeks.org/pyqt5-how-to-add-separator-in-status-bar/
class VLine(QFrame):

    # A simple Vertical line
    def __init__(self):
  
        super(VLine, self).__init__()
        self.setFrameShape(self.VLine|self.Sunken)


class WbarDialog(QDialog):
    """Main Window."""

    def __init__(self, wbarFile = None, *args, **kwargs):
        """Initializer."""
        super(WbarDialog, self).__init__(*args, **kwargs)

        wbarFileDefault = os.path.join(os.environ['HOME'], '.wbar') 

        if wbarFile:
            self.wbarFile = wbarFile
        else:
            self.wbarFile = wbarFileDefault

        self.window_title = 'WBar Settings'
        self.setWindowTitle(self.window_title)

        script_dir = os.path.dirname(os.path.realpath(__file__))
        self.icon_dir = os.path.join(script_dir, 'icons')
        self.window_icon_path = os.path.join(self.icon_dir, 'wbar.png')
        self.setWindowIcon(QIcon(self.window_icon_path))

        # Window size
        self.minWindowWidth = 400
        self.minWindowHeight = 400
        
        # Default widget (like buttons) width
        self.widgetWidth = 80
        self.widgetHeight = 24

        # StatusBar timout 
        self.timeout = 5000

        # Preferences
        self.fontPathDefault = (
        '/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf')
        self.fontExts = ['.ttf', '.otf']
        self.fontSearchPath = '/usr/share/fonts'
        self.fontSizeMin = 6
        self.fontSizeMax = 96
        self.fontSizeDefault = 12
        self.imageDirecDefault = '/usr/share/pixmaps'
        self.barImageDefault = '/usr/share/pixmaps/wbar/dock.png'
        self.iconPressed = True
        self.runOverDesktop = True
        self.verticalBar = True
        self.disableFontRender = True
        self.screenPosition = True
        self.screenPositionValue = 'right'
        self.iconsGrowth = False
        self.borderOffset = False
        self.borderOffsetValue = 0
        self.noReload = False       
        # Preferences

        # Effects
        self.iconSizesAll = [16, 24, 32, 48, 64, 72, 96, 128]
        self.iconSizeDefault = 32
        self.iconDistDefault = 5
        self.iconAnimDefault = 3
        self.zoomFactorDefault = 1.8
        self.jumpFactorDefault = 0.9
        self.doubleClickDefault = 250
        self.barAlfaDefault = 23
        self.barUnfocusAlfaDefault = 84
        self.colorFilterDict = {
            '0': 'none',
            '1': 'hovered',
            '2': 'others',
            '3': 'all'
        }
        self.colorFilterModeDefault = self.colorFilterDict['0'] 
        self.colorFilterDefault = '#ff00c800'
        self.colorFilterUser = self.colorFilterDefault
        self.lightGray = '#32989898'
        # Effects

        self.setMinimumWidth(self.minWindowWidth)
        self.setMinimumHeight(self.minWindowHeight)

        self.wbarConfig = {}
        self.listIcons = []

        self.vbox = QVBoxLayout()
        self.setLayout(self.vbox)

        self.settings = QSettings('wbar','window')

        try:
            self.resize(self.settings.value('windowSize'))
            self.move(self.settings.value('windowPosition'))
        except:
            pass

        # Create the widgets.
        self._createTabWidgets()
        self._createIconsTab()
        self._createPreferencesTab()
        self._createEffectsTab()
        self._createButtons()
        self._createStatusBar()

        # Upload the config file, if it exists
        if os.path.exists(self.wbarFile):

            self.wbarConfig, self.listIcons = self.readConfig(self.wbarFile)
            self.updateTable()
            self.iconTable.selectRow(0)
            self.updateWbarConfig()
            self.updatePreferences()
            self.updateEffects()

    def updateWbarConfig(self):
    
        # Update background image
        self.barImageEdit.setText(self.wbarConfig['icon'])
        
        # Update font path
        fontPathNoExt = os.path.dirname(self.wbarConfig['title']) 
        
        for ext in self.fontExts:
            filePath = fontPathNoExt + ext
            if os.path.exists(filePath):
                self.fontPathEdit.setText(filePath)
                break
        
        # Update font size
        fontSize = int(os.path.basename(self.wbarConfig['title']))
        self.fontSizeSpinBox.setValue(fontSize)

    def updatePreferences(self):

        command = self.wbarConfig['command'] 

        self.updateCheckBox(command, '--bpress', self.iconPressedCheckBox)

        self.updateCheckBox(command, '--above-desk', 
            self.runOverDesktopCheckBox)
        
        self.updateCheckBox(command, '--vbar', self.verticalBarCheckBox)

        self.updateCheckBox(command, '--nofont', 
            self.disableFontRenderCheckBox)

        self.updateCheckBox(command, '--grow', self.iconsGrowthCheckBox)
        
        self.updateCheckBox(command, '--noreload', self.noReloadCheckBox)

        self.updateComboBox(command, '--pos', self.screenPositionCheckBox, 
            self.screenPositionComboBox)

        self.updateSpinBox(command, '--offset', self.borderOffsetCheckBox, 
            self.borderOffsetSpinBox)

    def updateEffects(self):
        
        command = self.wbarConfig['command']

        self.updateComboBox(command, '--isize', self.iconSizeCheckBox, 
            self.iconSizeComboBox)

        self.updateSpinBox(command, '--idist', self.iconDistCheckBox, 
            self.iconDistSpinBox)

        self.updateSpinBox(command, '--nanim', self.iconAnimCheckBox, 
            self.iconAnimSpinBox)
        
        self.updateDoubleSpinBox(command, '--zoomf', self.zoomFactorCheckBox, 
            self.zoomFactorDSpinBox)

        self.updateDoubleSpinBox(command, '--jumpf', self.jumpFactorCheckBox, 
            self.jumpFactorDSpinBox)

        self.updateSpinBox(command, '--dblclk', self.doubleClickCheckBox, 
            self.doubleClickSpinBox)

        self.updateSpinBox(command, '--balfa', self.barAlfaCheckBox, 
            self.barAlfaSpinBox)

        self.updateSpinBox(command, '--falfa', self.barUnfocusAlfaCheckBox, 
            self.barUnfocusAlfaSpinBox)

        self.updateComboBoxDict(command, '--filter', 
            self.colorFilterModeCheckBox, self.colorFilterModeComboBox)

        self.updateColorButton(command, '--fc', self.colorFilterCheckBox, 
            self.colorFilterBtn)

    def updateCheckBox(self, cmd, text, checkBox):
        
        if text in cmd:
            checkBox.setChecked(True)
        else:
            checkBox.setChecked(False)

    def updateComboBox(self, cmd, text, checkBox, comboBox):

        if text in cmd:
            checkBox.setChecked(True)
            value = re.sub('.*' + text + ' ', '', cmd)
            value = re.sub(' .*','', value)
            comboBox.setCurrentText(value)
        else:
            checkBox.setChecked(False)

    def updateComboBoxDict(self, cmd, text, checkBox, comboBox):

        if text in cmd:
            checkBox.setChecked(True)
            key = re.sub('.*' + text + ' ', '', cmd)
            key = re.sub(' .*','', key)
            value = self.filterColorDict[key]
            comboBox.setCurrentText(value)
        else:
            checkBox.setChecked(False)

    def updateSpinBox(self, cmd, text, checkBox, spinBox):
        
        if text in cmd:
            checkBox.setChecked(True)
            value = re.sub('.*' + text + ' ', '', cmd)
            value = int(re.sub(' .*','', value))
            spinBox.setValue(value)
        else:
            checkBox.setChecked(False)

    def updateDoubleSpinBox(self, cmd, text, checkBox, doubleSpinBox):

        if text in cmd:
            checkBox.setChecked(True)
            value = re.sub('.*' + text + ' ', '', cmd)
            value = float(re.sub(' .*', '', value))
            doubleSpinBox.setValue(value)
        else:
            checkBox.setChecked(False)

    def updateColorButton(self, cmd, text, checkBox, pushButton):

        if text in cmd:
            checkBox.setChecked(True)
            value = re.sub('.*' + text + ' ', '', cmd)
            value = re.sub(' .*', '', value)
            value = re.sub("'", "", value)
            value = re.sub('"', '', value)
            value = re.sub('^0x', '#', value)
            pushButton.setStyleSheet("background-color: %s" % value)
            self.colorFilterUser = value
        else:
            checkBox.setChecked(False)

    def readConfig(self, confFl):

        ilst = []

        with open(confFl, 'r') as fh:

            for line in fh:
                line = line.strip()

                if line.startswith('#'):
                    # Avoid comment lines
                    continue

                else:
                    
                    # For non-comment lines
                    if 'i: ' in line:
                        dct = {}
                        dct['icon'] = line.replace('i: ', '')

                    elif 'c: ' in line:
                        dct['command'] = line.replace('c: ', '')

                    elif 't: ' in line:
                        dct['title'] = line.replace('t: ', '')

                    else:
                        if dct:
                            ilst.append(dct)
                            dct = None

        # Separate the 1st item in the list.
        wbConf = ilst.pop(0)

        return wbConf, ilst

    def saveConfig(self):
       
        # Write to config file
        fh = open(self.wbarFile, 'w') 
        
        # Dock background image
        fh.write("i: " + self.barImageEdit.text() + "\n")

        # Preferences and Effects
        cmd = self.getCommand()
        fh.write("c: " + cmd + "\n")
    
        # Font path and size
        fontPathSize = self.getFontPathSize()
        fh.write("t: " + fontPathSize + "\n")
        fh.write('\n')

        # Icons
        self.writeTable(fh)

        fh.close()

        self.statusBar.showMessage("Saved in '%s'. " % self.wbarFile
            + "Right-click on wbar to reload." , self.timeout)

    # Preferences and Effects
    def getCommand(self):

        cmd = 'wbar'
        
        # Preferences
        cmd = self.writeCheckBox(cmd, '--bpress', self.iconPressedCheckBox)
        
        cmd = self.writeCheckBox(cmd, '--above-desk', 
            self.runOverDesktopCheckBox)
        
        cmd = self.writeCheckBox(cmd, '--vbar', self.verticalBarCheckBox)
        
        cmd = self.writeCheckBox(cmd, '--nofont', 
            self.disableFontRenderCheckBox)
        
        cmd = self.writeCheckBox(cmd, '--grow', self.iconsGrowthCheckBox)
        
        cmd = self.writeCheckBox(cmd, '--noreload', self.noReloadCheckBox)
        
        cmd = self.writeComboBox(cmd, '--pos', self.screenPositionCheckBox,
            self.screenPositionComboBox)
        
        cmd = self.writeSpinBox(cmd, '--offset', self.borderOffsetCheckBox,
            self.borderOffsetSpinBox)
        # Preferences

        # Effects
        cmd = self.writeComboBox(cmd, '--isize', self.iconSizeCheckBox,
            self.iconSizeComboBox)

        cmd = self.writeSpinBox(cmd, '--idist', self.iconDistCheckBox, 
            self.iconDistSpinBox)

        cmd = self.writeSpinBox(cmd, '--nanim', self.iconAnimCheckBox, 
            self.iconAnimSpinBox)

        cmd = self.writeDoubleSpinBox(cmd, '--zoomf', self.zoomFactorCheckBox, 
            self.zoomFactorDSpinBox)

        cmd = self.writeDoubleSpinBox(cmd, '--jumpf', self.jumpFactorCheckBox, 
            self.jumpFactorDSpinBox)

        cmd = self.writeSpinBox(cmd, '--dblclk', self.doubleClickCheckBox, 
            self.doubleClickSpinBox)

        cmd = self.writeSpinBox(cmd, '--balfa', self.barAlfaCheckBox, 
            self.barAlfaSpinBox)

        cmd = self.writeSpinBox(cmd, '--falfa', 
            self.barUnfocusAlfaCheckBox, self.barUnfocusAlfaSpinBox)

        cmd = self.writeComboBoxDict(cmd, '--filter', 
            self.colorFilterModeCheckBox, self.colorFilterModeComboBox)

        cmd = self.writeColorButton(cmd, '--fc', self.colorFilterCheckBox, 
            self.colorFilterBtn)
        # Effects

        return cmd

    def writeCheckBox(self, cmd, text, checkBox):
        string = ' ' + text if checkBox.isChecked() else ''
        cmd = cmd + string
        return cmd

    def writeComboBox(self, cmd, text, checkBox, comboBox):
        
        if checkBox.isChecked():
            string = ' ' + text + ' ' + comboBox.currentText()
        else:
            string = ''

        cmd = cmd + string
        return cmd

    def writeComboBoxDict(self, cmd, text, checkBox, comboBox):
        
        key_list = list(self.colorFilterDict.keys())
        value_list = list(self.colorFilterDict.values())
        
        if checkBox.isChecked():
            value = comboBox.currentText()
            position = value_list.index(value)
            key = key_list[position]
            string = ' ' + text + ' ' + key
        else:
            string = ''

        cmd = cmd + string
        return cmd

    def writeSpinBox(self, cmd, text, checkBox, spinBox):
        
        if checkBox.isChecked():
            string = ' ' + text + ' ' + str(spinBox.value())
        else:
            string = ''

        cmd = cmd + string
        return cmd

    def writeDoubleSpinBox(self, cmd, text, checkBox, doubleSpinBox):
        
        if checkBox.isChecked():
            string = ' ' + text + ' ' + str(doubleSpinBox.value())
        else:
            string = ''

        cmd = cmd + string
        return cmd

    def writeColorButton(self, cmd, text, checkBox, pushButton):
        
        if checkBox.isChecked():
            color = pushButton.palette().color(QPalette.Window).name(
                QColor.HexArgb)
            color = re.sub('#', '0x', color)
            string = ' ' + text + ' ' + color
        else:
            string = ''

        cmd = cmd + string
        return cmd

    def getFontPathSize(self):
        
        fntPthSz = os.path.join(
            os.path.splitext(self.fontPathEdit.text())[0], 
            str(self.fontSizeSpinBox.value()))

        return fntPthSz

    def writeTable(self, fh):
        
        n = len(self.listIcons)
        for row in range(n):
            
            fh.write('i: ' + self.listIcons[row]['icon'] + '\n')
            fh.write('c: ' + self.listIcons[row]['command'] + '\n')
            fh.write('t: ' + self.listIcons[row]['title'] + '\n')
            fh.write('\n')

    def _createTabWidgets(self):
        
        self.tabs = QTabWidget()
        self.vbox.addWidget(self.tabs)

    def _createIconsTab(self):
        
        iconsWidget = QWidget()
        self.tabs.addTab(iconsWidget, "Icons")

        self.iconsVBox = QVBoxLayout()
        iconsWidget.setLayout(self.iconsVBox)

        self._createIconsHBox()
        self._createIconsTable()

    def _createIconsHBox(self):
        
        iconsHBox = QHBoxLayout()
        self.iconsVBox.addLayout(iconsHBox)

        self.addIconBtn = QPushButton(QIcon(os.path.join(self.icon_dir, 
            "document-new.png")), "")
        self.addIconBtn.setFixedSize(24,24)
        self.addIconBtn.setToolTip("Add Icons")
        self.addIconBtn.clicked.connect(self.addIconBtnClicked)        
        iconsHBox.addWidget(self.addIconBtn)

        self.editIconBtn = QPushButton(QIcon(os.path.join(self.icon_dir, 
            "gtk-edit.png")), "")
        self.editIconBtn.setFixedSize(24,24)
        self.editIconBtn.setToolTip("Edit Icons")
        self.editIconBtn.clicked.connect(self.editIconBtnClicked)        
        iconsHBox.addWidget(self.editIconBtn)

        self.delIconBtn = QPushButton(QIcon(os.path.join(self.icon_dir, 
            "gtk-close.png")), "")
        self.delIconBtn.setFixedSize(24,24)
        self.delIconBtn.setToolTip("Delete Icons")
        self.delIconBtn.clicked.connect(self.delIconBtnClicked)        
        iconsHBox.addWidget(self.delIconBtn)

        iconsHBox.addWidget(VLine())

        self.topIconBtn = QPushButton(QIcon(os.path.join(self.icon_dir, 
            "go-top.png")), "")
        self.topIconBtn.setFixedSize(24,24)
        self.topIconBtn.setToolTip("Move icons to the top")
        self.topIconBtn.clicked.connect(self.topIconBtnClicked)        
        iconsHBox.addWidget(self.topIconBtn)

        self.upIconBtn = QPushButton(QIcon(os.path.join(self.icon_dir, 
            "go-up.png")), "")
        self.upIconBtn.setFixedSize(24,24)
        self.upIconBtn.setToolTip("Move icons up")
        self.upIconBtn.clicked.connect(self.upIconBtnClicked)        
        iconsHBox.addWidget(self.upIconBtn)

        self.downIconBtn = QPushButton(QIcon(os.path.join(self.icon_dir, 
            "go-down.png")), "")
        self.downIconBtn.setFixedSize(24,24)
        self.downIconBtn.setToolTip("Move icons down")
        self.downIconBtn.clicked.connect(self.downIconBtnClicked)        
        iconsHBox.addWidget(self.downIconBtn)

        self.bottomIconBtn = QPushButton(QIcon(os.path.join(self.icon_dir, 
            "go-bottom.png")), "")
        self.bottomIconBtn.setFixedSize(24,24)
        self.bottomIconBtn.setToolTip("Move icons to the bottom")
        self.bottomIconBtn.clicked.connect(self.bottomIconBtnClicked)        
        iconsHBox.addWidget(self.bottomIconBtn)

        iconsHBox.addStretch()

    def _createIconsTable(self):

        n = len(self.listIcons)

        self.iconTable = QTableWidget()
        self.iconTable.setRowCount(n)
        self.iconTable.setColumnCount(3)

        self.iconTable.setHorizontalHeaderLabels(["Icon", "Title", "Command"])
        header = self.iconTable.horizontalHeader()
        
        # Resize the 1st column
        header.resizeSection(0, 48)
        
        # Stretch the last column to fit the window
        header.setStretchLastSection(True)
        
        # Hide the row number
        self.iconTable.verticalHeader().setVisible(False)

        # Select the whole row when instead of a single cell
        self.iconTable.setSelectionBehavior(QTableWidget.SelectRows)

        # Do not highlight the headers
        self.iconTable.horizontalHeader().setHighlightSections(False)

        # If the text changes
        self.iconTable.itemChanged.connect(self.itemTextChanged)

        # Add the table widget to the vertical layout
        self.iconsVBox.addWidget(self.iconTable)

    # If cell value have changed, then update them on the dictionary
    def itemTextChanged(self, item):

        row = item.row()
        col = item.column()

        # Get the 'key' = column header
        key = self.iconTable.horizontalHeaderItem(col).text().lower()

        # Get the 'value' = cell value from the table
        value = str(self.iconTable.item(row,col).text())

        # Update the dictionary
        self.listIcons[row][key] = value

    def updateTable(self):

        n = len(self.listIcons)

        # Block the signals so that any editing doesn't call any signal
        self.iconTable.blockSignals(True)

        # Clears the table
        self.iconTable.setRowCount(0) 

        for row in range(0,n):

            self.iconTable.insertRow(row)

            for col in range(3):
                
                # Get the column header in lowercase
                colheader = self.iconTable.horizontalHeaderItem(
                            col).text().lower()                

                if colheader == 'icon':

                    px = QPixmap(self.listIcons[row][colheader])
                    label = QLabel()
                    label.setPixmap(px.scaled(30, 30, Qt.KeepAspectRatio,
                        Qt.SmoothTransformation))
                    label.setAlignment(Qt.AlignCenter)
                    self.iconTable.setCellWidget(row, col, label)

                else:

                    itemString = self.listIcons[row][colheader]
                    item = QTableWidgetItem(itemString)
                    
                    self.iconTable.setItem(row, col, item) 

        self.iconTable.blockSignals(False)

    def addIconBtnClicked(self):

        dlg = SelectIcon(self.window_icon_path)
        
        if dlg.exec_() == SelectIcon.Accepted:
            iconDict = dlg.get_output()
            self.listIcons.append(iconDict)
            self.updateTable()
            n = len(self.listIcons)
            self.iconTable.selectRow(n-1)

    def editIconBtnClicked(self):

        row = self.iconTable.currentRow()
        
        if row >= 0:
            
            inputDict = self.listIcons[row] 
            dlg = SelectIcon(self.window_icon_path, inputDict)

            if dlg.exec_() == SelectIcon.Accepted:
                iconDict = dlg.get_output()

                # Remove the row and insert the updated dictionary
                del(self.listIcons[row])
                self.listIcons.insert(row, iconDict)

                self.updateTable()
                self.iconTable.selectRow(row)
        
    def delIconBtnClicked(self):
        
        row = self.iconTable.currentRow()
        n = len(self.listIcons)
        
        if row >= 0:

            rtn = self.delConfirmation(row)
            if rtn == QMessageBox.Ok:

                del(self.listIcons[row])
                self.updateTable()

                if row == n-1:
                    # If the last row have been selected then select the one
                    # above it
                    self.iconTable.selectRow(row-1)
                else:
                    # Select the same row once the row has been removed
                    self.iconTable.selectRow(row)

            else:
                return

    def delConfirmation(self, row):

        title = self.listIcons[row]['title']

        delDlg = QMessageBox()
        delDlg.setWindowIcon(QIcon(self.window_icon_path))
        delDlg.setIcon(QMessageBox.Warning)
        delDlg.setWindowTitle("Delete icon?")
        delDlg.setText("Delete the icon titled <b>'%s'</b>?" % title)
#         delDlg.setInformativeText("Your changes will be lost if you" 
#             + " delete it.")
        delDlg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        rtn = delDlg.exec_()
        return rtn

    def topIconBtnClicked(self):
        
        row = self.iconTable.currentRow()
        
        # Change only if it is not the first row
        if row != 0:
            tmpDict = self.listIcons.pop(row)
            self.listIcons.insert(0, tmpDict)
            self.updateTable()
            self.iconTable.selectRow(0)

    def upIconBtnClicked(self):

        row = self.iconTable.currentRow()

        # Change only if it is not the first row
        if row != 0:
            tmpDict = self.listIcons.pop(row)
            self.listIcons.insert(row-1, tmpDict)
            self.updateTable()
            self.iconTable.selectRow(row-1)

    def downIconBtnClicked(self):

        row = self.iconTable.currentRow()
        n = len(self.listIcons)
        
        # Change only if it is not the last row
        if row != n-1:
            tmpDict = self.listIcons.pop(row)
            self.listIcons.insert(row+1, tmpDict)
            self.updateTable()
            self.iconTable.selectRow(row+1)

    def bottomIconBtnClicked(self):

        row = self.iconTable.currentRow()
        n = len(self.listIcons)
        
        # Change only if it is not the last row
        if row != n-1:
            tmpDict = self.listIcons.pop(row)
            self.listIcons.append(tmpDict)
            self.updateTable()
            self.iconTable.selectRow(n-1)

    def _createPreferencesTab(self):
        
        preferencesWidget = QWidget()
        self.tabs.addTab(preferencesWidget, "Preferences")

        vBoxLayout = QVBoxLayout()
        preferencesWidget.setLayout(vBoxLayout)

        # Font
        fontHBox = QHBoxLayout()

        fontSelectBtn = QPushButton('Font')
        fontSelectBtn.setToolTip('Select font')
        fontSelectBtn.clicked.connect(self.fontSelectBtnClicked)
        fontHBox.addWidget(fontSelectBtn)

        self.fontPathEdit = QLineEdit()
        self.fontPathEdit.setToolTip('Font path')
        self.fontPathEdit.setText(self.fontPathDefault)
        fontHBox.addWidget(self.fontPathEdit)
        
        self.fontSizeSpinBox = QSpinBox()
        self.fontSizeSpinBox.setToolTip('Font size')
        self.fontSizeSpinBox.setRange(self.fontSizeMin, self.fontSizeMax)
        self.fontSizeSpinBox.setValue(self.fontSizeDefault)
        fontHBox.addWidget(self.fontSizeSpinBox)

        vBoxLayout.addLayout(fontHBox)
        # Font

        # Dock background image
        barImageHBox = QHBoxLayout()
        
        barImageBtn = QPushButton('Bar Image')
        barImageBtn.setToolTip('Select dock background image')
        barImageBtn.clicked.connect(self.barImageBtnClicked)
        barImageHBox.addWidget(barImageBtn)

        self.barImageEdit = QLineEdit()
        self.barImageEdit.setToolTip('Dock background image')
        self.barImageEdit.setText(self.barImageDefault)
        barImageHBox.addWidget(self.barImageEdit)

        vBoxLayout.addLayout(barImageHBox)
        # Dock background image

        vBoxLayout.addWidget(HLine())

        # Icons gets pressed
        self.iconPressedCheckBox = QCheckBox('Icon gets pressed')
        self.iconPressedCheckBox.setChecked(self.iconPressed)
        vBoxLayout.addWidget(self.iconPressedCheckBox)
        # Icons gets pressed

        # Run over the desktop
        self.runOverDesktopCheckBox = QCheckBox('Run over the desktop')
        self.runOverDesktopCheckBox.setChecked(self.runOverDesktop)
        vBoxLayout.addWidget(self.runOverDesktopCheckBox)
        # Run over the desktop

        # Vertical bar
        self.verticalBarCheckBox = QCheckBox('Vertical bar')
        self.verticalBarCheckBox.setChecked(self.verticalBar)
        vBoxLayout.addWidget(self.verticalBarCheckBox)
        # Vertical bar

        # Disable font rendering
        self.disableFontRenderCheckBox = QCheckBox('Disable font rendering')
        self.disableFontRenderCheckBox.setChecked(self.disableFontRender)
        vBoxLayout.addWidget(self.disableFontRenderCheckBox)
        # Disable font rendering

        # Inverting icons growth 
        self.iconsGrowthCheckBox = QCheckBox('Inverting icons growth')
        self.iconsGrowthCheckBox.setChecked(self.iconsGrowth)
        vBoxLayout.addWidget(self.iconsGrowthCheckBox)        
        # Inverting icons growth 

        # No reload
        self.noReloadCheckBox = QCheckBox('No reload')
        self.noReloadCheckBox.setChecked(self.noReload)
        vBoxLayout.addWidget(self.noReloadCheckBox)        
        # No reload bar

        # Screen position
        screenPositionHBox = QHBoxLayout()

        self.screenPositionCheckBox = QCheckBox('Screen position')
        self.screenPositionCheckBox.setChecked(self.screenPosition)
        self.screenPositionCheckBox.stateChanged.connect(
            self.screenPositionToggled)

        self.screenPositionComboBox = QComboBox()
        self.screenPositionComboBox.addItems(['top', 'bottom', 'left', 
            'right', 'center', 'bot-right', 'bot-left', 'top-right', 
            'top-left'])
        self.screenPositionComboBox.setCurrentText(self.screenPositionValue)
        self.screenPositionComboBox.setEnabled(
            self.screenPositionCheckBox.isChecked())        
        self.screenPositionComboBox.setFixedSize(self.widgetWidth,
            self.widgetHeight)
        
        screenPositionHBox.addWidget(self.screenPositionCheckBox)
        screenPositionHBox.addWidget(self.screenPositionComboBox)

        vBoxLayout.addLayout(screenPositionHBox)
        # Screen position

        # Border offset
        borderOffsetHBox = QHBoxLayout()

        self.borderOffsetCheckBox = QCheckBox('Border offset')
        self.borderOffsetCheckBox.setChecked(self.borderOffset)
        self.borderOffsetCheckBox.stateChanged.connect(
            self.borderOffsetToggled)

        self.borderOffsetSpinBox = QSpinBox()
        self.borderOffsetSpinBox.setRange(0,30)
        self.borderOffsetSpinBox.setValue(self.borderOffsetValue)
        self.borderOffsetSpinBox.setEnabled(
            self.borderOffsetCheckBox.isChecked())        
        self.borderOffsetSpinBox.setFixedSize(self.widgetWidth,
            self.widgetHeight)

        borderOffsetHBox.addWidget(self.borderOffsetCheckBox)
        borderOffsetHBox.addWidget(self.borderOffsetSpinBox)

        vBoxLayout.addLayout(borderOffsetHBox)
        # Border offset

        vBoxLayout.addStretch()

    def fontSelectBtnClicked(self):
        
        fontFile = self.fontPathEdit.text()
        fontSize = self.fontSizeSpinBox.value()
        
        fontDialog = FontDialogPreview(fontFile, fontSize, 
            self.fontSizeMin, self.fontSizeMax)
        fontDialog.setWindowTitle('Select font')
        fontDialog.setFileMode(QFileDialog.ExistingFile)
        fontDialog.setDirectory(self.fontSearchPath)
        fontDialog.selectFile(fontFile)
        fontFilter = ('Font Files (' 
            + ' '.join(['*' + ext for ext in self.fontExts])
            + ')')
        fontDialog.setNameFilters([fontFilter])
#         fontDialog.setNameFilters(['Font Files (*.ttf *.otf)'])

        if fontDialog.exec_() == FontDialogPreview.Accepted:
            font, fontPath = fontDialog.getFont()
            self.fontPathEdit.setText(fontPath)
            self.fontSizeSpinBox.setValue(font.pointSize())

    def barImageBtnClicked(self):

        currentImage = self.barImageEdit.text()
        
        imageSelectDialog = ImageDialogPreview(currentImage)
        imageSelectDialog.setWindowTitle('Select Image')
        imageSelectDialog.setDirectory(self.imageDirecDefault)
        imageSelectDialog.setNameFilters(["Image Files (*.png *.jpg *.jpeg)"])
        imageSelectDialog.setFileMode(QFileDialog.ExistingFile)

        if currentImage and os.path.exists(currentImage):
            imageSelectDialog.selectFile(currentImage)

        if imageSelectDialog.exec_() == ImageDialogPreview.Accepted:
            path = imageSelectDialog.getFileSelected()
            self.barImageEdit.setText(path)

    def _createEffectsTab(self):

        effectsWidget = QWidget()
        self.tabs.addTab(effectsWidget, "Effects")

        vboxEffectsLayout = QVBoxLayout()
        effectsWidget.setLayout(vboxEffectsLayout)

        # iconSize
        self.iconSizeHBox = QHBoxLayout()
        self.iconSizeCheckBox = QCheckBox('Icon Size', self)
        self.iconSizeCheckBox.setChecked(True)
        self.iconSizeCheckBox.stateChanged.connect(self.iconSizeToggled)
        
        self.iconSizeComboBox = QComboBox()
        self.iconSizeComboBox.addItems(list(map(str,self.iconSizesAll)))
        self.iconSizeComboBox.setEnabled(self.iconSizeCheckBox.isChecked())
        self.iconSizeComboBox.setCurrentText(str(self.iconSizeDefault))
        self.iconSizeComboBox.setFixedSize(self.widgetWidth,
            self.widgetHeight)        

        self.iconSizeHBox.addWidget(self.iconSizeCheckBox)
        self.iconSizeHBox.addStretch()
        self.iconSizeHBox.addWidget(self.iconSizeComboBox)
        vboxEffectsLayout.addLayout(self.iconSizeHBox)
        # iconSize

        # iconDist
        self.iconDistHBox = QHBoxLayout()
        self.iconDistCheckBox = QCheckBox('Icon Distance', self)
        self.iconDistCheckBox.setChecked(True)
        self.iconDistCheckBox.stateChanged.connect(self.iconDistToggled)
        
        self.iconDistSpinBox = QSpinBox()
        self.iconDistSpinBox.setRange(1,10)
        self.iconDistSpinBox.setMaximumWidth(self.widgetWidth)
        self.iconDistSpinBox.setEnabled(self.iconDistCheckBox.isChecked())
        self.iconDistSpinBox.setValue(self.iconDistDefault)

        self.iconDistHBox.addWidget(self.iconDistCheckBox)
        self.iconDistHBox.addWidget(self.iconDistSpinBox)
        vboxEffectsLayout.addLayout(self.iconDistHBox)
        # iconDist

        # iconAnim
        self.iconAnimHBox = QHBoxLayout()
        self.iconAnimCheckBox = QCheckBox('Number of animated icons', self)
        self.iconAnimCheckBox.setChecked(True)
        self.iconAnimCheckBox.stateChanged.connect(self.iconAnimToggled)
        
        self.iconAnimSpinBox = QSpinBox()
        self.iconAnimSpinBox.setRange(1,5)
        self.iconAnimSpinBox.setMaximumWidth(self.widgetWidth)
        self.iconAnimSpinBox.setEnabled(self.iconAnimCheckBox.isChecked())
        self.iconAnimSpinBox.setValue(self.iconAnimDefault)

        self.iconAnimHBox.addWidget(self.iconAnimCheckBox)
        self.iconAnimHBox.addWidget(self.iconAnimSpinBox)
        vboxEffectsLayout.addLayout(self.iconAnimHBox)
        # iconAnim

        # zoomFactor
        self.zoomFactorHBox = QHBoxLayout()
        self.zoomFactorCheckBox = QCheckBox('Zoom factor', self)
        self.zoomFactorCheckBox.setChecked(True)
        self.zoomFactorCheckBox.stateChanged.connect(self.zoomFactorToggled)
        
        self.zoomFactorDSpinBox = QDoubleSpinBox()
        self.zoomFactorDSpinBox.setRange(0,2.5)
        self.zoomFactorDSpinBox.setSingleStep(0.1)
        self.zoomFactorDSpinBox.setDecimals(1)
        self.zoomFactorDSpinBox.setMaximumWidth(self.widgetWidth)
        self.zoomFactorDSpinBox.setEnabled(self.zoomFactorCheckBox.isChecked())
        self.zoomFactorDSpinBox.setValue(self.zoomFactorDefault)

        self.zoomFactorHBox.addWidget(self.zoomFactorCheckBox)
        self.zoomFactorHBox.addWidget(self.zoomFactorDSpinBox)
        vboxEffectsLayout.addLayout(self.zoomFactorHBox)
        # zoomFactor

        # jumpFactor
        self.jumpFactorHBox = QHBoxLayout()
        self.jumpFactorCheckBox = QCheckBox('Jump factor', self)
        self.jumpFactorCheckBox.setChecked(True)
        self.jumpFactorCheckBox.stateChanged.connect(self.jumpFactorToggled)
        
        self.jumpFactorDSpinBox = QDoubleSpinBox()
        self.jumpFactorDSpinBox.setRange(0,1.5)
        self.jumpFactorDSpinBox.setSingleStep(0.1)
        self.jumpFactorDSpinBox.setDecimals(1)
        self.jumpFactorDSpinBox.setMaximumWidth(self.widgetWidth)
        self.jumpFactorDSpinBox.setEnabled(self.jumpFactorCheckBox.isChecked())
        self.jumpFactorDSpinBox.setValue(self.jumpFactorDefault)

        self.jumpFactorHBox.addWidget(self.jumpFactorCheckBox)
        self.jumpFactorHBox.addWidget(self.jumpFactorDSpinBox)
        vboxEffectsLayout.addLayout(self.jumpFactorHBox)
        # jumpFactor

        # doubleClick
        self.doubleClickHBox = QHBoxLayout()
        self.doubleClickCheckBox = QCheckBox('Time for double click (ms)', 
            self)
        self.doubleClickCheckBox.setChecked(True)
        self.doubleClickCheckBox.stateChanged.connect(self.doubleClickToggled)
        
        self.doubleClickSpinBox = QSpinBox()
        self.doubleClickSpinBox.setRange(0,300)
        self.doubleClickSpinBox.setMaximumWidth(self.widgetWidth)
        self.doubleClickSpinBox.setEnabled(self.doubleClickCheckBox.isChecked())
        self.doubleClickSpinBox.setValue(self.doubleClickDefault)

        self.doubleClickHBox.addWidget(self.doubleClickCheckBox)
        self.doubleClickHBox.addWidget(self.doubleClickSpinBox)
        vboxEffectsLayout.addLayout(self.doubleClickHBox)
        # doubleClick

        # barAlfa
        self.barAlfaHBox = QHBoxLayout()
        self.barAlfaCheckBox = QCheckBox('Bar alpha level', self)
        self.barAlfaCheckBox.setChecked(True)
        self.barAlfaCheckBox.stateChanged.connect(self.barAlfaToggled)
        
        self.barAlfaSpinBox = QSpinBox()
        self.barAlfaSpinBox.setRange(0,100)
        self.barAlfaSpinBox.setMaximumWidth(self.widgetWidth)
        self.barAlfaSpinBox.setEnabled(self.barAlfaCheckBox.isChecked())
        self.barAlfaSpinBox.setValue(self.barAlfaDefault)

        self.barAlfaHBox.addWidget(self.barAlfaCheckBox)
        self.barAlfaHBox.addWidget(self.barAlfaSpinBox)
        vboxEffectsLayout.addLayout(self.barAlfaHBox)
        # barAlfa

        # barUnfocusAlfa
        self.barUnfocusAlfaHBox = QHBoxLayout()
        self.barUnfocusAlfaCheckBox = QCheckBox('Bar unfocussed alpha level',
            self)
        self.barUnfocusAlfaCheckBox.setChecked(True)
        self.barUnfocusAlfaCheckBox.stateChanged.connect(
            self.barUnfocusAlfaToggled)
        
        self.barUnfocusAlfaSpinBox = QSpinBox()
        self.barUnfocusAlfaSpinBox.setRange(0,100)
        self.barUnfocusAlfaSpinBox.setMaximumWidth(self.widgetWidth)
        self.barUnfocusAlfaSpinBox.setEnabled(
            self.barUnfocusAlfaCheckBox.isChecked())
        self.barUnfocusAlfaSpinBox.setValue(self.barUnfocusAlfaDefault)

        self.barUnfocusAlfaHBox.addWidget(self.barUnfocusAlfaCheckBox)
        self.barUnfocusAlfaHBox.addWidget(self.barUnfocusAlfaSpinBox)
        vboxEffectsLayout.addLayout(self.barUnfocusAlfaHBox)
        # barUnfocusAlfa

        # colorFilterMode
        self.colorFilterModeHBox = QHBoxLayout()
        self.colorFilterModeCheckBox = QCheckBox('Color filter mode', self)
        self.colorFilterModeCheckBox.setChecked(True)
        self.colorFilterModeCheckBox.stateChanged.connect(
            self.colorFilterModeToggled)
        
        self.colorFilterModeComboBox = QComboBox()
        self.colorFilterModeComboBox.setFixedSize(self.widgetWidth,
            self.widgetHeight)
        self.colorFilterModeComboBox.addItems(['none', 'hovered', 'others',
            'all'])
        self.colorFilterModeComboBox.setEnabled(
            self.colorFilterModeCheckBox.isChecked())
        self.colorFilterModeComboBox.setCurrentText(str(
            self.colorFilterModeDefault))

        self.colorFilterModeHBox.addWidget(self.colorFilterModeCheckBox)
        self.colorFilterModeHBox.addStretch()
        self.colorFilterModeHBox.addWidget(self.colorFilterModeComboBox)
        vboxEffectsLayout.addLayout(self.colorFilterModeHBox)
        # colorFilterMode

        # colorFilter
        self.colorFilterHBox = QHBoxLayout()
        self.colorFilterCheckBox = QCheckBox('Color filter', self)
        self.colorFilterCheckBox.setChecked(True)
        self.colorFilterCheckBox.stateChanged.connect(
            self.colorFilterToggled)

        self.colorFilterBtn = QPushButton("")
        self.colorFilterBtn.setFixedSize(self.widgetWidth, self.widgetHeight)
        self.colorFilterBtn.setStyleSheet("background-color: %s" 
            % self.colorFilterDefault)
        self.colorFilterBtn.clicked.connect(self.colorFilterBtnClicked)

        self.colorFilterHBox.addWidget(self.colorFilterCheckBox)
        self.colorFilterHBox.addWidget(self.colorFilterBtn)
        vboxEffectsLayout.addLayout(self.colorFilterHBox)
        # colorFilter

    def screenPositionToggled(self):
        self.screenPositionComboBox.setEnabled(
            self.screenPositionCheckBox.isChecked())

    def borderOffsetToggled(self):
        self.borderOffsetSpinBox.setEnabled(
            self.borderOffsetCheckBox.isChecked())

    def iconSizeToggled(self):
        self.iconSizeComboBox.setEnabled(self.iconSizeCheckBox.isChecked())

    def iconDistToggled(self):
        self.iconDistSpinBox.setEnabled(self.iconDistCheckBox.isChecked())

    def iconAnimToggled(self):
        self.iconAnimSpinBox.setEnabled(self.iconAnimCheckBox.isChecked())

    def zoomFactorToggled(self):
        self.zoomFactorDSpinBox.setEnabled(self.zoomFactorCheckBox.isChecked())

    def jumpFactorToggled(self):
        self.jumpFactorDSpinBox.setEnabled(self.jumpFactorCheckBox.isChecked())

    def doubleClickToggled(self):
        self.doubleClickSpinBox.setEnabled(self.doubleClickCheckBox.isChecked())

    def barAlfaToggled(self):
        self.barAlfaSpinBox.setEnabled(self.barAlfaCheckBox.isChecked())

    def barUnfocusAlfaToggled(self):
        self.barUnfocusAlfaSpinBox.setEnabled(
            self.barUnfocusAlfaCheckBox.isChecked())

    def colorFilterModeToggled(self):
        self.colorFilterModeComboBox.setEnabled(
            self.colorFilterModeCheckBox.isChecked())

    def colorFilterToggled(self):
        self.colorFilterBtn.setEnabled(
            self.colorFilterCheckBox.isChecked())

        if self.colorFilterCheckBox.isChecked():
            self.colorFilterBtn.setStyleSheet(
                'background-color: %s' % self.colorFilterUser)            
        else:
            self.colorFilterBtn.setStyleSheet(
                'background-color: %s' % self.lightGray)

    def colorFilterBtnClicked(self):

        colorDialog = QColorDialog()
        color = colorDialog.getColor(options = QColorDialog.ShowAlphaChannel)

        if color.isValid():
            self.colorFilterUser = color.name(QColor.HexArgb)
            self.colorFilterBtn.setStyleSheet(
                'background-color: %s' % self.colorFilterUser)
        return

    def _createButtons(self):
        
        hboxButtons = QHBoxLayout()

        hboxButtons.addStretch()

        self.aboutBtn = QPushButton(QIcon.fromTheme('help-about',
            QIcon(os.path.join(self.icon_dir, "about.png"))), "About")
        self.aboutBtn.clicked.connect(self.aboutBtnClicked)
        hboxButtons.addWidget(self.aboutBtn)

        self.closeBtn = QPushButton(QIcon.fromTheme('window-close', 
            QIcon(os.path.join(self.icon_dir, "application-exit"))), "Close")
        self.closeBtn.clicked.connect(self.close)
        hboxButtons.addWidget(self.closeBtn)

        self.saveBtn = QPushButton(QIcon(os.path.join(self.icon_dir, 
            "document-save.png")), "Save")
        self.saveBtn.clicked.connect(self.saveConfig)
        hboxButtons.addWidget(self.saveBtn)

        self.vbox.addLayout(hboxButtons)

    def aboutBtnClicked(self):
        QMessageBox.about(self, "About %s" % self.window_title,
            "<p>The <b>%s</b> is an editor " % self.window_title 
            + "for the wbar dock.</p>")

    # Re-define closeEvent function to save the file before closing the window
    def closeEvent(self, event):
        self.settings.setValue('windowSize', self.size())
        self.settings.setValue('windowPosition', self.pos()) 

    def _createStatusBar(self):
        self.statusBar = QStatusBar()
        self.vbox.addWidget(self.statusBar)

def helptext(sname,athr,ver):

    print("Editor for wbar")
    print("Author:",athr)
    print("Version:",ver)
    print("Usage: %s [options]" % (sname))
    print("")
    print("Options:")
    print("-h|--help                    Show this help and exit.")
    print("-c|--config <wbarconfig>     Pass the wbar config file.")

if __name__ == '__main__':

    scriptname = os.path.basename(sys.argv[0])
    author = 'Anjishnu Sarkar'
    version = '0.9'

    wbarFile = None
    
    ## Parse through cli arguments
    numargv = len(sys.argv)-1
    iargv = 1
    
    while iargv <= numargv:
        if sys.argv[iargv] == "-h" or sys.argv[iargv] == "--help":
            helptext(scriptname,author,version)
            sys.exit(0)

        elif sys.argv[iargv] == "-c" or sys.argv[iargv] == "--config":
            wbarFile = sys.argv[iargv+1]
            iargv += 1 

        else:
            print("%s: Unspecified option. Aborting." % (scriptname))
            sys.exit(1)
  
        iargv += 1 

    app = QApplication(sys.argv)
    window = WbarDialog(wbarFile)
    window.show()  
    sys.exit(app.exec())
