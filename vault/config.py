# -*- coding: utf-8 -*-
"""
应用配置文件
集中管理所有可配置项
"""
import json
import os

# 应用基本配置
APP_CONFIG = {
    'name': 'MimaVault',
    'organization': 'Mima',
    'version': '1.1.0',
    'description': '密码管理器'
}

# 窗口配置
WINDOW_CONFIG = {
    'default_width': 1100,
    'default_height': 720,
    'min_width': 800,
    'min_height': 600,
    'resizable': True
}

# 卡片配置
CARD_CONFIG = {
    'width': 320,
    'height': 120,
    'fixed_height': 120,
    'grid_spacing': 12,
    'margins': {
        'card': 12,
        'content': 10,
        'layout': 6
    }
}

# 颜色主题配置
COLOR_THEME = {
    'primary': '#5865F2',
    'primary_hover': '#4752C4',
    'background': '#101014',
    'surface': '#141420',
    'surface_variant': '#171724',
    'surface_container': '#1a1a28',
    'on_primary': '#FFFFFF',
    'on_surface': '#EAEAF2',
    'on_surface_variant': '#D7D7E0',
    'outline': '#30304a',
    'outline_variant': '#2a2a3a',
    'accent': '#cfd3ff',
    'muted': '#9aa0b5',
    'notes': '#BFC5DF',
    'error': '#ff5e5e',
    'warning': '#ffb65e',
    'success': '#6eff8e'
}

# 字体配置
FONT_CONFIG = {
    'family': "'Segoe UI', 'Microsoft Yahei', sans-serif",
    'sizes': {
        'small': 12,
        'normal': 14,
        'title': 15,
        'large': 16,
        'xlarge': 18
    },
    'weights': {
        'normal': 400,
        'medium': 500,
        'semibold': 600,
        'bold': 700
    }
}

# 间距配置
SPACING_CONFIG = {
    'xs': 2,
    'sm': 4,
    'md': 6,
    'lg': 8,
    'xl': 10,
    'xxl': 12,
    'xxxl': 16
}

# 边框圆角配置
BORDER_RADIUS_CONFIG = {
    'small': 4,
    'medium': 6,
    'large': 8,
    'xlarge': 10,
    'xxlarge': 12
}

# 文件路径配置
FILE_CONFIG = {
    'data_file': 'vault.dat',
    'icon_ico': 'image/aipot.ico',
    'icon_png': 'image/aipot.png',
    'backup_dir': 'backups',
    'export_dir': 'exports'
}

# 安全配置
SECURITY_CONFIG = {
    'password_min_length': 8,
    'password_max_length': 128,
    'session_timeout': 3600,  # 会话超时时间（秒）
    'auto_lock_enabled': True,  # 是否启用自动锁定
    'clipboard_clear_timeout': 30,  # 剪贴板清除超时时间（秒）
}

# UI交互配置
UI_CONFIG = {
    'animation_duration': 200,  # 动画持续时间（毫秒）
    'tooltip_delay': 500,  # 工具提示延迟（毫秒）
    'double_click_interval': 400,  # 双击间隔（毫秒）
    'search_debounce': 300,  # 搜索防抖延迟（毫秒）
    'auto_save_interval': 30,  # 自动保存间隔（秒）
    'max_recent_files': 10,  # 最大最近文件数
    'batch_load_size': 50,  # 批量加载大小
    'scroll_load_threshold': 10,  # 滚动加载阈值
    'card_hover_animation': True,  # 卡片悬停动画
    'show_passwords_default': False,  # 默认是否显示密码
    'context_menu_enabled': True  # 是否启用右键菜单
}

# 对话框配置
DIALOG_CONFIG = {
    'password_generator': {
        'width': 100,  # 密码生成器对话框宽度
        'height': 300,  # 密码生成器对话框高度
        'modal': True,  # 是否为模态对话框
        'resizable': False  # 是否可调整大小
    },
    'account_dialog': {
        'width': 300,  # 账号对话框宽度
        'height': 400,  # 账号对话框高度
        'modal': True,  # 是否为模态对话框
        'resizable': True  # 是否可调整大小
    },
    'master_password': {
        'width': 350,  # 主密码对话框宽度
        'height': 200,  # 主密码对话框高度
        'modal': True,  # 是否为模态对话框
        'resizable': False  # 是否可调整大小
    },
    'settings': {
        'width': 500,  # 设置对话框宽度
        'height': 600,  # 设置对话框高度
        'modal': True,  # 是否为模态对话框
        'resizable': True  # 是否可调整大小
    },
    'input_dialog': {
        'width': 400,  # 输入对话框宽度
        'height': 150,  # 输入对话框高度
        'modal': True,  # 是否为模态对话框
        'resizable': False  # 是否可调整大小
    }
}

# 密码生成器配置
PASSWORD_GENERATOR_CONFIG = {
    'default_length': 16,  # 默认密码长度
    'min_length': 4,  # 最小密码长度
    'max_length': 128,  # 最大密码长度
    'default_include_lowercase': True,  # 默认包含小写字母
    'default_include_uppercase': True,  # 默认包含大写字母
    'default_include_digits': True,  # 默认包含数字
    'default_include_symbols': True,  # 默认包含符号
    'character_sets': {
        'lowercase': 'abcdefghijklmnopqrstuvwxyz',  # 小写字母字符集
        'uppercase': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',  # 大写字母字符集
        'digits': '0123456789',  # 数字字符集
        'symbols': '!@#$%^&*()-_=+[]{};:,.<>/?'  # 符号字符集
    }
}

# 密码强度评估配置
PASSWORD_STRENGTH_CONFIG = {
    'weights': {
        'length_multiplier': 4,  # 长度权重（每个字符的分数）
        'type_multiplier': 10,  # 字符类型权重（每种类型的分数）
        'bonus_score': 10,  # 奖励分数
        'max_length_score': 60,  # 长度分数上限
    },
    'thresholds': {
        'bonus_length': 12,  # 获得奖励分数的最小长度
        'bonus_types': 3,  # 获得奖励分数的最小字符类型数
    },
    'strength_labels': {  # 强度标签
        'weak': '弱',
        'fair': '中等', 
        'good': '强',
        'strong': '很强'
    },
    'strength_thresholds': {  # 强度阈值
        'weak': 25,
        'fair': 50,
        'good': 75
    }
}

# 导入导出配置
IMPORT_EXPORT_CONFIG = {
    'supported_formats': ['json', 'csv', 'encrypted'],
    'max_file_size': 10 * 1024 * 1024,  # 10MB
    'backup_on_import': True,
    'validate_on_import': True
}

# 日志配置
LOG_CONFIG = {
    'level': 'INFO',
    'file_path': 'logs/app.log',
    'max_file_size': 5 * 1024 * 1024,  # 5MB
    'backup_count': 3,
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
}

# 文本和消息配置
TEXT_CONFIG = {
    'app_title': 'Mima 密码保险箱',
    'default_values': {
        'unnamed_account': '未命名',
        'default_group': '未分组',
        'undefined_group': '未定义'
    },
    'labels': {
        'username': '用户名: ',
        'password': '密码: ',
        'url': '网址: ',
        'notes': '备注: ',
        'show_password': '显示密码',
        'hide_password': '隐藏密码',
        'move_to_group': '移动至分组',
        'select_migration_target': '选择迁移目标（可选）：'
    },
    'dialog_titles': {
        'delete_group': '删除分组',
        'change_master_password': '更改主密码',
        'error': '错误'
    },
    'error_messages': {
        'account_not_found': '找不到指定的账号',
        'group_not_found': '找不到目标分组',
        'move_account_failed': '移动账号失败: {error}',
        'save_failed': '保存失败: {error}',
        'import_failed': '导入失败：{error}',
        'add_group_failed': '添加分组失败: {error}',
        'general_error': '错误'
    },
    'ui_elements': {
        'search_cache_limit': 100,  # 搜索缓存限制
        'card_spacing': 10,  # 卡片间距
        'layout_margin': 6,   # 布局边距
        'no_migration': '不迁移（自动归入\'{default_group}\'）'
    }
}

# 获取配置的便捷函数
def get_app_config(key=None):
    """获取应用配置"""
    return APP_CONFIG.get(key) if key else APP_CONFIG

def get_window_config(key=None):
    """获取窗口配置"""
    return WINDOW_CONFIG.get(key) if key else WINDOW_CONFIG

def get_card_config(key=None):
    """获取卡片配置"""
    return CARD_CONFIG.get(key) if key else CARD_CONFIG

def get_color_theme(key=None):
    """获取颜色主题配置"""
    user_settings = _load_user_settings()
    if 'colors' in user_settings:
        config = COLOR_THEME.copy()
        config.update(user_settings['colors'])
        return config.get(key) if key else config
    return COLOR_THEME.get(key) if key else COLOR_THEME

def get_font_config(key=None):
    """获取字体配置"""
    user_settings = _load_user_settings()
    if 'fonts' in user_settings:
        config = FONT_CONFIG.copy()
        if 'family' in user_settings['fonts']:
            config['family'] = user_settings['fonts']['family']
        if 'sizes' in user_settings['fonts']:
            config['sizes'].update(user_settings['fonts']['sizes'])
        if 'weights' in user_settings['fonts']:
            config['weights'].update(user_settings['fonts']['weights'])
        return config.get(key) if key else config
    return FONT_CONFIG.get(key) if key else FONT_CONFIG

def get_spacing_config(key=None):
    """获取间距配置"""
    user_settings = _load_user_settings()
    if 'spacing' in user_settings:
        config = SPACING_CONFIG.copy()
        config.update(user_settings['spacing'])
        return config.get(key) if key else config
    return SPACING_CONFIG.get(key) if key else SPACING_CONFIG

def get_border_radius_config(key=None):
    """获取边框圆角配置"""
    user_settings = _load_user_settings()
    if 'radius' in user_settings:
        config = BORDER_RADIUS_CONFIG.copy()
        config.update(user_settings['radius'])
        return config.get(key) if key else config
    return BORDER_RADIUS_CONFIG.get(key) if key else BORDER_RADIUS_CONFIG

def get_file_config(key=None):
    """获取文件配置"""
    return FILE_CONFIG.get(key) if key else FILE_CONFIG

def get_security_config(key=None):
    """获取安全配置"""
    return SECURITY_CONFIG.get(key) if key else SECURITY_CONFIG

def get_ui_config(key=None):
    """获取UI配置"""
    return UI_CONFIG.get(key) if key else UI_CONFIG

def get_import_export_config(key=None):
    """获取导入导出配置"""
    return IMPORT_EXPORT_CONFIG.get(key) if key else IMPORT_EXPORT_CONFIG

def get_log_config(key=None):
    """获取日志配置"""
    return LOG_CONFIG.get(key) if key else LOG_CONFIG

def get_text_config(key=None):
    """获取文本配置"""
    if key:
        return TEXT_CONFIG.get(key)
    return TEXT_CONFIG

def get_text(category, key=None):
    """获取特定类别的文本"""
    category_config = TEXT_CONFIG.get(category, {})
    if key:
        return category_config.get(key, '')
    return category_config

def get_password_generator_config(key=None):
    """获取密码生成器配置"""
    return PASSWORD_GENERATOR_CONFIG.get(key) if key else PASSWORD_GENERATOR_CONFIG

def get_password_strength_config(key=None):
    """获取密码强度评估配置"""
    return PASSWORD_STRENGTH_CONFIG.get(key) if key else PASSWORD_STRENGTH_CONFIG

def get_dialog_config(key=None):
    """获取对话框配置"""
    return DIALOG_CONFIG.get(key) if key else DIALOG_CONFIG

# 字体族列表
FONT_FAMILIES = [
    "'Segoe UI', 'Microsoft Yahei', sans-serif",
    "'Arial', 'Microsoft Yahei', sans-serif",
    "'Helvetica', 'Microsoft Yahei', sans-serif",
    "'Consolas', 'Courier New', monospace",
    "'Times New Roman', 'SimSun', serif",
    "'Microsoft Yahei', sans-serif",
    "'SimHei', sans-serif",
    "'KaiTi', serif"
]

# 颜色主题列表
COLOR_THEMES = {
    "深色主题": {
        "primary": "#4752C4",
        "primary_hover": "#5865F2",
        "accent": "#8091ff",
        "background": "#101014",
        "surface": "#141420",
        "surface_variant": "#171724",
        "surface_container": "#1a1a28",
        "on_primary": "#FFFFFF",
        "on_surface": "#EAEAF2",
        "on_surface_variant": "#D7D7E0",
        "outline": "#30304a",
        "outline_variant": "#2a2a3a",
        "muted": "#9aa0b5",
        "notes": "#BFC5DF",
        "error": "#ff5e5e",
        "warning": "#ffb65e",
        "success": "#6eff8e"
    },
    "浅色主题": {
        "primary": "#2196F3",
        "primary_hover": "#1976D2",
        "accent": "#FF9800",
        "background": "#FFFFFF",
        "surface": "#F5F5F5",
        "surface_variant": "#EEEEEE",
        "surface_container": "#E0E0E0",
        "on_primary": "#FFFFFF",
        "on_surface": "#212121",
        "on_surface_variant": "#424242",
        "outline": "#BDBDBD",
        "outline_variant": "#E0E0E0",
        "muted": "#757575",
        "notes": "#616161",
        "error": "#F44336",
        "warning": "#FF9800",
        "success": "#4CAF50"
    }
}

def _load_user_settings():
    """加载用户自定义设置"""
    settings_file = os.path.join(os.path.dirname(__file__), '..', 'user_settings.json')
    if os.path.exists(settings_file):
        try:
            with open(settings_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def get_user_settings():
    """获取用户设置"""
    return _load_user_settings()

def save_user_settings(settings):
    """保存用户设置"""
    settings_file = os.path.join(os.path.dirname(__file__), '..', 'user_settings.json')
    try:
        # 确保目录存在
        os.makedirs(os.path.dirname(settings_file), exist_ok=True)
        with open(settings_file, 'w', encoding='utf-8') as f:
            json.dump(settings, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"保存用户设置失败: {e}")
        return False

def get_config_by_category(category):
    """根据类别获取配置项"""
    config_map = {
        'app': APP_CONFIG,
        'window': WINDOW_CONFIG,
        'card': CARD_CONFIG,
        'color': COLOR_THEME,
        'font': FONT_CONFIG,
        'spacing': SPACING_CONFIG,
        'border': BORDER_RADIUS_CONFIG,
        'file': FILE_CONFIG,
        'security': SECURITY_CONFIG,
        'ui': UI_CONFIG,
        'dialog': DIALOG_CONFIG,
        'password_generator': PASSWORD_GENERATOR_CONFIG,
        'password_strength': PASSWORD_STRENGTH_CONFIG,
        'import_export': IMPORT_EXPORT_CONFIG,
        'log': LOG_CONFIG,
        'text': TEXT_CONFIG
    }
    return config_map.get(category, {})

def update_config_by_category(category, new_config):
    """根据类别更新配置项"""
    global APP_CONFIG, WINDOW_CONFIG, CARD_CONFIG, COLOR_THEME, FONT_CONFIG
    global SPACING_CONFIG, BORDER_RADIUS_CONFIG, FILE_CONFIG, SECURITY_CONFIG
    global UI_CONFIG, DIALOG_CONFIG, PASSWORD_GENERATOR_CONFIG, PASSWORD_STRENGTH_CONFIG
    global IMPORT_EXPORT_CONFIG, LOG_CONFIG
    
    config_map = {
        'app': 'APP_CONFIG',
        'window': 'WINDOW_CONFIG',
        'card': 'CARD_CONFIG',
        'color': 'COLOR_THEME',
        'font': 'FONT_CONFIG',
        'spacing': 'SPACING_CONFIG',
        'border': 'BORDER_RADIUS_CONFIG',
        'file': 'FILE_CONFIG',
        'security': 'SECURITY_CONFIG',
        'ui': 'UI_CONFIG',
        'dialog': 'DIALOG_CONFIG',
        'password_generator': 'PASSWORD_GENERATOR_CONFIG',
        'password_strength': 'PASSWORD_STRENGTH_CONFIG',
        'import_export': 'IMPORT_EXPORT_CONFIG',
        'log': 'LOG_CONFIG'
    }
    
    if category in config_map:
        globals()[config_map[category]].update(new_config)
        return True
    return False

def apply_user_config(user_config):
    """应用用户配置到当前运行的配置"""
    for config_name, config_data in user_config.items():
        if config_name in globals():
            globals()[config_name].update(config_data)

def load_and_apply_user_config():
    """加载并应用用户配置"""
    user_settings = get_user_settings()
    if user_settings:
        apply_user_config(user_settings)