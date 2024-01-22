#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from PySide6.QtCore import Qt, QCoreApplication
from PySide6.QtWidgets import QApplication

from keyctl.gui._gui import KeyringApp


# -------------------------------------------------------------------


def main():
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)

    app = QApplication(sys.argv)

    window = KeyringApp()
    window.ui.show()
    window.center_window()
    window.activateWindow()

    ret = app.exec()
    sys.exit(ret)


# -------------------------------------------------------------------


if __name__ == '__main__':
    main()
