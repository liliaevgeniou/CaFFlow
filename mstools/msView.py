#!/usr/bin/env python3


import os
import sys
import time

import PyQt5 # hint for pyinstaller
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtMultimedia import QCameraInfo

import cv2 as cv

from common.preview import CQCameraPreviewWindow
from common.preview import COpenCVPreviewWindow
from common.preview import CMiniScopePreviewWindow
from common.capture import COpenCVframeCaptureThread


"""
Copyright (C) 2019 Denis Polygalov,
Laboratory for Circuit and Behavioral Physiology,
RIKEN Center for Brain Science, Saitama, Japan.

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, a copy is available at
http://www.fsf.org/
"""


class CMainWindow(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(CMainWindow, self).__init__(*args, **kwargs)

        self.oc_frame_cap_thread = None
        self.win_preview = None

        # check if we have any cameras before doing anything else
        self.l_cameras = QCameraInfo.availableCameras()
        if len(self.l_cameras) == 0:
            self.fatal_error("No cameras found!")

        self.lbl_video_source = QtWidgets.QLabel("Select video source:")

        self.cbox_cam_selector = QtWidgets.QComboBox()
        self.cbox_cam_selector.addItems([ "[ %i ] %s" % (i_idx, oc_cam.description()) for i_idx, oc_cam in enumerate(self.l_cameras)])

        self.btn_preview = QtWidgets.QPushButton("Preview")
        self.btn_preview.clicked.connect(self.__cb_on_btn_preview)

        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.lbl_video_source, 0, 0, 1, 1)
        layout.addWidget(self.cbox_cam_selector, 1, 0, 1, 1)
        layout.addWidget(self.btn_preview, 1, 1, 1, 1)

        self.setLayout(layout)
        self.setMinimumWidth(350)
        self.setWindowTitle("Video Source Selector")

    def __cb_on_btn_preview(self):
        self.btn_preview.setEnabled(False)
        self.cbox_cam_selector.setEnabled(False)

        if self.win_preview != None:
            self.win_preview.close()
            del self.win_preview
            self.win_preview = None

        i_idx = self.cbox_cam_selector.currentIndex()
        s_cam_descr = self.l_cameras[i_idx].description()

        # >>> window type selection depend on the present hardware <<<
        if s_cam_descr.find("MINISCOPE") >= 0:
            self.win_preview = CMiniScopePreviewWindow(b_enable_close_button=True)
            self.oc_frame_cap_thread = COpenCVframeCaptureThread(i_idx, self.win_preview)

        elif s_cam_descr.find("C310") >= 0:
            self.win_preview = CMiniScopePreviewWindow(b_enable_close_button=True, b_emulation_mode=True)
            self.oc_frame_cap_thread = COpenCVframeCaptureThread(i_idx, self.win_preview)

        elif s_cam_descr.find("Tape Recorder") >= 0:
            self.win_preview = COpenCVPreviewWindow()
            self.oc_frame_cap_thread = COpenCVframeCaptureThread(i_idx, self.win_preview)

        else:
            self.win_preview = CQCameraPreviewWindow()
            # WARNING: do not create self.oc_frame_cap_thread object
            # for the CQCameraPreviewWindow() type of window!
            # Check self.oc_frame_cap_thread == None all the way below!
        # ------------------------------------------------------------

        self.win_preview.closeSignal.connect(self.__cb_on_preview_closed)
        self.win_preview.show()
        self.win_preview.start_preview(i_idx, self.l_cameras[i_idx], self.oc_frame_cap_thread)
        if self.oc_frame_cap_thread != None:
            self.oc_frame_cap_thread.start()

    def __cb_on_preview_closed(self):
        self.__interrupt_threads_gracefully()
        self.btn_preview.setEnabled(True)
        self.cbox_cam_selector.setEnabled(True)
    #

    def __interrupt_threads_gracefully(self):
        if self.oc_frame_cap_thread != None:
            self.oc_frame_cap_thread.requestInterruption()
            self.oc_frame_cap_thread.wait(10000)
            del self.oc_frame_cap_thread
            self.oc_frame_cap_thread = None

    def fatal_error(self, s_msg):
        self.__interrupt_threads_gracefully()
        QtWidgets.QMessageBox.critical(None, "Fatal Error", "%s\nThe application will exit now." % s_msg)
        sys.exit(-1)

    def closeEvent(self, event):
        self.__interrupt_threads_gracefully()
        if self.win_preview != None:
            self.win_preview.close()
#


if __name__ == '__main__':
    s_qt_plugin_path = os.path.join(os.getcwd(), 'PyQt5', 'Qt', 'plugins')
    if os.path.isdir(s_qt_plugin_path):
        os.environ['QT_PLUGIN_PATH'] = s_qt_plugin_path

    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName("msView")

    oc_main_win = CMainWindow()
    oc_main_win.show()
    sys.exit(app.exec_())
#

