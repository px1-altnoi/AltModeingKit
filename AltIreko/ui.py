# coding: utf-8
"""
AltIreko version 1.00

Copyrights(c) 2021 altnoi

This software is released under the MIT License.
http://opensource.org/licenses/mit-license.php
"""
import sys
from PySide2 import QtCore, QtWidgets, QtGui
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import maya.cmds as cmds
from functools import partial

import AltModelingKit.AltIreko.lib as ireko_lib

MAYA_VERSION = cmds.about(version=True)


def maya_main_window():
    """
    Mayaのメインウィンドウを取得
    :return:
    """
    main_wnd_ptr = omui.MQtUtil.mainWindow()

    if MAYA_VERSION >= 2022:
        return wrapInstance(int(main_wnd_ptr), QtWidgets.QWidget)
    else:
        return wrapInstance(long(main_wnd_ptr), QtWidgets.QWidget)


class IrekoMainWnd(QtWidgets.QDialog):
    dlg_instance = None
    @classmethod
    def show_dialog(cls):
        if not cls.dlg_instance:
            cls.dlg_instance = IrekoMainWnd()

        if cls.dlg_instance.isHidden():
            cls.dlg_instance.show()
        else:
            cls.dlg_instance.raise_()
            cls.dlg_instance.activateWindow()

    def __init__(self, parent=maya_main_window()):
        super(IrekoMainWnd, self).__init__(parent)
        self.script_job_number = -1

        # 重複ウィンドーを削除する
        child_list = self.parent().children()
        for c in child_list:
            if self.__class__.__name__ == c.__class__.__name__:
                c.close()

        self.setWindowTitle("AltIreko version 1.0.0")
        self.setMinimumSize(240, 120)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.geometry = None

        self.data = ireko_lib.IrekoData(10)
        self.lib = ireko_lib.IrekoLib(self.data)

        self.create_widgets()
        self.create_layout()
        self.create_connection()

    def create_widgets(self):
        self.show_all_btn = QtWidgets.QPushButton("Solo / Un Solo")
        self.floating_btn = QtWidgets.QPushButton("Previous")
        self.dive_in_btn = QtWidgets.QPushButton("Dive in")

    def create_layout(self):
        main_lo = QtWidgets.QVBoxLayout(self)

        main_lo.addWidget(self.show_all_btn)
        main_lo.addWidget(self.floating_btn)
        main_lo.addWidget(self.dive_in_btn)

    def create_connection(self):
        self.show_all_btn.clicked.connect(self.lib.show_all_action)
        self.floating_btn.clicked.connect(self.lib.previous_action)
        self.dive_in_btn.clicked.connect(self.lib.dive_in_action)

    def set_script_job_enabled(self, enabled):
        if enabled and self.script_job_number < 0:
            self.script_job_number = cmds.scriptJob(event=["DagObjectCreated", partial(self.lib.add_new_obj)],
                                                    protected=True)
        elif not enabled and self.script_job_number >= 0:
            cmds.scriptJob(kill=self.script_job_number, force=True)
            self.script_job_number = -1

    def showEvent(self, arg__1):
        super(IrekoMainWnd, self).showEvent(arg__1)
        self.set_script_job_enabled(True)
        if self.geometry:
            self.restoreGeometry(self.geometry)

    def closeEvent(self, arg__1):
        if isinstance(self, IrekoMainWnd):
            super(IrekoMainWnd, self).closeEvent(arg__1)
            self.set_script_job_enabled(False)
            self.geometry = self.saveGeometry()


if __name__ == "__main__":
    ui = IrekoMainWnd()
    ui.show()
