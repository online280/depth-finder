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
    <h1>Calculate Depth for Tree</h1>
    <form method="POST">
        <label for="r_values">Enter diameter values (d) separated by commas:</label><br>
        <input type="text" id="r_values" name="r_values" required><br><br>
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

def find_depth(r):
    """Calculate the depth using the given formula."""
    depth = math.ceil((r + 1) / 3)
    return depth

@app.route('/', methods=['GET', 'POST'])
def depth_calculator():
    results = []
    if request.method == 'POST':
        r_values = request.form.get('r_values', '').split(",")
        for r in r_values:
            try:
                r = int(r.strip())  # Convert to integer after stripping spaces
                depth = find_depth(r)
                results.append(f"Diameter (r): {r} => Depth: {depth}")
            except ValueError:
                results.append(f"Invalid input '{r.strip()}'. Please enter only integer values.")
    return render_template_string(HTML_TEMPLATE, results=results)

if __name__ == "__main__":
    app.run(debug=True, port=8001)
