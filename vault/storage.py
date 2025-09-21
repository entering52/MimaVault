import json
import os
from typing import Optional, Dict
from dataclasses import asdict

from .models import VaultData, Account, Group, gen_id
from .crypto import encrypt, decrypt, _crypto_manager
from .config import get_security_config, get_text


class VaultError(Exception):
    pass


class VaultStorage:
    def __init__(self, path: str):
        self.path = path
        self.vault = VaultData()
        self._master_salt: Optional[bytes] = None
        self._master_hash: Optional[bytes] = None
        self._master_password: Optional[str] = None

    # ----- Master password flow -----
    def create_new(self, master_password: str):
        """创建新的保险库"""
        self._master_password = master_password
        self._master_salt, self._master_hash = _crypto_manager.create_master_hash(master_password)
        # default group
        default_group_name = get_text('default_values', 'default_group') or "未分组"
        default_group = Group(id=gen_id(), name=default_group_name)
        self.vault.groups.append(default_group)

    def verify_master(self, master_password: str) -> bool:
        if not self._master_salt or not self._master_hash:
            return False
        return _crypto_manager.verify_master_password(master_password, self._master_salt, self._master_hash)

    def change_master(self, old_password: str, new_password: str):
        """修改主密码"""
        if not self.verify_master(old_password):
            raise VaultError("主密码不正确")
        # Re-encrypt with new password on save
        self._master_password = new_password
        self._master_salt, self._master_hash = _crypto_manager.create_master_hash(new_password)
        self.save()

    # ----- Helpers -----
    def _find_default_group(self) -> Optional[Group]:
        default_group_name = get_text('default_values', 'default_group') or "未分组"
        undefined_group_name = get_text('default_values', 'undefined_group') or "未定义"
        for g in self.vault.groups:
            if g.name in (default_group_name, undefined_group_name):
                return g
        return None

    def default_group_id(self) -> str:
        g = self._find_default_group()
        if g:
            return g.id
        # If missing (older数据或异常情况)，自动创建
        default_group_name = get_text('default_values', 'default_group') or "未分组"
        g = Group(id=gen_id(), name=default_group_name)
        self.vault.groups.append(g)
        return g.id

    def _name_exists(self, name: str) -> bool:
        name = (name or "").strip()
        return any(g.name == name for g in self.vault.groups)

    # ----- Persistence -----
    def _serialize(self) -> bytes:
        # 优化序列化过程，减少不必要的转换
        meta = {
            "salt": self._master_salt.hex() if self._master_salt else None,
            "hash": self._master_hash.hex() if self._master_hash else None,
            "version": self.vault.version,
        }
        
        # 预分配数据字典以提高性能
        data = {
            "version": self.vault.version,
        }
        
        # 批量序列化对象以提高性能
        data["groups"] = [None] * len(self.vault.groups)
        data["accounts"] = [None] * len(self.vault.accounts)
        
        for i, g in enumerate(self.vault.groups):
            data["groups"][i] = asdict(g)
            
        for i, a in enumerate(self.vault.accounts):
            data["accounts"][i] = asdict(a)
        
        obj = {
            "meta": meta,
            "data": data,
        }
        plain = json.dumps(obj, separators=(',', ':'), ensure_ascii=False).encode("utf-8")
        return plain

    def _deserialize(self, plain: bytes):
        obj = json.loads(plain.decode("utf-8"))
        meta = obj.get("meta", {})
        self._master_salt = bytes.fromhex(meta.get("salt")) if meta.get("salt") else None
        self._master_hash = bytes.fromhex(meta.get("hash")) if meta.get("hash") else None
        
        # 解析数据部分，优化大数据量处理
        data = obj.get("data", {})
        self.vault.version = data.get("version", 1)
        
        # 预分配列表空间以提高性能
        groups_data = data.get("groups", [])
        accounts_data = data.get("accounts", [])
        
        self.vault.groups = [None] * len(groups_data)
        self.vault.accounts = [None] * len(accounts_data)
        
        # 批量创建对象以提高性能
        for i, g in enumerate(groups_data):
            self.vault.groups[i] = Group(**g)
            
        for i, a in enumerate(accounts_data):
            self.vault.accounts[i] = Account(**a)

    def save(self):
        if not self._master_password:
            raise VaultError("未设置主密码")
        plain = self._serialize()
        encrypted_data = encrypt(self._master_password, plain)
        with open(self.path, "wb") as f:
            f.write(encrypted_data)

    def load(self, master_password: str):
        if not os.path.exists(self.path):
            raise VaultError("数据文件不存在")
        with open(self.path, "rb") as f:
            encrypted_data = f.read()
        try:
            plain = decrypt(master_password, encrypted_data)
            self._deserialize(plain)
        except Exception:
            raise VaultError("数据损坏或密码不正确")
        # Verify master
        if not self._master_salt or not self._master_hash:
            raise VaultError("数据格式错误")
        if not _crypto_manager.verify_master_password(master_password, self._master_salt, self._master_hash):
            raise VaultError("主密码错误")
        self._master_password = master_password

    # ----- Groups and Accounts API -----
    def add_group(self, name: str) -> Group:
        name = (name or "").strip()
        if not name:
            raise VaultError("分组名称不能为空")
        # 禁止与现有分组重名，禁止使用保留名称重复创建
        if self._name_exists(name):
            raise VaultError("分组名称已存在")
        default_group_name = get_text('default_values', 'default_group') or "未分组"
        undefined_group_name = get_text('default_values', 'undefined_group') or "未定义"
        if name in (default_group_name, undefined_group_name) and self._find_default_group():
            raise VaultError("该名称为保留分组，已存在")
        g = Group(id=gen_id(), name=name)
        self.vault.groups.append(g)
        return g

    def rename_group(self, gid: str, name: str):
        name = (name or "").strip()
        if not name:
            raise VaultError("分组名称不能为空")
        # 不允许重名（排除自己）
        if any(g.name == name and g.id != gid for g in self.vault.groups):
            raise VaultError("分组名称已存在")
        for g in self.vault.groups:
            if g.id == gid:
                g.name = name
                return
        raise VaultError("分组不存在")

    def delete_group(self, gid: str, migrate_to: Optional[str]):
        # 禁止删除默认分组
        if gid == self.default_group_id():
            raise VaultError("默认分组不可删除")
        target_gid = migrate_to or self.default_group_id()
        # 删除分组
        self.vault.groups = [g for g in self.vault.groups if g.id != gid]
        # 迁移账号（仅迁移被删分组内账号，未分组的账号不会受影响）
        for a in self.vault.accounts:
            if a.group_id == gid:
                a.group_id = target_gid

    def add_account(self, a: Account):
        if not a.group_id:
            a.group_id = self.default_group_id()
        self.vault.accounts.append(a)

    def update_account(self, a: Account):
        for i, item in enumerate(self.vault.accounts):
            if item.id == a.id:
                # 确保更新后也有有效分组
                if not a.group_id:
                    a.group_id = self.default_group_id()
                self.vault.accounts[i] = a
                return
        raise VaultError("账号不存在")

    def delete_account(self, aid: str):
        self.vault.accounts = [a for a in self.vault.accounts if a.id != aid]

    # ----- Import/Export -----
    def export_plain(self) -> str:
        data = {
            "groups": [asdict(g) for g in self.vault.groups],
            "accounts": [asdict(a) for a in self.vault.accounts],
            "version": self.vault.version,
        }
        return json.dumps(data, ensure_ascii=False, indent=2)

    def import_plain(self, text: str, merge: bool = True):
        data = json.loads(text)
        if not merge:
            self.vault.version = data.get("version", 1)
            self.vault.groups = [Group(**g) for g in data.get("groups", [])]
            self.vault.accounts = [Account(**a) for a in data.get("accounts", [])]
            return
        # merge groups by name
        name_to_gid = {g.name: g.id for g in self.vault.groups}
        for g in data.get("groups", []):
            if g["name"] in name_to_gid:
                gid = name_to_gid[g["name"]]
            else:
                ng = self.add_group(g["name"])
                gid = ng.id
                name_to_gid[g["name"]] = gid
        # merge accounts by (name, username)
        existing = {(a.name, a.username): a for a in self.vault.accounts}
        for a in data.get("accounts", []):
            key = (a["name"], a["username"])
            a_group_name = next((g.name for g in data.get("groups", []) if g["id"] == a["group_id"]), None)
            a["group_id"] = name_to_gid.get(a_group_name) or self.default_group_id()
            if key in existing:
                # overwrite
                a["id"] = existing[key].id
                self.update_account(Account(**a))
            else:
                a["id"] = gen_id()
                self.add_account(Account(**a))

    def export_encrypted(self) -> bytes:
        plain = self._serialize()
        if not self._master_password:
            raise VaultError("未设置主密码")
        return encrypt(self._master_password, plain)

    def import_encrypted(self, blob: bytes, password: Optional[str] = None, merge: bool = True):
        # Allow providing a password for foreign encrypted file
        pwd = password or self._master_password
        if not pwd:
            raise VaultError("缺少解密密码")
        plain = decrypt(pwd, blob)
        data = json.loads(plain.decode("utf-8"))
        if not merge:
            meta = data.get("meta", {})
            self._master_salt = bytes.fromhex(meta.get("salt")) if meta.get("salt") else None
            self._master_hash = bytes.fromhex(meta.get("hash")) if meta.get("hash") else None
            
            data_content = data.get("data", {})
            self.vault.version = data_content.get("version", 1)
            self.vault.groups = [Group(**g) for g in data_content.get("groups", [])]
            self.vault.accounts = [Account(**a) for a in data_content.get("accounts", [])]
            return
        # simple merge: append groups/accounts with new ids
        old_names = {g.name for g in self.vault.groups}
        map_gid: Dict[str, str] = {}
        data_content = data.get("data", {})
        for g in data_content.get("groups", []):
            if g["name"] in old_names:
                exist_gid = next(x.id for x in self.vault.groups if x.name == g["name"])
                map_gid[g["id"]] = exist_gid
            else:
                ng = self.add_group(g["name"])
                map_gid[g["id"]] = ng.id
        for a in data_content.get("accounts", []):
            a["id"] = gen_id()
            a["group_id"] = map_gid.get(a["group_id"]) or self.default_group_id()
            self.add_account(Account(**a))
