import argparse
import logging

from labelCloud import __version__


def main():
    parser = argparse.ArgumentParser(
        description="Label 3D bounding boxes inside point clouds."
    )
    parser.add_argument(
        "-e",
        "--example",
        action="store_true",
        help="Setup a project with an example point cloud and label.",
    )
    parser.add_argument(
        "-v", "--version", action="version", version="%(prog)s " + __version__
    )
    args = parser.parse_args()

    if args.example:
        setup_example_project()

    start_gui()


def setup_example_project() -> None:
    import shutil
    from pathlib import Path

    import importlib_resources

    from labelCloud.control.config_manager import config

    logging.info(
        "Starting labelCloud in example mode.\n"
        "Setting up project with example point cloud ,label and default config."
    )
    cwdir = Path().cwd()

    # Create folders
    pcd_folder = cwdir.joinpath(config.get("FILE", "pointcloud_folder"))
    pcd_folder.mkdir(exist_ok=True)
    label_folder = cwdir.joinpath(config.get("FILE", "label_folder"))
    label_folder.mkdir(exist_ok=True)

    # Copy example files
    shutil.copy(
        str(
            importlib_resources.files("labelCloud.resources").joinpath(
                "default_config.ini"
            )
        ),
        str(cwdir.joinpath("config.ini")),
    )
    shutil.copy(
        str(
            importlib_resources.files("labelCloud.resources.examples").joinpath(
                "exemplary.ply"
            )
        ),
        str(pcd_folder.joinpath("exemplary.ply")),
    )
    shutil.copy(
        str(
            importlib_resources.files("labelCloud.resources").joinpath(
                "default_classes.json"
            )
        ),
        str(label_folder.joinpath("_classes.json")),
    )
    shutil.copy(
        str(
            importlib_resources.files("labelCloud.resources.examples").joinpath(
                "exemplary.json"
            )
        ),
        str(label_folder.joinpath("exemplary.json")),
    )
    logging.info(
        f"Setup example project in {cwdir}:"
        "\n - config.ini"
        "\n - pointclouds/exemplary.ply"
        "\n - labels/exemplary.json"
    )


def start_gui():
    import os
    import sys

    # Suppress Qt accessibility warnings on Linux
    os.environ["NO_AT_BRIDGE"] = "1"
    os.environ["QT_LINUX_ACCESSIBILITY_ALWAYS_ON"] = "0"
    os.environ["QT_LOGGING_RULES"] = (
        "qt.accessibility.atspi=false;qt.accessibility.cache=false"
    )

    from PySide6.QtCore import QCoreApplication, Qt
    from PySide6.QtQuick import QQuickWindow, QSGRendererInterface
    from PySide6.QtWidgets import QApplication

    # Suppress WebEngine warning initialized from plugin
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    QQuickWindow.setGraphicsApi(QSGRendererInterface.OpenGLRhi)

    from labelCloud.control.controller import Controller
    from labelCloud.view.gui import GUI

    app = QApplication(sys.argv)

    # Setup Model-View-Control structure
    control = Controller()
    view = GUI(control)

    # Install event filter to catch user interventions
    app.installEventFilter(view)

    # Start GUI
    view.show()

    app.setStyle("Fusion")
    screen = QApplication.primaryScreen().availableGeometry()
    width = (screen.width() - view.width()) // 2
    height = (screen.height() - view.height()) // 2
    view.move(width, height)

    logging.info("Showing GUI...")
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
