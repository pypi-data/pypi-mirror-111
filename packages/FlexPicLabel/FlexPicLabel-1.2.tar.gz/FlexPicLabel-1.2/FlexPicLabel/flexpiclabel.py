#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function,
                        with_statement, unicode_literals)

__author__ = "Stephan Sokolow (deitarion/SSokolow)/poshl9k"
__license__ = "MIT"


from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore

class FlexPicLabel(QFrame):
    """Base class"""
    movie_aspect = None
    orig_pixmap = None

    def __init__(self):
        super(FlexPicLabel, self).__init__()

        # We need a layout if we want to prevent the image from distorting
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        # Set the letterbox/pillarbox bars to be black
        # https://wiki.qt.io/How_to_Change_the_Background_Color_of_QWidget
        # pal = self.palette()
        # pal.setColor(QPalette.Background, Qt.black)
        # self.setAutoFillBackground(True)
        # self.setPalette(pal)

        # No black bordering on non-letterbox/pillarbox edges
        layout.setContentsMargins(0, 0, 0, 0)

    def load(self, source):
        """Load anything that QImageReader or QMovie constructors accept"""

        # Use QImageReader to identify animated GIFs for separate handling
        # (Thanks to https://stackoverflow.com/a/20674469/435253 for this)
        image_reader = QImageReader(source)
        from PySide6.QtGui import QImageIOHandler
        if image_reader.supportsAnimation() and image_reader.imageCount() > 1:
            movie = QMovie(source)

            # Calculate the aspect ratio and adjust the widget size
            movie.jumpToFrame(0)
            movie_size = movie.currentImage().size()
            self.movie_aspect = movie_size.width() / movie_size.height()
            self.resizeEvent()

            self.label.setMovie(movie)
            movie.start()

            # Free memory if the previous image was non-animated
            self.orig_pixmap = None
        else:
            self.orig_pixmap = QPixmap(image_reader.read())
            self.label.setPixmap(self.orig_pixmap)
            rect = self.geometry()
            size = QSize(rect.width(), rect.height())
            pixmap_size = self.label.pixmap().size()
            if (pixmap_size.width() == size.width() and
              pixmap_size.height() <= size.height()):
                return
            if (pixmap_size.height() == size.height() and
              pixmap_size.width() <= size.width()):
                return
            self.label.setPixmap(self.orig_pixmap.scaled(size,
                Qt.KeepAspectRatio, Qt.SmoothTransformation))

            # Fail quickly if our violated invariants result in stale
            # aspect-ratio information getting reused
            self.movie_aspect = None
        # Keep the image from preventing downscaling
        # self.setMinimumSize(1, 1)

    def resizeEvent(self, _event=None):
        """Resize handler to update dimensions of displayed image/animation"""
        rect = self.geometry()
        movie = self.label.movie()
        if movie:
            width = rect.height() * self.movie_aspect
            if width <= rect.width():
                size = QSize(width, rect.height())
            else:
                height = rect.width() / self.movie_aspect
                size = QSize(rect.width(), height)

            movie.setScaledSize(size)
        elif self.orig_pixmap and not self.orig_pixmap.isNull():
            size = QSize(rect.width(), rect.height())
            pixmap_size = self.label.pixmap().size()
            if (pixmap_size.width() == size.width() and
              pixmap_size.height() <= size.height()):
                return
            if (pixmap_size.height() == size.height() and
              pixmap_size.width() <= size.width()):
                return
            self.label.setPixmap(self.orig_pixmap.scaled(size,
                Qt.KeepAspectRatio, Qt.SmoothTransformation))

