from PyQt5 import QtWidgets, QtCore
from typing import Optional
from .models import Account, gen_id, PasswordStrength
from .config import get_dialog_config, get_password_generator_config


class MasterPasswordDialog(QtWidgets.QDialog):
    def __init__(self, first_run: bool = False, parent=None):
        super().__init__(parent)
        self.setWindowTitle("主密码")
        self.setModal(True)
        self._first = first_run
        layout = QtWidgets.QVBoxLayout(self)

        label = QtWidgets.QLabel("首次使用，请设置主密码" if first_run else "请输入主密码")
        layout.addWidget(label)

        self.edit = QtWidgets.QLineEdit()
        self.edit.setEchoMode(QtWidgets.QLineEdit.Password)
        layout.addWidget(self.edit)

        if first_run:
            self.edit2 = QtWidgets.QLineEdit()
            self.edit2.setEchoMode(QtWidgets.QLineEdit.Password)
            self.edit2.setPlaceholderText("确认主密码")
            layout.addWidget(self.edit2)

        btns = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        btns.accepted.connect(self._on_ok)
        btns.rejected.connect(self.reject)
        layout.addWidget(btns)

    def _on_ok(self):
        pwd = self.edit.text().strip()
        if not pwd:
            QtWidgets.QMessageBox.warning(self, "提示", "请输入主密码")
            return
        if self._first:
            if pwd != self.edit2.text().strip():
                QtWidgets.QMessageBox.warning(self, "提示", "两次输入不一致")
                return
        self.accept()

    def get_password(self) -> str:
        return self.edit.text().strip()


class PasswordGeneratorDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("密码生成器")
        
        # 使用配置项设置对话框属性
        dialog_config = get_dialog_config('password_generator')
        generator_config = get_password_generator_config()
        
        self.setModal(dialog_config['modal'])
        self.resize(dialog_config['width'], dialog_config['height'])
        self.setObjectName("PasswordGeneratorDialog")
        v = QtWidgets.QVBoxLayout(self)

        form = QtWidgets.QFormLayout()
        self.spin_len = QtWidgets.QSpinBox()
        self.spin_len.setRange(generator_config['min_length'], generator_config['max_length'])
        self.spin_len.setValue(generator_config['default_length'])
        form.addRow("长度", self.spin_len)

        self.chk_lower = QtWidgets.QCheckBox("小写字母")
        self.chk_lower.setChecked(generator_config['default_include_lowercase'])
        self.chk_upper = QtWidgets.QCheckBox("大写字母")
        self.chk_upper.setChecked(generator_config['default_include_uppercase'])
        self.chk_digit = QtWidgets.QCheckBox("数字")
        self.chk_digit.setChecked(generator_config['default_include_digits'])
        self.chk_symbol = QtWidgets.QCheckBox("符号")
        self.chk_symbol.setChecked(generator_config['default_include_symbols'])
        ops = QtWidgets.QHBoxLayout()
        ops.addWidget(self.chk_lower)
        ops.addWidget(self.chk_upper)
        ops.addWidget(self.chk_digit)
        ops.addWidget(self.chk_symbol)
        form.addRow("包含", ops)

        v.addLayout(form)

        self.out = QtWidgets.QLineEdit()
        v.addWidget(self.out)

        self.strength = QtWidgets.QProgressBar()
        self.strength.setRange(0, 100)
        v.addWidget(self.strength)

        btns = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        v.addWidget(btns)
        btns.accepted.connect(self.accept)
        btns.rejected.connect(self.reject)

        gen_btn = QtWidgets.QPushButton("生成")
        gen_btn.setObjectName("Primary")
        gen_btn.clicked.connect(self.generate)
        v.addWidget(gen_btn)

        self.out.textChanged.connect(self._on_pw_change)

    def generate(self):
        import random
        generator_config = get_password_generator_config()
        character_sets = generator_config['character_sets']
        
        lower = character_sets['lowercase'] if self.chk_lower.isChecked() else ""
        upper = character_sets['uppercase'] if self.chk_upper.isChecked() else ""
        digits = character_sets['digits'] if self.chk_digit.isChecked() else ""
        symbols = character_sets['symbols'] if self.chk_symbol.isChecked() else ""
        pool = lower + upper + digits + symbols
        if not pool:
            QtWidgets.QMessageBox.warning(self, "提示", "请选择至少一种字符类型")
            return
        n = self.spin_len.value()
        pw = ''.join(random.choice(pool) for _ in range(n))
        self.out.setText(pw)

    def _on_pw_change(self, text: str):
        s = PasswordStrength.score(text)
        self.strength.setValue(s)
        self.strength.setFormat(f"强度: {PasswordStrength.label(s)} ({s})")

    def get_password(self) -> str:
        return self.out.text()


class AccountDialog(QtWidgets.QDialog):
    def __init__(self, account: Optional[Account] = None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("账号信息")
        
        # 使用配置项设置对话框属性
        dialog_config = get_dialog_config('account_dialog')
        
        self.setModal(dialog_config['modal'])
        self.resize(dialog_config['width'], dialog_config['height'])
        self.setObjectName("AccountDialog")
        self._account = account
        v = QtWidgets.QVBoxLayout(self)

        form = QtWidgets.QFormLayout()
        self.ed_name = QtWidgets.QLineEdit()
        self.ed_user = QtWidgets.QLineEdit()
        self.ed_pw = QtWidgets.QLineEdit()
        self.ed_pw.setEchoMode(QtWidgets.QLineEdit.Password)
        self.btn_toggle = QtWidgets.QToolButton()
        self.btn_toggle.setText("显示")
        self.btn_toggle.setCheckable(True)
        self.btn_toggle.toggled.connect(self._toggle_pw)
        pw_row = QtWidgets.QHBoxLayout()
        pw_row.addWidget(self.ed_pw)
        pw_row.addWidget(self.btn_toggle)
        self.btn_gen = QtWidgets.QToolButton()
        self.btn_gen.setText("生成")
        self.btn_gen.clicked.connect(self._open_generator)
        pw_row.addWidget(self.btn_gen)
        self.ed_url = QtWidgets.QLineEdit()
        self.ed_notes = QtWidgets.QTextEdit()

        form.addRow("名称", self.ed_name)
        form.addRow("用户名", self.ed_user)
        form.addRow("密码", pw_row)
        form.addRow("网址", self.ed_url)
        form.addRow("备注", self.ed_notes)
        v.addLayout(form)

        self.strength = QtWidgets.QProgressBar()
        self.strength.setRange(0, 100)
        v.addWidget(self.strength)
        self.ed_pw.textChanged.connect(self._on_pw_change)

        btns = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        v.addWidget(btns)
        btns.accepted.connect(self._on_ok)
        btns.rejected.connect(self.reject)

        if account:
            self.ed_name.setText(account.name)
            self.ed_user.setText(account.username)
            self.ed_pw.setText(account.password)
            self.ed_url.setText(account.url)
            self.ed_notes.setPlainText(account.notes)

    def _toggle_pw(self, checked):
        self.ed_pw.setEchoMode(QtWidgets.QLineEdit.Normal if checked else QtWidgets.QLineEdit.Password)
        self.btn_toggle.setText("隐藏" if checked else "显示")

    def _open_generator(self):
        dlg = PasswordGeneratorDialog(self)
        if dlg.exec_() == QtWidgets.QDialog.Accepted:
            self.ed_pw.setText(dlg.get_password())

    def _on_pw_change(self, text: str):
        s = PasswordStrength.score(text)
        self.strength.setValue(s)
        self.strength.setFormat(f"强度: {PasswordStrength.label(s)} ({s})")

    def _on_ok(self):
        if not self.ed_name.text().strip() or not self.ed_user.text().strip():
            QtWidgets.QMessageBox.warning(self, "提示", "名称和用户名不能为空")
            return
        self.accept()

    def get_account(self, group_id: Optional[str]) -> Account:
        if self._account:
            aid = self._account.id
        else:
            aid = gen_id()
        return Account(
            id=aid,
            name=self.ed_name.text().strip(),
            username=self.ed_user.text().strip(),
            password=self.ed_pw.text(),
            url=self.ed_url.text().strip(),
            notes=self.ed_notes.toPlainText().strip(),
            group_id=group_id,
        )
    
    def __del__(self):
        """析构函数：清理信号连接"""
        self._cleanup_signals()
    
    def _cleanup_signals(self):
        """清理所有信号连接"""
        try:
            # 清理按钮信号
            if hasattr(self, 'btns'):
                self.btns.accepted.disconnect()
                self.btns.rejected.disconnect()
            
            # 清理其他控件信号
            if hasattr(self, 'btn_toggle'):
                self.btn_toggle.toggled.disconnect()
            if hasattr(self, 'btn_gen'):
                self.btn_gen.clicked.disconnect()
            if hasattr(self, 'ed_pw'):
                self.ed_pw.textChanged.disconnect()
                
        except (TypeError, RuntimeError, AttributeError):
            pass


class InputDialog(QtWidgets.QDialog):
    def __init__(self, title: str, label: str, text: str = "", parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        
        # 使用配置项设置对话框属性
        dialog_config = get_dialog_config('input_dialog')
        
        self.setModal(dialog_config['modal'])
        self.resize(dialog_config['width'], dialog_config['height'])
        self.setObjectName("InputDialog")
        v = QtWidgets.QVBoxLayout(self)
        self.lbl = QtWidgets.QLabel(label)
        self.ed = QtWidgets.QLineEdit(text)
        v.addWidget(self.lbl)
        v.addWidget(self.ed)
        btns = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        v.addWidget(btns)
        btns.accepted.connect(self.accept)
        btns.rejected.connect(self.reject)

    def get_text(self) -> str:
        return self.ed.text().strip()
    
    def __del__(self):
        """析构函数：清理信号连接"""
        self._cleanup_signals()
    
    def _cleanup_signals(self):
        """清理所有信号连接"""
        try:
            # 清理按钮信号
            if hasattr(self, 'btns'):
                self.btns.accepted.disconnect()
                self.btns.rejected.disconnect()
        except (TypeError, RuntimeError, AttributeError):
            pass