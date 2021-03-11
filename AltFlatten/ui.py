# coding=utf-8
"""
AltFlatten version 1.0.0

Copyrights(c) 2021 altnoi

This software is released under the MIT License.
http://opensource.org/licenses/mit-license.php
"""
from PySide2 import QtWidgets, QtCore, QtGui
from shiboken2 import wrapInstance

import maya.OpenMayaUI as omui

import AltModelingKit.AltFlatten.lib as flatlib


def maya_main_window():
    """
    Mayaのメインウィンドウを取得
    :return:
    """
    main_wnd_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_wnd_ptr), QtWidgets.QWidget)


class flattenMainUI(QtWidgets.QDialog):
    # dlg_instanceでインスタンスを保持し、再度呼び出された場合はこれを使って情報を復元する
    dlg_instance = None

    @classmethod
    def show_dialog(cls):
        if not cls.dlg_instance:
            cls.dlg_instance = flattenMainUI()

        if cls.dlg_instance.isHidden():
            cls.dlg_instance.show()
        else:
            cls.dlg_instance.raise_()
            cls.dlg_instance.activateWindow()

    def __init__(self, parent=maya_main_window()):
        super(flattenMainUI, self).__init__(parent)

        # 重複ウィンドーを削除する
        child_list = self.parent().children()
        for c in child_list:
            if self.__class__.__name__ == c.__class__.__name__:
                c.close()

        self.setWindowTitle("AltFlatten version 1.0.0")
        self.setMinimumSize(300, 120)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        self.lib = flatlib.flattenLib()

        self.create_widgets()
        self.create_layout()
        self.create_connection()

    def create_widgets(self):
        self.status_text = QtWidgets.QLabel("ベースとする3点を指定しSet baseを押してください")
        self.is_area_limited_chk = QtWidgets.QCheckBox("三点に囲まれた内側のみに実行")
        self.set_base_btn = QtWidgets.QPushButton("Set base")
        self.exec_btn = QtWidgets.QPushButton("実行")

    def create_layout(self):
        main_lo = QtWidgets.QVBoxLayout(self)

        main_lo.addWidget(self.status_text)
        main_lo.addWidget(self.is_area_limited_chk)

        bottom_btn_lo = QtWidgets.QHBoxLayout()
        bottom_btn_lo.addStretch()
        bottom_btn_lo.addWidget(self.set_base_btn)
        bottom_btn_lo.addWidget(self.exec_btn)
        main_lo.addLayout(bottom_btn_lo)

    def create_connection(self):
        self.set_base_btn.clicked.connect(self.set_base_strap)
        self.exec_btn.clicked.connect(self.exec_main_strap)

    def set_base_strap(self):
        self.lib.setup_base()
        if self.lib.base_standby:
            self.status_text.setText("Ready")
        else:
            self.status_text.setText(self.lib.error_message)

    def exec_main_strap(self):
        self.lib.is_area_limited = self.is_area_limited_chk.isChecked()
        self.lib.move_target_vertex()
        if self.lib.error_message:
            self.status_text.setText(self.lib.error_message)
