from .config import get_color_theme, get_font_config, get_spacing_config, get_border_radius_config


def load_app_style():
    # 获取配置
    colors = get_color_theme()
    fonts = get_font_config()
    spacing = get_spacing_config()
    radius = get_border_radius_config()
    
    # Modern dark theme QSS (使用配置)
    return f"""
    * {{ font-family: {fonts['family']}; }}
    QMainWindow {{ background: {colors['background']}; }}

    QMenuBar {{ background-color: {colors['surface']}; color: {colors['on_surface']}; border-bottom: 1px solid {colors['outline_variant']}; }}
    QMenuBar::item {{ padding: {spacing['md']}px {spacing['xxl']}px; margin: {spacing['xs']}px {spacing['sm']}px; border-radius: {radius['medium']}px; }}
    QMenuBar::item:selected {{ background: {colors['outline_variant']}; }}
    QMenuBar::item:pressed {{ background: #23233a; }}

    QMenu {{ background: {colors['surface_container']}; color: {colors['on_surface']}; border: 1px solid {colors['outline']}; padding: {spacing['md']}px; }}
    QMenu::item {{ padding: {spacing['md']}px {spacing['xl']}px; border-radius: {radius['medium']}px; }}
    QMenu::item:selected {{ background: #2b2b40; color: {colors['accent']}; }}
    QMenu::separator {{ height: 1px; background: {colors['outline_variant']}; margin: {spacing['md']}px {spacing['sm']}px; }}
    QStatusBar {{ color: {colors['on_surface_variant']}; }}

    QWidget#SidePanel {{ background: {colors['surface']}; border-right: 1px solid {colors['outline_variant']}; }}
    QTreeWidget {{ background: {colors['surface_variant']}; color: {colors['on_surface_variant']}; border: none; outline: none; }}
    QTreeWidget::item {{ 
        padding: {spacing['md']}px {spacing['lg']}px; 
        border-radius: {radius['medium']}px; 
        margin: 1px {spacing['xs']}px;
    }}
    QTreeWidget::item:selected {{ 
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {colors['primary']}, stop:1 {colors['primary_hover']});
        color: {colors['on_primary']};
        border: 2px solid {colors['accent']};
        font-weight: {fonts['weights']['semibold']};
    }}
    QTreeWidget::item:hover {{ 
        background: {colors['surface_container']}; 
        border: 1px solid {colors['outline']};
    }}
    QTreeWidget::item:selected:hover {{ 
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {colors['primary_hover']}, stop:1 {colors['primary']});
        border: 2px solid {colors['accent']};
    }}

    QLineEdit, QTextEdit, QSpinBox, QComboBox {{
        background: {colors['surface_container']}; color: {colors['on_surface']}; border: 1px solid {colors['outline']}; border-radius: {radius['medium']}px; padding: {spacing['md']}px; }}
    QLineEdit:focus, QTextEdit:focus, QComboBox:focus {{ border: 1px solid {colors['primary']}; }}
    /* QComboBox 下拉面板与箭头 */
    QComboBox::drop-down {{ border-left: 1px solid {colors['outline']}; width: 26px; background: #1f1f2e; }}
    QComboBox::down-arrow {{ width: 10px; height: 10px; }}
    QComboBox QAbstractItemView {{ background: {colors['surface_container']}; color: {colors['on_surface']}; selection-background-color: #2c2c44; selection-color: {colors['accent']}; border: 1px solid {colors['outline']}; outline: 0; }}
    QComboBox QAbstractItemView::item {{ padding: {spacing['md']}px {spacing['xl']}px; }}
    QComboBox QAbstractItemView::item:selected {{ background: #2c2c44; }}

    QPushButton {{ background: #2b2b40; color: #ffffff; border: 1px solid #3a3a55; border-radius: {radius['large']}px; padding: {spacing['md']}px {spacing['xxl']}px; }}
    QPushButton:hover {{ background: #353557; }}
    QPushButton:pressed {{ background: #262644; }}
    QPushButton#Primary {{ background: {colors['primary']}; border: none; }}
    QPushButton#Primary:hover {{ background: {colors['primary_hover']}; }}

    QSplitter#MainSplitter::handle {{ background: {colors['background']}; }}
    QSplitter::handle:horizontal {{ width: {spacing['md']}px; }}

    QHeaderView::section {{ background: #1d1d2b; color: {colors['accent']}; border: none; padding: {spacing['md']}px; }}
    QTableWidget {{ background: {colors['surface_variant']}; color: {colors['on_surface_variant']}; gridline-color: {colors['outline_variant']}; alternate-background-color: #141422; }}
    QTableWidget::item {{ padding: {spacing['md']}px; }}
    QTableWidget::item:selected {{ background: #2c2c44; border-radius: {radius['medium']}px; }}
    QTableWidget QTableCornerButton::section {{ background: #1d1d2b; }}

    /* 行高更舒适 */
    QTableView::item {{ height: 30px; }}

    QProgressBar {{ background: #1b1b28; border: 1px solid {colors['outline']}; border-radius: {radius['large']}px; text-align: center; color: {colors['accent']}; }}
    QProgressBar::chunk {{ background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {colors['error']}, stop:0.5 {colors['warning']}, stop:1 {colors['success']}); border-radius: {radius['large']}px; }}

    QToolBar {{ background: {colors['surface']}; border-bottom: 1px solid {colors['outline_variant']}; spacing: {spacing['lg']}px; padding: {spacing['sm']}px {spacing['md']}px; }}
    QToolBar QLineEdit {{ min-height: 28px; border-radius: {radius['medium']}px; padding-left: {spacing['lg']}px; }}
    QToolBar QToolButton {{ background: #2b2b40; color: {colors['on_surface']}; border: 1px solid #3a3a55; border-radius: {radius['medium']}px; padding: {spacing['sm']}px {spacing['xl']}px; }}
    QToolBar QToolButton:hover {{ background: #353557; }}
    QToolBar QToolButton:pressed {{ background: #262644; }}
    QToolBar QToolButton:checked {{ background: {colors['primary_hover']}; border-color: {colors['primary_hover']}; }}

    QDialog {{ background: #161624; }}
    QLabel {{ color: {colors['on_surface_variant']}; }}

    /* 复选框样式 - 提高文字对比度和醒目程度 */
    QCheckBox {{
        color: {colors['on_surface']};
        font-weight: {fonts['weights']['medium']};
        font-size: {fonts['sizes']['normal']}px;
        spacing: {spacing['md']}px;
        padding: {spacing['sm']}px;
    }}
    QCheckBox::indicator {{
        width: 18px;
        height: 18px;
        border: 2px solid {colors['outline']};
        border-radius: {radius['small']}px;
        background: {colors['surface_container']};
    }}
    QCheckBox::indicator:hover {{
        border-color: {colors['primary']};
        background: {colors['surface_container']};
    }}
    QCheckBox::indicator:checked {{
        background: {colors['primary']};
        border-color: {colors['primary']};
        image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iMTIiIHZpZXdCb3g9IjAgMCAxMiAxMiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTEwIDNMNC41IDguNUwyIDYiIHN0cm9rZT0iI2ZmZmZmZiIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiLz4KPC9zdmc+);
    }}
    QCheckBox::indicator:checked:hover {{
        background: {colors['primary_hover']};
        border-color: {colors['primary_hover']};
    }}
    QCheckBox:disabled {{
        color: {colors['on_surface_variant']};
    }}
    QCheckBox::indicator:disabled {{
        border-color: {colors['outline_variant']};
        background: {colors['surface_variant']};
    }}

    /* 密码生成器对话框专用样式 */
    QDialog#PasswordGeneratorDialog {{
        background: {colors['surface']};
        border: 1px solid {colors['outline']};
        border-radius: {radius['large']}px;
    }}
    QDialog#PasswordGeneratorDialog QCheckBox {{
        color: {colors['on_surface']};
        font-weight: {fonts['weights']['semibold']};
        font-size: {fonts['sizes']['normal']}px;
        padding: {spacing['md']}px {spacing['lg']}px;
        margin: {spacing['sm']}px 0px;
    }}
    QDialog#PasswordGeneratorDialog QLabel {{
        color: {colors['on_surface']};
        font-weight: {fonts['weights']['medium']};
    }}
    QDialog#PasswordGeneratorDialog QSpinBox {{
        font-weight: {fonts['weights']['medium']};
        min-width: 80px;
    }}
    QDialog#PasswordGeneratorDialog QPushButton {{
        font-weight: {fonts['weights']['medium']};
        min-height: 32px;
        padding: {spacing['md']}px {spacing['xl']}px;
    }}
    QDialog#PasswordGeneratorDialog QLineEdit {{
        font-weight: {fonts['weights']['medium']};
        min-height: 28px;
    }}
    QDialog#PasswordGeneratorDialog QProgressBar {{
        font-weight: {fonts['weights']['medium']};
        text-align: center;
    }}

    /* 账号对话框中的工具按钮样式 */
    QDialog#AccountDialog QToolButton {{
        background: #2b2b40;
        color: {colors['on_surface']};
        border: 1px solid #3a3a55;
        border-radius: {radius['medium']}px;
        padding: {spacing['sm']}px {spacing['lg']}px;
        font-weight: {fonts['weights']['medium']};
        min-width: 50px;
        min-height: 28px;
    }}
    QDialog#AccountDialog QToolButton:hover {{
        background: #353557;
        border-color: {colors['primary']};
    }}
    QDialog#AccountDialog QToolButton:pressed {{
        background: #262644;
        border-color: {colors['accent']};
    }}
    QDialog#AccountDialog QToolButton:checked {{
        background: {colors['primary']};
        color: {colors['on_primary']};
        border-color: {colors['primary']};
    }}
    QDialog#AccountDialog QToolButton:checked:hover {{
        background: {colors['primary_hover']};
        border-color: {colors['primary_hover']};
    }}

    /* 卡片视图样式 */
    QListWidget#CardList {{ background: {colors['surface_variant']}; color: {colors['on_surface_variant']}; border: none; padding: {spacing['md']}px; }}
    QListWidget#CardList::item {{ margin: 0px; }}

    /* 账号卡片样式 - 禁用文本选择，优化交互反馈 */
    QFrame#AccountCard {{ 
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #1c1c2a, stop:1 #181826); 
        color: {colors['on_surface']}; 
        border: 1px solid {colors['outline']}; 
        border-radius: {radius['large']}px;
        selection-background-color: transparent;
        margin: {spacing['xs']}px;
    }}
    
    /* 禁用所有卡片内文本选择 */
    QFrame#AccountCard QLabel {{
        selection-background-color: transparent;
        selection-color: {colors['on_surface']};
    }}
    
    /* 悬停状态 - 使用QSS支持的属性 */
    QFrame#AccountCard[hovered="true"] {{ 
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #212137, stop:1 #1d1d33); 
        border-color: {colors['primary_hover']};
    }}
    
    /* 选中状态 */
    QFrame#AccountCard[selected="true"] {{ 
        border: 2px solid {colors['accent']}; 
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #1f1f35, stop:1 #1b1b31);
    }}
    
    /* 选中且悬停状态 */
    QFrame#AccountCard[selected="true"][hovered="true"] {{ 
        border: 2px solid #9ca6ff; 
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #242240, stop:1 #202038);
    }}

    QLabel[role="title"] {{ font-size: {fonts['sizes']['large']}px; font-weight: {fonts['weights']['bold']}; color: {colors['on_surface']}; }}
    QLabel[role="muted"] {{ color: {colors['on_surface_variant']}; }}
    QLabel[role="notes"] {{ color: #BFC5DF; }}
    QLabel#GroupTag {{ 
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {colors['primary']}, stop:1 {colors['primary_hover']});
        border: 1px solid {colors['accent']}; 
        border-radius: {radius['large']}px; 
        padding: {spacing['sm']}px {spacing['xl']}px; 
        color: {colors['on_primary']}; 
        font-weight: {fonts['weights']['medium']};
        font-size: {fonts['sizes']['small']}px;
        min-height: 20px;
    }}

    QScrollBar:vertical {{ background: {colors['surface']}; width: {spacing['xl']}px; margin: 0px; }}
    QScrollBar::handle:vertical {{ background: #2b2b40; border-radius: {spacing['sm']}px; }}
    QScrollBar::handle:vertical:hover {{ background: #353557; }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
    """