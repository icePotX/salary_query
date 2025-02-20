from flask import Flask, render_template, request, jsonify
import os
import pandas as pd

app = Flask(__name__)

# 获取Excel文件列表
def get_excel_files():
    table_dir = os.path.join(os.path.dirname(__file__), 'table')
    return [f for f in os.listdir(table_dir) if f.endswith(('.xlsx', '.xls'))]

# 查询工资数据
def query_salary(file, name, id_number):
    table_dir = os.path.join(os.path.dirname(__file__), 'table')
    file_path = os.path.join(table_dir, file)
    try:
        # 根据文件扩展名选择读取方式
        if file.endswith('.xlsx'):
            df = pd.read_excel(file_path, engine='openpyxl')
        elif file.endswith('.xls'):
            df = pd.read_excel(file_path, engine='xlrd')
        else:
            return {'error': '不支持的文件类型'}
        
        # 查询匹配的行
        result = df[(df['姓名'] == name) & (df['身份证号'] == id_number)]
        if not result.empty:
            # 获取列顺序
            columns = df.columns.tolist()
            # 返回结果和列顺序
            return {
                'data': result.iloc[0].to_dict(),
                'columns': columns
            }
        else:
            return {'error': '未找到匹配的记录'}
    except Exception as e:
        return {'error': str(e)}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_files')
def get_files():
    files = get_excel_files()
    return jsonify(files)

@app.route('/query', methods=['POST'])
def query():
    data = request.json
    result = query_salary(data['file'], data['name'], data['idNumber'])
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)