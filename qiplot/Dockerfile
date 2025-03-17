# 基础镜像
FROM python:3.10

# 设置工作目录
WORKDIR /app

# 复制项目文件
COPY . .

# 安装常见的可视化库
RUN pip install --no-cache-dir \
    fastapi uvicorn \
    matplotlib seaborn plotly pandas numpy openai

# 启动 FastAPI 服务器
CMD ["uvicorn", "backend_fastapi:app", "--host", "0.0.0.0", "--port", "8000"]