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

import json
import os

class SettingsManager:
    def __init__(self, settings_file='setting.json'):
        self.settings_file = settings_file
        self.settings = {}
        self.load_settings()
        
    def load_settings(self):
        """加载设置文件"""
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    self.settings = json.load(f)
            except Exception as e:
                print(f"加载设置文件失败: {e}")
                self.settings = {}
        else:
            # 创建默认设置
            self.settings = {
                'window_title': 'Yunmo Note 12',
                'background_color': '#2b2b2b',
                'background_image': '',
                'font_family': '宋体',
                'font_size': 12,
                'text_color': '#ffffff',
                'qss_style': ''
            }
            self.save_settings()
        
    def save_settings(self):
        """保存设置到文件"""
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"保存设置文件失败: {e}")
            
    def get(self, key, default=None):
        """获取设置值"""
        return self.settings.get(key, default)
        
    def set(self, key, value):
        """设置设置值"""
        self.settings[key] = value
        self.save_settings()
