from flask import Flask, render_template, request, jsonify
import math

app = Flask(__name__)

# Allowable safe math functions
allowed_names = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}
allowed_names.update({
    'avg': lambda *args: sum(args) / len(args) if args else 0
})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    expr = data.get("expression", "")
    try:
        # Replace % with /100 to allow percentage
        expr = expr.replace('%', '/100')
        result = eval(expr, {"__builtins__": {}}, allowed_names)
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"result": f"Error: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)
