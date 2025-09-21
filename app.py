import sys
import os
from PyQt5 import QtWidgets, QtGui, QtCore

from vault.main_window import MainWindow
from vault.storage import VaultStorage, VaultError
from vault.dialogs import MasterPasswordDialog
from vault.style import load_app_style
from vault.config import get_app_config, get_window_config, get_file_config


def main():
    # 启用高DPI支持
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    
    app = QtWidgets.QApplication(sys.argv)
    app_config = get_app_config()
    app.setApplicationName(app_config['name'])
    app.setOrganizationName(app_config['organization'])

    # 使用应用脚本所在目录作为基准路径，避免不同工作目录导致读写文件不一致
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # 设置应用图标（优先 .ico，回退 .png）
    file_config = get_file_config()
    icon_path_ico = os.path.join(base_dir, file_config['icon_ico'])
    icon_path_png = os.path.join(base_dir, file_config['icon_png'])
    icon = QtGui.QIcon(icon_path_ico if os.path.exists(icon_path_ico) else icon_path_png)
    app.setWindowIcon(icon)

    # Load global stylesheet (modern dark theme)
    app.setStyleSheet(load_app_style())

    data_path = os.path.join(base_dir, file_config['data_file'])
    storage = VaultStorage(data_path)

    # Determine first-run or login
    first_run = not os.path.exists(data_path)

    # 预创建对话框以提高响应速度
    dlg = MasterPasswordDialog(first_run=first_run)
    if dlg.exec_() != QtWidgets.QDialog.Accepted:
        sys.exit(0)

    master_password = dlg.get_password()

    try:
        if first_run:
            storage.create_new(master_password)
            storage.save()
        else:
            storage.load(master_password)
    except VaultError as e:
        QtWidgets.QMessageBox.critical(None, "错误", str(e))
        sys.exit(1)

    # 延迟创建主窗口以提高启动速度
    win = MainWindow(storage)
    window_config = get_window_config()
    win.resize(window_config['default_width'], window_config['default_height'])
    # 确保窗口标题栏/任务栏也使用该图标
    try:
        win.setWindowIcon(icon)
    except Exception:
        pass
    
    # 使用 QTimer.singleShot 延迟显示窗口，让事件循环先启动
    QtCore.QTimer.singleShot(0, win.show)

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()