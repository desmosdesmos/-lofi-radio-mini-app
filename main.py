#!/usr/bin/env python3
"""
Warm Retro Music Player
A beautiful PyQt6 music player with frameless rounded window,
vinyl animation, and warm retro design.
"""

import sys
import os
import random
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QSlider, QFrame, QGraphicsDropShadowEffect
)
from PyQt6.QtCore import (
    Qt, QTimer, QPropertyAnimation, QEasingCurve, QRectF,
    QUrl, pyqtProperty
)
from PyQt6.QtGui import (
    QPainter, QBrush, QColor, QPen, QPainterPath, QFontDatabase,
    QBitmap, QRadialGradient, QIcon, QPixmap
)
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtSvg import QSvgRenderer


# ═══════════════════════════════════════════════════════════════
# DESIGN SYSTEM
# ═══════════════════════════════════════════════════════════════
COLOR_BG = "#FFF9F0"      # Cream background
COLOR_ACCENT = "#FFC085"  # Orange accent
COLOR_DARK = "#2D3748"    # Dark grey/blue
COLOR_WHITE = "#FFFFFF"   # White

ASSETS_DIR = "assets"


# ═══════════════════════════════════════════════════════════════
# SVG ICON HELPER
# ═══════════════════════════════════════════════════════════════
class SvgIcon(QPixmap):
    """Load SVG file and render as QPixmap with custom color."""
    
    def __init__(self, filepath: str, size: int = 64, color: str = None):
        super().__init__(size, size)
        self.fill(Qt.GlobalColor.transparent)
        
        renderer = QSvgRenderer(filepath)
        if not renderer.isValid():
            return
        
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        if color:
            # Render SVG with custom color using composition mode
            painter.setBrush(QBrush(QColor(color)))
            painter.setPen(Qt.PenStyle.NoPen)
            renderer.render(painter)
        else:
            renderer.render(painter)
        
        painter.end()


# ═══════════════════════════════════════════════════════════════
# VINYL RECORD (Perfect Circle + QPropertyAnimation)
# ═══════════════════════════════════════════════════════════════
class VinylRecord(QFrame):
    def __init__(self):
        super().__init__()
        self.setFixedSize(260, 260)
        self._rotation = 0.0
        
        # Perfect circle using mask
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
    
    def set_playing(self, playing: bool):
        if self.is_playing == playing:
            return
        self.is_playing = playing
        
        if playing:
            if self.rotation_anim.state() == QAbstractAnimation.State.Stopped:
                self.rotation_anim.start()
            elif self.rotation_anim.state() == QAbstractAnimation.State.Paused:
                self.rotation_anim.resume()
        else:
            self.rotation_anim.pause()  # Freeze in place
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        cx, cy = 130, 130
        radius = 120
        
        painter.save()
        painter.translate(cx, cy)
        painter.rotate(self._rotation)
        
        # Vinyl disc gradient
        vinyl_grad = QRadialGradient(0, 0, radius)
        vinyl_grad.setColorAt(0, QColor("#1a202c"))
        vinyl_grad.setColorAt(0.7, QColor("#2d3748"))
        vinyl_grad.setColorAt(1, QColor("#1a202c"))
        
        painter.setBrush(QBrush(vinyl_grad))
        painter.setPen(QPen(QColor(COLOR_DARK), 2))
        painter.drawEllipse(-radius, -radius, radius * 2, radius * 2)
        
        # Grooves
        for r in range(radius - 15, 45, -10):
            painter.setPen(QPen(QColor("#4a5568"), 1))
            painter.drawEllipse(-r, -r, r * 2, r * 2)
        
        painter.restore()
        
        # Center label
        label_r = 48
        label_grad = QRadialGradient(cx, cy, label_r)
        label_grad.setColorAt(0, QColor(COLOR_ACCENT))
        label_grad.setColorAt(1, QColor("#f6ad55"))
        
        painter.setBrush(QBrush(label_grad))
        painter.setPen(QPen(QColor(COLOR_DARK), 2))
        painter.drawEllipse(cx - label_r, cy - label_r, label_r * 2, label_r * 2)
        
        # Inner circle
        painter.setBrush(QBrush(QColor("#ed8936")))
        painter.drawEllipse(cx - 16, cy - 16, 32, 32)
        
        # Center dot
        painter.setBrush(QBrush(QColor(COLOR_BG)))
        painter.drawEllipse(cx - 5, cy - 5, 10, 10)


# ═══════════════════════════════════════════════════════════════
# VISUALIZER (15 bars)
# ═══════════════════════════════════════════════════════════════
class VisualizerWidget(QFrame):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(60)
        self.setMinimumWidth(200)
        self.bars = []
        
        layout = QHBoxLayout(self)
        layout.setSpacing(6)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
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
    
    def set_playing(self, playing: bool):
        self.is_playing = playing
        if playing:
            self.timer.start()
        else:
            self.timer.stop()
            for bar in self.bars:
                bar.setFixedHeight(5)
    
    def _animate(self):
        for bar in self.bars:
            h = random.randint(10, 50)
            bar.setFixedHeight(h)


# ═══════════════════════════════════════════════════════════════
# MAIN WINDOW
# ═══════════════════════════════════════════════════════════════
class WarmRetroPlayer(QMainWindow):
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

    STATION_NAMES = [
        "Drone Zone", "Smooth Chill", "Lofi Girl", "Groove Salad",
        "Space Station", "Deep Space One", "Secret Agent", "Beat Blender",
        "Fluid", "PopTron", "Def Con"
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
    
    # Window sizes
    SIZE_FULL = (400, 800)
    SIZE_MINI = (300, 150)
    
    def __init__(self):
        super().__init__()
        self._drag_pos = None
        self.station_idx = 2  # Start with Lofi Girl
        self.playing = False
        self.is_mini = False
        
        self.setup_window()
        self.setup_ui()
        self.setup_player()
        self.apply_styles()
        
        # Fade in animation
        self.fade_anim = QPropertyAnimation(self, b"windowOpacity")
        self.fade_anim.setDuration(400)
        self.fade_anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.fade_anim.setStartValue(0.0)
        self.fade_anim.setEndValue(1.0)
        self.fade_anim.start()
    
    def setup_window(self):
        """Setup frameless, translucent window."""
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(*self.SIZE_FULL)
        
        central = QWidget()
        self.setCentralWidget(central)
        self.main_layout = QVBoxLayout(central)
        self.main_layout.setContentsMargins(24, 24, 24, 24)
        self.main_layout.setSpacing(0)
        
        # Window shadow
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(60)
        shadow.setYOffset(30)
        shadow.setColor(QColor(0, 0, 0, 50))
        central.setGraphicsEffect(shadow)
    
    def paintEvent(self, event):
        """Draw rounded rectangle background."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        path = QPainterPath()
        path.addRoundedRect(QRectF(self.rect()), 25, 25)
        painter.fillPath(path, QBrush(QColor(COLOR_BG)))
    
    def mousePressEvent(self, event):
        """Start window drag."""
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
    
    def mouseMoveEvent(self, event):
        """Handle window drag."""
        if self._drag_pos:
            self.move(event.globalPosition().toPoint() - self._drag_pos)
    
    def mouseReleaseEvent(self, event):
        """End window drag."""
        self._drag_pos = None
    
    def setup_ui(self):
        """Build the UI components."""
        # === TOP TABS ===
        tab_layout = QHBoxLayout()
        tab_layout.setSpacing(10)
        
        self.tab_buttons = {}
        for i, name in enumerate(self.STATION_NAMES):
            btn = QPushButton(name)
            btn.setCheckable(True)
            btn.setChecked(i == self.station_idx)
            btn.setFixedHeight(36)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda _, x=i: self.set_station(x))
            self.tab_buttons[i] = btn
            tab_layout.addWidget(btn, 1)
        
        self.main_layout.addLayout(tab_layout)
        self.main_layout.addSpacing(30)
        
        # === VINYL RECORD ===
        self.vinyl = VinylRecord()
        self.main_layout.addWidget(self.vinyl, 0, Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addSpacing(30)
        
        # === TRACK INFO ===
        self.title_label = QLabel(self.TITLES[self.station_idx][0])
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet(f"color: {COLOR_DARK}; font-size: 20px; font-weight: bold;")
        self.main_layout.addWidget(self.title_label)
        
        self.subtitle_label = QLabel(self.TITLES[self.station_idx][1])
        self.subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.subtitle_label.setStyleSheet(f"color: {COLOR_DARK}; font-size: 12px;")
        self.main_layout.addWidget(self.subtitle_label)
        self.main_layout.addSpacing(25)
        
        # === CONTROLS ===
        ctrl_layout = QHBoxLayout()
        ctrl_layout.setSpacing(30)
        ctrl_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Previous
        self.prev_btn = QPushButton()
        self.prev_btn.setFixedSize(50, 50)
        self.prev_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.prev_btn.clicked.connect(lambda: self.set_station((self.station_idx - 1) % len(self.STREAMS)))
        ctrl_layout.addWidget(self.prev_btn)
        
        # Play/Pause (Hero button)
        self.play_btn = QPushButton()
        self.play_btn.setFixedSize(80, 80)
        self.play_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.play_btn.clicked.connect(self.toggle_play)
        ctrl_layout.addWidget(self.play_btn)
        
        # Next
        self.next_btn = QPushButton()
        self.next_btn.setFixedSize(50, 50)
        self.next_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.next_btn.clicked.connect(lambda: self.set_station((self.station_idx + 1) % len(self.STREAMS)))
        ctrl_layout.addWidget(self.next_btn)
        
        self.main_layout.addLayout(ctrl_layout)
        self.main_layout.addSpacing(20)
        
        # === VISUALIZER ===
        self.visualizer = VisualizerWidget()
        self.main_layout.addWidget(self.visualizer, 0, Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addSpacing(20)
        
        # === VOLUME SLIDER ===
        vol_layout = QHBoxLayout()
        vol_layout.setSpacing(12)
        vol_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Heart icon
        heart_label = QLabel()
        try:
            heart_pixmap = QPixmap(f"{ASSETS_DIR}/heart.svg")
            if not heart_pixmap.isNull():
                heart_pixmap = heart_pixmap.scaled(24, 24, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransform)
            else:
                heart_pixmap = QPixmap(24, 24)
                heart_pixmap.fill(QColor(COLOR_ACCENT))
        except:
            heart_pixmap = QPixmap(24, 24)
            heart_pixmap.fill(QColor(COLOR_ACCENT))
        heart_label.setPixmap(heart_pixmap)
        vol_layout.addWidget(heart_label)
        
        self.vol_slider = QSlider(Qt.Orientation.Horizontal)
        self.vol_slider.setRange(0, 100)
        self.vol_slider.setValue(70)
        self.vol_slider.setFixedWidth(180)
        self.vol_slider.valueChanged.connect(lambda v: self.vol_label.setText(f"{v}%"))
        vol_layout.addWidget(self.vol_slider)
        
        self.vol_label = QLabel("70%")
        self.vol_label.setStyleSheet(f"color: {COLOR_DARK}; font-size: 12px; min-width: 35px;")
        vol_layout.addWidget(self.vol_label)
        
        self.main_layout.addLayout(vol_layout)
        self.main_layout.addStretch(1)
        
        # === FOOTER BUTTONS ===
        footer_layout = QHBoxLayout()
        footer_layout.setSpacing(12)
        
        # Mini/Expand button
        self.mini_btn = QPushButton("▭ Mini")
        self.mini_btn.setFixedHeight(42)
        self.mini_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.mini_btn.clicked.connect(self.toggle_mini_mode)
        footer_layout.addWidget(self.mini_btn, 1)
        
        self.main_layout.addLayout(footer_layout)
    
    def setup_player(self):
        """Setup media player."""
        self.player = QMediaPlayer(self)
        self.audio = QAudioOutput(self)
        self.player.setAudioOutput(self.audio)
        self.audio.setVolume(0.7)
        self.player.setSource(QUrl(self.STREAMS[self.station_idx]))
        self.player.playbackStateChanged.connect(self.on_state_changed)
        self.player.errorOccurred.connect(self.on_error)
    
    def apply_styles(self):
        """Apply all stylesheets."""
        # Tab buttons
        for i, btn in self.tab_buttons.items():
            active = i == self.station_idx
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
                        color: {COLOR_DARK};
                        border: 1px solid {COLOR_DARK};
                        border-radius: 18px;
                        font-size: 13px;
                    }}
                """)
        
        # Volume slider - Thick groove, thick handle
        self.vol_slider.setStyleSheet(f"""
            QSlider::groove:horizontal {{
                border: none;
                height: 10px;
                background: {COLOR_WHITE};
                border-radius: 5px;
            }}
            QSlider::handle:horizontal {{
                background: {COLOR_WHITE};
                border: 3px solid {COLOR_DARK};
                width: 24px;
                margin: -7px 0;
                border-radius: 12px;
            }}
            QSlider::sub-page:horizontal {{
                background: {COLOR_ACCENT};
                border-radius: 5px;
            }}
            QSlider::add-page:horizontal {{
                background: {COLOR_WHITE};
                border-radius: 5px;
            }}
        """)
        
        # Previous button
        self.prev_btn.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                border: 2px solid {COLOR_DARK};
                border-radius: 25px;
            }}
            QPushButton:hover {{
                background: {COLOR_ACCENT};
            }}
        """)
        self.prev_btn.setIcon(self.load_icon("prev.svg", 28))
        self.prev_btn.setIconSize(QSize(28, 28))
        
        # Play/Pause button (Hero)
        self.play_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLOR_ACCENT};
                border: 2px solid {COLOR_DARK};
                border-radius: 40px;
            }}
            QPushButton:hover {{
                background-color: #ffb16e;
            }}
            QPushButton:pressed {{
                background-color: #ff9f5c;
            }}
        """)
        self.play_btn.setIcon(self.load_icon("play.svg", 40))
        self.play_btn.setIconSize(QSize(40, 40))
        
        # Next button
        self.next_btn.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                border: 2px solid {COLOR_DARK};
                border-radius: 25px;
            }}
            QPushButton:hover {{
                background: {COLOR_ACCENT};
            }}
        """)
        self.next_btn.setIcon(self.load_icon("next.svg", 28))
        self.next_btn.setIconSize(QSize(28, 28))
        
        # Mini button
        self.mini_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLOR_BG};
                color: {COLOR_DARK};
                border: 1px solid {COLOR_DARK};
                border-radius: 12px;
                font-size: 12px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                background-color: {COLOR_ACCENT};
            }}
        """)
    
    def load_icon(self, filename: str, size: int) -> QIcon:
        """Load SVG icon from assets folder."""
        filepath = f"{ASSETS_DIR}/{filename}"
        if os.path.exists(filepath):
            pixmap = QPixmap(filepath)
            if not pixmap.isNull():
                pixmap = pixmap.scaled(size, size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransform)
                return QIcon(pixmap)
        # Fallback: create empty icon
        return QIcon(QPixmap(size, size))
    
    def toggle_play(self):
        """Toggle play/pause."""
        if self.playing:
            self.player.pause()
        else:
            self.player.play()
    
    def on_state_changed(self, state):
        """Handle playback state changes."""
        from PyQt6.QtMultimedia import QMediaPlayer
        
        self.playing = (state == QMediaPlayer.PlaybackState.PlayingState)
        
        # Update vinyl rotation
        self.vinyl.set_playing(self.playing)
        
        # Update visualizer
        self.visualizer.set_playing(self.playing)
        
        # Update play/pause icon
        icon_name = "pause.svg" if self.playing else "play.svg"
        self.play_btn.setIcon(self.load_icon(icon_name, 40))
    
    def on_error(self, error):
        """Handle player errors."""
        print(f"Player error: {error}")
        self.playing = False
    
    def set_station(self, idx: int):
        """Switch to a different station."""
        if idx == self.station_idx:
            return
        
        self.station_idx = idx
        
        # Update tab buttons
        for i, btn in self.tab_buttons.items():
            btn.setChecked(i == idx)
        
        # Update labels
        self.title_label.setText(self.TITLES[idx][0])
        self.subtitle_label.setText(self.TITLES[idx][1])
        
        # Switch stream
        was_playing = self.playing
        self.player.stop()
        self.player.setSource(QUrl(self.STREAMS[idx]))
        
        self.apply_styles()
        
        if was_playing:
            QTimer.singleShot(500, self.player.play)
    
    def toggle_mini_mode(self):
        """Toggle between full and mini mode."""
        if self.is_mini:
            # Restore to full size
            self.is_mini = False
            self.setFixedSize(*self.SIZE_FULL)
            
            # Show hidden widgets
            self.vinyl.show()
            self.visualizer.show()
            self.title_label.show()
            self.subtitle_label.show()
            self.mini_btn.setText("▭ Mini")
            
            self.apply_styles()
        else:
            # Switch to mini mode
            self.is_mini = True
            self.setFixedSize(*self.SIZE_MINI)
            
            # Hide large widgets
            self.vinyl.hide()
            self.visualizer.hide()
            self.title_label.hide()
            self.subtitle_label.hide()
            self.mini_btn.setText("⤢ Full")


# ═══════════════════════════════════════════════════════════════
# MAIN ENTRY POINT
# ═══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    # Check for assets
    if not os.path.exists(ASSETS_DIR):
        print(f"Error: '{ASSETS_DIR}' folder not found!")
        print("Please run 'python setup_assets.py' first.")
        sys.exit(1)
    
    # Load font
    font_path = f"{ASSETS_DIR}/Nunito-Bold.ttf"
    if os.path.exists(font_path):
        font_id = QFontDatabase.addApplicationFont(font_path)
        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            app_font = QFont(font_family, 10)
        else:
            app_font = QFont("Segoe UI", 10)
    else:
        print(f"Warning: Font '{font_path}' not found. Using system font.")
        app_font = QFont("Segoe UI", 10)
    
    app = QApplication(sys.argv)
    app.setFont(app_font)
    
    window = WarmRetroPlayer()
    window.show()
    
    sys.exit(app.exec())
