import logging
import os
import shutil
import time
from pathlib import Path
from typing import Tuple

import pytest
from PySide6 import QtCore

from labelCloud.control.config_manager import config
from labelCloud.control.controller import Controller
from labelCloud.model.bbox import BBox
from labelCloud.view.gui import GUI
from labelCloud.view.startup.dialog import StartupDialog


def pytest_configure(config):
    os.chdir("../labelCloud")
    os.environ["NO_AT_BRIDGE"] = "1"
    os.environ["QT_LINUX_ACCESSIBILITY_ALWAYS_ON"] = "0"
    os.environ["QT_LOGGING_RULES"] = (
        "qt.accessibility.atspi=false;qt.accessibility.cache=false"
    )

    from PySide6.QtCore import QCoreApplication, Qt
    from PySide6.QtQuick import QQuickWindow, QSGRendererInterface

    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    QQuickWindow.setGraphicsApi(QSGRendererInterface.OpenGLRhi)

    logging.info(f"Set working directory to {os.getcwd()}.")


@pytest.fixture
def startup_qt(qtbot, qapp, monkeypatch):
    # Backup label
    pathToLabel = config.getpath("FILE", "label_folder") / "exemplary.json"
    pathToBackup = Path().cwd() / pathToLabel.name

    shutil.copy(pathToLabel, pathToBackup)

    # Setup Model-View-Control structure
    control = Controller()

    monkeypatch.setattr(StartupDialog, "exec", lambda self: 1)

    view = GUI(control)
    qtbot.addWidget(view)
    qtbot.addWidget(view.gl_widget)

    # Install event filter to catch user interventions
    qapp.installEventFilter(view)

    # Start GUI
    view.show()
    yield view, control

    shutil.move(pathToBackup, pathToLabel)


@pytest.fixture
def bbox():
    return BBox(cx=0, cy=0, cz=0, length=3, width=2, height=1)
