import os
import hashlib
from typing import Tuple, Optional
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from .config import get_security_config

# ECC加密模块 - 提供基于椭圆曲线的加密和解密接口
# 使用 ECIES (椭圆曲线集成加密方案) 和 P-256 椭圆曲线


class CryptoManager:
    """ECC加密管理器 - 提供基于椭圆曲线的加密和解密接口"""
    
    def __init__(self):
        self.security_config = get_security_config()
        self.curve = ec.SECP256R1()  # 使用 P-256 椭圆曲线
    
    def encrypt(self, password: str, data: bytes) -> bytes:
        """ECC混合加密接口
        
        Args:
            password: 加密密码（用于派生密钥）
            data: 要加密的数据
            
        Returns:
            加密后的数据包（包含临时公钥、盐值和密文）
        """
        # 生成临时密钥对
        ephemeral_private_key = ec.generate_private_key(self.curve)
        ephemeral_public_key = ephemeral_private_key.public_key()
        
        # 从密码派生接收方密钥对
        recipient_private_key = self._derive_key_pair_from_password(password)
        recipient_public_key = recipient_private_key.public_key()
        
        # 执行ECDH密钥交换
        shared_key = ephemeral_private_key.exchange(ec.ECDH(), recipient_public_key)
        
        # 使用HKDF派生AES密钥
        salt = os.urandom(16)
        derived_key = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            info=b'ECIES-AES-256-GCM'
        ).derive(shared_key)
        
        # 使用AES-GCM加密数据
        aesgcm = AESGCM(derived_key)
        nonce = os.urandom(12)
        ciphertext = aesgcm.encrypt(nonce, data, None)
        
        # 序列化临时公钥
        ephemeral_public_bytes = ephemeral_public_key.public_bytes(
            encoding=serialization.Encoding.X962,
            format=serialization.PublicFormat.UncompressedPoint
        )
        
        # 返回格式：公钥长度(1字节) + 临时公钥 + 盐值长度(1字节) + 盐值 + nonce长度(1字节) + nonce + 密文
        return (bytes([len(ephemeral_public_bytes)]) + ephemeral_public_bytes + 
                bytes([len(salt)]) + salt + 
                bytes([len(nonce)]) + nonce + ciphertext)
    
    def decrypt(self, password: str, encrypted_data: bytes) -> bytes:
        """ECC混合解密接口
        
        Args:
            password: 解密密码
            encrypted_data: 加密的数据包
            
        Returns:
            解密后的原始数据
            
        Raises:
            ValueError: 数据格式错误或解密失败
        """
        if len(encrypted_data) < 4:
            raise ValueError("加密数据格式错误")
            
        offset = 0
        
        # 解析临时公钥
        pubkey_len = encrypted_data[offset]
        offset += 1
        if len(encrypted_data) < offset + pubkey_len:
            raise ValueError("加密数据格式错误")
        ephemeral_public_bytes = encrypted_data[offset:offset + pubkey_len]
        offset += pubkey_len
        
        # 解析盐值
        if len(encrypted_data) < offset + 1:
            raise ValueError("加密数据格式错误")
        salt_len = encrypted_data[offset]
        offset += 1
        if len(encrypted_data) < offset + salt_len:
            raise ValueError("加密数据格式错误")
        salt = encrypted_data[offset:offset + salt_len]
        offset += salt_len
        
        # 解析nonce
        if len(encrypted_data) < offset + 1:
            raise ValueError("加密数据格式错误")
        nonce_len = encrypted_data[offset]
        offset += 1
        if len(encrypted_data) < offset + nonce_len:
            raise ValueError("加密数据格式错误")
        nonce = encrypted_data[offset:offset + nonce_len]
        offset += nonce_len
        
        # 获取密文
        ciphertext = encrypted_data[offset:]
        
        try:
            # 重构临时公钥
            ephemeral_public_key = ec.EllipticCurvePublicKey.from_encoded_point(
                self.curve, ephemeral_public_bytes
            )
            
            # 从密码派生接收方密钥对
            recipient_private_key = self._derive_key_pair_from_password(password)
            
            # 执行ECDH密钥交换
            shared_key = recipient_private_key.exchange(ec.ECDH(), ephemeral_public_key)
            
            # 使用HKDF派生AES密钥
            derived_key = HKDF(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                info=b'ECIES-AES-256-GCM'
            ).derive(shared_key)
            
            # 使用AES-GCM解密数据
            aesgcm = AESGCM(derived_key)
            plaintext = aesgcm.decrypt(nonce, ciphertext, None)
            
            return plaintext
            
        except Exception as e:
            raise ValueError(f"解密失败: {str(e)}")
    
    def create_master_hash(self, password: str) -> Tuple[bytes, bytes]:
        """创建主密码哈希
        
        Args:
            password: 主密码
            
        Returns:
            (盐值, 哈希值) 元组
        """
        salt_size = 16  # 固定主密码盐长度为16字节
        salt = os.urandom(salt_size)
        hash_value = self._hash_master(password, salt)
        return salt, hash_value
    
    def verify_master_password(self, password: str, salt: bytes, expected_hash: bytes) -> bool:
        """验证主密码
        
        Args:
            password: 要验证的密码
            salt: 存储的盐值
            expected_hash: 期望的哈希值
            
        Returns:
            验证是否成功
        """
        computed_hash = self._hash_master(password, salt)
        return computed_hash == expected_hash
    
    def _derive_key_pair_from_password(self, password: str) -> ec.EllipticCurvePrivateKey:
        """从密码派生ECC密钥对
        
        Args:
            password: 密码字符串
            
        Returns:
            ECC私钥对象
        """
        # 使用PBKDF2从密码派生32字节的种子
        iterations = 200000  # 固定数据加密迭代次数
        # 使用固定盐值确保相同密码总是生成相同的密钥对
        fixed_salt = b'ECIES-KeyDerivation-Salt-2024'
        seed = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), fixed_salt, iterations, dklen=32)
        
        # 将种子转换为私钥标量（确保在曲线阶数范围内）
        private_value = int.from_bytes(seed, 'big')
        # P-256曲线的阶数
        curve_order = 0xffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc632551
        private_value = private_value % curve_order
        if private_value == 0:
            private_value = 1  # 避免零值
        
        # 创建私钥对象
        return ec.derive_private_key(private_value, self.curve)
    
    def _hash_master(self, password: str, salt: bytes) -> bytes:
        """生成主密码的哈希值用于验证"""
        iterations = 300000  # 固定主密码哈希迭代次数
        return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations, dklen=32)


# 全局加密管理器实例
_crypto_manager = CryptoManager()


# 标准化接口函数
def encrypt(password: str, data: bytes) -> bytes:
    """加密数据
    
    Args:
        password: 加密密码
        data: 要加密的数据
        
    Returns:
        加密后的数据包
    """
    return _crypto_manager.encrypt(password, data)


def decrypt(password: str, encrypted_data: bytes) -> bytes:
    """解密数据
    
    Args:
        password: 解密密码
        encrypted_data: 加密的数据包
        
    Returns:
        解密后的原始数据
    """
    return _crypto_manager.decrypt(password, encrypted_data)