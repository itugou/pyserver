# 简单的HTTP文件服务器

这是一个基于Python的简单HTTP文件服务器,可以用于快速分享文件。

## 功能特点

- 支持配置文件自定义设置
- 提供健康检查接口
- 详细的访问日志记录
- 优雅的退出处理
- 支持命令行参数配置

## 使用方法

### 直接运行Python脚本

```bash
# 使用默认配置运行
python http_server.py

# 指定端口运行
python http_server.py -p 8080

# 指定主机地址
python http_server.py --host 0.0.0.0
```

### 运行打包后的exe

```bash
# 直接运行
http_server.exe

# 指定端口运行
http_server.exe -p 8080
```

## 配置文件

程序会自动查找当前目录下的`config.json`文件,示例配置:

```json
{
    "PORT": 8000,
    "HOST": "",
    "LOG_LEVEL": "INFO"
}
```

## 健康检查

访问 `http://localhost:8000/health` 可以获取服务器状态信息。

## 注意事项

1. 默认端口为8000
2. 如果端口被占用会提示错误
3. 按Ctrl+C可以安全退出服务器

## 构建exe

使用PyInstaller打包:

```bash
# 安装pyinstaller
pip install pyinstaller

# 打包命令
pyinstaller --clean --onefile --name http_server ^
    --add-data "static;static" ^
    --add-data "templates;templates" ^
    --add-data "config.json;." ^
    http_server.py
``` 
