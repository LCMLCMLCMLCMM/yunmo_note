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
from PyQt6.QtWidgets import QApplication, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QPixmap


class SponsorDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('赞助支持')
        self.setFixedSize(500,600)
        self.setWindowIcon(QIcon("icon.png"))
        
        # 设置深色主题样式
        self.setStyleSheet("""
            QDialog {
                background-color: #2b2b2b;
            }
            QLabel {
                color: #ffffff;
            }
            QPushButton {
                background-color: #3c3f41;
                color: #ffffff;
                border: 1px solid #555555;
                padding: 8px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #4b6eaf;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        # 标题
        title = QLabel('感谢您的支持！')
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)
        
        # 说明文字
        description = QLabel('如果您觉得 Yunmo Note 对您有帮助，\n欢迎通过以下方式赞助支持开发者：')
        description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        description.setStyleSheet("font-size: 14px; margin: 10px;")
        layout.addWidget(description)
        
        # 赞助方式
        methods_label = QLabel('赞助方式：')
        methods_label.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px; margin-top: 20px;")
        layout.addWidget(methods_label)
        
        # 支付宝赞助按钮
        alipay_button = QPushButton('支付宝赞助')
        alipay_button.setStyleSheet("""
            QPushButton {
                background-color: #108ee9;
                color: white;
                border: none;
                padding: 12px;
                font-size: 14px;
                border-radius: 4px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #49a9ee;
            }
        """)
        alipay_button.clicked.connect(self.alipay_sponsor)
        layout.addWidget(alipay_button)
        
        # 微信赞助按钮
        wechat_button = QPushButton('微信赞助')
        wechat_button.setStyleSheet("""
            QPushButton {
                background-color: #29c300;
                color: white;
                border: none;
                padding: 12px;
                font-size: 14px;
                border-radius: 4px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #3bd300;
            }
        """)
        wechat_button.clicked.connect(self.wechat_sponsor)
        layout.addWidget(wechat_button)
        
        # 关闭按钮
        close_button = QPushButton('关闭')
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #3c3f41;
                color: #ffffff;
                border: 1px solid #555555;
                padding: 10px;
                font-size: 14px;
                border-radius: 4px;
                margin: 5px;
                margin-top: 15px;
            }
            QPushButton:hover {
                background-color: #4b6eaf;
            }
        """)
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)
        
        self.setLayout(layout)
        
    def alipay_sponsor(self):
        def wechat_sponsor(self):
            class QRCODE(QDialog):
                def __init__(self, qr_type="alipay"):
                    super().__init__()
                    self.qr_type = qr_type
                    self.initUI()

                def initUI(self):
                    if self.qr_type == "alipay":
                        self.setWindowTitle('支付宝赞助二维码')
                        image_path = 'ZZ10-ALIPAY.jpg'
                    else:
                        self.setWindowTitle('微信赞助二维码')
                        image_path = 'ZZ10.jpg'  # 你的微信二维码路径

                    # 设置合适的窗口大小
                    self.setFixedSize(400, 500)  # 调整为更合适的尺寸

                    layout = QVBoxLayout()

                    qrcode = QLabel()

                    # 加载并拉伸图片
                    pixmap = QPixmap(image_path)
                    if not pixmap.isNull():
                        # 拉伸图片到合适大小，保持宽高比
                        scaled_pixmap = pixmap.scaled(
                            350, 350,  # 目标尺寸
                            Qt.AspectRatioMode.KeepAspectRatio,
                            Qt.TransformationMode.SmoothTransformation
                        )
                        qrcode.setPixmap(scaled_pixmap)
                    else:
                        qrcode.setText("无法加载二维码图片")

                    qrcode.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    layout.addWidget(qrcode)

                    # 添加提示文字
                    tip_label = QLabel("请扫描二维码")
                    tip_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    layout.addWidget(tip_label)

                    self.setLayout(layout)
            QRCODE().exec()
        wechat_sponsor(self)
    def wechat_sponsor(self):
        class QRCODE(QDialog):
            def __init__(self, qr_type="wechat"):
                super().__init__()
                self.qr_type = qr_type
                self.initUI()

            def initUI(self):
                if self.qr_type == "alipay":
                    self.setWindowTitle('支付宝赞助二维码')
                    image_path = 'ZZ10-ALIPAY.jpg'
                else:
                    self.setWindowTitle('微信赞助二维码')
                    image_path = 'ZZ10.jpg'  # 你的微信二维码路径

                # 设置合适的窗口大小
                self.setFixedSize(400, 500)  # 调整为更合适的尺寸

                layout = QVBoxLayout()

                qrcode = QLabel()

                # 加载并拉伸图片
                pixmap = QPixmap(image_path)
                if not pixmap.isNull():
                    # 拉伸图片到合适大小，保持宽高比
                    scaled_pixmap = pixmap.scaled(
                        350, 350,  # 目标尺寸
                        Qt.AspectRatioMode.KeepAspectRatio,
                        Qt.TransformationMode.SmoothTransformation
                    )
                    qrcode.setPixmap(scaled_pixmap)
                else:
                    qrcode.setText("无法加载二维码图片")

                qrcode.setAlignment(Qt.AlignmentFlag.AlignCenter)
                layout.addWidget(qrcode)

                # 添加提示文字
                tip_label = QLabel("请扫描二维码")
                tip_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                layout.addWidget(tip_label)

                self.setLayout(layout)

        QRCODE().exec()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = SponsorDialog()
    dialog.show()
    sys.exit(app.exec())
