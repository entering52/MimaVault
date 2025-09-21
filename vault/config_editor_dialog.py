# -*- coding: utf-8 -*-
"""
配置编辑对话框
提供统一的配置项编辑界面，按功能分类组织到不同选项卡
"""

import json
import os
from PyQt5 import QtWidgets, QtCore, QtGui
from typing import Dict, Any
from . import config


class ConfigEditorDialog(QtWidgets.QDialog):
    """配置编辑对话框"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("配置编辑")
        self.setModal(True)
        self.resize(800, 600)
        
        # 存储配置更改
        self.config_changes = {}
        
        self._init_ui()
        self._load_current_config()
        self._apply_styles()
    
    def _init_ui(self):
        """初始化用户界面"""
        layout = QtWidgets.QVBoxLayout(self)
        
        # 创建选项卡控件
        self.tab_widget = QtWidgets.QTabWidget()
        layout.addWidget(self.tab_widget)
        
        # 创建各个选项卡
        self._create_app_tab()
        self._create_ui_tab()
        self._create_security_tab()
        self._create_advanced_tab()
        
        # 按钮区域
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addStretch()
        
        self.reset_btn = QtWidgets.QPushButton("重置")
        self.reset_btn.clicked.connect(self._reset_config)
        button_layout.addWidget(self.reset_btn)
        
        self.cancel_btn = QtWidgets.QPushButton("取消")
        self.cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_btn)
        
        self.save_btn = QtWidgets.QPushButton("保存")
        self.save_btn.clicked.connect(self._save_config)
        self.save_btn.setDefault(True)
        button_layout.addWidget(self.save_btn)
        
        layout.addLayout(button_layout)
    
    def _create_app_tab(self):
        """创建应用配置选项卡"""
        tab = QtWidgets.QWidget()
        self.tab_widget.addTab(tab, "应用配置")
        
        layout = QtWidgets.QFormLayout(tab)
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # 应用基本信息
        app_group = QtWidgets.QGroupBox("应用信息")
        app_layout = QtWidgets.QFormLayout(app_group)
        
        self.app_name_edit = QtWidgets.QLineEdit()
        app_layout.addRow("应用名称:", self.app_name_edit)
        
        self.app_version_edit = QtWidgets.QLineEdit()
        app_layout.addRow("版本号:", self.app_version_edit)
        
        self.app_description_edit = QtWidgets.QLineEdit()
        app_layout.addRow("描述:", self.app_description_edit)
        
        layout.addRow(app_group)
        
        # 窗口配置
        window_group = QtWidgets.QGroupBox("窗口配置")
        window_layout = QtWidgets.QFormLayout(window_group)
        
        self.default_width_spin = QtWidgets.QSpinBox()
        self.default_width_spin.setRange(600, 2000)
        window_layout.addRow("默认宽度:", self.default_width_spin)
        
        self.default_height_spin = QtWidgets.QSpinBox()
        self.default_height_spin.setRange(400, 1500)
        window_layout.addRow("默认高度:", self.default_height_spin)
        
        self.min_width_spin = QtWidgets.QSpinBox()
        self.min_width_spin.setRange(400, 1000)
        window_layout.addRow("最小宽度:", self.min_width_spin)
        
        self.min_height_spin = QtWidgets.QSpinBox()
        self.min_height_spin.setRange(300, 800)
        window_layout.addRow("最小高度:", self.min_height_spin)
        
        self.resizable_check = QtWidgets.QCheckBox("允许调整窗口大小")
        window_layout.addRow(self.resizable_check)
        
        layout.addRow(window_group)
        
        # 卡片配置
        card_group = QtWidgets.QGroupBox("卡片配置")
        card_layout = QtWidgets.QFormLayout(card_group)
        
        self.card_width_spin = QtWidgets.QSpinBox()
        self.card_width_spin.setRange(200, 500)
        card_layout.addRow("卡片宽度:", self.card_width_spin)
        
        self.card_height_spin = QtWidgets.QSpinBox()
        self.card_height_spin.setRange(80, 200)
        card_layout.addRow("卡片高度:", self.card_height_spin)
        
        self.grid_spacing_spin = QtWidgets.QSpinBox()
        self.grid_spacing_spin.setRange(4, 30)
        card_layout.addRow("网格间距:", self.grid_spacing_spin)
        
        layout.addRow(card_group)
    
    def _create_ui_tab(self):
        """创建界面配置选项卡"""
        tab = QtWidgets.QWidget()
        self.tab_widget.addTab(tab, "界面配置")
        
        layout = QtWidgets.QVBoxLayout(tab)
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # 颜色主题配置
        color_group = QtWidgets.QGroupBox("颜色主题")
        color_layout = QtWidgets.QFormLayout(color_group)
        
        self.theme_combo = QtWidgets.QComboBox()
        self.theme_combo.addItems(["深色主题", "浅色主题"])
        color_layout.addRow("主题选择:", self.theme_combo)
        
        # 主要颜色配置
        self.primary_color_btn = self._create_color_button()
        color_layout.addRow("主色调:", self.primary_color_btn)
        
        self.accent_color_btn = self._create_color_button()
        color_layout.addRow("强调色:", self.accent_color_btn)
        
        layout.addWidget(color_group)
        
        # 字体配置
        font_group = QtWidgets.QGroupBox("字体配置")
        font_layout = QtWidgets.QFormLayout(font_group)
        
        self.font_family_combo = QtWidgets.QComboBox()
        self.font_family_combo.addItems(config.FONT_FAMILIES)
        font_layout.addRow("字体族:", self.font_family_combo)
        
        self.font_size_small_spin = QtWidgets.QSpinBox()
        self.font_size_small_spin.setRange(8, 20)
        font_layout.addRow("小字体大小:", self.font_size_small_spin)
        
        self.font_size_normal_spin = QtWidgets.QSpinBox()
        self.font_size_normal_spin.setRange(10, 24)
        font_layout.addRow("正常字体大小:", self.font_size_normal_spin)
        
        self.font_size_large_spin = QtWidgets.QSpinBox()
        self.font_size_large_spin.setRange(12, 28)
        font_layout.addRow("大字体大小:", self.font_size_large_spin)
        
        layout.addWidget(font_group)
        
        # UI行为配置
        behavior_group = QtWidgets.QGroupBox("界面行为")
        behavior_layout = QtWidgets.QFormLayout(behavior_group)
        
        self.animation_duration_spin = QtWidgets.QSpinBox()
        self.animation_duration_spin.setRange(0, 1000)
        self.animation_duration_spin.setSuffix(" ms")
        behavior_layout.addRow("动画持续时间:", self.animation_duration_spin)
        
        self.tooltip_delay_spin = QtWidgets.QSpinBox()
        self.tooltip_delay_spin.setRange(0, 2000)
        self.tooltip_delay_spin.setSuffix(" ms")
        behavior_layout.addRow("工具提示延迟:", self.tooltip_delay_spin)
        
        self.auto_save_interval_spin = QtWidgets.QSpinBox()
        self.auto_save_interval_spin.setRange(10, 300)
        self.auto_save_interval_spin.setSuffix(" 秒")
        behavior_layout.addRow("自动保存间隔:", self.auto_save_interval_spin)
        
        self.show_passwords_check = QtWidgets.QCheckBox("默认显示密码")
        behavior_layout.addRow(self.show_passwords_check)
        
        self.card_hover_animation_check = QtWidgets.QCheckBox("卡片悬停动画")
        behavior_layout.addRow(self.card_hover_animation_check)
        
        layout.addWidget(behavior_group)
        
        layout.addStretch()
    
    def _create_security_tab(self):
        """创建安全配置选项卡"""
        tab = QtWidgets.QWidget()
        self.tab_widget.addTab(tab, "安全配置")
        
        layout = QtWidgets.QVBoxLayout(tab)
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # 密码策略
        password_group = QtWidgets.QGroupBox("密码策略")
        password_layout = QtWidgets.QFormLayout(password_group)
        
        self.password_min_length_spin = QtWidgets.QSpinBox()
        self.password_min_length_spin.setRange(4, 32)
        password_layout.addRow("最小密码长度:", self.password_min_length_spin)
        
        self.password_max_length_spin = QtWidgets.QSpinBox()
        self.password_max_length_spin.setRange(32, 256)
        password_layout.addRow("最大密码长度:", self.password_max_length_spin)
        
        layout.addWidget(password_group)
        
        # 移除了旧的加密配置控件
        
        # 会话安全
        session_group = QtWidgets.QGroupBox("会话安全")
        session_layout = QtWidgets.QFormLayout(session_group)
        
        self.session_timeout_spin = QtWidgets.QSpinBox()
        self.session_timeout_spin.setRange(300, 7200)
        self.session_timeout_spin.setSuffix(" 秒")
        session_layout.addRow("会话超时时间:", self.session_timeout_spin)
        
        self.auto_lock_check = QtWidgets.QCheckBox("启用自动锁定")
        session_layout.addRow(self.auto_lock_check)
        
        self.clipboard_timeout_spin = QtWidgets.QSpinBox()
        self.clipboard_timeout_spin.setRange(5, 300)
        self.clipboard_timeout_spin.setSuffix(" 秒")
        session_layout.addRow("剪贴板清除超时:", self.clipboard_timeout_spin)
        
        layout.addWidget(session_group)
        
        layout.addStretch()
    
    def _create_advanced_tab(self):
        """创建高级配置选项卡"""
        tab = QtWidgets.QWidget()
        self.tab_widget.addTab(tab, "高级配置")
        
        layout = QtWidgets.QVBoxLayout(tab)
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # 性能配置
        performance_group = QtWidgets.QGroupBox("性能配置")
        performance_layout = QtWidgets.QFormLayout(performance_group)
        
        self.batch_load_size_spin = QtWidgets.QSpinBox()
        self.batch_load_size_spin.setRange(10, 200)
        performance_layout.addRow("批量加载大小:", self.batch_load_size_spin)
        
        self.scroll_load_threshold_spin = QtWidgets.QSpinBox()
        self.scroll_load_threshold_spin.setRange(5, 50)
        performance_layout.addRow("滚动加载阈值:", self.scroll_load_threshold_spin)
        
        self.max_recent_files_spin = QtWidgets.QSpinBox()
        self.max_recent_files_spin.setRange(5, 50)
        performance_layout.addRow("最大最近文件数:", self.max_recent_files_spin)
        
        layout.addWidget(performance_group)
        
        # 导入导出配置
        import_export_group = QtWidgets.QGroupBox("导入导出")
        import_export_layout = QtWidgets.QFormLayout(import_export_group)
        
        self.max_file_size_spin = QtWidgets.QSpinBox()
        self.max_file_size_spin.setRange(1, 100)
        self.max_file_size_spin.setSuffix(" MB")
        import_export_layout.addRow("最大文件大小:", self.max_file_size_spin)
        
        self.backup_on_import_check = QtWidgets.QCheckBox("导入时备份")
        import_export_layout.addRow(self.backup_on_import_check)
        
        self.validate_on_import_check = QtWidgets.QCheckBox("导入时验证")
        import_export_layout.addRow(self.validate_on_import_check)
        
        layout.addWidget(import_export_group)
        
        # 日志配置
        log_group = QtWidgets.QGroupBox("日志配置")
        log_layout = QtWidgets.QFormLayout(log_group)
        
        self.log_level_combo = QtWidgets.QComboBox()
        self.log_level_combo.addItems(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
        log_layout.addRow("日志级别:", self.log_level_combo)
        
        self.log_file_path_edit = QtWidgets.QLineEdit()
        log_layout.addRow("日志文件路径:", self.log_file_path_edit)
        
        self.log_max_size_spin = QtWidgets.QSpinBox()
        self.log_max_size_spin.setRange(1, 50)
        self.log_max_size_spin.setSuffix(" MB")
        log_layout.addRow("最大日志文件大小:", self.log_max_size_spin)
        
        self.log_backup_count_spin = QtWidgets.QSpinBox()
        self.log_backup_count_spin.setRange(1, 20)
        log_layout.addRow("日志备份数量:", self.log_backup_count_spin)
        
        layout.addWidget(log_group)
        
        layout.addStretch()
    
    def _create_color_button(self):
        """创建颜色选择按钮"""
        button = QtWidgets.QPushButton()
        button.setFixedSize(60, 30)
        button.clicked.connect(lambda: self._choose_color(button))
        return button
    
    def _choose_color(self, button):
        """选择颜色"""
        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            button.setStyleSheet(f"background-color: {color.name()}; border: 1px solid #ccc;")
            button.color = color.name()
    
    def _load_current_config(self):
        """加载当前配置"""
        # 应用配置
        app_config = config.get_app_config()
        self.app_name_edit.setText(app_config.get('name', ''))
        self.app_version_edit.setText(app_config.get('version', ''))
        self.app_description_edit.setText(app_config.get('description', ''))
        
        # 窗口配置
        window_config = config.get_window_config()
        self.default_width_spin.setValue(window_config.get('default_width', 1100))
        self.default_height_spin.setValue(window_config.get('default_height', 720))
        self.min_width_spin.setValue(window_config.get('min_width', 800))
        self.min_height_spin.setValue(window_config.get('min_height', 600))
        self.resizable_check.setChecked(window_config.get('resizable', True))
        
        # 卡片配置
        card_config = config.get_card_config()
        self.card_width_spin.setValue(card_config.get('width', 320))
        self.card_height_spin.setValue(card_config.get('height', 120))
        self.grid_spacing_spin.setValue(card_config.get('grid_spacing', 12))
        
        # 字体配置
        font_config = config.get_font_config()
        font_family = font_config.get('family', '')
        if font_family in config.FONT_FAMILIES:
            self.font_family_combo.setCurrentText(font_family)
        
        font_sizes = font_config.get('sizes', {})
        self.font_size_small_spin.setValue(font_sizes.get('small', 12))
        self.font_size_normal_spin.setValue(font_sizes.get('normal', 14))
        self.font_size_large_spin.setValue(font_sizes.get('large', 16))
        
        # UI配置
        ui_config = config.get_ui_config()
        self.animation_duration_spin.setValue(ui_config.get('animation_duration', 200))
        self.tooltip_delay_spin.setValue(ui_config.get('tooltip_delay', 500))
        self.auto_save_interval_spin.setValue(ui_config.get('auto_save_interval', 30))
        self.show_passwords_check.setChecked(ui_config.get('show_passwords_default', False))
        self.card_hover_animation_check.setChecked(ui_config.get('card_hover_animation', True))
        self.batch_load_size_spin.setValue(ui_config.get('batch_load_size', 50))
        self.scroll_load_threshold_spin.setValue(ui_config.get('scroll_load_threshold', 10))
        self.max_recent_files_spin.setValue(ui_config.get('max_recent_files', 10))
        
        # 安全配置
        security_config = config.get_security_config()
        self.password_min_length_spin.setValue(security_config.get('password_min_length', 8))
        self.password_max_length_spin.setValue(security_config.get('password_max_length', 128))
        self.session_timeout_spin.setValue(security_config.get('session_timeout', 3600))
        self.auto_lock_check.setChecked(security_config.get('auto_lock_enabled', True))
        self.clipboard_timeout_spin.setValue(security_config.get('clipboard_clear_timeout', 30))
        
        # 导入导出配置
        import_export_config = config.get_import_export_config()
        max_file_size_mb = import_export_config.get('max_file_size', 10485760) // (1024 * 1024)
        self.max_file_size_spin.setValue(max_file_size_mb)
        self.backup_on_import_check.setChecked(import_export_config.get('backup_on_import', True))
        self.validate_on_import_check.setChecked(import_export_config.get('validate_on_import', True))
        
        # 日志配置
        log_config = config.get_log_config()
        self.log_level_combo.setCurrentText(log_config.get('level', 'INFO'))
        self.log_file_path_edit.setText(log_config.get('file_path', 'logs/app.log'))
        log_max_size_mb = log_config.get('max_file_size', 5242880) // (1024 * 1024)
        self.log_max_size_spin.setValue(log_max_size_mb)
        self.log_backup_count_spin.setValue(log_config.get('backup_count', 3))
        
        # 颜色配置
        color_theme = config.get_color_theme()
        self._set_color_button(self.primary_color_btn, color_theme.get('primary', '#5865F2'))
        self._set_color_button(self.accent_color_btn, color_theme.get('accent', '#cfd3ff'))
    
    def _set_color_button(self, button, color):
        """设置颜色按钮的颜色"""
        button.setStyleSheet(f"background-color: {color}; border: 1px solid #ccc;")
        button.color = color
    
    def _apply_styles(self):
        """应用样式"""
        from .config_editor_style import load_config_editor_style
        self.setStyleSheet(load_config_editor_style())
    
    def _reset_config(self):
        """重置配置到默认值"""
        reply = QtWidgets.QMessageBox.question(
            self, "确认重置", 
            "确定要重置所有配置到默认值吗？这将丢失所有自定义设置。",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No
        )
        
        if reply == QtWidgets.QMessageBox.Yes:
            self._load_current_config()
    
    def _save_config(self):
        """保存配置"""
        try:
            # 收集所有配置更改
            self._collect_config_changes()
            
            # 保存到用户配置文件
            self._save_user_config()
            
            # 应用配置到当前运行的config模块
            config.apply_user_config(self.config_changes)
            
            QtWidgets.QMessageBox.information(
                self, "保存成功", 
                "配置已成功保存并应用。"
            )
            
            self.accept()
            
        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self, "保存失败", 
                f"保存配置时发生错误：{str(e)}"
            )
    
    def _collect_config_changes(self):
        """收集配置更改"""
        self.config_changes = {
            'APP_CONFIG': {
                'name': self.app_name_edit.text(),
                'version': self.app_version_edit.text(),
                'description': self.app_description_edit.text()
            },
            'WINDOW_CONFIG': {
                'default_width': self.default_width_spin.value(),
                'default_height': self.default_height_spin.value(),
                'min_width': self.min_width_spin.value(),
                'min_height': self.min_height_spin.value(),
                'resizable': self.resizable_check.isChecked()
            },
            'CARD_CONFIG': {
                'width': self.card_width_spin.value(),
                'height': self.card_height_spin.value(),
                'grid_spacing': self.grid_spacing_spin.value()
            },
            'FONT_CONFIG': {
                'family': self.font_family_combo.currentText(),
                'sizes': {
                    'small': self.font_size_small_spin.value(),
                    'normal': self.font_size_normal_spin.value(),
                    'large': self.font_size_large_spin.value()
                }
            },
            'UI_CONFIG': {
                'animation_duration': self.animation_duration_spin.value(),
                'tooltip_delay': self.tooltip_delay_spin.value(),
                'auto_save_interval': self.auto_save_interval_spin.value(),
                'show_passwords_default': self.show_passwords_check.isChecked(),
                'card_hover_animation': self.card_hover_animation_check.isChecked(),
                'batch_load_size': self.batch_load_size_spin.value(),
                'scroll_load_threshold': self.scroll_load_threshold_spin.value(),
                'max_recent_files': self.max_recent_files_spin.value()
            },
            'SECURITY_CONFIG': {
                'password_min_length': self.password_min_length_spin.value(),
                'password_max_length': self.password_max_length_spin.value(),
                'session_timeout': self.session_timeout_spin.value(),
                'auto_lock_enabled': self.auto_lock_check.isChecked(),
                'clipboard_clear_timeout': self.clipboard_timeout_spin.value()
            },
            'IMPORT_EXPORT_CONFIG': {
                'max_file_size': self.max_file_size_spin.value() * 1024 * 1024,
                'backup_on_import': self.backup_on_import_check.isChecked(),
                'validate_on_import': self.validate_on_import_check.isChecked()
            },
            'LOG_CONFIG': {
                'level': self.log_level_combo.currentText(),
                'file_path': self.log_file_path_edit.text(),
                'max_file_size': self.log_max_size_spin.value() * 1024 * 1024,
                'backup_count': self.log_backup_count_spin.value()
            }
        }
        
        # 颜色配置
        if hasattr(self.primary_color_btn, 'color'):
            if 'COLOR_THEME' not in self.config_changes:
                self.config_changes['COLOR_THEME'] = {}
            self.config_changes['COLOR_THEME']['primary'] = self.primary_color_btn.color
        
        if hasattr(self.accent_color_btn, 'color'):
            if 'COLOR_THEME' not in self.config_changes:
                self.config_changes['COLOR_THEME'] = {}
            self.config_changes['COLOR_THEME']['accent'] = self.accent_color_btn.color
    
    def _save_user_config(self):
        """保存用户配置到文件"""
        # 使用config模块的保存功能
        if not config.save_user_settings(self.config_changes):
            raise Exception("保存用户配置失败")