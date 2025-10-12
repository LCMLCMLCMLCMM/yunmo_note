#
# Yunmo Note - A simple yet powerful text editor.
# Copyright (C) 2024–2025  LCM_MC (https://github.com/LCMLCMLCMLCMM)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

import sys
from PyQt6.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
import requests as req
import webbrowser

version = "12.0.1"

class UpdateDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("检查更新")
        self.setFixedSize(400, 150)
        # 如果没有图标文件，可以注释掉下面这行
        # self.setWindowIcon(QIcon("icon.png"))
        self.setStyleSheet("background-color: #2b2b2b; color: white;")
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        self.label = QLabel("正在检查更新...")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("font-size: 16px;")
        layout.addWidget(self.label)
        
        # 调用更新检查
        self.check_update()
        
    def check_update(self):
        try:
            # 模拟网络请求（实际使用时取消注释下面的行）
            # data = req.get("https://bluish-hydrogeologic-cathie.ngrok-free.dev/Update-data.txt", timeout=5)
            # 模拟响应
            data_text = "12.0.1"  # 模拟已经是最新版本
            
            if data_text.strip() == version:
                self.label.setText("当前已为最新版本")
                self.label.setStyleSheet("font-size: 16px; color: #00ff00;")
            else:
                self.label.setText("有新版本可用")
                self.label.setStyleSheet("font-size: 16px; color: #ffcc00;")
                dt = req.get("https://bluish-hydrogeologic-cathie.ngrok-free.dev/File-data.txt", timeout=5)
                if dt.text == "CANNOT-DOWNLOAD":
                    self.label.setText("无法下载更新：新版本内测中或您没有权限下载。")
                else:
                    self.label.setText("即将下载更新")
                    webbrowser.open(dt.text)
        except Exception as e:
            self.label.setText(f"检查更新失败: {str(e)}")
            self.label.setStyleSheet("font-size: 14px; color: #ff0000;")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    update_dialog = UpdateDialog()
    update_dialog.show()
    sys.exit(app.exec())
