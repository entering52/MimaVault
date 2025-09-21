import functools
import re
from PyQt5 import QtWidgets, QtGui, QtCore
from typing import Optional, Tuple, Dict
from .models import Group, Account, PasswordStrength
from .storage import VaultStorage, VaultError
from .dialogs import AccountDialog, InputDialog, PasswordGeneratorDialog
from .settings_dialog import SettingsDialog
from .config import get_card_config, get_color_theme, get_font_config, get_spacing_config, get_border_radius_config, get_ui_config, get_text_config, get_text


class SaveThread(QtCore.QThread):
    """异步保存线程"""
    save_completed = QtCore.pyqtSignal()
    save_failed = QtCore.pyqtSignal(str)
    
    def __init__(self, storage: VaultStorage):
        super().__init__()
        self.storage = storage
    
    def run(self):
        """在后台线程中执行保存操作"""
        try:
            self.storage.save()
            self.save_completed.emit()
        except VaultError as e:
            self.save_failed.emit(str(e))
        except Exception as e:
            self.save_failed.emit(f"未知错误: {str(e)}")


class AddAccountThread(QtCore.QThread):
    """异步添加账号线程"""
    add_completed = QtCore.pyqtSignal()
    add_failed = QtCore.pyqtSignal(str)
    
    def __init__(self, storage: VaultStorage, account: Account):
        super().__init__()
        self.storage = storage
        self.account = account
    
    def run(self):
        """在后台线程中执行添加账号和保存操作"""
        try:
            self.storage.add_account(self.account)
            self.storage.save()
            self.add_completed.emit()
        except VaultError as e:
            self.add_failed.emit(str(e))
        except Exception as e:
            self.add_failed.emit(f"未知错误: {str(e)}")


class AddGroupThread(QtCore.QThread):
    """异步添加分组线程"""
    group_added = QtCore.pyqtSignal(str, str)  # real_group_id, temp_id
    group_add_failed = QtCore.pyqtSignal(str, str)  # error_msg, temp_id
    
    def __init__(self, storage: VaultStorage, group_name: str, temp_id: str):
        super().__init__()
        self.storage = storage
        self.group_name = group_name
        self.temp_id = temp_id
    
    def run(self):
        """在后台线程中执行添加分组和保存操作"""
        try:
            new_group = self.storage.add_group(self.group_name)
            self.storage.save()
            self.group_added.emit(new_group.id, self.temp_id)
        except VaultError as e:
            self.group_add_failed.emit(str(e), self.temp_id)
        except Exception as e:
            self.group_add_failed.emit(f"未知错误: {str(e)}", self.temp_id)


class AccountCard(QtWidgets.QFrame):
    # 在类级别定义信号
    clicked = QtCore.pyqtSignal(str)
    doubleClicked = QtCore.pyqtSignal(str)
    deleteRequested = QtCore.pyqtSignal(str)  # 新增删除请求信号
    moveToGroupRequested = QtCore.pyqtSignal(str, str)  # 新增移动至分组请求信号 (account_id, group_id)
    
    # 类级别缓存配置，避免重复获取
    _card_config = None
    _label_styles = {}  # 缓存标签样式
    
    @classmethod
    def _get_card_config(cls):
        if cls._card_config is None:
            cls._card_config = get_card_config()
        return cls._card_config
    
    @classmethod
    def _get_label_style(cls, role: str):
        """缓存标签样式以提高创建性能"""
        if role not in cls._label_styles:
            cls._label_styles[role] = f"[role=\"{role}\"] {{ }}"
        return cls._label_styles[role]
    
    def __init__(self, account: Account, group_name: str, show_passwords: bool, groups: list = None, parent=None):
        super().__init__(parent)
        self.account = account
        self.show_passwords = show_passwords
        self.selected = False
        self.groups = groups or []  # 存储所有分组信息
        
        self.setObjectName("AccountCard")
        card_config = self._get_card_config()
        self.setFixedHeight(card_config['fixed_height'])
        self.setContentsMargins(0, 0, 0, 0)
        
        # 设置鼠标跟踪以支持悬停效果
        self.setMouseTracking(True)
        
        # 预创建所有可能需要的标签以提高性能
        self._setup_ui(group_name)

    def _setup_ui(self, group_name: str):
        """预创建UI组件以提高性能"""
        card_config = self._get_card_config()
        
        # 创建布局
        layout = QtWidgets.QVBoxLayout(self)
        card_margins = card_config['margins']
        layout.setContentsMargins(card_margins['card'], card_margins['content'], card_margins['card'], card_margins['content'])
        layout.setSpacing(6)
        
        # 标题行
        title_layout = QtWidgets.QHBoxLayout()
        title_layout.setContentsMargins(0, 0, 0, 0)
        
        self.name_label = QtWidgets.QLabel(self.account.name or get_text('default_values', 'unnamed_account'))
        self.name_label.setProperty("role", "title")
        self.name_label.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        title_layout.addWidget(self.name_label)
        
        title_layout.addStretch()
        
        self.group_label = QtWidgets.QLabel(group_name)
        self.group_label.setObjectName("GroupTag")
        self.group_label.setProperty("role", "muted")
        self.group_label.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        title_layout.addWidget(self.group_label)
        
        layout.addLayout(title_layout)
        
        # 用户名
        username_prefix = get_text('labels', 'username')
        self.username_label = QtWidgets.QLabel(f"{username_prefix}{self.account.username or ''}")
        self.username_label.setProperty("role", "muted")
        self.username_label.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        layout.addWidget(self.username_label)
        
        # 密码
        self.password_label = QtWidgets.QLabel()
        self.password_label.setProperty("role", "muted")
        self.password_label.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        layout.addWidget(self.password_label)
        self.set_show_passwords(self.show_passwords)
        
        # URL（延迟创建，仅在需要时创建）
        self.url_label = None
        if self.account.url:
            url_prefix = get_text('labels', 'url')
            self.url_label = QtWidgets.QLabel(f"{url_prefix}{self.account.url}")
            self.url_label.setProperty("role", "muted")
            self.url_label.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
            layout.addWidget(self.url_label)
        
        # 备注（延迟创建，仅在需要时创建）
        self.notes_label = None
        if self.account.notes:
            notes_prefix = get_text('labels', 'notes')
            self.notes_label = QtWidgets.QLabel(f"{notes_prefix}{self.account.notes}")
            self.notes_label.setProperty("role", "notes")
            self.notes_label.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
            layout.addWidget(self.notes_label)

    def set_show_passwords(self, show: bool):
        """设置是否显示密码"""
        self.show_passwords = show
        password_prefix = get_text('labels', 'password')
        if show:
            self.password_label.setText(f"{password_prefix}{self.account.password or ''}")
        else:
            self.password_label.setText(password_prefix + "*" * len(self.account.password or ""))

    def set_selected(self, selected: bool):
        """设置选中状态"""
        self.selected = selected
        self.setProperty("selected", selected)
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()

    # Click/DoubleClick passthrough
    def mousePressEvent(self, e: QtGui.QMouseEvent):
        # 只处理左键和右键，其他按键直接忽略
        if e.button() == QtCore.Qt.LeftButton:
            self.clicked.emit(self.account.id)
            e.accept()
        elif e.button() == QtCore.Qt.RightButton:
            self._show_context_menu(e.globalPos())
            e.accept()
        # 移除else分支，减少不必要的事件传播

    def mouseDoubleClickEvent(self, e: QtGui.QMouseEvent):
        if e.button() == QtCore.Qt.LeftButton:
            self.doubleClicked.emit(self.account.id)
            e.accept()  # 阻止事件继续传播
            return
        super().mouseDoubleClickEvent(e)

    def _show_context_menu(self, pos: QtCore.QPoint):
        """显示账号卡片的右键菜单"""
        menu = QtWidgets.QMenu(self)
        
        edit_action = menu.addAction("编辑")
        edit_action.triggered.connect(lambda: self.doubleClicked.emit(self.account.id))
        
        copy_menu = menu.addMenu("复制")
        copy_username = copy_menu.addAction("复制用户名")
        copy_username.triggered.connect(lambda: self._copy_to_clipboard(self.account.username))
        copy_password = copy_menu.addAction("复制密码")
        copy_password.triggered.connect(lambda: self._copy_to_clipboard(self.account.password))
        copy_url = copy_menu.addAction("复制网址")
        copy_url.triggered.connect(lambda: self._copy_to_clipboard(self.account.url))
        
        # 添加移动至分组的子菜单
        if self.groups:
            menu.addSeparator()
            move_to_group_text = get_text('labels', 'move_to_group')
            move_menu = menu.addMenu(move_to_group_text)
            
            # 获取当前账号所在的分组ID
            current_group_id = self.account.group_id
            
            for group in self.groups:
                # 如果是当前分组，则跳过
                if group.id == current_group_id:
                    continue
                    
                move_action = move_menu.addAction(group.name)
                # 使用lambda的默认参数来捕获group.id的值
                move_action.triggered.connect(
                    lambda checked, gid=group.id: self.moveToGroupRequested.emit(self.account.id, gid)
                )
        
        menu.addSeparator()
        delete_action = menu.addAction("删除")
        delete_action.triggered.connect(lambda: self.deleteRequested.emit(self.account.id))
        
        # 执行菜单并在完成后清理
        try:
            menu.exec_(pos)
        finally:
            # 确保菜单被正确销毁
            menu.deleteLater()

    def _copy_to_clipboard(self, text: str):
        """复制文本到剪贴板"""
        if text:
            clipboard = QtWidgets.QApplication.clipboard()
            clipboard.setText(text)
            # 可以添加一个临时提示
            QtWidgets.QToolTip.showText(QtGui.QCursor.pos(), "已复制到剪贴板", self, QtCore.QRect(), 1500)

    def enterEvent(self, event):
        """鼠标悬停效果"""
        self.setProperty("hovered", True)
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event):
        """鼠标离开效果"""
        self.setProperty("hovered", False)
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()
        super().leaveEvent(event)
    
    def __del__(self):
        """析构函数：确保信号正确断开"""
        try:
            # 断开所有信号连接
            self.clicked.disconnect()
            self.doubleClicked.disconnect()
            self.deleteRequested.disconnect()
            self.moveToGroupRequested.disconnect()
        except (TypeError, RuntimeError):
            # 信号已经断开或对象已被销毁
            pass
    
    def cleanup_signals(self):
        """手动清理信号连接"""
        try:
            self.clicked.disconnect()
            self.doubleClicked.disconnect()
            self.deleteRequested.disconnect()
            self.moveToGroupRequested.disconnect()
        except (TypeError, RuntimeError):
            # 信号已经断开或对象已被销毁
            pass


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, storage: VaultStorage):
        super().__init__()
        self.setWindowTitle(get_text('default_values', 'app_title') or "Mima 密码保险箱")
        self.storage = storage
        self.show_passwords = False
        self._card_items: Dict[str, Tuple[QtWidgets.QListWidgetItem, AccountCard]] = {}
        # 账号缓存：ID -> Account对象，提高查找效率
        self._account_cache: Dict[str, Account] = {}
        # 分组缓存：ID -> Group对象
        self._group_cache: Dict[str, Group] = {}
        # 正则表达式缓存：避免重复编译
        self._regex_cache: Dict[str, re.Pattern] = {}
        # 搜索结果缓存
        self._search_cache: Dict[str, Dict[str, bool]] = {}
        # 筛选结果缓存
        self._filter_cache: Dict[str, bool] = {}
        # 搜索防抖定时器
        self._search_timer = QtCore.QTimer()
        self._search_timer.setSingleShot(True)
        self._search_timer.timeout.connect(self._do_apply_filter)
        # 添加分页加载相关属性
        ui_config = get_ui_config()
        self._batch_size = ui_config['batch_load_size']  # 每批加载的卡片数量
        self._current_batch = 0  # 当前已加载的批次数
        self._pending_accounts = []  # 待加载的账号列表
        # 添加初始化完成标志
        self._initialization_complete = False

        self._init_ui()
        # 延迟加载数据以提高窗口显示速度
        QtCore.QTimer.singleShot(10, self._load_data)

    def _init_ui(self):
        # Menu bar
        menu = self.menuBar()
        file_menu = menu.addMenu("文件")
        act_save = file_menu.addAction("保存")
        act_save.triggered.connect(self._save)
        file_menu.addSeparator()
        act_import = file_menu.addAction("导入…")
        act_import.triggered.connect(self._import)
        act_export = file_menu.addAction("导出…")
        act_export.triggered.connect(self._export)
        file_menu.addSeparator()
        act_quit = file_menu.addAction("退出")
        act_quit.triggered.connect(self.close)

        tools_menu = menu.addMenu("工具")
        act_gen = tools_menu.addAction("密码生成器")
        act_gen.triggered.connect(self._open_generator)
        act_change_master = tools_menu.addAction("更改主密码")
        act_change_master.triggered.connect(self._change_master)

        config_menu = menu.addMenu("设置")
        act_settings = config_menu.addAction("界面设置")
        act_settings.triggered.connect(self._open_settings)
        act_config_edit = config_menu.addAction("配置编辑")
        act_config_edit.triggered.connect(self._open_config_editor)

        help_menu = menu.addMenu("帮助")
        help_menu.addAction("关于", self._about)

        # Toolbar
        tb = self.addToolBar("tb")
        tb.setMovable(False)
        self.search_edit = QtWidgets.QLineEdit()
        self.search_edit.setPlaceholderText("搜索名称/用户名/网址…（支持模糊匹配和正则表达式）")
        self.search_edit.textChanged.connect(self._on_search_text_changed)
        tb.addWidget(QtWidgets.QLabel(" 搜索:"))
        tb.addWidget(self.search_edit)
        # toggle password show/hide
        self.toggle_pw_btn = QtWidgets.QToolButton()
        self.toggle_pw_btn.setText("显示密码")
        self.toggle_pw_btn.setCheckable(True)
        self.toggle_pw_btn.toggled.connect(self._toggle_passwords)
        tb.addSeparator()
        tb.addWidget(self.toggle_pw_btn)

        # Central splitter
        splitter = QtWidgets.QSplitter()
        splitter.setObjectName("MainSplitter")
        self.setCentralWidget(splitter)

        # Left: group panel
        left = QtWidgets.QWidget()
        left.setObjectName("SidePanel")
        lyt_left = QtWidgets.QVBoxLayout(left)
        layout_margin = get_card_config()['margins']['layout']
        lyt_left.setContentsMargins(layout_margin, layout_margin, layout_margin, layout_margin)

        self.group_tree = QtWidgets.QTreeWidget()
        self.group_tree.setHeaderHidden(True)
        self.group_tree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.group_tree.customContextMenuRequested.connect(self._group_menu)
        self.group_tree.itemSelectionChanged.connect(self._apply_filter)
        lyt_left.addWidget(self.group_tree)

        btn_row = QtWidgets.QHBoxLayout()
        btn_add_g = QtWidgets.QPushButton("新建分组")
        btn_add_g.clicked.connect(self._new_group)
        btn_row.addWidget(btn_add_g)
        lyt_left.addLayout(btn_row)

        splitter.addWidget(left)

        # Right: card list (replace table)
        right = QtWidgets.QWidget()
        lyt_right = QtWidgets.QVBoxLayout(right)
        lyt_right.setContentsMargins(layout_margin, layout_margin, layout_margin, layout_margin)

        self.card_list = QtWidgets.QListWidget()
        self.card_list.setObjectName("CardList")
        self.card_list.setViewMode(QtWidgets.QListView.IconMode)
        self.card_list.setResizeMode(QtWidgets.QListView.Adjust)
        self.card_list.setMovement(QtWidgets.QListView.Static)
        self.card_list.setWrapping(True)
        self.card_list.setSpacing(10)
        self.card_list.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.card_list.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.card_list.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.card_list.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.card_list.setFocusPolicy(QtCore.Qt.NoFocus)
        self.card_list.itemSelectionChanged.connect(self._on_card_selection_changed)
        self.card_list.itemDoubleClicked.connect(lambda _: self._edit_selected())
        # default card size
        card_config = get_card_config()
        self.card_size = QtCore.QSize(card_config['width'], card_config['height'])
        grid_spacing = card_config['grid_spacing']
        self.card_list.setGridSize(self.card_size + QtCore.QSize(grid_spacing, grid_spacing))

        lyt_right.addWidget(self.card_list)

        btns = QtWidgets.QHBoxLayout()
        b_add = QtWidgets.QPushButton("添加")
        b_add.clicked.connect(self._add_account)
        b_edit = QtWidgets.QPushButton("编辑")
        b_edit.clicked.connect(self._edit_selected)
        b_del = QtWidgets.QPushButton("删除")
        b_del.clicked.connect(self._delete_selected)
        btns.addWidget(b_add)
        btns.addWidget(b_edit)
        btns.addWidget(b_del)
        lyt_right.addLayout(btns)

        splitter.addWidget(right)
        splitter.setStretchFactor(1, 1)

        # Status bar
        self.statusBar().showMessage("就绪")

    # ----- Data binding -----
    def _load_data(self):
        self._rebuild_caches()
        self._refresh_groups()
        self._refresh_table_initial()  # 使用增量加载方式初始化表格
        self._initialization_complete = True

    def _rebuild_caches(self):
        """重建账号和分组缓存"""
        self._account_cache = {a.id: a for a in self.storage.vault.accounts}
        self._group_cache = {g.id: g for g in self.storage.vault.groups}
        # 清空搜索和筛选缓存
        self._search_cache.clear()
        self._filter_cache.clear()

    def _refresh_groups(self):
        selected_gid = self._current_group_id()
        def_gid = self.storage.default_group_id()
        
        # 获取当前分组列表
        current_groups = {g.id: g for g in self.storage.vault.groups}
        existing_items = {}
        
        # 收集现有项目
        for i in range(self.group_tree.topLevelItemCount()):
            item = self.group_tree.topLevelItem(i)
            gid = item.data(0, QtCore.Qt.UserRole)
            existing_items[gid] = item
        
        # 批量更新UI
        self.group_tree.setUpdatesEnabled(False)
        try:
            # 移除已删除的分组
            for gid in list(existing_items.keys()):
                if gid not in current_groups:
                    item = existing_items[gid]
                    self.group_tree.takeTopLevelItem(self.group_tree.indexOfTopLevelItem(item))
                    del existing_items[gid]
            
            # 更新或添加分组
            groups = list(current_groups.values())
            default_group_name = get_text('default_values', 'default_group') or "未分组"
            undefined_group_name = get_text('default_values', 'undefined_group') or "未定义"
            groups.sort(key=lambda g: (0 if (g.id == def_gid or g.name in (default_group_name, undefined_group_name)) else 1, (g.name or "")))
            
            to_select_item = None
            for i, g in enumerate(groups):
                if g.id in existing_items:
                    # 更新现有项目
                    item = existing_items[g.id]
                    if item.text(0) != g.name:
                        item.setText(0, g.name)
                    # 确保项目在正确位置
                    current_index = self.group_tree.indexOfTopLevelItem(item)
                    if current_index != i:
                        self.group_tree.takeTopLevelItem(current_index)
                        self.group_tree.insertTopLevelItem(i, item)
                else:
                    # 添加新项目
                    item = QtWidgets.QTreeWidgetItem([g.name])
                    item.setData(0, QtCore.Qt.UserRole, g.id)
                    self.group_tree.insertTopLevelItem(i, item)
                
                if g.id == selected_gid:
                    to_select_item = item
            
            # 恢复选中状态
            if to_select_item is None and def_gid in current_groups:
                for i in range(self.group_tree.topLevelItemCount()):
                    item = self.group_tree.topLevelItem(i)
                    if item.data(0, QtCore.Qt.UserRole) == def_gid:
                        to_select_item = item
                        break
            
            if to_select_item is not None:
                self.group_tree.setCurrentItem(to_select_item)
        finally:
            self.group_tree.setUpdatesEnabled(True)

    # ----- Group actions -----
    def _group_menu(self, pos):
        item = self.group_tree.itemAt(pos)
        menu = QtWidgets.QMenu(self)
        act_new = menu.addAction("新建分组")
        act_new.triggered.connect(self._new_group)
        if item:
            gid = item.data(0, QtCore.Qt.UserRole)
            act_rename = menu.addAction("重命名")
            act_rename.triggered.connect(functools.partial(self._rename_group, gid))
            act_delete = menu.addAction("删除分组…")
            act_delete.triggered.connect(functools.partial(self._delete_group, gid))
        menu.exec_(self.group_tree.mapToGlobal(pos))

    def _delete_group(self, gid: str):
        # Ask migrate
        names = [g.name for g in self.storage.vault.groups if g.id != gid]
        gids = [g.id for g in self.storage.vault.groups if g.id != gid]
        dlg = QtWidgets.QDialog(self)
        delete_group_title = get_text('dialog_titles', 'delete_group') or "删除分组"
        dlg.setWindowTitle(delete_group_title)
        v = QtWidgets.QVBoxLayout(dlg)
        migration_label = get_text('labels', 'select_migration_target') or "选择迁移目标（可选）："
        v.addWidget(QtWidgets.QLabel(migration_label))
        combo = QtWidgets.QComboBox()
        default_group_name = get_text('default_values', 'default_group') or "未分组"
        no_migration_text = get_text('ui_elements', 'no_migration').format(default_group=default_group_name) or f"不迁移（自动归入'{default_group_name}'）"
        combo.addItem(no_migration_text, None)
        for name, id_ in zip(names, gids):
            combo.addItem(name, id_)
        v.addWidget(combo)
        btns = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        v.addWidget(btns)
        btns.accepted.connect(dlg.accept)
        btns.rejected.connect(dlg.reject)
        if dlg.exec_() == QtWidgets.QDialog.Accepted:
            migrate_to = combo.currentData()
            
            # 批量更新模式：暂停UI更新
            self.setUpdatesEnabled(False)
            try:
                self.storage.delete_group(gid, migrate_to)
                # 重建缓存以反映分组变化
                self._rebuild_caches()
                # 删除后自动选中默认分组，避免筛选导致误以为账号丢失
                def_gid = self.storage.default_group_id()
                self._refresh_groups()
                for i in range(self.group_tree.topLevelItemCount()):
                    it = self.group_tree.topLevelItem(i)
                    if it.data(0, QtCore.Qt.UserRole) == def_gid:
                        self.group_tree.setCurrentItem(it)
                        break
                self._refresh_table()
            finally:
                # 恢复UI更新
                self.setUpdatesEnabled(True)
                
            try:
                self.storage.save()
            except VaultError as e:
                QtWidgets.QMessageBox.critical(self, "错误", str(e))
            self._refresh_table()

    # ----- Account actions -----
    def _selected_account_id(self) -> Optional[str]:
        items = self.card_list.selectedItems()
        if not items:
            return None
        return items[0].data(QtCore.Qt.UserRole)

    def _add_account(self):
        gid = self._current_group_id()
        dlg = AccountDialog(parent=self)
        try:
            if dlg.exec_() == QtWidgets.QDialog.Accepted:
                acc = dlg.get_account(gid)
                
                # 立即添加到内存缓存，避免阻塞UI
                self._account_cache[acc.id] = acc
                
                # 立即在界面显示新账号
                default_group_name = get_text('default_values', 'default_group') or "未分组"
                group_name = next((g.name for g in self.storage.vault.groups if g.id == gid), default_group_name)
                self._create_account_card(acc, group_name)
                
                # 延迟应用筛选条件，避免立即阻塞UI
                QtCore.QTimer.singleShot(10, self._apply_filter)
                
                # 异步添加到存储并保存，完全避免阻塞界面
                QtCore.QTimer.singleShot(50, lambda: self._add_account_async(acc))
        finally:
            # 确保对话框被正确释放
            dlg.deleteLater()
    
    def _add_account_async(self, account: Account):
        """异步添加账号到存储"""
        # 如果已有保存线程在运行，则跳过
        if hasattr(self, '_add_thread') and self._add_thread.isRunning():
            return
            
        # 创建添加账号线程
        self._add_thread = AddAccountThread(self.storage, account)
        self._add_thread.add_completed.connect(self._on_add_completed)
        self._add_thread.add_failed.connect(self._on_add_failed)
        self._add_thread.start()
    
    def _on_add_completed(self):
        """添加账号完成回调"""
        self.statusBar().showMessage("账号已保存", 2000)
    
    def _on_add_failed(self, error_msg: str):
        """添加账号失败回调"""
        QtWidgets.QMessageBox.critical(self, "错误", f"保存失败: {error_msg}")
        self.statusBar().showMessage("保存失败", 3000)
    
    def _save_async(self):
        """异步保存数据到文件"""
        # 如果已有保存线程在运行，则跳过
        if hasattr(self, '_save_thread') and self._save_thread.isRunning():
            return
            
        # 创建保存线程
        self._save_thread = SaveThread(self.storage)
        self._save_thread.save_completed.connect(self._on_save_completed)
        self._save_thread.save_failed.connect(self._on_save_failed)
        self._save_thread.start()
    
    def _on_save_completed(self):
        """保存完成回调"""
        self.statusBar().showMessage("账号已保存", 2000)
    
    def _on_save_failed(self, error_msg: str):
        """保存失败回调"""
        QtWidgets.QMessageBox.critical(self, "错误", f"保存失败: {error_msg}")
        self.statusBar().showMessage("保存失败", 3000)

    def _get_account(self, aid: str) -> Optional[Account]:
        """从缓存中快速获取账号对象"""
        return self._account_cache.get(aid)

    def _edit_selected(self):
        aid = self._selected_account_id()
        if not aid:
            return
        a = self._get_account(aid)
        if not a:
            return
        dlg = AccountDialog(a, self)
        try:
            if dlg.exec_() == QtWidgets.QDialog.Accepted:
                na = dlg.get_account(a.group_id)
                self.storage.update_account(na)
                # 更新缓存
                self._account_cache[na.id] = na
                
                # 延迟刷新表格，避免立即阻塞UI
                QtCore.QTimer.singleShot(10, self._refresh_table)
                
                # 异步保存，避免阻塞UI
                QtCore.QTimer.singleShot(50, self._save_async)
        finally:
            # 确保对话框被正确释放
            dlg.deleteLater()

    def _delete_selected(self):
        aid = self._selected_account_id()
        if not aid:
            return
        if QtWidgets.QMessageBox.question(self, "确认", "确定删除选中账号？") == QtWidgets.QMessageBox.Yes:
            self.storage.delete_account(aid)
            # 从缓存中移除
            self._account_cache.pop(aid, None)
            
            # 延迟刷新表格，避免立即阻塞UI
            QtCore.QTimer.singleShot(10, self._refresh_table)
            
            # 异步保存，避免阻塞UI
            QtCore.QTimer.singleShot(50, self._save_async)

    def _delete_account_by_id(self, account_id: str):
        """根据账号ID删除账号"""
        account = self._get_account(account_id)
        if not account:
            return
        
        reply = QtWidgets.QMessageBox.question(
            self, "确认删除", 
            f"确定要删除账号 '{account.name}' 吗？",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No
        )
        
        if reply == QtWidgets.QMessageBox.Yes:
            try:
                self.storage.delete_account(account_id)
                # 从缓存中移除
                self._account_cache.pop(account_id, None)
                
                # 延迟刷新表格，避免立即阻塞UI
                QtCore.QTimer.singleShot(10, self._refresh_table)
                
                # 异步保存，避免阻塞UI
                QtCore.QTimer.singleShot(50, self._save_async)
                
            except VaultError as e:
                QtWidgets.QMessageBox.critical(self, "错误", str(e))

    # ----- Card interactions -----
    def _on_card_clicked(self, aid: str):
        # select corresponding QListWidgetItem
        item, _ = self._card_items.get(aid, (None, None))
        if item:
            self.card_list.setCurrentItem(item)

    def _on_card_selection_changed(self):
        # update selected property on widgets
        selected_ids = set()
        for it in self.card_list.selectedItems():
            selected_ids.add(it.data(QtCore.Qt.UserRole))
        
        # 只更新状态发生变化的卡片，减少不必要的UI更新
        for aid, (it, w) in self._card_items.items():
            new_selected = aid in selected_ids
            if w.selected != new_selected:
                w.set_selected(new_selected)

    # ----- Filter/Search -----
    def _current_group_id(self) -> Optional[str]:
        items = self.group_tree.selectedItems()
        if not items:
            return None
        return items[0].data(0, QtCore.Qt.UserRole)

    def _on_search_text_changed(self):
        """搜索文本变化时的防抖处理"""
        # 清空搜索缓存以确保结果准确性
        self._search_cache.clear()
        
        self._search_timer.stop()
        # 减少防抖延迟，提高响应速度
        self._search_timer.start(150)  # 150ms防抖延迟
    
    def _apply_filter(self):
        """立即应用过滤器（用于分组选择等）"""
        self._search_timer.stop()
        self._do_apply_filter()
    
    def _do_apply_filter(self):
        """执行实际的过滤操作"""
        text = self.search_edit.text().strip()
        gid = self._current_group_id()
        visible_count = 0
        
        # 批量处理UI更新以提高性能
        self.card_list.setUpdatesEnabled(False)
        try:
            for aid, (item, widget) in self._card_items.items():
                a = self._get_account(aid)
                if not a:
                    if not item.isHidden():
                        item.setHidden(True)
                    continue
                
                group_match = True if gid is None else (a.group_id == gid)
                text_match = self._match_text(text, a)
                should_show = group_match and text_match
                
                # 仅在状态改变时更新UI
                if item.isHidden() == should_show:
                    item.setHidden(not should_show)
                
                if should_show:
                    visible_count += 1
        finally:
            self.card_list.setUpdatesEnabled(True)
        
        # 减少状态栏更新频率
        current_message = self.statusBar().currentMessage()
        new_message = f"显示 {visible_count} 条记录"
        if current_message != new_message:
            self.statusBar().showMessage(new_message)
    
    def _match_text(self, search_text: str, account: Account) -> bool:
        """智能匹配文本：自动检测正则表达式，否则使用模糊匹配"""
        if not search_text:
            return True
        
        # 检查搜索缓存
        cache_key = f"{search_text}:{account.id}"
        if cache_key in self._search_cache:
            return self._search_cache[cache_key]
        
        # 搜索字段
        fields = [
            account.name or "",
            account.username or "",
            account.url or ""
        ]
        
        result = False
        
        # 检测是否为正则表达式（包含特殊字符）
        regex_chars = r'[.*+?^${}()|[\]\\]'
        is_regex = bool(re.search(regex_chars, search_text))
        
        if is_regex:
            # 使用缓存的正则表达式
            pattern = self._regex_cache.get(search_text)
            if pattern is None:
                try:
                    pattern = re.compile(search_text, re.IGNORECASE)
                    self._regex_cache[search_text] = pattern
                    # 限制缓存大小，避免内存泄漏
                    if len(self._regex_cache) > 50:
                        # 清除最旧的缓存项
                        oldest_key = next(iter(self._regex_cache))
                        del self._regex_cache[oldest_key]
                except re.error:
                    # 正则表达式错误时回退到模糊匹配
                    pattern = None
            
            if pattern:
                result = any(pattern.search(field) for field in fields)
        
        if not result:
            # 默认使用模糊匹配
            search_lower = search_text.lower()
            for field in fields:
                field_lower = field.lower()
                if self._fuzzy_match(search_lower, field_lower):
                    result = True
                    break
        
        # 缓存结果（限制缓存大小）
        if len(self._search_cache) > 200:
            # 清除一半的缓存
            keys_to_remove = list(self._search_cache.keys())[:100]
            for key in keys_to_remove:
                del self._search_cache[key]
        
        self._search_cache[cache_key] = result
        return result
    
    def _fuzzy_match(self, pattern: str, text: str) -> bool:
        """优化的模糊匹配算法"""
        if not pattern:
            return True
        if not text:
            return False
        
        pattern_len = len(pattern)
        text_len = len(text)
        
        # 如果模式长度大于文本长度，不可能匹配
        if pattern_len > text_len:
            return False
            
        # 简单的子序列匹配优化
        pattern_idx = 0
        for char in text:
            if pattern_idx < pattern_len and char.lower() == pattern[pattern_idx].lower():
                pattern_idx += 1
                # 如果已经匹配完所有字符，直接返回True
                if pattern_idx == pattern_len:
                    return True
        
        return pattern_idx == pattern_len

    def _toggle_passwords(self, checked: bool):
        # 如果状态没有变化，直接返回
        if self.show_passwords == checked:
            return
            
        self.show_passwords = checked
        self.toggle_pw_btn.setText("隐藏密码" if checked else "显示密码")
        
        # 批量更新UI以提高性能
        self.card_list.setUpdatesEnabled(False)
        try:
            for aid, (item, w) in self._card_items.items():
                if not item.isHidden():  # 只更新可见的卡片
                    w.set_show_passwords(checked)
        finally:
            self.card_list.setUpdatesEnabled(True)

    # ----- Menu actions -----
    def _save(self):
        try:
            self.storage.save()
            QtWidgets.QMessageBox.information(self, "提示", "已保存")
        except VaultError as e:
            QtWidgets.QMessageBox.critical(self, "错误", str(e))

    def _export(self):
        path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "导出", "vault.json", "JSON (*.json);;加密文件 (*.mima)")
        if not path:
            return
        if path.endswith(".mima"):
            data = self.storage.export_encrypted()
            with open(path, "wb") as f:
                f.write(data)
        else:
            text = self.storage.export_plain()
            with open(path, "w", encoding="utf-8") as f:
                f.write(text)
        QtWidgets.QMessageBox.information(self, "提示", "导出成功")

    def _import(self):
        path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "导入", "", "所有文件 (*.*)")
        if not path:
            return
        try:
            with open(path, "rb") as f:
                blob = f.read()
            # auto detect format: encrypted starts with 0x10 and length >= 17, json likely starts with '{' or '[' or whitespace
            is_encrypted = len(blob) >= 17 and blob[0] == 16
            if is_encrypted:
                # Ask password (optional)
                text, ok = QtWidgets.QInputDialog.getText(self, "导入加密文件", "输入密码（留空使用当前主密码）：")
                pwd = text if ok and text else None
                self.storage.import_encrypted(blob, password=pwd, merge=True)
            else:
                text = blob.decode("utf-8")
                self.storage.import_plain(text, merge=True)
            
            # 使用批量更新模式
            self._batch_updating = True
            self._rebuild_caches()
            self._refresh_groups()
            self._batch_updating = False
            self._refresh_table()
            
            QtWidgets.QMessageBox.information(self, "提示", "导入成功")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "错误", f"导入失败：{e}")

    def _open_generator(self):
        dlg = PasswordGeneratorDialog(self)
        try:
            dlg.exec_()
        finally:
            dlg.deleteLater()

    def _change_master(self):
        # Ask old/new
        dlg = QtWidgets.QDialog(self)
        dlg.setWindowTitle("更改主密码")
        v = QtWidgets.QVBoxLayout(dlg)
        ed_old = QtWidgets.QLineEdit()
        ed_old.setEchoMode(QtWidgets.QLineEdit.Password)
        ed_new = QtWidgets.QLineEdit()
        ed_new.setEchoMode(QtWidgets.QLineEdit.Password)
        v.addWidget(QtWidgets.QLabel("旧密码"))
        v.addWidget(ed_old)
        v.addWidget(QtWidgets.QLabel("新密码"))
        v.addWidget(ed_new)
        btns = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        v.addWidget(btns)
        btns.accepted.connect(dlg.accept)
        btns.rejected.connect(dlg.reject)
        try:
            if dlg.exec_() == QtWidgets.QDialog.Accepted:
                # 验证输入
                old_password = ed_old.text().strip()
                new_password = ed_new.text().strip()
                
                if not old_password:
                    QtWidgets.QMessageBox.warning(self, "提示", "请输入旧密码")
                    return
                
                if not new_password:
                    QtWidgets.QMessageBox.warning(self, "提示", "请输入新密码")
                    return
                
                if old_password == new_password:
                    QtWidgets.QMessageBox.warning(self, "提示", "新密码不能与旧密码相同")
                    return
                
                try:
                    self.storage.change_master(old_password, new_password)
                    QtWidgets.QMessageBox.information(self, "提示", "主密码已更改")
                except VaultError as e:
                    QtWidgets.QMessageBox.critical(self, "错误", str(e))
        finally:
            dlg.deleteLater()

    def _about(self):
        QtWidgets.QMessageBox.information(self, "关于", "Mima 密码保险箱\n使用 PyQt5 构建，数据采用主密码保护与ECC加密存储。")
    
    def _open_settings(self):
        """打开设置对话框"""
        dialog = SettingsDialog(self)
        dialog.settingsChanged.connect(self._on_settings_changed)
        try:
            dialog.exec_()
        finally:
            dialog.deleteLater()

    def _open_config_editor(self):
        """打开配置编辑对话框"""
        from .config_editor_dialog import ConfigEditorDialog
        dialog = ConfigEditorDialog(self)
        try:
            if dialog.exec_() == QtWidgets.QDialog.Accepted:
                # 配置已更改，刷新界面
                self._on_settings_changed()
        finally:
            dialog.deleteLater()
    
    def _on_settings_changed(self):
        """设置更改后的处理"""
        # 重新加载样式
        from .style import load_app_style
        QtWidgets.QApplication.instance().setStyleSheet(load_app_style())
        
        # 刷新界面
        self._refresh_table()
        self._refresh_groups()
        
        # 显示提示
        QtWidgets.QMessageBox.information(self, "设置已保存", "界面设置已更新并应用。")

    # ----- Group actions -----
    def _new_group(self):
        dlg = InputDialog("新建分组", "请输入分组名称：", "")
        try:
            if dlg.exec_() == QtWidgets.QDialog.Accepted:
                name = dlg.get_text()
                if name:
                    # 立即在UI中显示新分组，避免阻塞
                    from .models import Group
                    import uuid
                    
                    # 创建临时分组对象用于UI显示
                    temp_group = Group(id=str(uuid.uuid4()), name=name)
                    
                    # 直接在分组树中添加新项
                    item = QtWidgets.QTreeWidgetItem([temp_group.name])
                    item.setData(0, QtCore.Qt.UserRole, temp_group.id)
                    self.group_tree.addTopLevelItem(item)
                    
                    # 选中新创建的分组
                    self.group_tree.setCurrentItem(item)
                    
                    # 异步添加到存储并保存，完全避免阻塞界面
                    QtCore.QTimer.singleShot(50, lambda: self._add_group_async(name, temp_group.id))
        finally:
            dlg.deleteLater()
    
    def _add_group_async(self, group_name: str, temp_id: str):
        """异步添加分组到存储"""
        # 如果已有添加分组线程在运行，则跳过
        if hasattr(self, '_add_group_thread') and self._add_group_thread.isRunning():
            return
            
        # 创建添加分组线程
        self._add_group_thread = AddGroupThread(self.storage, group_name, temp_id)
        self._add_group_thread.group_added.connect(self._on_group_added)
        self._add_group_thread.group_add_failed.connect(self._on_group_add_failed)
        self._add_group_thread.start()
    
    def _on_group_added(self, real_group_id: str, temp_id: str):
        """分组添加完成回调"""
        # 更新UI中的分组ID为真实ID
        for i in range(self.group_tree.topLevelItemCount()):
            item = self.group_tree.topLevelItem(i)
            if item.data(0, QtCore.Qt.UserRole) == temp_id:
                item.setData(0, QtCore.Qt.UserRole, real_group_id)
                break
        
        self.statusBar().showMessage("分组已保存", 2000)
    
    def _on_group_add_failed(self, error_msg: str, temp_id: str):
        """分组添加失败回调"""
        # 从UI中移除临时分组
        for i in range(self.group_tree.topLevelItemCount()):
            item = self.group_tree.topLevelItem(i)
            if item.data(0, QtCore.Qt.UserRole) == temp_id:
                self.group_tree.takeTopLevelItem(i)
                break
        
        QtWidgets.QMessageBox.critical(self, "错误", f"添加分组失败: {error_msg}")
        self.statusBar().showMessage("添加分组失败", 3000)

    def _rename_group(self, gid: str):
        old = next((g.name for g in self.storage.vault.groups if g.id == gid), "")
        dlg = InputDialog("重命名分组", "新的分组名称：", old)
        try:
            if dlg.exec_() == QtWidgets.QDialog.Accepted:
                name = dlg.get_text()
                if name:
                    try:
                        # 重命名分组
                        self.storage.rename_group(gid, name)
                        
                        # 直接更新分组树中的对应项
                        for i in range(self.group_tree.topLevelItemCount()):
                            item = self.group_tree.topLevelItem(i)
                            if item.data(0, QtCore.Qt.UserRole) == gid:
                                item.setText(0, name)
                                break
                        
                        # 延迟刷新表格以更新分组标签，避免立即阻塞
                        QtCore.QTimer.singleShot(10, self._refresh_table)
                        
                        # 异步保存，避免阻塞UI
                        QtCore.QTimer.singleShot(50, self._save_async)
                        
                    except VaultError as e:
                        QtWidgets.QMessageBox.critical(self, "错误", str(e))
        finally:
            dlg.deleteLater()

    def _refresh_table_initial(self):
        """初始表格刷新，使用分批加载方式"""
        # 清空现有卡片
        self.card_list.clear()
        self._card_items.clear()
        
        # 准备待加载的账号列表
        self._pending_accounts = list(self.storage.vault.accounts)
        self._current_batch = 0
        
        # 开始分批加载
        self._load_next_batch()

    def _load_next_batch(self):
        """加载下一批账号卡片"""
        start_idx = self._current_batch * self._batch_size
        end_idx = min(start_idx + self._batch_size, len(self._pending_accounts))
        
        # 获取当前批次的账号
        batch_accounts = self._pending_accounts[start_idx:end_idx]
        
        if not batch_accounts:
            # 所有账号加载完成，应用筛选条件
            self._apply_filter()
            return
        
        # 分组名映射
        group_name_map = {g.id: g.name for g in self.storage.vault.groups}
        
        # 批量更新UI以提高性能
        self.card_list.setUpdatesEnabled(False)
        try:
            default_group_name = get_text('default_values', 'default_group') or "未分组"
            for a in batch_accounts:
                gname = group_name_map.get(a.group_id, default_group_name)
                self._create_account_card(a, gname)
        finally:
            self.card_list.setUpdatesEnabled(True)
        
        self._current_batch += 1
        
        # 如果还有更多账号需要加载，安排下一批加载
        if end_idx < len(self._pending_accounts):
            # 使用单次定时器来避免阻塞UI线程
            QtCore.QTimer.singleShot(1, self._load_next_batch)
        else:
            # 所有账号加载完成，应用筛选条件
            self._apply_filter()

    def _refresh_table(self):
        """优化的表格刷新方法，支持增量更新"""
        # 获取当前账号ID集合
        current_account_ids = {a.id for a in self.storage.vault.accounts}
        existing_account_ids = set(self._card_items.keys())
        
        # 分组名映射
        group_name_map = {g.id: g.name for g in self.storage.vault.groups}
        
        # 批量处理UI更新以提高性能
        self.card_list.setUpdatesEnabled(False)
        try:
            # 移除已删除的账号卡片
            for aid in existing_account_ids - current_account_ids:
                item, card = self._card_items.pop(aid)
                # 使用新的cleanup_signals方法
                card.cleanup_signals()
                row = self.card_list.row(item)
                if row >= 0:
                    self.card_list.takeItem(row)
                # 显式删除卡片对象
                card.deleteLater()
            
            # 添加新账号卡片或更新现有卡片
            default_group_name = get_text('default_values', 'default_group') or "未分组"
            for a in self.storage.vault.accounts:
                gname = group_name_map.get(a.group_id, default_group_name)
                
                if a.id in self._card_items:
                    # 更新现有卡片 - 只在数据真正变化时才重建
                    item, card = self._card_items[a.id]
                    if (card.account.name != a.name or 
                        card.account.username != a.username or 
                        card.account.password != a.password or 
                        card.account.url != a.url or 
                        card.account.notes != a.notes):
                        
                        # 更新卡片数据而不重建整个卡片
                        card.account = a
                        card.name_label.setText(a.name or "未命名")
                        card.username_label.setText(f"用户名: {a.username or ''}")
                        card.set_show_passwords(self.show_passwords)
                        
                        # 更新URL标签（如果存在）
                        if hasattr(card, 'url_label') and card.url_label is not None:
                            if a.url:
                                card.url_label.setText(f"网址: {a.url}")
                                card.url_label.show()
                            else:
                                card.url_label.hide()
                        elif a.url and (not hasattr(card, 'url_label') or card.url_label is None):
                            # 如果账号有URL但卡片没有URL标签，创建一个
                            card.url_label = QtWidgets.QLabel(f"网址: {a.url}")
                            card.url_label.setProperty("role", "muted")
                            card.url_label.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
                            card.layout().addWidget(card.url_label)
                        
                        # 更新备注标签（如果存在）
                        if hasattr(card, 'notes_label') and card.notes_label is not None:
                            if a.notes:
                                card.notes_label.setText(f"备注: {a.notes}")
                                card.notes_label.show()
                            else:
                                card.notes_label.hide()
                        elif a.notes and (not hasattr(card, 'notes_label') or card.notes_label is None):
                            # 如果账号有备注但卡片没有备注标签，创建一个
                            card.notes_label = QtWidgets.QLabel(f"备注: {a.notes}")
                            card.notes_label.setProperty("role", "notes")
                            card.notes_label.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
                            card.layout().addWidget(card.notes_label)
                else:
                    # 添加新卡片（仅在非初始化加载时直接添加）
                    if not self._pending_accounts:  # 不在分批加载过程中
                        self._create_account_card(a, gname)
        finally:
            self.card_list.setUpdatesEnabled(True)
        
        # 延迟应用筛选条件以避免阻塞UI
        QtCore.QTimer.singleShot(10, self._apply_filter)
    
    def _create_account_card(self, account: Account, group_name: str):
        """创建新的账号卡片"""
        # 传递所有分组信息给卡片
        groups = self.storage.vault.groups
        card = AccountCard(account, group_name, self.show_passwords, groups, self.card_list)
        card.clicked.connect(functools.partial(self._on_card_clicked, account.id))
        card.doubleClicked.connect(self._create_double_click_handler(account.id))
        card.deleteRequested.connect(functools.partial(self._delete_account_by_id, account.id))
        card.moveToGroupRequested.connect(self._move_account_to_group)

        item = QtWidgets.QListWidgetItem()
        item.setData(QtCore.Qt.UserRole, account.id)
        item.setSizeHint(self.card_size)
        self.card_list.addItem(item)
        self.card_list.setItemWidget(item, card)
        self._card_items[account.id] = (item, card)

    def _move_account_to_group(self, account_id: str, group_id: str):
        """移动账号到指定分组"""
        try:
            # 获取账号信息
            account = self._get_account(account_id)
            if not account:
                error_title = get_text('dialog_titles', 'error')
                error_msg = get_text('error_messages', 'account_not_found')
                QtWidgets.QMessageBox.warning(self, error_title, error_msg)
                return
            
            # 获取目标分组信息
            target_group = None
            for group in self.storage.vault.groups:
                if group.id == group_id:
                    target_group = group
                    break
            
            if not target_group:
                error_title = get_text('dialog_titles', 'error')
                error_msg = get_text('error_messages', 'group_not_found')
                QtWidgets.QMessageBox.warning(self, error_title, error_msg)
                return
            
            # 更新账号的分组ID
            account.group_id = group_id
            
            # 更新存储
            self.storage.update_account(account)
            
            # 刷新界面
            self._refresh_table()
            
            # 异步保存
            QtCore.QTimer.singleShot(50, self._save_async)
            
        except Exception as e:
            error_title = get_text('dialog_titles', 'error')
            error_template = get_text('error_messages', 'move_account_failed')
            error_msg = error_template.format(error=str(e))
            QtWidgets.QMessageBox.critical(self, error_title, error_msg)

    def _create_double_click_handler(self, account_id: str):
        """创建双击处理器，避免lambda闭包问题"""
        def handler():
            # 直接编辑指定账号，避免通过选中状态间接获取
            a = self._get_account(account_id)
            if not a:
                return
            dlg = AccountDialog(a, self)
            if dlg.exec_() == QtWidgets.QDialog.Accepted:
                na = dlg.get_account(a.group_id)
                self.storage.update_account(na)
                # 更新缓存
                self._account_cache[na.id] = na
                
                # 延迟刷新表格，避免立即阻塞UI
                QtCore.QTimer.singleShot(10, self._refresh_table)
                
                # 异步保存，避免阻塞UI
                QtCore.QTimer.singleShot(50, self._save_async)
        return handler

    def closeEvent(self, event: QtGui.QCloseEvent):
        # 直接关闭程序，不做其他操作
        event.accept()
        super().closeEvent(event)
    
    def __del__(self):
        """析构函数：确保所有资源正确释放"""
        self._cleanup_all_signals()
    
    def _cleanup_all_signals(self):
        """清理所有信号连接和资源"""
        try:
            # 停止搜索定时器
            if hasattr(self, '_search_timer') and self._search_timer:
                self._search_timer.stop()
                try:
                    self._search_timer.timeout.disconnect()
                except (TypeError, RuntimeError):
                    pass
            
            # 快速清理所有账号卡片的信号
            if hasattr(self, '_card_items'):
                for aid, (item, card) in list(self._card_items.items()):
                    try:
                        card.cleanup_signals()
                        card.deleteLater()
                    except (RuntimeError, AttributeError):
                        pass
                self._card_items.clear()
            
            # 清理缓存
            if hasattr(self, '_account_cache'):
                self._account_cache.clear()
            if hasattr(self, '_group_cache'):
                self._group_cache.clear()
            if hasattr(self, '_regex_cache'):
                self._regex_cache.clear()
            
            # 清空缓存
            self._card_items.clear()
            self._account_cache.clear()
            self._group_cache.clear()
            self._regex_cache.clear()
            
        except (TypeError, RuntimeError, AttributeError):
            # 对象可能已被销毁或信号已断开
            pass