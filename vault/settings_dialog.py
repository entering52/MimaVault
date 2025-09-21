# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtGui, QtCore
from .config import (
    get_color_theme, get_font_config, get_spacing_config, 
    get_border_radius_config, FONT_FAMILIES, COLOR_THEME, get_dialog_config
)
from .settings_dialog_style import load_settings_dialog_style
import json
import os

class SettingsDialog(QtWidgets.QDialog):
    """设置对话框 - 提供界面自定义功能"""
    
    # 设置更改信号
    settingsChanged = QtCore.pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # 设置对话框标识符
        self.setObjectName("SettingsDialog")
        
        self.setWindowTitle("界面设置")
        
        # 使用配置项设置对话框属性
        dialog_config = get_dialog_config('settings')
        
        self.setModal(dialog_config['modal'])
        self.resize(dialog_config['width'], dialog_config['height'])
        
        # 应用专用样式
        self.setStyleSheet(load_settings_dialog_style())
        
        # 设置文件路径
        self.settings_file = os.path.join(os.path.dirname(__file__), '..', 'user_settings.json')
        
        # 加载用户设置
        self.user_settings = self._load_user_settings()
        
        self._setup_ui()
        self._load_current_settings()
        
    def _setup_ui(self):
        """设置UI界面"""
        layout = QtWidgets.QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # 移除标题，直接显示选项卡
        
        # 创建选项卡
        tab_widget = QtWidgets.QTabWidget()
        
        # 主题选项卡
        theme_tab = self._create_theme_tab()
        tab_widget.addTab(theme_tab, "主题")
        
        # 字体选项卡
        font_tab = self._create_font_tab()
        tab_widget.addTab(font_tab, "字体")
        
        # 布局选项卡
        layout_tab = self._create_layout_tab()
        tab_widget.addTab(layout_tab, "布局")
        
        layout.addWidget(tab_widget)
        
        # 按钮区域
        button_layout = QtWidgets.QHBoxLayout()
        
        # 重置按钮
        reset_btn = QtWidgets.QPushButton("重置默认")
        reset_btn.setObjectName("ResetButton")
        reset_btn.clicked.connect(self._reset_to_default)
        button_layout.addWidget(reset_btn)
        
        button_layout.addStretch()
        
        # 确定和取消按钮
        ok_btn = QtWidgets.QPushButton("确定")
        ok_btn.setObjectName("PrimaryButton")
        ok_btn.clicked.connect(self._apply_settings)
        cancel_btn = QtWidgets.QPushButton("取消")
        cancel_btn.clicked.connect(self.reject)
        
        button_layout.addWidget(ok_btn)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        
    def _create_theme_tab(self):
        """创建主题选项卡"""
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(widget)
        
        # 预设主题选择
        theme_group = QtWidgets.QGroupBox("预设主题")
        theme_layout = QtWidgets.QVBoxLayout(theme_group)
        theme_layout.setSpacing(12)
        theme_layout.setContentsMargins(16, 20, 16, 16)
        
        # 主题说明
        theme_desc = QtWidgets.QLabel("选择预设主题或自定义颜色方案")
        theme_desc.setStyleSheet("color: #9aa0b5; font-size: 12px;")
        theme_layout.addWidget(theme_desc)
        
        self.theme_combo = QtWidgets.QComboBox()
        self.theme_combo.addItems(["深色主题", "浅色主题", "高对比度", "护眼模式"])
        self.theme_combo.currentTextChanged.connect(self._on_theme_changed)
        theme_layout.addWidget(self.theme_combo)
        
        layout.addWidget(theme_group)
        
        # 自定义颜色
        color_group = QtWidgets.QGroupBox("自定义颜色")
        color_layout = QtWidgets.QGridLayout(color_group)
        color_layout.setSpacing(12)
        color_layout.setContentsMargins(16, 20, 16, 16)
        
        # 颜色说明
        color_desc = QtWidgets.QLabel("点击颜色按钮自定义界面配色")
        color_desc.setStyleSheet("color: #9aa0b5; font-size: 12px;")
        color_layout.addWidget(color_desc, 0, 0, 1, 4)
        
        self.color_buttons = {}
        color_items = [
            ("主色调", "primary"),
            ("强调色", "accent"),
            ("背景色", "background"),
            ("表面色", "surface"),
            ("错误色", "error"),
            ("成功色", "success")
        ]
        
        for i, (label, key) in enumerate(color_items):
            row, col = (i // 2) + 1, (i % 2) * 2  # +1 因为第0行是说明文字
            
            label_widget = QtWidgets.QLabel(label + ":")
            label_widget.setMinimumWidth(80)
            color_layout.addWidget(label_widget, row, col)
            
            color_btn = QtWidgets.QPushButton()
            color_btn.setObjectName("ColorButton")
            color_btn.setFixedSize(80, 32)
            color_btn.setToolTip(f"点击选择{label}")
            color_btn.clicked.connect(lambda checked, k=key: self._choose_color(k))
            self.color_buttons[key] = color_btn
            color_layout.addWidget(color_btn, row, col + 1)
        
        layout.addWidget(color_group)
        layout.addStretch()
        
        return widget
        
    def _create_font_tab(self):
        """创建字体选项卡"""
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(widget)
        
        # 字体族选择
        font_group = QtWidgets.QGroupBox("字体设置")
        font_layout = QtWidgets.QVBoxLayout(font_group)
        font_layout.setSpacing(12)
        font_layout.setContentsMargins(16, 20, 16, 16)
        
        # 字体说明
        font_desc = QtWidgets.QLabel("调整界面字体和大小设置")
        font_desc.setStyleSheet("color: #9aa0b5; font-size: 12px;")
        font_layout.addWidget(font_desc)
        
        # 字体族选择
        family_layout = QtWidgets.QHBoxLayout()
        family_layout.addWidget(QtWidgets.QLabel("字体族："))
        self.font_family_combo = QtWidgets.QComboBox()
        self.font_family_combo.addItems(FONT_FAMILIES)
        family_layout.addWidget(self.font_family_combo)
        family_layout.addStretch()
        font_layout.addLayout(family_layout)
        
        # 字体大小
        size_group = QtWidgets.QGroupBox("字体大小")
        size_layout = QtWidgets.QFormLayout(size_group)
        size_layout.setSpacing(8)
        size_layout.setContentsMargins(16, 20, 16, 16)
        
        self.font_size_spinboxes = {}
        size_items = [
            ("小字体", "small"),
            ("普通字体", "normal"),
            ("标题字体", "title"),
            ("大字体", "large")
        ]
        
        for label, key in size_items:
            spinbox = QtWidgets.QSpinBox()
            spinbox.setRange(8, 24)
            spinbox.setSuffix(" px")
            spinbox.setToolTip(f"设置{label}大小")
            self.font_size_spinboxes[key] = spinbox
            size_layout.addRow(label + "：", spinbox)
        
        layout.addWidget(font_group)
        layout.addWidget(size_group)
        layout.addStretch()
        
        return widget
        
    def _create_layout_tab(self):
        """创建布局选项卡"""
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(widget)
        
        # 布局说明
        layout_desc = QtWidgets.QLabel("调整界面元素的间距和圆角设置")
        layout_desc.setStyleSheet("color: #9aa0b5; font-size: 12px; margin-bottom: 12px;")
        layout.addWidget(layout_desc)
        
        # 间距设置
        spacing_group = QtWidgets.QGroupBox("间距设置")
        spacing_layout = QtWidgets.QFormLayout(spacing_group)
        spacing_layout.setSpacing(8)
        spacing_layout.setContentsMargins(16, 20, 16, 16)
        
        self.spacing_spinboxes = {}
        spacing_items = [
            ("极小间距", "xs"),
            ("小间距", "sm"),
            ("中等间距", "md"),
            ("大间距", "lg"),
            ("极大间距", "xl")
        ]
        
        for label, key in spacing_items:
            spinbox = QtWidgets.QSpinBox()
            spinbox.setRange(1, 20)
            spinbox.setSuffix(" px")
            spinbox.setToolTip(f"设置{label}的像素值")
            self.spacing_spinboxes[key] = spinbox
            spacing_layout.addRow(label + "：", spinbox)
        
        # 圆角设置
        radius_group = QtWidgets.QGroupBox("圆角设置")
        radius_layout = QtWidgets.QFormLayout(radius_group)
        radius_layout.setSpacing(8)
        radius_layout.setContentsMargins(16, 20, 16, 16)
        
        self.radius_spinboxes = {}
        radius_items = [
            ("小圆角", "small"),
            ("中等圆角", "medium"),
            ("大圆角", "large")
        ]
        
        for label, key in radius_items:
            spinbox = QtWidgets.QSpinBox()
            spinbox.setRange(0, 20)
            spinbox.setSuffix(" px")
            spinbox.setToolTip(f"设置{label}的像素值")
            self.radius_spinboxes[key] = spinbox
            radius_layout.addRow(label + "：", spinbox)
        
        layout.addWidget(spacing_group)
        layout.addWidget(radius_group)
        layout.addStretch()
        
        return widget
        
    def _load_current_settings(self):
        """加载当前设置到界面"""
        # 加载颜色设置
        colors = get_color_theme()
        for key, button in self.color_buttons.items():
            if key in colors:
                color = colors[key]
                # 计算文字颜色以确保可读性
                qcolor = QtGui.QColor(color)
                text_color = '#FFFFFF' if qcolor.lightness() < 128 else '#000000'
                
                button.setStyleSheet(
                    f"background-color: {color}; "
                    f"border: 1px solid #8091ff; "
                    f"color: {text_color};"
                )
                button.setText(color)
        
        # 加载字体设置
        fonts = get_font_config()
        if 'family' in fonts:
            index = self.font_family_combo.findText(fonts['family'].split(',')[0].strip("'"))
            if index >= 0:
                self.font_family_combo.setCurrentIndex(index)
        
        if 'sizes' in fonts:
            for key, spinbox in self.font_size_spinboxes.items():
                if key in fonts['sizes']:
                    spinbox.setValue(fonts['sizes'][key])
        
        # 加载间距设置
        spacing = get_spacing_config()
        for key, spinbox in self.spacing_spinboxes.items():
            if key in spacing:
                spinbox.setValue(spacing[key])
        
        # 加载圆角设置
        radius = get_border_radius_config()
        for key, spinbox in self.radius_spinboxes.items():
            if key in radius:
                spinbox.setValue(radius[key])
    
    def _on_theme_changed(self, theme_name):
        """主题改变时的处理"""
        # 这里可以预设不同主题的颜色方案
        theme_colors = {
            "深色主题": {
                "primary": "#4752C4",
                "accent": "#8091ff",
                "background": "#101014",
                "surface": "#141420",
                "error": "#ff5e5e",
                "success": "#6eff8e"
            },
            "浅色主题": {
                "primary": "#2196F3",
                "accent": "#FF9800",
                "background": "#FFFFFF",
                "surface": "#F5F5F5",
                "error": "#F44336",
                "success": "#4CAF50"
            }
        }
        
        if theme_name in theme_colors:
            colors = theme_colors[theme_name]
            for key, color in colors.items():
                if key in self.color_buttons:
                    button = self.color_buttons[key]
                    button.setStyleSheet(f"background-color: {color}; border: 1px solid #ccc;")
                    button.setText(color)
    
    def _choose_color(self, color_key):
        """选择颜色"""
        current_color = self.color_buttons[color_key].text() or "#FFFFFF"
        
        # 创建颜色对话框
        color_dialog = QtWidgets.QColorDialog(QtGui.QColor(current_color), self)
        color_dialog.setWindowTitle(f"选择{self._get_color_label(color_key)}")
        color_dialog.setOption(QtWidgets.QColorDialog.ShowAlphaChannel, False)
        
        if color_dialog.exec_() == QtWidgets.QDialog.Accepted:
            color = color_dialog.selectedColor()
            color_hex = color.name()
            
            # 更新按钮样式和文本
            self.color_buttons[color_key].setStyleSheet(
                f"background-color: {color_hex}; "
                f"border: 2px solid #8091ff; "
                f"color: {'#FFFFFF' if color.lightness() < 128 else '#000000'};"
            )
            self.color_buttons[color_key].setText(color_hex)
    
    def _get_color_label(self, color_key):
        """获取颜色标签"""
        labels = {
            "primary": "主色调",
            "accent": "强调色", 
            "background": "背景色",
            "surface": "表面色",
            "error": "错误色",
            "success": "成功色"
        }
        return labels.get(color_key, color_key)
    
    def _reset_to_default(self):
        """重置为默认设置"""
        reply = QtWidgets.QMessageBox.question(
            self, "确认重置", 
            "确定要重置所有设置为默认值吗？",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No
        )
        
        if reply == QtWidgets.QMessageBox.Yes:
            # 删除用户设置文件
            if os.path.exists(self.settings_file):
                os.remove(self.settings_file)
            
            # 重新加载默认设置
            self.user_settings = {}
            self._load_current_settings()
    
    def _apply_settings(self):
        """应用设置"""
        # 收集所有设置
        settings = {
            'colors': {},
            'fonts': {
                'family': self.font_family_combo.currentText(),
                'sizes': {},
                'weights': get_font_config()['weights']  # 保持权重不变
            },
            'spacing': {},
            'radius': {}
        }
        
        # 收集颜色设置
        for key, button in self.color_buttons.items():
            settings['colors'][key] = button.text()
        
        # 收集字体大小设置
        for key, spinbox in self.font_size_spinboxes.items():
            settings['fonts']['sizes'][key] = spinbox.value()
        
        # 收集间距设置
        for key, spinbox in self.spacing_spinboxes.items():
            settings['spacing'][key] = spinbox.value()
        
        # 收集圆角设置
        for key, spinbox in self.radius_spinboxes.items():
            settings['radius'][key] = spinbox.value()
        
        # 保存设置
        self._save_user_settings(settings)
        
        # 发出设置更改信号
        self.settingsChanged.emit()
        
        self.accept()
    
    def _load_user_settings(self):
        """加载用户设置"""
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass
        return {}
    
    def _save_user_settings(self, settings):
        """保存用户设置"""
        try:
            os.makedirs(os.path.dirname(self.settings_file), exist_ok=True)
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=2, ensure_ascii=False)
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "保存失败", f"无法保存设置：{str(e)}")
    
    def __del__(self):
        """析构函数：清理信号连接"""
        self._cleanup_signals()
    
    def _cleanup_signals(self):
        """清理所有信号连接"""
        try:
            # 清理主题选择信号
            if hasattr(self, 'theme_combo'):
                self.theme_combo.currentTextChanged.disconnect()
            
            # 清理颜色按钮信号
            if hasattr(self, 'color_buttons'):
                for button in self.color_buttons.values():
                    button.clicked.disconnect()
                    
        except (TypeError, RuntimeError, AttributeError):
            pass