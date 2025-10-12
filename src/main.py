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
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtPrintSupport import *
import os
import re
from concurrent.futures import ThreadPoolExecutor
import subprocess
import platform
import threading

#本程序仅为Windows系统开发

class yumonote(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        # 属性
        self.setWindowTitle('Yunmo Note 12')
        self.setGeometry(100, 100, 800, 600)

        #创建中央部件和布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        #textedit
        self.textedit = QTextEdit()
        layout.addWidget(self.textedit)

        # menubar
        self.menubar = QMenuBar()
        self.setMenuBar(self.menubar)
        self.file_menu = self.menubar.addMenu('文件')
        self.file_menu.addAction('新建', self.new_file)
        self.file_menu.addAction('打开', self.open_file)
        self.file_menu.addAction('保存', self.save_file)
        self.file_menu.addAction('保存为', self.save_as_file)
        self.file_menu.addAction('设置', self.set)
        self.file_menu.addAction('退出', self.close)

        self.edit_menu = self.menubar.addMenu('编辑')
        self.edit_menu.addAction('撤销', self.undo)
        self.edit_menu.addAction('重做', self.redo)
        self.edit_menu.addAction('剪切', self.cut)
        self.edit_menu.addAction('复制', self.copy)
        self.edit_menu.addAction('粘贴', self.paste)
        self.edit_menu.addAction('查找', self.find)
        self.edit_menu.addAction('替换', self.replace)
        self.edit_menu.addAction('全选', self.select_all)

        self.view_menu = self.menubar.addMenu('视图')
        self.view_menu.addAction('缩放', self.zoom)
        self.view_menu.addAction('全屏/取消全屏', self.fullscreen)

        self.help_menu = self.menubar.addMenu('关于')
        self.help_menu.addAction('关于 YunmoNote', self.about)
        self.help_menu.addAction('帮助', self.help)
        self.help_menu.addAction('检查更新', self.check_update)
        self.help_menu.addAction('反馈', self.feedback)
        self.help_menu.addAction('赞助', self.sponsor)
        self.help_menu.addAction('BiliBili', self.blbl)
        self.help_menu.addAction('GitHub', self.github)
        self.help_menu.addAction('关于 Qt', self.about_qt)
        self.sizea = 14
        self.setStyleSheet('''
            QMainWindow {
                background-color: #2b2b2b;
            }
            QMenuBar {
                background-color: #3c3f41;
                color: #ffffff;
                border-bottom: 1px solid #555555;
            }
            QMenuBar::item {
                background: transparent;
                padding: 5px 10px;
            }
            QMenuBar::item:selected {
                background: #4b6eaf;
            }
            QMenuBar::item:pressed {
                background: #4b6eaf;
            }
            QMenu {
                background-color: #3c3f41;
                color: #ffffff;
                border: 1px solid #555555;
            }
            QMenu::item {
                padding: 5px 20px;
            }
            QMenu::item:selected {
                background-color: #4b6eaf;
            }
            QTextEdit {
                background-color: #2b2b2b;
                border: 1px solid #555555;
                padding: 5px;
                color: #ffffff;
                selection-background-color: #4b6eaf;
                selection-color: #ffffff;
                font-size: 14px;
            }
        ''')
        self.filename = None
        self.show()
    def new_file(self):
        self.textedit.clear()
        self.setWindowTitle('Untitled - Yunmonote 12')
        self.filename = None

    def open_file(self):
        filename = QFileDialog.getOpenFileName(self, '打开文件', '', 'Text Files (*.txt);;All Files (*)')[0]
        if filename:
            with open(filename, 'r') as f:
                self.textedit.setText(f.read())
            self.setWindowTitle(os.path.basename(filename) + ' - Yunmonote 12')
            self.filename = filename

    def save_file(self):
        if self.filename is None:
            self.save_as_file()
        else:
            with open(self.filename, 'w') as f:
                f.write(self.textedit.toPlainText())
            self.setWindowTitle(os.path.basename(self.filename) + ' - Yunmonote 12')

    def save_as_file(self):
        filename = QFileDialog.getSaveFileName(self, '保存文件', '', 'Text Files (*.txt);;All Files (*)')[0]
        if filename:
            with open(filename, 'w') as f:
                f.write(self.textedit.toPlainText())
            self.setWindowTitle(os.path.basename(filename) + ' - Yunmonote 12')
            self.filename = filename

    def set(self):
        a = SettingsDialog(self)
        a.exec()

    def undo(self):
        self.textedit.undo()

    def redo(self):
        self.textedit.redo()

    def cut(self):
        self.textedit.cut()

    def copy(self):
        self.textedit.copy()

    def paste(self):
        self.textedit.paste()

    def find(self):
        # 创建查找对话框
        dialog = FindReplaceDialog(self.textedit, self)
        dialog.show_find()

    def replace(self):
        # 创建替换对话框
        dialog = FindReplaceDialog(self.textedit, self)
        dialog.show_replace()

    def select_all(self):
        self.textedit.selectAll()

    def zoom(self):
        QMessageBox.information(self, '缩放', '暂不支持')

    def fullscreen(self):
        self.toggle_fullscreen()

    def toggle_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def about(self):
        QMessageBox.information(self, '关于 YunmoNote', '版本:12.0.1-B\n测试版')

    def help(self):
        threading.Thread(target=self.mailto).start()

    def feedback(self):
        threading.Thread(target=self.mailto).start()

    def sponsor(self):

        os.system("pythonw.exe zz.py")

    def check_update(self):
        os.system("pythonw.exe gx.py")

    def blbl(self):
        QDesktopServices.openUrl(QUrl('https://space.bilibili.com/3493268817971411'))

    def github(self):
        QDesktopServices.openUrl(QUrl('https://github.com/LCMLCMLCMLCMM/'))

    def about_qt(self):
        QMessageBox.aboutQt(self, '关于 Qt', 'Qt 6.8.1')

    def close(self):
        if QMessageBox.question(self, '退出', '确定要退出吗？') == QMessageBox.Yes:
            sys.exit()
    def mailto(self):
        QDesktopServices.openUrl(QUrl('mailto://liuchimo@outlook.com'))




class FindReplaceDialog(QDialog):
    def __init__(self, text_edit, parent=None):
        super().__init__(parent)
        self.text_edit = text_edit
        self.parent = parent
        self.matches = []
        self.current_match_index = -1
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle('查找和替换')
        self.setModal(False)
        self.resize(450, 200)
        
        # 设置样式表
        self.setStyleSheet('''
            QDialog {
                background-color: #2b2b2b;
            }
            QLabel {
                color: #ffffff;
                font-size: 12px;
            }
            QLineEdit {
                background-color: #3c3f41;
                border: 1px solid #555555;
                color: #ffffff;
                padding: 5px;
                border-radius: 4px;
            }
            QPushButton {
                background-color: #3c3f41;
                border: 1px solid #555555;
                color: #ffffff;
                padding: 6px 12px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #4b6eaf;
                border: 1px solid #4b6eaf;
            }
            QPushButton:pressed {
                background-color: #3a5a8a;
                border: 1px solid #3a5a8a;
            }
            QCheckBox {
                color: #ffffff;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
            }
            QCheckBox::indicator:unchecked {
                border: 1px solid #555555;
                background-color: #3c3f41;
            }
            QCheckBox::indicator:checked {
                border: 1px solid #4b6eaf;
                background-color: #4b6eaf;
            }
        ''')
        
        # 创建布局
        layout = QVBoxLayout()
        layout.setSpacing(10)
        
        # 查找框
        find_layout = QHBoxLayout()
        find_label = QLabel('查找:')
        find_label.setFixedWidth(50)
        self.find_edit = QLineEdit()
        self.find_edit.setPlaceholderText("输入要查找的文本")
        find_layout.addWidget(find_label)
        find_layout.addWidget(self.find_edit)
        layout.addLayout(find_layout)
        
        # 替换框
        replace_layout = QHBoxLayout()
        replace_label = QLabel('替换:')
        replace_label.setFixedWidth(50)
        self.replace_edit = QLineEdit()
        self.replace_edit.setPlaceholderText("输入替换文本")
        replace_layout.addWidget(replace_label)
        replace_layout.addWidget(self.replace_edit)
        layout.addLayout(replace_layout)
        
        # 选项
        options_layout = QHBoxLayout()
        self.case_sensitive = QCheckBox('区分大小写')
        self.whole_words = QCheckBox('全词匹配')
        options_layout.addWidget(self.case_sensitive)
        options_layout.addWidget(self.whole_words)
        options_layout.addStretch()
        layout.addLayout(options_layout)
        
        # 按钮
        buttons_layout = QGridLayout()
        
        self.find_next_btn = QPushButton('查找下一个')
        self.find_prev_btn = QPushButton('查找上一个')
        self.replace_next_btn = QPushButton('替换下一个')
        self.replace_all_btn = QPushButton('替换全部')
        self.close_btn = QPushButton('关闭')
        
        buttons_layout.addWidget(self.find_next_btn, 0, 0)
        buttons_layout.addWidget(self.find_prev_btn, 0, 1)
        buttons_layout.addWidget(self.replace_next_btn, 1, 0)
        buttons_layout.addWidget(self.replace_all_btn, 1, 1)
        buttons_layout.addWidget(self.close_btn, 2, 0, 1, 2)
        
        layout.addLayout(buttons_layout)
        
        self.setLayout(layout)
        
        # 连接信号和槽
        self.find_next_btn.clicked.connect(self.find_next)
        self.find_prev_btn.clicked.connect(self.find_prev)
        self.replace_next_btn.clicked.connect(self.replace_next)
        self.replace_all_btn.clicked.connect(self.replace_all)
        self.close_btn.clicked.connect(self.close)
        self.find_edit.textChanged.connect(self.reset_search)
        
    def show_find(self):
        self.replace_edit.setEnabled(False)
        self.replace_next_btn.setEnabled(False)
        self.replace_all_btn.setEnabled(False)
        self.show()
        
    def show_replace(self):
        self.replace_edit.setEnabled(True)
        self.replace_next_btn.setEnabled(True)
        self.replace_all_btn.setEnabled(True)
        self.show()
        
    def reset_search(self):
        self.matches = []
        self.current_match_index = -1
        
    def find_matches(self):
        if not self.matches:
            text = self.text_edit.toPlainText()
            search_text = self.find_edit.text()
            
            if not search_text:
                return []
                
            flags = 0 if self.case_sensitive.isChecked() else re.IGNORECASE
            
            if self.whole_words.isChecked():
                pattern = r'\b' + re.escape(search_text) + r'\b'
            else:
                pattern = re.escape(search_text)
                
            self.matches = []
            for match in re.finditer(pattern, text, flags):
                self.matches.append((match.start(), match.end()))
                
        return self.matches
        
    def find_next(self):
        matches = self.find_matches()
        if not matches:
            QMessageBox.information(self, '查找', '未找到匹配项')
            return
            
        # 更新当前匹配索引
        self.current_match_index += 1
        if self.current_match_index >= len(matches):
            self.current_match_index = 0
            
        # 高亮匹配项
        self.highlight_match(self.current_match_index)
        
    def find_prev(self):
        matches = self.find_matches()
        if not matches:
            QMessageBox.information(self, '查找', '未找到匹配项')
            return
            
        # 更新当前匹配索引
        self.current_match_index -= 1
        if self.current_match_index < 0:
            self.current_match_index = len(matches) - 1
            
        # 高亮匹配项
        self.highlight_match(self.current_match_index)
        
    def highlight_match(self, index):
        if 0 <= index < len(self.matches):
            start, end = self.matches[index]
            cursor = self.text_edit.textCursor()
            cursor.setPosition(start)
            cursor.setPosition(end, QTextCursor.MoveMode.KeepAnchor)
            self.text_edit.setTextCursor(cursor)
            
    def replace_next(self):
        # 如果还没有查找过，先执行查找
        if not self.matches:
            self.find_next()
            return
            
        # 替换当前选中的匹配项
        cursor = self.text_edit.textCursor()
        if cursor.hasSelection():
            replace_text = self.replace_edit.text()
            cursor.insertText(replace_text)
            
            # 更新匹配项位置信息
            self.matches = []
            self.current_match_index = -1
            QMessageBox.information(self, '替换', '已替换选中的匹配项')
        else:
            # 如果没有选中，执行查找下一个
            self.find_next()
            
    def replace_all(self):
        search_text = self.find_edit.text()
        replace_text = self.replace_edit.text()
        
        if not search_text:
            QMessageBox.warning(self, '替换', '请输入要查找的文本')
            return
            
        # 使用多线程执行替换全部操作
        self.executor = ThreadPoolExecutor(max_workers=1)
        future = self.executor.submit(self.perform_replace_all, search_text, replace_text)
        future.add_done_callback(self.replace_all_finished)
        
    def perform_replace_all(self, search_text, replace_text):
        # 在后台线程中执行替换全部
        content = self.text_edit.toPlainText()
        
        # 构建正则表达式
        flags = 0 if self.case_sensitive.isChecked() else re.IGNORECASE
        if self.whole_words.isChecked():
            pattern = r'\b' + re.escape(search_text) + r'\b'
        else:
            pattern = re.escape(search_text)
            
        # 执行替换并计算替换次数
        new_content, count = re.subn(pattern, replace_text, content, flags=flags)
        return new_content, count
        
    def replace_all_finished(self, future):
        # 在主线程中处理替换全部结果
        try:
            new_content, count = future.result()
            self.text_edit.setPlainText(new_content)
            QMessageBox.information(self, '替换全部', f'已完成替换 {count} 个匹配项')
            
            # 重置匹配信息
            self.matches = []
            self.current_match_index = -1
        except Exception as e:
            QMessageBox.critical(self, '错误', f'替换过程中出现错误: {str(e)}')


import json
import os

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent  # 主窗口引用，用于更新样式和标题
        self.settings_file = "data\\settings.json"
        self.settings = {
            "window_title": "Yunmo Note 12",
            "background_type": "color",  # 'color' or 'image'
            "background_color": "#2b2b2b",
            "background_image": "",
            "text_color": "#ffffff",
            "font_family": "Consolas",
            "font_size": 12,
        }
        self.load_settings()
        self.init_ui()
        self.apply_current_settings()

    def init_ui(self):
        self.setWindowTitle("设置")
        self.resize(500, 400)
        layout = QVBoxLayout()

        # 窗口标题
        title_layout = QHBoxLayout()
        title_label = QLabel("窗口标题:")
        title_label.setFixedWidth(100)
        self.title_edit = QLineEdit()
        self.title_edit.setText(self.settings["window_title"])
        title_layout.addWidget(title_label)
        title_layout.addWidget(self.title_edit)
        layout.addLayout(title_layout)

        # 背景类型选择
        bg_type_layout = QHBoxLayout()
        bg_type_label = QLabel("背景类型:")
        bg_type_label.setFixedWidth(100)
        self.bg_color_radio = QRadioButton("纯色")
        self.bg_image_radio = QRadioButton("图片")
        self.bg_color_radio.setChecked(self.settings["background_type"] == "color")
        self.bg_image_radio.setChecked(self.settings["background_type"] == "image")
        bg_type_layout.addWidget(bg_type_label)
        bg_type_layout.addWidget(self.bg_color_radio)
        bg_type_layout.addWidget(self.bg_image_radio)
        bg_type_group = QButtonGroup()
        bg_type_group.addButton(self.bg_color_radio)
        bg_type_group.addButton(self.bg_image_radio)
        layout.addLayout(bg_type_layout)

        # 背景色选择
        bg_color_layout = QHBoxLayout()
        bg_color_label = QLabel("背景颜色:")
        bg_color_label.setFixedWidth(100)
        self.bg_color_button = QPushButton("选择颜色")
        self.bg_color_display = QLabel()
        self.bg_color_display.setFixedSize(30, 30)
        self.update_bg_color_display()
        bg_color_layout.addWidget(bg_color_label)
        bg_color_layout.addWidget(self.bg_color_button)
        bg_color_layout.addWidget(self.bg_color_display)
        layout.addLayout(bg_color_layout)

        # 背景图片选择
        bg_image_layout = QHBoxLayout()
        bg_image_label = QLabel("背景图片:")
        bg_image_label.setFixedWidth(100)
        self.bg_image_path = QLineEdit()
        self.bg_image_path.setText(self.settings["background_image"])
        self.bg_image_browse = QPushButton("浏览...")
        bg_image_layout.addWidget(bg_image_label)
        bg_image_layout.addWidget(self.bg_image_path)
        bg_image_layout.addWidget(self.bg_image_browse)
        layout.addLayout(bg_image_layout)

        # 字体颜色
        text_color_layout = QHBoxLayout()
        text_color_label = QLabel("字体颜色:")
        text_color_label.setFixedWidth(100)
        self.text_color_button = QPushButton("选择颜色")
        self.text_color_display = QLabel()
        self.text_color_display.setFixedSize(30, 30)
        self.update_text_color_display()
        text_color_layout.addWidget(text_color_label)
        text_color_layout.addWidget(self.text_color_button)
        text_color_layout.addWidget(self.text_color_display)
        layout.addLayout(text_color_layout)

        # 字体族
        font_layout = QHBoxLayout()
        font_label = QLabel("字体:")
        font_label.setFixedWidth(100)
        self.font_combo = QFontComboBox()
        self.font_combo.setCurrentText(self.settings["font_family"])
        font_layout.addWidget(font_label)
        font_layout.addWidget(self.font_combo)
        layout.addLayout(font_layout)

        # 字体大小
        size_layout = QHBoxLayout()
        size_label = QLabel("字体大小:")
        size_label.setFixedWidth(100)
        self.size_spin = QSpinBox()
        self.size_spin.setRange(8, 72)
        self.size_spin.setValue(self.settings["font_size"])
        size_layout.addWidget(size_label)
        size_layout.addWidget(self.size_spin)
        layout.addLayout(size_layout)

        # 按钮
        btn_layout = QHBoxLayout()
        self.ok_btn = QPushButton("确定")
        self.apply_btn = QPushButton("应用")
        self.cancel_btn = QPushButton("取消")
        btn_layout.addStretch()
        btn_layout.addWidget(self.ok_btn)
        btn_layout.addWidget(self.apply_btn)
        btn_layout.addWidget(self.cancel_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

        # 连接信号
        self.bg_color_button.clicked.connect(self.choose_bg_color)
        self.bg_image_browse.clicked.connect(self.choose_bg_image)
        self.text_color_button.clicked.connect(self.choose_text_color)
        self.ok_btn.clicked.connect(self.on_ok)
        self.apply_btn.clicked.connect(self.on_apply)
        self.cancel_btn.clicked.connect(self.reject)
        self.bg_color_radio.toggled.connect(self.toggle_bg_options)
        self.bg_image_radio.toggled.connect(self.toggle_bg_options)

        self.toggle_bg_options()

    def update_bg_color_display(self):
        color = self.settings["background_color"]
        self.bg_color_display.setStyleSheet(f"background-color: {color}; border: 1px solid #555;")

    def update_text_color_display(self):
        color = self.settings["text_color"]
        self.text_color_display.setStyleSheet(f"background-color: {color}; border: 1px solid #555;")

    def choose_bg_color(self):
        color = QColorDialog.getColor(QColor(self.settings["background_color"]), self, "选择背景颜色")
        if color.isValid():
            self.settings["background_color"] = color.name()
            self.update_bg_color_display()

    def choose_text_color(self):
        color = QColorDialog.getColor(QColor(self.settings["text_color"]), self, "选择字体颜色")
        if color.isValid():
            self.settings["text_color"] = color.name()
            self.update_text_color_display()

    def choose_bg_image(self):
        filename, _ = QFileDialog.getOpenFileName(
            self, "选择背景图片", "", "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        if filename:
            self.bg_image_path.setText(filename)
            self.settings["background_image"] = filename

    def toggle_bg_options(self):
        is_color = self.bg_color_radio.isChecked()
        self.bg_color_button.setEnabled(is_color)
        self.bg_color_display.setEnabled(is_color)
        self.bg_image_path.setEnabled(not is_color)
        self.bg_image_browse.setEnabled(not is_color)

    def load_settings(self):
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    self.settings.update(loaded)
            except Exception as e:
                print(f"加载设置失败: {e}")

    def save_settings(self):
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, ensure_ascii=False, indent=4)
        except Exception as e:
            QMessageBox.critical(self, "错误", f"无法保存设置: {str(e)}")

    def apply_current_settings(self):
        # 更新当前对话框中的控件状态
        self.title_edit.setText(self.settings["window_title"])
        self.bg_color_radio.setChecked(self.settings["background_type"] == "color")
        self.bg_image_radio.setChecked(self.settings["background_type"] == "image")
        self.settings["background_color"] = self.settings.get("background_color", "#2b2b2b")
        self.settings["text_color"] = self.settings.get("text_color", "#ffffff")
        self.update_bg_color_display()
        self.update_text_color_display()
        self.bg_image_path.setText(self.settings["background_image"])

        # 应用样式到主程序
        self.apply_stylesheet_to_parent()

    def apply_stylesheet_to_parent(self):
        if not self.parent:
            return

        # 构建 QSS
        bg = ""
        if self.settings["background_type"] == "color":
            bg = self.settings["background_color"]
        else:
            img = self.settings["background_image"]
            if img and os.path.exists(img):
                bg = f"url({img})"
            else:
                bg = self.settings["background_color"]  # 回退

        font_family = self.settings["font_family"]
        font_size = self.settings["font_size"]
        text_color = self.settings["text_color"]

        qss = f'''
            QMainWindow {{
                background-color: {bg};
                background-image: {f"url({self.settings['background_image']})" if self.settings['background_type'] == 'image' and self.settings['background_image'] else 'none'};
                background-repeat: no-repeat;
                background-position: center;
            }}
            QMenuBar {{
                background-color: #3c3f41;
                color: #ffffff;
                border-bottom: 1px solid #555555;
            }}
            QMenuBar::item {{
                background: transparent;
                padding: 5px 10px;
            }}
            QMenuBar::item:selected {{
                background: #4b6eaf;
            }}
            QMenu {{
                background-color: #3c3f41;
                color: #ffffff;
                border: 1px solid #555555;
            }}
            QTextEdit {{
                background-color: transparent;
                border: 1px solid #555555;
                padding: 5px;
                color: {text_color};
                selection-background-color: #4b6eaf;
                selection-color: #ffffff;
                font-family: "{font_family}";
                font-size: {font_size}px;
            }}
            QLabel, QLineEdit, QPushButton {{
                color: {text_color};
                font-family: "{font_family}";
                font-size: {font_size}px;
            }}
        '''
        self.parent.setStyleSheet(qss)

        # 设置窗口标题
        self.parent.setWindowTitle(self.settings["window_title"])
        self.setStyleSheet('''
                    QMenu::item {
                padding: 5px 20px;
            }
            QMenu::item:selected {
                background-color: #4b6eaf;
            }
            QTextEdit {
                background-color: #2b2b2b;
                border: 1px solid #555555;
                padding: 5px;
                color: #ffffff;
                selection-background-color: #4b6eaf;
                selection-color: #ffffff;
            }
        ''')

    def on_apply(self):
        # 获取最新设置
        self.settings["window_title"] = self.title_edit.text().strip() or "Yunmo Note 12"
        self.settings["background_type"] = "color" if self.bg_color_radio.isChecked() else "image"
        self.settings["font_family"] = self.font_combo.currentText()
        self.settings["font_size"] = self.size_spin.value()

        # 应用并保存
        self.apply_stylesheet_to_parent()
        self.save_settings()

    def on_ok(self):
        self.on_apply()
        self.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = yumonote()

    sys.exit(app.exec())
