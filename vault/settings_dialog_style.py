from .config import get_color_theme, get_font_config, get_spacing_config, get_border_radius_config


def load_settings_dialog_style():
    """加载设置对话框专用样式"""
    # 获取配置
    colors = get_color_theme()
    fonts = get_font_config()
    spacing = get_spacing_config()
    radius = get_border_radius_config()
    
    return f"""
    /* 设置对话框基础样式 */
    QDialog#SettingsDialog {{
        background: {colors['surface']};
        border: 1px solid {colors['outline']};
        border-radius: {radius['large']}px;
        color: {colors['on_surface']};
    }}
    
    /* 移除标题样式 */
    
    /* 选项卡样式 */
    QDialog#SettingsDialog QTabWidget {{
        background: transparent;
        border: none;
    }}
    
    QDialog#SettingsDialog QTabWidget::pane {{
        background: {colors['surface_container']};
        border: 1px solid {colors['outline']};
        border-radius: {radius['medium']}px;
        margin-top: {spacing['sm']}px;
    }}
    
    QDialog#SettingsDialog QTabBar::tab {{
        background: {colors['surface_variant']};
        color: {colors['on_surface_variant']};
        border: 1px solid {colors['outline_variant']};
        border-bottom: none;
        border-radius: {radius['medium']}px {radius['medium']}px 0px 0px;
        padding: {spacing['md']}px {spacing['xxl']}px;
        margin-right: {spacing['xs']}px;
        font-weight: {fonts['weights']['medium']};
        font-size: {fonts['sizes']['normal']}px;
    }}
    
    QDialog#SettingsDialog QTabBar::tab:selected {{
        background: {colors['primary']};
        color: {colors['on_primary']};
        border-color: {colors['primary']};
        font-weight: {fonts['weights']['semibold']};
    }}
    
    QDialog#SettingsDialog QTabBar::tab:hover:!selected {{
        background: {colors['surface_container']};
        border-color: {colors['outline']};
    }}
    
    /* 分组框样式 */
    QDialog#SettingsDialog QGroupBox {{
        font-weight: {fonts['weights']['semibold']};
        font-size: {fonts['sizes']['title']}px;
        color: {colors['on_surface']};
        border: 1px solid {colors['outline']};
        border-radius: {radius['medium']}px;
        margin-top: {spacing['lg']}px;
        padding-top: {spacing['md']}px;
        background: {colors['surface_variant']};
    }}
    
    QDialog#SettingsDialog QGroupBox::title {{
        subcontrol-origin: margin;
        left: {spacing['lg']}px;
        padding: 0px {spacing['md']}px;
        background: {colors['surface_variant']};
        color: {colors['accent']};
        font-weight: {fonts['weights']['bold']};
    }}
    
    /* 标签样式 */
    QDialog#SettingsDialog QLabel {{
        color: {colors['on_surface']};
        font-size: {fonts['sizes']['normal']}px;
        font-weight: {fonts['weights']['medium']};
        padding: {spacing['sm']}px 0px;
    }}
    
    /* 下拉框样式 */
    QDialog#SettingsDialog QComboBox {{
        background: {colors['surface_container']};
        color: {colors['on_surface']};
        border: 1px solid {colors['outline']};
        border-radius: {radius['medium']}px;
        padding: {spacing['md']}px {spacing['lg']}px;
        font-size: {fonts['sizes']['normal']}px;
        font-weight: {fonts['weights']['medium']};
        min-height: 28px;
    }}
    
    QDialog#SettingsDialog QComboBox:focus {{
        border: 2px solid {colors['primary']};
    }}
    
    QDialog#SettingsDialog QComboBox::drop-down {{
        border-left: 1px solid {colors['outline']};
        width: 26px;
        background: {colors['surface_container']};
        border-radius: 0px {radius['medium']}px {radius['medium']}px 0px;
    }}
    
    QDialog#SettingsDialog QComboBox::down-arrow {{
        width: 12px;
        height: 12px;
        image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iMTIiIHZpZXdCb3g9IjAgMCAxMiAxMiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTMgNC41TDYgNy41TDkgNC41IiBzdHJva2U9IiM4MDkxZmYiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIi8+Cjwvc3ZnPg==);
    }}
    
    QDialog#SettingsDialog QComboBox QAbstractItemView {{
        background: {colors['surface_container']};
        color: {colors['on_surface']};
        selection-background-color: {colors['primary']};
        selection-color: {colors['on_primary']};
        border: 1px solid {colors['outline']};
        border-radius: {radius['medium']}px;
        outline: none;
    }}
    
    QDialog#SettingsDialog QComboBox QAbstractItemView::item {{
        padding: {spacing['md']}px {spacing['lg']}px;
        border: none;
        min-height: 24px;
    }}
    
    QDialog#SettingsDialog QComboBox QAbstractItemView::item:selected {{
        background: {colors['primary']};
        color: {colors['on_primary']};
    }}
    
    QDialog#SettingsDialog QComboBox QAbstractItemView::item:hover {{
        background: {colors['surface_variant']};
    }}
    
    /* 数字输入框样式 */
    QDialog#SettingsDialog QSpinBox {{
        background: {colors['surface_container']};
        color: {colors['on_surface']};
        border: 1px solid {colors['outline']};
        border-radius: {radius['medium']}px;
        padding: {spacing['md']}px {spacing['lg']}px;
        font-size: {fonts['sizes']['normal']}px;
        font-weight: {fonts['weights']['medium']};
        min-height: 28px;
        min-width: 80px;
    }}
    
    QDialog#SettingsDialog QSpinBox:focus {{
        border: 2px solid {colors['primary']};
    }}
    
    QDialog#SettingsDialog QSpinBox::up-button, 
    QDialog#SettingsDialog QSpinBox::down-button {{
        background: {colors['surface_variant']};
        border: 1px solid {colors['outline']};
        width: 20px;
    }}
    
    QDialog#SettingsDialog QSpinBox::up-button:hover, 
    QDialog#SettingsDialog QSpinBox::down-button:hover {{
        background: {colors['primary_hover']};
    }}
    
    QDialog#SettingsDialog QSpinBox::up-arrow {{
        image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTAiIGhlaWdodD0iMTAiIHZpZXdCb3g9IjAgMCAxMCAxMCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTIuNSA2LjI1TDUgMy43NUw3LjUgNi4yNSIgc3Ryb2tlPSIjODA5MWZmIiBzdHJva2Utd2lkdGg9IjEuNSIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIi8+Cjwvc3ZnPg==);
        width: 10px;
        height: 10px;
    }}
    
    QDialog#SettingsDialog QSpinBox::down-arrow {{
        image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTAiIGhlaWdodD0iMTAiIHZpZXdCb3g9IjAgMCAxMCAxMCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTcuNSAzLjc1TDUgNi4yNUwyLjUgMy43NSIgc3Ryb2tlPSIjODA5MWZmIiBzdHJva2Utd2lkdGg9IjEuNSIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIi8+Cjwvc3ZnPg==);
        width: 10px;
        height: 10px;
    }}
    
    /* 颜色按钮样式 */
    QDialog#SettingsDialog QPushButton#ColorButton {{
        border: 2px solid {colors['outline']};
        border-radius: {radius['medium']}px;
        font-size: {fonts['sizes']['small']}px;
        font-weight: {fonts['weights']['medium']};
        color: {colors['on_surface']};
        min-height: 30px;
        min-width: 60px;
    }}
    
    QDialog#SettingsDialog QPushButton#ColorButton:hover {{
        border-color: {colors['primary']};
    }}
    
    QDialog#SettingsDialog QPushButton#ColorButton:pressed {{
        border-color: {colors['accent']};
    }}
    
    /* 普通按钮样式 */
    QDialog#SettingsDialog QPushButton {{
        background: {colors['surface_variant']};
        color: {colors['on_surface']};
        border: 1px solid {colors['outline']};
        border-radius: {radius['medium']}px;
        padding: {spacing['md']}px {spacing['xxl']}px;
        font-size: {fonts['sizes']['normal']}px;
        font-weight: {fonts['weights']['medium']};
        min-height: 32px;
    }}
    
    QDialog#SettingsDialog QPushButton:hover {{
        background: {colors['surface_container']};
        border-color: {colors['primary']};
    }}
    
    QDialog#SettingsDialog QPushButton:pressed {{
        background: {colors['surface']};
        border-color: {colors['accent']};
    }}
    
    /* 主要按钮样式 */
    QDialog#SettingsDialog QPushButton#PrimaryButton {{
        background: {colors['primary']};
        color: {colors['on_primary']};
        border: none;
        font-weight: {fonts['weights']['semibold']};
    }}
    
    QDialog#SettingsDialog QPushButton#PrimaryButton:hover {{
        background: {colors['primary_hover']};
    }}
    
    QDialog#SettingsDialog QPushButton#PrimaryButton:pressed {{
        background: {colors['primary']};
    }}
    
    /* 重置按钮样式 */
    QDialog#SettingsDialog QPushButton#ResetButton {{
        background: {colors['error']};
        color: {colors['on_primary']};
        border: none;
        font-weight: {fonts['weights']['medium']};
    }}
    
    QDialog#SettingsDialog QPushButton#ResetButton:hover {{
        background: #ff7070;
    }}
    
    QDialog#SettingsDialog QPushButton#ResetButton:pressed {{
        background: {colors['error']};
    }}
    
    /* 表单布局样式 */
    QDialog#SettingsDialog QFormLayout {{
        spacing: {spacing['lg']}px;
    }}
    
    /* 滚动区域样式 */
    QDialog#SettingsDialog QScrollArea {{
        background: transparent;
        border: none;
    }}
    
    QDialog#SettingsDialog QScrollArea QWidget {{
        background: transparent;
    }}
    
    QDialog#SettingsDialog QScrollBar:vertical {{
        background: {colors['surface_variant']};
        width: {spacing['lg']}px;
        border-radius: {radius['small']}px;
        margin: 0px;
    }}
    
    QDialog#SettingsDialog QScrollBar::handle:vertical {{
        background: {colors['outline']};
        border-radius: {radius['small']}px;
        min-height: 20px;
    }}
    
    QDialog#SettingsDialog QScrollBar::handle:vertical:hover {{
        background: {colors['primary']};
    }}
    
    QDialog#SettingsDialog QScrollBar::add-line:vertical, 
    QDialog#SettingsDialog QScrollBar::sub-line:vertical {{
        height: 0;
    }}
    
    /* 移除不支持的动画效果 */
    """