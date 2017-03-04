#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from PySide.QtGui import QApplication

from gui import KeyringApp


# -------------------------------------------------------------------


def main():
    app = QApplication(sys.argv)

    window = KeyringApp()
    window.ui.show()
    window.center_window()
    window.activateWindow()

    ret = app.exec_()
    sys.exit(ret)


# -------------------------------------------------------------------


if __name__ == '__main__':
    main()
