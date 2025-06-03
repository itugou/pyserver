import http.server
import socketserver
import signal
import sys
import os
import json
import time
import argparse
from pathlib import Path

# 默认配置
DEFAULT_CONFIG = {
    'PORT': 8000,
    'HOST': '',
    'LOG_LEVEL': 'INFO'
}

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{timestamp}] 访问记录: {format%args}")
        
    def log_error(self, format, *args):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{timestamp}] 错误: {format%args}")

    def do_GET(self):
        # 添加健康检查接口
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            health_info = {
                'status': 'healthy',
                'timestamp': time.time()
            }
            self.wfile.write(json.dumps(health_info).encode())
            return
        return super().do_GET()

def load_config():
    """加载配置文件"""
    config = DEFAULT_CONFIG.copy()
    config_path = Path('config.json')
    
    if config_path.exists():
        try:
            with open(config_path) as f:
                config.update(json.load(f))
            print(f"已加载配置文件: {config_path}")
        except Exception as e:
            print(f"加载配置文件出错: {e}")
    else:
        print("未找到配置文件,使用默认配置")
        
    return config

def signal_handler(sig, frame):
    """处理退出信号"""
    print("\n正在关闭服务器...")
    try:
        httpd.server_close()
        print("服务器已正常关闭")
    except Exception as e:
        print(f"关闭服务器时出错: {e}")
    sys.exit(0)

def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='简单的HTTP文件服务器')
    parser.add_argument('-p', '--port', type=int, help='服务器端口号')
    parser.add_argument('--host', help='服务器主机地址')
    return parser.parse_args()

if __name__ == "__main__":
    # 注册信号处理器
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # 加载配置
    config = load_config()
    
    # 解析命令行参数
    args = parse_arguments()
    if args.port:
        config['PORT'] = args.port
    if args.host:
        config['HOST'] = args.host

    # 设置工作目录
    if getattr(sys, 'frozen', False):
        os.chdir(os.path.dirname(sys.executable))
    else:
        os.chdir(os.path.dirname(os.path.abspath(__file__)))

    try:
        server_address = (config['HOST'], config['PORT'])
        with socketserver.TCPServer(server_address, MyHTTPRequestHandler) as httpd:
            print(f"启动HTTP服务器 - 主机: {config['HOST'] or '*'}, 端口: {config['PORT']}")
            print(f"可以通过浏览器访问: http://localhost:{config['PORT']}")
            print("健康检查接口: http://localhost:{config['PORT']}/health")
            print("按Ctrl+C可以停止服务器")
            httpd.serve_forever()
    except OSError as e:
        if e.errno == 10048:  # Windows下端口被占用的错误码
            print(f"错误：端口 {config['PORT']} 已被占用")
        else:
            print(f"错误：{e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n正在关闭服务器...")
        sys.exit(0)
    except Exception as e:
        print(f"发生未知错误: {e}")
        sys.exit(1) 