# -*- coding: utf-8 -*-
"""
配置编辑对话框样式
为配置编辑对话框提供统一的样式定义
"""

from .config import get_color_theme, get_font_config, get_spacing_config, get_border_radius_config


def load_config_editor_style():
    """加载配置编辑对话框样式"""
    colors = get_color_theme()
    fonts = get_font_config()
    spacing = get_spacing_config()
    radius = get_border_radius_config()
    
    return f"""
    /* 配置编辑对话框主体样式 */
    QDialog#ConfigEditorDialog {{
        background-color: {colors['background']};
        color: {colors['on_surface']};
        font-family: {fonts['family']};
        font-size: {fonts['sizes']['normal']}px;
    }}
    
    /* 选项卡控件样式 */
    QTabWidget {{
        background-color: {colors['surface']};
        border: 1px solid {colors['outline_variant']};
        border-radius: {radius['medium']}px;
    }}
    
    QTabWidget::pane {{
        background-color: {colors['surface']};
        border: 1px solid {colors['outline_variant']};
        border-radius: {radius['medium']}px;
        top: -1px;
    }}
    
    QTabBar::tab {{
        background-color: {colors['surface_variant']};
        color: {colors['on_surface_variant']};
        padding: {spacing['lg']}px {spacing['xxl']}px;
        margin-right: {spacing['xs']}px;
        border-top-left-radius: {radius['medium']}px;
        border-top-right-radius: {radius['medium']}px;
        font-weight: {fonts['weights']['medium']};
        min-width: 80px;
    }}
    
    QTabBar::tab:selected {{
        background-color: {colors['primary']};
        color: {colors['on_primary']};
        font-weight: {fonts['weights']['semibold']};
    }}
    
    QTabBar::tab:hover:!selected {{
        background-color: {colors['outline_variant']};
        color: {colors['on_surface']};
    }}
    
    /* 分组框样式 */
    QGroupBox {{
        font-weight: {fonts['weights']['semibold']};
        font-size: {fonts['sizes']['title']}px;
        color: {colors['on_surface']};
        border: 1px solid {colors['outline_variant']};
        border-radius: {radius['medium']}px;
        margin-top: {spacing['xl']}px;
        padding-top: {spacing['md']}px;
    }}
    
    QGroupBox::title {{
        subcontrol-origin: margin;
        left: {spacing['xl']}px;
        padding: 0 {spacing['md']}px 0 {spacing['md']}px;
        background-color: {colors['surface']};
        color: {colors['primary']};
    }}
    
    /* 表单布局样式 */
    QFormLayout {{
        spacing: {spacing['lg']}px;
    }}
    
    /* 标签样式 */
    QLabel {{
        color: {colors['on_surface']};
        font-size: {fonts['sizes']['normal']}px;
        font-weight: {fonts['weights']['normal']};
    }}
    
    /* 输入框样式 */
    QLineEdit {{
        background-color: {colors['surface_container']};
        color: {colors['on_surface']};
        border: 1px solid {colors['outline_variant']};
        border-radius: {radius['small']}px;
        padding: {spacing['md']}px {spacing['lg']}px;
        font-size: {fonts['sizes']['normal']}px;
        selection-background-color: {colors['primary']};
        selection-color: {colors['on_primary']};
    }}
    
    QLineEdit:focus {{
        border: 2px solid {colors['primary']};
        background-color: {colors['surface']};
    }}
    
    QLineEdit:hover {{
        border-color: {colors['outline']};
    }}
    
    /* 数字输入框样式 */
    QSpinBox {{
        background-color: {colors['surface_container']};
        color: {colors['on_surface']};
        border: 1px solid {colors['outline_variant']};
        border-radius: {radius['small']}px;
        padding: {spacing['md']}px {spacing['lg']}px;
        font-size: {fonts['sizes']['normal']}px;
        selection-background-color: {colors['primary']};
        selection-color: {colors['on_primary']};
    }}
    
    QSpinBox:focus {{
        border: 2px solid {colors['primary']};
        background-color: {colors['surface']};
    }}
    
    QSpinBox:hover {{
        border-color: {colors['outline']};
    }}
    
    QSpinBox::up-button, QSpinBox::down-button {{
        background-color: {colors['surface_variant']};
        border: none;
        width: 16px;
        border-radius: {radius['small']}px;
    }}
    
    QSpinBox::up-button:hover, QSpinBox::down-button:hover {{
        background-color: {colors['outline_variant']};
    }}
    
    QSpinBox::up-arrow {{
        image: none;
        border-left: 4px solid transparent;
        border-right: 4px solid transparent;
        border-bottom: 4px solid {colors['on_surface_variant']};
        width: 0px;
        height: 0px;
    }}
    
    QSpinBox::down-arrow {{
        image: none;
        border-left: 4px solid transparent;
        border-right: 4px solid transparent;
        border-top: 4px solid {colors['on_surface_variant']};
        width: 0px;
        height: 0px;
    }}
    
    /* 下拉框样式 */
    QComboBox {{
        background-color: {colors['surface_container']};
        color: {colors['on_surface']};
        border: 1px solid {colors['outline_variant']};
        border-radius: {radius['small']}px;
        padding: {spacing['md']}px {spacing['lg']}px;
        font-size: {fonts['sizes']['normal']}px;
        min-width: 120px;
    }}
    
    QComboBox:focus {{
        border: 2px solid {colors['primary']};
        background-color: {colors['surface']};
    }}
    
    QComboBox:hover {{
        border-color: {colors['outline']};
    }}
    
    QComboBox::drop-down {{
        border: none;
        width: 20px;
    }}
    
    QComboBox::down-arrow {{
        image: none;
        border-left: 4px solid transparent;
        border-right: 4px solid transparent;
        border-top: 4px solid {colors['on_surface_variant']};
        width: 0px;
        height: 0px;
    }}
    
    QComboBox QAbstractItemView {{
        background-color: {colors['surface']};
        color: {colors['on_surface']};
        border: 1px solid {colors['outline_variant']};
        border-radius: {radius['small']}px;
        selection-background-color: {colors['primary']};
        selection-color: {colors['on_primary']};
        outline: none;
    }}
    
    /* 复选框样式 */
    QCheckBox {{
        color: {colors['on_surface']};
        font-size: {fonts['sizes']['normal']}px;
        spacing: {spacing['md']}px;
    }}
    
    QCheckBox::indicator {{
        width: 16px;
        height: 16px;
        border: 2px solid {colors['outline_variant']};
        border-radius: {radius['small']}px;
        background-color: {colors['surface_container']};
    }}
    
    QCheckBox::indicator:hover {{
        border-color: {colors['primary']};
        background-color: {colors['surface']};
    }}
    
    QCheckBox::indicator:checked {{
        background-color: {colors['primary']};
        border-color: {colors['primary']};
        image: none;
    }}
    
    /* 按钮样式 */
    QPushButton {{
        background-color: {colors['surface_variant']};
        color: {colors['on_surface']};
        border: 1px solid {colors['outline_variant']};
        border-radius: {radius['medium']}px;
        padding: {spacing['lg']}px {spacing['xxl']}px;
        font-size: {fonts['sizes']['normal']}px;
        font-weight: {fonts['weights']['medium']};
        min-width: 80px;
    }}
    
    QPushButton:hover {{
        background-color: {colors['outline_variant']};
        border-color: {colors['outline']};
    }}
    
    QPushButton:pressed {{
        background-color: {colors['outline']};
    }}
    
    QPushButton:default {{
        background-color: {colors['primary']};
        color: {colors['on_primary']};
        border-color: {colors['primary']};
        font-weight: {fonts['weights']['semibold']};
    }}
    
    QPushButton:default:hover {{
        background-color: {colors['primary_hover']};
        border-color: {colors['primary_hover']};
    }}
    
    QPushButton:default:pressed {{
        background-color: {colors['primary']};
    }}
    
    /* 颜色选择按钮特殊样式 */
    QPushButton[objectName="colorButton"] {{
        border: 2px solid {colors['outline_variant']};
        border-radius: {radius['small']}px;
        min-width: 60px;
        max-width: 60px;
        min-height: 30px;
        max-height: 30px;
    }}
    
    QPushButton[objectName="colorButton"]:hover {{
        border-color: {colors['primary']};
    }}
    
    /* 滚动区域样式 */
    QScrollArea {{
        background-color: {colors['surface']};
        border: none;
    }}
    
    QScrollBar:vertical {{
        background-color: {colors['surface_variant']};
        width: 12px;
        border-radius: 6px;
        margin: 0;
    }}
    
    QScrollBar::handle:vertical {{
        background-color: {colors['outline_variant']};
        border-radius: 6px;
        min-height: 20px;
        margin: 2px;
    }}
    
    QScrollBar::handle:vertical:hover {{
        background-color: {colors['outline']};
    }}
    
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0px;
    }}
    
    QScrollBar:horizontal {{
        background-color: {colors['surface_variant']};
        height: 12px;
        border-radius: 6px;
        margin: 0;
    }}
    
    QScrollBar::handle:horizontal {{
        background-color: {colors['outline_variant']};
        border-radius: 6px;
        min-width: 20px;
        margin: 2px;
    }}
    
    QScrollBar::handle:horizontal:hover {{
        background-color: {colors['outline']};
    }}
    
    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
        width: 0px;
    }}
    
    /* 工具提示样式 */
    QToolTip {{
        background-color: {colors['surface_container']};
        color: {colors['on_surface']};
        border: 1px solid {colors['outline_variant']};
        border-radius: {radius['small']}px;
        padding: {spacing['sm']}px {spacing['md']}px;
        font-size: {fonts['sizes']['small']}px;
    }}
    """