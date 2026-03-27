#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import subprocess
from urllib.parse import quote

from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QVBoxLayout
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont


class SearchBox(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.setup_window_properties()
        self.center()

    def setup_ui(self):
        # 创建一个输入框
        self.edit = QLineEdit(self)
        self.edit.setPlaceholderText("Input here...")
        self.edit.setFont(QFont("HarmonyOS Sans", 14))
        self.edit.returnPressed.connect(self.on_search)

        # 布局
        layout = QVBoxLayout()
        layout.addWidget(self.edit)
        self.setLayout(layout)

    def setup_window_properties(self):
        # 无边框、固定大小、不可调整大小
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setFixedSize(QSize(600, 60))   # 宽度600，高度60，适合搜索框

        # 设置背景色（可选，便于看清窗口边界）
        self.setStyleSheet("""
            QWidget {
                background-color: #2b2b2b;
                border-radius: 8px;
            }
            QLineEdit {
                background-color: #aaaaaa;
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 5px;
            }
        """)

        # 确保窗口接收焦点（初始自动获得焦点）
        self.setFocusPolicy(Qt.StrongFocus)

    def center(self):
        """将窗口置于屏幕正中央"""
        screen_geometry = QApplication.primaryScreen().geometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)

    def focusOutEvent(self, event):
        """当窗口失去焦点时（点击窗口外部）关闭程序"""
        self.close()

    def on_search(self):
        """当用户按下回车时，调用 Vivaldi 打开 Bing 搜索"""
        text = self.edit.text().strip()
        if not text:
            # 如果输入为空，直接关闭窗口
            self.close()
            return

        if text.startswith(":"):
            subprocess.Popen(text.lstrip(":").split(" "), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            self.close()
            return

        # 构造 Bing 搜索 URL
        encoded_text = quote(text)
        url = f"https://cn.bing.com/search?q={encoded_text}"

        # 启动 Vivaldi 浏览器（不等待返回）
        try:
            subprocess.Popen(["vivaldi", url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except FileNotFoundError:
            # 如果 vivaldi 命令不存在，提示用户（静默关闭）
            pass

        # 关闭搜索窗口
        self.close()

    def keyPressEvent(self, event):
        """可选：按 ESC 键也关闭窗口"""
        if event.key() == Qt.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(event)


def main():
    app = QApplication(sys.argv)

    # 设置应用程序名称（非必须）
    app.setApplicationName("Search Bar")

    window = SearchBox()
    window.show()

    # 窗口显示后自动获得焦点，以便直接输入
    window.edit.setFocus()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
