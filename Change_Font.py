#// auth_ Noobj2
#// Copyright (c) 2020-2023 Noobj2

from os.path import dirname
import webbrowser
from aqt.webview import AnkiWebView
from aqt import mw, colors
from aqt.qt import *
from aqt.theme import theme_manager
from aqt.utils import showInfo
from anki import version
import anki
from anki.utils import is_mac, is_win
anki_version = int(version.replace('.', ''))

config = mw.addonManager.getConfig(__name__)

def refreshConfig():
    global C_font, C_fontSize, C_fallbackFont
    C_font = config["Interface Font"]
    C_fontSize = config["Font Size"]
    C_fallbackFont = config["Fallback Font"]

class FontDialog(QDialog):
    def __init__(self, parent=None):
        super(FontDialog, self).__init__(parent)
        self.mainWindow()
    def mainWindow(self):
        addon_path = dirname(__file__)
        self.choose_font()
        self.setWindowFlags(Qt.WindowType.MSWindowsFixedSizeDialogHint)
        self.setLayout(self.layout)
        self.setWindowTitle("Anki - Change Font")
        self.setWindowIcon(QIcon(addon_path + "/icon.png"))

    def choose_font(self):
        addon_path = dirname(__file__)
        refreshConfig()
        font_label = QLabel("Font: ")
        font_label.setFixedWidth(100)
        self.interface_font = QFontComboBox()
        self.interface_font.setFixedWidth(200)
        self.interface_font.setCurrentFont(QFont(C_font))
        fallback_font_label = QLabel("Fallback font: ")
        fallback_font_label.setFixedWidth(100)
        self.interface_fallback_font = QFontComboBox()
        self.interface_fallback_font.setFixedWidth(200)
        self.interface_fallback_font.setCurrentFont(QFont(C_fallbackFont))
        size_label = QLabel("Font Size: ")
        size_label.setFixedWidth(100)
        self.font_size = QSpinBox()
        self.font_size.setFixedWidth(200)
        self.font_size.setValue(C_fontSize)
        self.font_size.setSuffix("px")
        apply_button = QPushButton("&Apply")
        apply_button.clicked.connect(lambda: self.onApply())
        apply_button.clicked.connect(lambda: self.hide())
        restore_button = QPushButton("&Default")
        restore_button.clicked.connect(lambda: self.restore_defaults())
        restore_button.clicked.connect(lambda: self.hide())
        cancel_button = QPushButton("&Cancel")
        cancel_button.clicked.connect(lambda: self.hide())
        buyMeACoffee_button = QPushButton()
        buyMeACoffee_button.setIcon(QIcon(addon_path + "/bmac.png"))
        buyMeACoffee_button.setIconSize(QSize(130,40))
        buyMeACoffee_button.setGeometry(QRect(1030, 500, 161, 61))
        buyMeACoffee_button.clicked.connect(lambda: webbrowser.open('https://www.buymeacoffee.com/noobj2'))
        font_line = QHBoxLayout()
        font_line.addWidget(font_label)
        font_line.addStretch()
        font_line.addWidget(self.interface_font)
        fallback_font_line = QHBoxLayout()
        fallback_font_line.addWidget(fallback_font_label)
        fallback_font_line.addStretch()
        fallback_font_line.addWidget(self.interface_fallback_font)
        size_line = QHBoxLayout()
        size_line.addWidget(size_label)
        size_line.addStretch()
        size_line.addWidget(self.font_size)
        button_line = QHBoxLayout()
        button_line.addWidget(apply_button)
        button_line.addWidget(restore_button)
        button_line.addWidget(cancel_button)
        buyMeACoffee_line = QHBoxLayout()
        buyMeACoffee_line.addWidget(buyMeACoffee_button)
        self.layout = QVBoxLayout()
        self.layout.addLayout(font_line)
        self.layout.addLayout(fallback_font_line)
        self.layout.addLayout(size_line)
        self.layout.addLayout(button_line)
        self.layout.addLayout(buyMeACoffee_line)

    def onApply(self):
        conf = {
        "Interface Font": self.interface_font.currentFont().family(),
        "Fallback Font": self.interface_fallback_font.currentFont().family(),
        "Font Size": self.font_size.value()
        }
        mw.addonManager.writeConfig(__name__, conf)
        showInfo("Changes will take effect after you restart anki.", title="Anki - Change Font")

    def restore_defaults(self):
        if is_win:
            font = "Segoe UI"
            fallback_font = "Apple Color Emoji"
            font_size = 12
        elif is_mac:
            font = "Helvetica"
            fallback_font = "Apple Color Emoji"
            font_size = 15
        else:
            font = "Segoe UI"
            fallback_font = "Apple Color Emoji"
            font_size = 14
        conf = {
        "Interface Font": font,
        "Fallback Font": fallback_font,
        "Font Size": font_size
        }
        mw.addonManager.writeConfig(__name__, conf)
        showInfo("Changes will take effect after you restart anki.", title="Anki - Change Font")

def standard_css_new(self) -> str:
    color_hl = theme_manager.var(colors.BORDER_FOCUS)

    family = config["Interface Font"]
    fallback_family = config["Fallback Font"]
    font_size = config["Font Size"]

    if is_win:
        # T: include a font for your language on Windows, eg: "Segoe UI", "MS Mincho"
        button_style = f"""
        button {{ font-family: {family}, '{fallback_family}'; }}
        """
        font = f"font-family: {family}, '{fallback_family}';"
    elif is_mac:
        font = f'font-family:"{family}", "{fallback_family}";'
        button_style = """
        button {
        --canvas: #fff;
        -webkit-appearance: none;
        background: var(--canvas);
        border-radius: var(--border-radius);
        padding: 3px 12px;
        border: 0.5px solid var(--border);
        box-shadow: 0px 1px 3px var(--border-subtle);
        font-family: %s
        }
        .night-mode button { --canvas: #606060; --fg: #eee; }
        """ % family
    else:
        font = f'font-family: "{family}", "{fallback_family}", sans-serif;'
        button_style = """
        /* Buttons */
        button{{
            font-family: "{family}", "{fallback_family}", sans-serif;
        }}
        /* Input field focus outline */
        textarea:focus, input:focus, input[type]:focus, .uneditable-input:focus,
        div[contenteditable="true"]:focus {{
            outline: 0 none;
            border-color: {color_hl};
        }}
        """.format(
            family=family,
            fallback_family=fallback_family,
            color_hl=color_hl
        )

    zoom = self.app_zoom_factor()

    return f"""
    body {{ zoom: {zoom}; background-color: var(--canvas); font-size: {font_size}px }}
    html {{ {font} }}
    {button_style}
    :root {{ --canvas: {colors.CANVAS["light"]} }}
    :root[class*=night-mode] {{ --canvas: {colors.CANVAS["dark"]} }}
    """

def open_window():
    font_dialog = FontDialog()
    font_dialog.exec()

action = QAction("Change Interface &Font", mw)
action.triggered.connect(open_window)
mw.form.menuTools.addAction(action)
mw.addonManager.setConfigAction(__name__, open_window)
AnkiWebView.standard_css = standard_css_new
