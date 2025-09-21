# MimaVault 密码保险箱

一个安全、现代化的密码管理器，采用PyQt5构建，提供优雅的用户界面和强大的密码管理功能。

## 🌟 主要特性

### 🔐 安全性
- **AES-256加密**：使用工业级加密算法保护您的数据
- **主密码保护**：所有数据通过主密码加密存储
- **本地存储**：数据完全存储在本地，无需担心云端泄露
- **自动锁定**：支持会话超时自动锁定功能
- **安全剪贴板**：密码复制后自动清除剪贴板

### 🎨 用户界面
- **现代化设计**：采用深色主题，提供优雅的视觉体验
- **响应式布局**：支持高DPI显示器，界面清晰美观
- **卡片式展示**：账号信息以卡片形式展示，直观易用
- **主题切换**：支持深色和浅色主题切换
- **动画效果**：流畅的界面动画和过渡效果

### 📊 功能特性
- **分组管理**：支持创建自定义分组，便于账号分类
- **搜索功能**：快速搜索和筛选账号信息
- **密码生成器**：内置强密码生成器，支持自定义规则
- **密码强度评估**：实时评估密码强度
- **批量操作**：支持批量导入导出账号数据
- **备份恢复**：支持数据备份和恢复功能

## 📋 系统要求

- **操作系统**：Windows 7/8/10/11, macOS 10.12+, Linux
- **Python版本**：3.7 或更高版本
- **内存**：至少 512MB RAM
- **存储空间**：至少 100MB 可用空间

## 🚀 快速开始

### 安装依赖

```bash
# 克隆项目
git clone https://github.com/your-username/MimaVault.git
cd MimaVault

# 安装依赖
pip install -r requirements.txt
```

### 运行应用

```bash
python app.py
```

### 首次使用

1. **设置主密码**：首次运行时，系统会提示您设置主密码
2. **创建账号**：点击"添加账号"按钮创建您的第一个密码条目
3. **创建分组**：可以创建自定义分组来组织您的账号
4. **开始使用**：享受安全便捷的密码管理体验

## 📁 项目结构

```
MimaVault/
├── app.py                 # 应用程序入口
├── requirements.txt       # 项目依赖
├── README.md             # 项目说明文档
├── vault.dat             # 加密数据文件（运行后生成）
├── user_settings.json    # 用户设置文件
├── image/                # 应用图标资源
│   ├── aipot.ico
│   └── aipot.png
├── logs/                 # 日志文件目录
│   └── vault_errors.log
├── output/               # 打包输出目录
│   └── MimaVault_Setup_v1.1.0.exe
└── vault/                # 核心模块
    ├── __init__.py
    ├── config.py         # 配置管理
    ├── main_window.py    # 主窗口界面
    ├── storage.py        # 数据存储和加密
    ├── crypto.py         # 加密解密功能
    ├── dialogs.py        # 对话框组件
    ├── models.py         # 数据模型
    ├── style.py          # 界面样式
    └── settings_dialog.py # 设置对话框
```

## 🔧 配置说明

### 应用配置

应用的所有配置都在 `vault/config.py` 文件中，包括：

- **界面配置**：窗口大小、颜色主题、字体设置
- **安全配置**：密码长度限制、会话超时时间
- **功能配置**：自动保存间隔、搜索设置等

### 用户设置

用户个人设置保存在 `user_settings.json` 文件中，支持：

- 主题选择
- 窗口位置和大小
- 界面语言设置
- 其他个性化配置

## 🛠️ 开发指南

### 开发环境设置

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 安装开发依赖
pip install -r requirements.txt
```

### 代码结构

- **MVC架构**：采用模型-视图-控制器架构模式
- **模块化设计**：功能模块独立，便于维护和扩展
- **配置驱动**：通过配置文件控制应用行为
- **国际化支持**：支持多语言界面（预留接口）

### 打包发布

```bash
# 使用PyInstaller打包
pyinstaller --onefile --windowed --icon=image/aipot.ico app.py
```

## 🔒 安全说明

### 加密机制

- 使用 **AES-256-CBC** 加密算法
- 密钥通过 **PBKDF2** 从主密码派生
- 每次加密使用随机 **IV**（初始化向量）
- 数据完整性通过 **HMAC** 验证

### 安全建议

1. **强主密码**：使用包含大小写字母、数字和特殊字符的强密码
2. **定期备份**：定期备份您的密码数据库
3. **安全环境**：在安全的计算机环境中使用本应用
4. **及时更新**：保持应用程序为最新版本

## 📝 更新日志

### v1.1.0 (当前版本)
- ✨ 新增分组管理功能
- 🎨 优化用户界面设计
- 🔧 改进配置管理系统
- 🐛 修复已知问题
- 📈 提升应用性能

### v1.0.0
- 🎉 首个正式版本发布
- 🔐 基础密码管理功能
- 🎨 现代化界面设计
- 🔒 AES-256加密支持

## 🤝 贡献指南

欢迎贡献代码！请遵循以下步骤：

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 📞 联系方式

- **项目主页**：[GitHub Repository](https://github.com/your-username/MimaVault)
- **问题反馈**：[Issues](https://github.com/your-username/MimaVault/issues)
- **邮箱**：your-email@example.com

## 🙏 致谢

感谢以下开源项目：

- [PyQt5](https://www.riverbankcomputing.com/software/pyqt/) - 跨平台GUI框架
- [cryptography](https://cryptography.io/) - 现代加密库
- [PyInstaller](https://www.pyinstaller.org/) - Python应用打包工具

---

⭐ 如果这个项目对您有帮助，请给我们一个星标！