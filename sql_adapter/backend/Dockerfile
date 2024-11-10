# 使用基础镜像
FROM ubuntu_base_os_image:3.0

# 设置工作目录
WORKDIR /app

# 复制项目依赖文件 requirements.txt 到工作目录
COPY requirements.txt .

# 安装项目依赖
RUN pip3.11 install --no-cache-dir -r requirements.txt

# 复制当前目录下的所有文件到容器的工作目录
COPY . .

# 设置环境变量
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# 开放 Flask 的默认端口
EXPOSE 5001

# 启动命令
#CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5001", "app:app"]
CMD ["flask", "run"]
