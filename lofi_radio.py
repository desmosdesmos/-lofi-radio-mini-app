#!/usr/bin/env python3
"""
Lo-Fi Radio Player - Warm Retro Design
ПОЛНОСТЬЮ ИСПРАВЛЕННАЯ ВЕРСИЯ
"""

import sys
import random
import os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtMultimedia import *


# ═══════════════════════════════════════════════════════════════
# DESIGN SYSTEM
# ═══════════════════════════════════════════════════════════════
COLOR_BG = "#FFF9F0"
COLOR_ACCENT = "#FFC085"
COLOR_DARK = "#2D3748"
COLOR_GREY = "#718096"
COLOR_BORDER = "#CBD5E0"
COLOR_WHITE = "#FFFFFF"

ASSETS_DIR = "assets"


# ═══════════════════════════════════════════════════════════════
# ICON HELPER (встроенные иконки)
# ═══════════════════════════════════════════════════════════════
class IconGenerator:
    @staticmethod
    def create_pixmap(draw_func, size=64):
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        draw_func(painter, size, size)
        painter.end()
        return pixmap
    
    @staticmethod
    def draw_play(painter, w, h):
        painter.setBrush(QBrush(QColor(COLOR_DARK)))
        painter.setPen(Qt.PenStyle.NoPen)
        path = QPainterPath()
        path.moveTo(w * 0.28, h * 0.12)
        path.lineTo(w * 0.28, h * 0.88)
        path.lineTo(w * 0.88, h * 0.5)
        path.closeSubpath()
        painter.drawPath(path)
    
    @staticmethod
    def draw_pause(painter, w, h):
        """Исправленная иконка Pause - две равные полосы."""
        painter.setBrush(QBrush(QColor(COLOR_DARK)))
        painter.setPen(Qt.PenStyle.NoPen)
        # Левая полоса
        painter.drawRoundedRect(int(w * 0.22), int(h * 0.15), int(w * 0.22), int(h * 0.7), 3, 3)
        # Правая полоса
        painter.drawRoundedRect(int(w * 0.56), int(h * 0.15), int(w * 0.22), int(h * 0.7), 3, 3)
    
    @staticmethod
    def draw_next(painter, w, h):
        painter.setBrush(QBrush(QColor(COLOR_DARK)))
        painter.setPen(Qt.PenStyle.NoPen)
        path = QPainterPath()
        path.moveTo(w * 0.38, h * 0.15)
        path.lineTo(w * 0.38, h * 0.85)
        path.lineTo(w * 0.88, h * 0.5)
        path.closeSubpath()
        painter.drawPath(path)
        painter.drawRoundedRect(int(w * 0.12), int(h * 0.15), int(w * 0.12), int(h * 0.7), 3, 3)
    
    @staticmethod
    def draw_prev(painter, w, h):
        painter.setBrush(QBrush(QColor(COLOR_DARK)))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(int(w * 0.76), int(h * 0.15), int(w * 0.12), int(h * 0.7), 3, 3)
        path = QPainterPath()
        path.moveTo(w * 0.62, h * 0.15)
        path.lineTo(w * 0.62, h * 0.85)
        path.lineTo(w * 0.12, h * 0.5)
        path.closeSubpath()
        painter.drawPath(path)
    
    @staticmethod
    def draw_heart(painter, w, h):
        painter.setBrush(QBrush(QColor(COLOR_ACCENT)))
        painter.setPen(Qt.PenStyle.NoPen)
        path = QPainterPath()
        path.moveTo(w * 0.5, h * 0.78)
        path.cubicTo(w * 0.15, h * 0.55, w * 0.02, h * 0.32, w * 0.18, h * 0.15)
        path.cubicTo(w * 0.35, h * 0.02, w * 0.45, h * 0.12, w * 0.5, h * 0.25)
        path.cubicTo(w * 0.55, h * 0.12, w * 0.65, h * 0.02, w * 0.82, h * 0.15)
        path.cubicTo(w * 0.98, h * 0.32, w * 0.85, h * 0.55, w * 0.5, h * 0.78)
        painter.drawPath(path)
    
    @staticmethod
    def draw_sleep(painter, w, h):
        painter.setBrush(QBrush(QColor(COLOR_DARK)))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(int(w * 0.2), int(h * 0.2), int(w * 0.6), int(h * 0.6))
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_DestinationOut)
        painter.drawEllipse(int(w * 0.35), int(h * 0.2), int(w * 0.4), int(h * 0.4))
    
    @staticmethod
    def draw_expand(painter, w, h):
        painter.setBrush(QBrush(QColor(COLOR_DARK)))
        painter.setPen(QPen(QColor(COLOR_DARK), 5, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        # Угловые стрелки
        painter.drawLine(int(w * 0.35), int(h * 0.25), int(w * 0.2), int(h * 0.25))
        painter.drawLine(int(w * 0.2), int(h * 0.25), int(w * 0.2), int(h * 0.35))
        painter.drawLine(int(w * 0.65), int(h * 0.25), int(w * 0.8), int(h * 0.25))
        painter.drawLine(int(w * 0.8), int(h * 0.25), int(w * 0.8), int(h * 0.35))
        painter.drawLine(int(w * 0.35), int(h * 0.75), int(w * 0.2), int(h * 0.75))
        painter.drawLine(int(w * 0.2), int(h * 0.75), int(w * 0.2), int(h * 0.65))
        painter.drawLine(int(w * 0.65), int(h * 0.75), int(w * 0.8), int(h * 0.75))
        painter.drawLine(int(w * 0.8), int(h * 0.75), int(w * 0.8), int(h * 0.65))
    
    @staticmethod
    def draw_stations(painter, w, h):
        painter.setBrush(QBrush(QColor(COLOR_DARK)))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(int(w * 0.2), int(h * 0.18), int(w * 0.6), int(h * 0.14), 4, 4)
        painter.drawRoundedRect(int(w * 0.2), int(h * 0.43), int(w * 0.6), int(h * 0.14), 4, 4)
        painter.drawRoundedRect(int(w * 0.2), int(h * 0.68), int(w * 0.6), int(h * 0.14), 4, 4)
    
    @staticmethod
    def draw_mini(painter, w, h):
        painter.setBrush(QBrush(QColor(COLOR_DARK)))
        painter.setPen(QPen(QColor(COLOR_DARK), 5, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        painter.drawRect(int(w * 0.25), int(h * 0.25), int(w * 0.5), int(h * 0.5))
    
    @staticmethod
    def draw_volume(painter, w, h):
        painter.setBrush(QBrush(QColor(COLOR_DARK)))
        painter.setPen(Qt.PenStyle.NoPen)
        # Динамик
        path = QPainterPath()
        path.moveTo(w * 0.15, h * 0.35)
        path.lineTo(w * 0.35, h * 0.35)
        path.lineTo(w * 0.55, h * 0.15)
        path.lineTo(w * 0.55, h * 0.85)
        path.lineTo(w * 0.35, h * 0.65)
        path.lineTo(w * 0.15, h * 0.65)
        path.closeSubpath()
        painter.drawPath(path)
        # Волны
        painter.drawArc(int(w * 0.58), int(h * 0.25), int(w * 0.3), int(h * 0.5), -70 * 16, 140 * 16)
    
    @classmethod
    def get_icon(cls, name, size=64):
        icons = {
            "play": cls.draw_play,
            "pause": cls.draw_pause,
            "next": cls.draw_next,
            "prev": cls.draw_prev,
            "heart": cls.draw_heart,
            "sleep": cls.draw_sleep,
            "expand": cls.draw_expand,
            "stations": cls.draw_stations,
            "mini": cls.draw_mini,
            "volume": cls.draw_volume,
        }
        if name in icons:
            pixmap = cls.create_pixmap(icons[name], size)
            return QIcon(pixmap)
        return QIcon()


# ═══════════════════════════════════════════════════════════════
# VINYL RECORD
# ═══════════════════════════════════════════════════════════════
class VinylRecord(QFrame):
    def __init__(self):
        super().__init__()
        self.setFixedSize(260, 260)
        self._rotation = 0.0
        
        # Perfect circle mask
        mask = QBitmap(260, 260)
        mask.fill(Qt.GlobalColor.color0)
        painter = QPainter(mask)
        painter.setBrush(Qt.GlobalColor.color1)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(0, 0, 260, 260)
        painter.end()
        self.setMask(mask)
        
        # Shadow
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 38))
        self.setGraphicsEffect(shadow)
        
        # Rotation animation
        self.rotation_anim = QPropertyAnimation(self, b"rotation")
        self.rotation_anim.setDuration(6000)
        self.rotation_anim.setStartValue(0)
        self.rotation_anim.setEndValue(360)
        self.rotation_anim.setLoopCount(-1)
        self.rotation_anim.setEasingCurve(QEasingCurve.Type.Linear)
        
        self.is_playing = False
    
    @pyqtProperty(float)
    def rotation(self):
        return self._rotation
    
    @rotation.setter
    def rotation(self, value):
        self._rotation = value % 360
        self.update()
    
    def set_playing(self, playing):
        if self.is_playing == playing:
            return
        self.is_playing = playing
        
        if playing:
            if self.rotation_anim.state() == QAbstractAnimation.State.Stopped:
                self.rotation_anim.start()
            elif self.rotation_anim.state() == QAbstractAnimation.State.Paused:
                self.rotation_anim.resume()
        else:
            self.rotation_anim.pause()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        cx, cy = 130, 130
        radius = 120
        
        painter.save()
        painter.translate(cx, cy)
        painter.rotate(self._rotation)
        
        # Vinyl disc
        vinyl_grad = QRadialGradient(0, 0, radius)
        vinyl_grad.setColorAt(0, QColor("#1a202c"))
        vinyl_grad.setColorAt(0.7, QColor("#2d3748"))
        vinyl_grad.setColorAt(1, QColor("#1a202c"))
        
        painter.setBrush(QBrush(vinyl_grad))
        painter.setPen(QPen(QColor(COLOR_DARK), 2))
        painter.drawEllipse(-radius, -radius, radius*2, radius*2)
        
        # Grooves
        for r in range(radius - 15, 45, -10):
            painter.setPen(QPen(QColor("#4a5568"), 1))
            painter.drawEllipse(-r, -r, r*2, r*2)
        
        painter.restore()
        
        # Center label
        label_r = 48
        label_grad = QRadialGradient(cx, cy, label_r)
        label_grad.setColorAt(0, QColor(COLOR_ACCENT))
        label_grad.setColorAt(1, QColor("#f6ad55"))
        
        painter.setBrush(QBrush(label_grad))
        painter.setPen(QPen(QColor(COLOR_DARK), 2))
        painter.drawEllipse(cx - label_r, cy - label_r, label_r*2, label_r*2)
        
        painter.setBrush(QBrush(QColor("#ed8936")))
        painter.drawEllipse(cx - 16, cy - 16, 32, 32)
        
        painter.setBrush(QBrush(QColor(COLOR_BG)))
        painter.drawEllipse(cx - 5, cy - 5, 10, 10)


# ═══════════════════════════════════════════════════════════════
# VISUALIZER
# ═══════════════════════════════════════════════════════════════
class VisualizerWidget(QFrame):
    def __init__(self):
        super().__init__()
        self.setFixedSize(220, 50)
        self.bars = []
        
        layout = QHBoxLayout(self)
        layout.setSpacing(4)
        layout.setContentsMargins(0, 0, 0, 0)
        
        for i in range(15):
            bar = QFrame()
            bar.setFixedWidth(10)
            bar.setFixedHeight(5)
            bar.setStyleSheet(f"""
                QFrame {{
                    background-color: {COLOR_ACCENT};
                    border-radius: 5px;
                }}
            """)
            self.bars.append(bar)
            layout.addWidget(bar)
        
        self.timer = QTimer()
        self.timer.timeout.connect(self._animate)
        self.timer.setInterval(50)
        self.is_playing = False
    
    def set_playing(self, playing):
        self.is_playing = playing
        if playing:
            self.timer.start()
        else:
            self.timer.stop()
            for bar in self.bars:
                bar.setFixedHeight(5)
    
    def _animate(self):
        for bar in self.bars:
            h = random.randint(10, 45)
            bar.setFixedHeight(h)


# ═══════════════════════════════════════════════════════════════
# SLEEP TIMER DIALOG
# ═══════════════════════════════════════════════════════════════
class SleepTimerDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(300, 220)
        self.timer_minutes = 0
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        self.bg = QWidget()
        self.bg.setStyleSheet(f"""
            QWidget {{
                background-color: {COLOR_BG};
                border-radius: 20px;
            }}
        """)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(40)
        shadow.setColor(QColor(0, 0, 0, 50))
        self.bg.setGraphicsEffect(shadow)
        
        bg_layout = QVBoxLayout(self.bg)
        bg_layout.setSpacing(15)
        
        title = QLabel("☾ Sleep Timer")
        title.setFont(QFont("Nunito", 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(f"color: {COLOR_DARK};")
        bg_layout.addWidget(title)
        
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(0, 120)
        self.slider.setSingleStep(15)
        self.slider.setStyleSheet(f"""
            QSlider::groove:horizontal {{ border: none; height: 6px; background: {COLOR_ACCENT}; border-radius: 3px; }}
            QSlider::handle:horizontal {{ background: {COLOR_BG}; border: 2px solid {COLOR_DARK}; width: 18px; margin: -6px 0; border-radius: 9px; }}
            QSlider::sub-page:horizontal {{ background: {COLOR_ACCENT}; border-radius: 3px; }}
        """)
        self.slider.valueChanged.connect(self.update_label)
        bg_layout.addWidget(self.slider)
        
        self.time_label = QLabel("Off")
        self.time_label.setFont(QFont("Nunito", 14))
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.time_label.setStyleSheet(f"color: {COLOR_GREY};")
        bg_layout.addWidget(self.time_label)
        
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setFixedHeight(40)
        cancel_btn.setStyleSheet(f"""
            QPushButton {{
                background: {COLOR_BG};
                color: {COLOR_GREY};
                border: 1px solid {COLOR_BORDER};
                border-radius: 12px;
                font-size: 13px;
                font-weight: 600;
            }}
        """)
        cancel_btn.clicked.connect(self.reject)
        
        ok_btn = QPushButton("Set")
        ok_btn.setFixedHeight(40)
        ok_btn.setStyleSheet(f"""
            QPushButton {{
                background: {COLOR_ACCENT};
                color: {COLOR_DARK};
                border: 2px solid {COLOR_DARK};
                border-radius: 12px;
                font-size: 13px;
                font-weight: 600;
            }}
        """)
        ok_btn.clicked.connect(self.accept)
        
        btn_layout.addWidget(cancel_btn)
        btn_layout.addWidget(ok_btn)
        bg_layout.addLayout(btn_layout)
        
        layout.addWidget(self.bg)
    
    def update_label(self, value):
        if value == 0:
            self.time_label.setText("Off")
        else:
            self.time_label.setText(f"{value} min")
            self.timer_minutes = value


# ═══════════════════════════════════════════════════════════════
# STATIONS DIALOG
# ═══════════════════════════════════════════════════════════════
class StationsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(340, 280)
        self.selected_idx = -1
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        self.bg = QWidget()
        self.bg.setStyleSheet(f"""
            QWidget {{
                background-color: {COLOR_BG};
                border-radius: 20px;
            }}
        """)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(40)
        shadow.setColor(QColor(0, 0, 0, 50))
        self.bg.setGraphicsEffect(shadow)
        
        bg_layout = QVBoxLayout(self.bg)
        bg_layout.setSpacing(15)
        
        title = QLabel("📻 Radio Stations")
        title.setFont(QFont("Nunito", 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(f"color: {COLOR_DARK};")
        bg_layout.addWidget(title)
        
        self.station_list = QListWidget()
        self.station_list.setFont(QFont("Nunito", 12))
        self.station_list.setStyleSheet(f"""
            QListWidget {{
                border: none;
                background: {COLOR_BG};
                border: 1px solid {COLOR_BORDER};
                border-radius: 12px;
                padding: 10px;
            }}
            QListWidget::item {{
                padding: 12px;
                border-radius: 8px;
                color: {COLOR_DARK};
                border: 2px solid transparent;
            }}
            QListWidget::item:selected {{
                background: {COLOR_ACCENT};
                color: {COLOR_DARK};
                border-color: {COLOR_DARK};
            }}
            QListWidget::item:hover {{
                background: {COLOR_BG};
            }}
        """)
        self.station_list.addItems([
            "🎵 Drone Zone\n   ambient · drone · sleep",
            "🎵 Smooth Chill\n   smooth · chillout · relax",
            "🎵 Lofi Girl\n   lofi hip hop · study · relax",
            "🎵 Groove Salad\n   chillout · ambient · downtempo",
            "🎵 Space Station\n   space ambient · downtempo · chill",
            "🎵 Deep Space One\n   deep ambient · space · relax",
            "🎵 Secret Agent\n   liquid drum n bass · chill",
            "🎵 Beat Blender\n   deep beats · downtempo · chill",
            "🎵 Fluid\n   fluidic beats · chill · downtempo",
            "🎵 PopTron\n   upbeat · pop · electronic",
            "🎵 Def Con\n   industrial · noise · techno"
        ])
        self.station_list.setCurrentRow(2)  # Lofi Girl по умолчанию
        self.station_list.itemClicked.connect(self.on_select)
        bg_layout.addWidget(self.station_list)
        
        close_btn = QPushButton("Play Selected")
        close_btn.setFixedHeight(45)
        close_btn.setStyleSheet(f"""
            QPushButton {{
                background: {COLOR_ACCENT};
                color: {COLOR_DARK};
                border: 2px solid {COLOR_DARK};
                border-radius: 12px;
                font-size: 14px;
                font-weight: 600;
            }}
        """)
        close_btn.clicked.connect(self.accept)
        bg_layout.addWidget(close_btn)
        
        layout.addWidget(self.bg)
    
    def on_select(self, item):
        self.selected_idx = self.station_list.row(item)


# ═══════════════════════════════════════════════════════════════
# MINI PLAYER (с кнопкой Expand + Sleep + Stations)
# ═══════════════════════════════════════════════════════════════
class MiniPlayerWindow(QMainWindow):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(400, 110)
        self._drag_pos = None
        
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(8)
        
        central.setStyleSheet(f"""
            QWidget {{
                background-color: {COLOR_BG};
                border-radius: 15px;
            }}
        """)
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(40)
        shadow.setYOffset(15)
        shadow.setColor(QColor(0, 0, 0, 40))
        central.setGraphicsEffect(shadow)
        
        # Top row: controls
        top_layout = QHBoxLayout()
        top_layout.setSpacing(10)
        
        # Prev
        self.prev_btn = QPushButton()
        self.prev_btn.setFixedSize(34, 34)
        self.prev_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.prev_btn.setIcon(IconGenerator.get_icon("prev", 28))
        self.prev_btn.setIconSize(QSize(20, 20))
        self.prev_btn.setStyleSheet(f"""
            QPushButton {{
                background: {COLOR_BG};
                border: 1px solid {COLOR_BORDER};
                border-radius: 17px;
            }}
            QPushButton:hover {{
                background: {COLOR_ACCENT};
            }}
        """)
        self.prev_btn.clicked.connect(lambda: self.main_window.set_tab((self.main_window.tab_idx - 1) % len(self.main_window.STREAMS)))
        top_layout.addWidget(self.prev_btn)

        # Play/Pause
        self.play_btn = QPushButton()
        self.play_btn.setFixedSize(42, 42)
        self.play_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.play_btn.setIcon(IconGenerator.get_icon("play", 32))
        self.play_btn.setIconSize(QSize(24, 24))
        self.play_btn.setStyleSheet(f"""
            QPushButton {{
                background: {COLOR_ACCENT};
                border: 2px solid {COLOR_DARK};
                border-radius: 21px;
            }}
            QPushButton:hover {{
                background: #ffb16e;
            }}
        """)
        self.play_btn.clicked.connect(self.main_window.toggle_play)
        top_layout.addWidget(self.play_btn)

        # Next
        self.next_btn = QPushButton()
        self.next_btn.setFixedSize(34, 34)
        self.next_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.next_btn.setIcon(IconGenerator.get_icon("next", 28))
        self.next_btn.setIconSize(QSize(20, 20))
        self.next_btn.setStyleSheet(f"""
            QPushButton {{
                background: {COLOR_BG};
                border: 1px solid {COLOR_BORDER};
                border-radius: 17px;
            }}
            QPushButton:hover {{
                background: {COLOR_ACCENT};
            }}
        """)
        self.next_btn.clicked.connect(lambda: self.main_window.set_tab((self.main_window.tab_idx + 1) % len(self.main_window.STREAMS)))
        top_layout.addWidget(self.next_btn)
        
        # Volume - ИСПРАВЛЕНА регулировка громкости
        self.vol_slider = QSlider(Qt.Orientation.Horizontal)
        self.vol_slider.setRange(0, 100)
        self.vol_slider.setValue(int(self.main_window.audio.volume() * 100))
        self.vol_slider.setFixedWidth(90)
        self.vol_slider.setStyleSheet(f"""
            QSlider::groove:horizontal {{
                border: none;
                height: 6px;
                background: {COLOR_WHITE};
                border-radius: 3px;
            }}
            QSlider::handle:horizontal {{
                background: {COLOR_ACCENT};
                border: 2px solid {COLOR_DARK};
                width: 18px;
                margin: -6px 0;
                border-radius: 9px;
            }}
            QSlider::sub-page:horizontal {{
                background: {COLOR_ACCENT};
                border-radius: 3px;
            }}
        """)
        # ИСПРАВЛЕНО: прямое подключение к audio
        self.vol_slider.valueChanged.connect(self.on_volume_changed)
        top_layout.addWidget(self.vol_slider)
        
        # Expand button
        self.expand_btn = QPushButton()
        self.expand_btn.setFixedSize(34, 34)
        self.expand_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.expand_btn.setIcon(IconGenerator.get_icon("expand", 28))
        self.expand_btn.setIconSize(QSize(20, 20))
        self.expand_btn.setToolTip("Expand to Full")
        self.expand_btn.setStyleSheet(f"""
            QPushButton {{
                background: {COLOR_ACCENT};
                border: 2px solid {COLOR_DARK};
                border-radius: 17px;
            }}
            QPushButton:hover {{
                background: #ffb16e;
            }}
        """)
        self.expand_btn.clicked.connect(self.expand_to_full)
        top_layout.addWidget(self.expand_btn)
        
        layout.addLayout(top_layout)
        
        # Bottom row: Sleep + Stations
        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(8)
        
        sleep_btn = QPushButton("☾ Sleep")
        sleep_btn.setFixedHeight(30)
        sleep_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        sleep_btn.clicked.connect(self.show_sleep_timer)
        sleep_btn.setStyleSheet(f"""
            QPushButton {{
                background: {COLOR_BG};
                color: {COLOR_DARK};
                border: 1px solid {COLOR_BORDER};
                border-radius: 8px;
                font-size: 11px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                background: {COLOR_ACCENT};
            }}
        """)
        bottom_layout.addWidget(sleep_btn, 1)
        
        stations_btn = QPushButton("📻 Stations")
        stations_btn.setFixedHeight(30)
        stations_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        stations_btn.clicked.connect(self.show_stations)
        stations_btn.setStyleSheet(f"""
            QPushButton {{
                background: {COLOR_BG};
                color: {COLOR_DARK};
                border: 1px solid {COLOR_BORDER};
                border-radius: 8px;
                font-size: 11px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                background: {COLOR_ACCENT};
            }}
        """)
        bottom_layout.addWidget(stations_btn, 1)
        
        layout.addLayout(bottom_layout)
    
    def on_volume_changed(self, value):
        """ИСПРАВЛЕНО: изменение громкости теперь работает."""
        self.main_window.audio.setVolume(value / 100.0)
    
    def expand_to_full(self):
        self.close()
        self.main_window.show()
    
    def show_sleep_timer(self):
        dialog = SleepTimerDialog()
        dialog.setParent(None)
        dialog.setWindowModality(Qt.WindowModality.ApplicationModal)
        x = self.x() + (self.width() - dialog.width()) // 2
        y = self.y() + (self.height() - dialog.height()) // 2
        dialog.move(max(0, x), max(0, y))
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.main_window.apply_sleep_timer(dialog.timer_minutes)

    def show_stations(self):
        dialog = StationsDialog()
        dialog.setParent(None)
        dialog.setWindowModality(Qt.WindowModality.ApplicationModal)
        x = self.x() + (self.width() - dialog.width()) // 2
        y = self.y() + (self.height() - dialog.height()) // 2
        dialog.move(max(0, x), max(0, y))
        if dialog.exec() == QDialog.DialogCode.Accepted:
            if dialog.selected_idx >= 0:
                self.main_window.set_tab(dialog.selected_idx)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
    
    def mouseMoveEvent(self, event):
        if self._drag_pos:
            self.move(event.globalPosition().toPoint() - self._drag_pos)
    
    def mouseReleaseEvent(self, event):
        self._drag_pos = None
    
    def update_play_state(self, playing):
        icon_name = "pause" if playing else "play"
        self.play_btn.setIcon(IconGenerator.get_icon(icon_name, 32))


# ═══════════════════════════════════════════════════════════════
# MAIN WINDOW
# ═══════════════════════════════════════════════════════════════
class AnimatedWindow(QMainWindow):
    # 11 спокойных радиостанций (как в веб-версии)
    STREAMS = [
        "https://ice1.somafm.com/dronezone-128-mp3",      # Drone Zone
        "https://media-ssl.musicradio.com/SmoothChill",   # Smooth Chill
        "https://play.streamafrica.net/lofiradio",        # Lofi Girl
        "https://ice1.somafm.com/groovesalad-128-mp3",    # Groove Salad
        "https://ice1.somafm.com/spacestation-128-mp3",   # Space Station
        "https://ice1.somafm.com/deepspaceone-128-mp3",   # Deep Space One
        "https://ice1.somafm.com/secretagent-128-mp3",    # Secret Agent
        "https://ice1.somafm.com/beatblender-128-mp3",    # Beat Blender
        "https://ice1.somafm.com/fluid-128-mp3",          # Fluid
        "https://ice1.somafm.com/poptron-128-mp3",        # PopTron
        "https://ice1.somafm.com/defcon-128-mp3",         # Def Con
    ]

    TITLES = [
        ("Drone Zone", "ambient · drone · sleep"),
        ("Smooth Chill", "smooth · chillout · relax"),
        ("Lofi Girl", "lofi hip hop · study · relax"),
        ("Groove Salad", "chillout · ambient · downtempo"),
        ("Space Station", "space ambient · downtempo · chill"),
        ("Deep Space One", "deep ambient · space · relax"),
        ("Secret Agent", "liquid drum n bass · chill"),
        ("Beat Blender", "deep beats · downtempo · chill"),
        ("Fluid", "fluidic beats · chill · downtempo"),
        ("PopTron", "upbeat · pop · electronic"),
        ("Def Con", "industrial · noise · techno"),
    ]
    
    def __init__(self):
        super().__init__()
        self._drag_pos = None
        self.tab_idx = 2  # Lofi Girl по умолчанию
        self.playing = False
        self.loading = False
        self.sleep_timer = None
        self.mini_window = None
        
        # Load font
        font_id = QFontDatabase.addApplicationFont("Nunito.ttf")
        self.nunito = QFontDatabase.applicationFontFamilies(font_id)[0] if font_id != -1 else "Segoe UI"
        
        self.setup_window()
        self.setup_ui()
        self.setup_player()
        self.apply_styles()
        
        # Fade in
        self.fade_anim = QPropertyAnimation(self, b"windowOpacity")
        self.fade_anim.setDuration(400)
        self.fade_anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.fade_anim.setStartValue(0.0)
        self.fade_anim.setEndValue(1.0)
        self.fade_anim.start()
    
    def setup_window(self):
        # Frameless + Translucent
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(400, 840)
        
        central = QWidget()
        self.setCentralWidget(central)
        self.main_layout = QVBoxLayout(central)
        self.main_layout.setContentsMargins(24, 24, 24, 24)
        self.main_layout.setSpacing(0)
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(60)
        shadow.setYOffset(30)
        shadow.setColor(QColor(0, 0, 0, 50))
        central.setGraphicsEffect(shadow)
    
    def paintEvent(self, event):
        # Закруглённый фон (radius 20px)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        path = QPainterPath()
        path.addRoundedRect(QRectF(self.rect()), 20, 20)
        painter.fillPath(path, QBrush(QColor(COLOR_BG)))
    
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
    
    def mouseMoveEvent(self, event):
        if self._drag_pos:
            self.move(event.globalPosition().toPoint() - self._drag_pos)
    
    def mouseReleaseEvent(self, event):
        self._drag_pos = None
    
    def setup_ui(self):
        # === TABS ===
        tab_layout = QHBoxLayout()
        tab_layout.setSpacing(10)
        
        self.tabs = {}
        tab_names = ["Focus", "Sleep", "Sunny"]
        for i, name in enumerate(tab_names):
            btn = QPushButton(name)
            btn.setCheckable(True)
            btn.setChecked(i == 1)
            btn.setFixedHeight(36)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda _, x=i: self.set_tab(x))
            self.tabs[i] = btn
            tab_layout.addWidget(btn, 1)
        
        self.main_layout.addLayout(tab_layout)
        self.main_layout.addSpacing(40)
        
        # === VINYL ===
        self.vinyl = VinylRecord()
        self.main_layout.addWidget(self.vinyl, 0, Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addSpacing(40)
        
        # === INFO ===
        self.title_lbl = QLabel("Lofi Girl")
        self.title_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_lbl.setFont(QFont(self.nunito, 20, QFont.Weight.Bold))
        self.main_layout.addWidget(self.title_lbl)
        
        self.subtitle_lbl = QLabel("chillout · ambient · downtempo")
        self.subtitle_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.subtitle_lbl.setFont(QFont(self.nunito, 12))
        self.main_layout.addWidget(self.subtitle_lbl)
        self.main_layout.addSpacing(35)
        
        # === CONTROLS ===
        ctrl = QHBoxLayout()
        ctrl.setSpacing(35)
        ctrl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.prev_btn = QPushButton()
        self.prev_btn.setFixedSize(50, 50)
        self.prev_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.prev_btn.setIcon(IconGenerator.get_icon("prev", 36))
        self.prev_btn.setIconSize(QSize(28, 28))
        self.prev_btn.clicked.connect(lambda: self.set_tab((self.tab_idx - 1) % len(self.STREAMS)))
        ctrl.addWidget(self.prev_btn)

        self.play_btn = QPushButton()
        self.play_btn.setFixedSize(70, 70)
        self.play_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.play_btn.setIcon(IconGenerator.get_icon("play", 40))
        self.play_btn.setIconSize(QSize(32, 32))
        self.play_btn.clicked.connect(self.toggle_play)
        ctrl.addWidget(self.play_btn)

        self.next_btn = QPushButton()
        self.next_btn.setFixedSize(50, 50)
        self.next_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.next_btn.setIcon(IconGenerator.get_icon("next", 36))
        self.next_btn.setIconSize(QSize(28, 28))
        self.next_btn.clicked.connect(lambda: self.set_tab((self.tab_idx + 1) % len(self.STREAMS)))
        ctrl.addWidget(self.next_btn)
        
        self.main_layout.addLayout(ctrl)
        self.main_layout.addSpacing(35)
        
        # === VISUALIZER ===
        self.visualizer = VisualizerWidget()
        self.main_layout.addWidget(self.visualizer, 0, Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addSpacing(30)
        
        # === VOLUME (ИСПРАВЛЕННЫЙ дизайн) ===
        vol_layout = QHBoxLayout()
        vol_layout.setSpacing(12)
        
        vol_icon = QLabel()
        vol_icon.setPixmap(IconGenerator.get_icon("heart", 24).pixmap(24, 24))
        vol_layout.addWidget(vol_icon)
        
        self.vol_slider = QSlider(Qt.Orientation.Horizontal)
        self.vol_slider.setRange(0, 100)
        self.vol_slider.setValue(70)
        self.vol_slider.setStyleSheet(f"""
            QSlider::groove:horizontal {{
                border: none;
                height: 6px;
                background: {COLOR_WHITE};
                border-radius: 3px;
            }}
            QSlider::handle:horizontal {{
                background: {COLOR_ACCENT};
                border: 2px solid {COLOR_DARK};
                width: 18px;
                margin: -6px 0;
                border-radius: 9px;
            }}
            QSlider::sub-page:horizontal {{
                background: {COLOR_ACCENT};
                border-radius: 3px;
            }}
            QSlider::add-page:horizontal {{
                background: {COLOR_WHITE};
                border-radius: 3px;
            }}
        """)
        self.vol_slider.valueChanged.connect(lambda v: (self.vol_lbl.setText(f"{v}%"), self.audio.setVolume(v / 100.0)))
        vol_layout.addWidget(self.vol_slider)
        
        self.vol_lbl = QLabel("70%")
        self.vol_lbl.setFixedWidth(42)
        vol_layout.addWidget(self.vol_lbl)
        self.main_layout.addLayout(vol_layout)
        self.main_layout.addSpacing(25)
        
        # === TIMER ===
        self.timer_lbl = QLabel("")
        self.timer_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.timer_lbl.setFont(QFont(self.nunito, 10))
        self.main_layout.addWidget(self.timer_lbl)
        self.main_layout.addSpacing(20)
        
        # === FOOTER ===
        footer = QHBoxLayout()
        footer.setSpacing(12)
        
        footer_btns = [
            ("☾ Sleep", self.show_sleep_timer),
            ("⤢ Full", self.toggle_fullscreen),
            ("▭ Mini", self.toggle_mini_mode),
            ("📻 Stations", self.show_stations),
        ]
        
        for text, handler in footer_btns:
            btn = QPushButton(text)
            btn.setFixedHeight(42)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(handler)
            footer.addWidget(btn, 1)
        
        self.main_layout.addLayout(footer)
    
    def setup_player(self):
        self.player = QMediaPlayer(self)
        self.audio = QAudioOutput(self)
        self.player.setAudioOutput(self.audio)
        self.audio.setVolume(0.7)  # 70% громкости
        self.player.setSource(QUrl(self.STREAMS[self.tab_idx]))
        self.player.playbackStateChanged.connect(self.on_state_changed)
        self.player.errorOccurred.connect(self.on_error)
    
    def apply_styles(self):
        self.centralWidget().setStyleSheet(f"""
            QWidget {{
                background-color: {COLOR_BG};
                border-radius: 20px;
            }}
        """)
        
        for i, btn in self.tabs.items():
            active = i == self.tab_idx
            if active:
                btn.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {COLOR_ACCENT};
                        color: {COLOR_DARK};
                        border: 1px solid {COLOR_DARK};
                        border-radius: 18px;
                        font-size: 13px;
                        font-weight: bold;
                    }}
                """)
            else:
                btn.setStyleSheet(f"""
                    QPushButton {{
                        background-color: transparent;
                        color: {COLOR_GREY};
                        border: 1px solid {COLOR_BORDER};
                        border-radius: 18px;
                        font-size: 13px;
                    }}
                """)
        
        self.title_lbl.setStyleSheet(f"color: {COLOR_DARK};")
        self.subtitle_lbl.setStyleSheet(f"color: {COLOR_GREY};")
        self.vol_lbl.setStyleSheet(f"color: {COLOR_GREY}; font-size: 11px;")
        self.timer_lbl.setStyleSheet(f"color: {COLOR_ACCENT};")
        
        footer_style = f"""
            QPushButton {{
                background-color: {COLOR_BG};
                color: {COLOR_DARK};
                border: 1px solid {COLOR_BORDER};
                border-radius: 12px;
                font-size: 12px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                background-color: {COLOR_ACCENT};
            }}
        """
        
        for btn in self.findChildren(QPushButton):
            if btn.text() in ["☾ Sleep", "⤢ Full", "▭ Mini", "📻 Stations"]:
                btn.setStyleSheet(footer_style)
    
    def toggle_play(self):
        if self.loading:
            return
        if self.playing:
            self.player.pause()
        else:
            self.player.play()
    
    def on_state_changed(self, state):
        self.playing = (state == QMediaPlayer.PlaybackState.PlayingState)
        self.vinyl.set_playing(self.playing)
        self.visualizer.set_playing(self.playing)
        
        icon_name = "pause" if self.playing else "play"
        self.play_btn.setIcon(IconGenerator.get_icon(icon_name, 40))
        
        if self.mini_window:
            self.mini_window.update_play_state(self.playing)
    
    def on_error(self, error):
        self.loading = False
    
    def set_tab(self, i):
        if i == self.tab_idx:
            return

        self.tab_idx = i

        for j, btn in self.tabs.items():
            btn.setChecked(j == i)

        was_playing = self.playing
        self.player.stop()
        self.player.setSource(QUrl(self.STREAMS[i]))
        self.title_lbl.setText(self.TITLES[i][0])
        self.subtitle_lbl.setText(self.TITLES[i][1])

        self.apply_styles()

        if was_playing:
            self.player.play()
    
    def apply_sleep_timer(self, minutes):
        if minutes > 0:
            self.timer_lbl.setText(f"☾ Sleep: {minutes} min")
            if self.sleep_timer:
                self.sleep_timer.stop()
            self.sleep_timer = QTimer()
            self.sleep_timer.timeout.connect(self.on_sleep_timeout)
            self.sleep_timer.start(minutes * 60 * 1000)
        else:
            self.timer_lbl.setText("")
            if self.sleep_timer:
                self.sleep_timer.stop()
    
    def show_sleep_timer(self):
        dialog = SleepTimerDialog()
        dialog.setParent(None)
        dialog.setWindowModality(Qt.WindowModality.ApplicationModal)
        x = self.x() + (self.width() - dialog.width()) // 2
        y = self.y() + (self.height() - dialog.height()) // 2
        dialog.move(max(0, x), max(0, y))
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.apply_sleep_timer(dialog.timer_minutes)
    
    def on_sleep_timeout(self):
        if self.sleep_timer:
            self.sleep_timer.stop()
        self.player.stop()
        self.playing = False
        self.vinyl.set_playing(False)
        self.visualizer.set_playing(False)
        self.play_btn.setIcon(IconGenerator.get_icon("play", 40))
        self.timer_lbl.setText("☾ Good night! ♡")
        QTimer.singleShot(3000, lambda: self.timer_lbl.setText(""))
    
    def toggle_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
            self.setFixedSize(400, 840)
        else:
            self.showFullScreen()
    
    def toggle_mini_mode(self):
        if self.mini_window and self.mini_window.isVisible():
            self.mini_window.close()
            self.mini_window = None
            self.show()
        else:
            self.mini_window = MiniPlayerWindow(self)
            self.mini_window.show()
            self.hide()
    
    def show_stations(self):
        dialog = StationsDialog()
        dialog.setParent(None)
        dialog.setWindowModality(Qt.WindowModality.ApplicationModal)
        x = self.x() + (self.width() - dialog.width()) // 2
        y = self.y() + (self.height() - dialog.height()) // 2
        dialog.move(max(0, x), max(0, y))
        if dialog.exec() == QDialog.DialogCode.Accepted:
            if dialog.selected_idx >= 0:
                self.set_tab(dialog.selected_idx)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 10))
    
    window = AnimatedWindow()
    window.show()
    sys.exit(app.exec())
