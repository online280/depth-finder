from flask import Flask, request, render_template_string
import math

app = Flask(__name__)

# HTML template for the form
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Depth Calculator</title>
</head>
<body>
    <h1>Calculate Depth for Path</h1>
    <p>Formula: depth(K/I) = ⌈n / 3⌉</p>
    <form method="POST">
        <label for="m_values">Enter values of n separated by commas:</label><br>
        <input type="text" id="m_values" name="m_values" required><br><br>
        <button type="submit">Calculate</button>
    </form>
    {% if results %}
        <h2>Calculated Depths:</h2>
        <ul>
            {% for result in results %}
                <li>{{ result }}</li>
            {% endfor %}
        </ul>
    {% endif %}
</body>
</html>
"""

def calculate_depth(m):
    """
    Calculate the depth of K/I given m, using the formula depth(K/I) = ceil(m / 3).
    """
    return math.ceil(m / 3)

@app.route('/', methods=['GET', 'POST'])
def depth_calculator():
    results = []
    if request.method == 'POST':
        m_values = request.form.get('m_values', '').strip()
        try:
            m_list = [int(m) for m in m_values.split(",")]
            for m in m_list:
                depth = calculate_depth(m)
                results.append(f"For m = {m}, depth(K/I) = {depth}")
        except ValueError:
            results.append("Invalid input! Please enter integers separated by commas.")
    return render_template_string(HTML_TEMPLATE, results=results)

if __name__ == "__main__":
    app.run(debug=True, port=8002)
