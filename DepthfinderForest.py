from flask import Flask, request, render_template_string
import math

app = Flask(__name__)

# HTML template for the form
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Depth Calculator</title>
    <style>
        .result { color: red; font-weight: bold; }
    </style>
</head>
<body>
    <h1>Calculate Depth for Forest</h1>
    <form method="POST">
        <label for="d_values">Enter d values (comma-separated, maximum diameter):</label><br>
        <input type="text" id="d_values" name="d_values" required><br><br>
        
        <label for="t_values">Enter t values (comma-separated, time parameter):</label><br>
        <input type="text" id="t_values" name="t_values" required><br><br>
        
        <label for="p_values">Enter p values (comma-separated, number of connected components):</label><br>
        <input type="text" id="p_values" name="p_values" required><br><br>
        
        <button type="submit">Calculate</button>
    </form>
    {% if results %}
        <h2>Results:</h2>
        <ul>
            {% for result in results %}
                <li class="result">{{ result }}</li>
            {% endfor %}
        </ul>
    {% endif %}
</body>
</html>
"""

def compute_depth(d, t, p):
    # Calculate the expression [(d - t + 2) / 3] for each t ≥ 1
    depth_expression = (d - t + 2) / 3
    # Take the ceiling of the division as the expression is rounded up
    depth_expression_ceil = math.ceil(depth_expression)
    
    # Compute the depth using the given formula
    depth = max(depth_expression_ceil + p - 1, p)
    return depth

@app.route('/', methods=['GET', 'POST'])
def depth_calculator():
    results = []
    if request.method == 'POST':
        d_values = request.form.get('d_values', '').split(',')
        t_values = request.form.get('t_values', '').split(',')
        p_values = request.form.get('p_values', '').split(',')
        
        # Validate input
        if len(d_values) != len(t_values) or len(d_values) != len(p_values):
            results.append("Error: The number of d, t, and p values must be the same!")
        else:
            for d, t, p in zip(d_values, t_values, p_values):
                try:
                    d = int(d.strip())  # Convert d to integer
                    t = int(t.strip())  # Convert t to integer
                    p = int(p.strip())  # Convert p to integer
                    
                    # Calculate depth
                    depth = compute_depth(d, t, p)
                    results.append(f"d: {d}, t: {t}, p: {p} => Depth: {depth}")
                except ValueError:
                    results.append(f"Invalid input for d: {d.strip()}, t: {t.strip()}, or p: {p.strip()}. Please enter only integer values.")
    
    return render_template_string(HTML_TEMPLATE, results=results)

if __name__ == "__main__":
    app.run(debug=True, port=5001)
