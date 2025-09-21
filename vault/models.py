import uuid
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional
import re
from .config import get_password_strength_config


def gen_id():
    return uuid.uuid4().hex


@dataclass
class Account:
    id: str
    name: str
    username: str
    password: str
    url: str = ""
    notes: str = ""
    group_id: Optional[str] = None


@dataclass
class Group:
    id: str
    name: str


@dataclass
class VaultData:
    groups: List[Group] = field(default_factory=list)
    accounts: List[Account] = field(default_factory=list)
    version: int = 1

    def to_dict(self):
        return {
            "groups": [asdict(g) for g in self.groups],
            "accounts": [asdict(a) for a in self.accounts],
            "version": self.version,
        }

    @staticmethod
    def from_dict(d: Dict):
        vd = VaultData()
        vd.version = d.get("version", 1)
        vd.groups = [Group(**g) for g in d.get("groups", [])]
        vd.accounts = [Account(**a) for a in d.get("accounts", [])]
        return vd


# Password strength scoring 0-100
class PasswordStrength:
    @staticmethod
    def score(pw: str) -> int:
        """计算密码强度评分"""
        if not pw:
            return 0
        
        config = get_password_strength_config()
        weights = config['weights']
        thresholds = config['thresholds']
        
        length = len(pw)
        types = 0
        if re.search(r"[a-z]", pw):
            types += 1
        if re.search(r"[A-Z]", pw):
            types += 1
        if re.search(r"\d", pw):
            types += 1
        if re.search(r"[^a-zA-Z0-9]", pw):
            types += 1
        
        base = min(weights['max_length_score'], length * weights['length_multiplier'])
        diversity = types * weights['type_multiplier']
        bonus = 0
        if length >= thresholds['bonus_length'] and types >= thresholds['bonus_types']:
            bonus = weights['bonus_score']
        score = min(100, base + diversity + bonus)
        return score

    @staticmethod
    def label(score: int) -> str:
        """根据评分返回密码强度标签"""
        config = get_password_strength_config()
        thresholds = config['strength_thresholds']
        
        if score < thresholds['weak']:
            return "弱"
        if score < thresholds['fair']:
            return "中等"
        if score < thresholds['good']:
            return "强"
        return "很强"