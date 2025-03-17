from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
import shutil
import os
import openai  # 或者使用 DeepSeek API
import subprocess
import traceback

app = FastAPI()
UPLOAD_DIR = "uploaded_files"
OUTPUT_DIR = "output_images"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

OPENAI_API_KEY = "your_openai_api_key"


# 代码生成函数
def generate_python_code(description: str, file_path: str):
    prompt = f"""
    根据以下描述和数据文件生成 Python 代码：
    描述: {description}
    数据文件: {file_path}
    请选择合适的可视化库（如 Matplotlib, Seaborn, Plotly），并编写完整的 Python 代码，包括数据读取、清洗、可视化。
    请确保最终保存图像到 '{OUTPUT_DIR}/output.png'
    """

    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",  # 或者使用 deepseek-coder API
        messages=[{"role": "system", "content": "你是一个数据可视化专家。"},
                  {"role": "user", "content": prompt}],
        temperature=0.7
    )

    return response["choices"][0]["message"]["content"]


# 运行生成的代码并保存
def execute_python_code(code: str):
    script_path = os.path.join(OUTPUT_DIR, "generated_script.py")
    with open(script_path, "w") as f:
        f.write(code)

    try:
        subprocess.run(["python", script_path], check=True, timeout=30)
        return {"output_image": os.path.join(OUTPUT_DIR, "output.png"), "script_path": script_path}
    except subprocess.CalledProcessError as e:
        return {"error": f"执行错误: {e}"}
    except subprocess.TimeoutExpired:
        return {"error": "代码执行超时"}
    except Exception as e:
        return {"error": f"未知错误: {traceback.format_exc()}"}


@app.post("/generate")
async def generate_chart(description: str = Form(...), file: UploadFile = File(...)):
    # 保存上传文件
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 调用 API 生成代码
    python_code = generate_python_code(description, file_path)

    # 执行生成的代码
    execution_result = execute_python_code(python_code)

    return JSONResponse({
        "message": "代码执行完成",
        "file_path": file_path,
        "description": description,
        "generated_code": python_code,
        "execution_result": execution_result
    })
