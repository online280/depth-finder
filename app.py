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
    <h1>Calculate Depth</h1>
    <form method="POST">
        <label for="n_values">Enter n values (comma-separated, n >= 2):</label><br>
        <input type="text" id="n_values" name="n_values" required><br><br>
        
        <label for="t_values">Enter t values (comma-separated):</label><br>
        <input type="text" id="t_values" name="t_values" required><br><br>
        
        <button type="submit">Calculate</button>
    </form>
    {% if results %}
        <h2>Results:</h2>
        <ul>
            {% for result in results %}
                <li>{{ result }}</li>
            {% endfor %}
        </ul>
    {% endif %}
</body>
</html>
"""

def calculate_depth(n, t):
    """Calculate the depth using the given formula."""
    depth_part = math.ceil((n - t + 1) / 3)  # First part of the formula
    depth = max(depth_part, 1)  # Ensure the depth is at least 1
    return depth

@app.route('/', methods=['GET', 'POST'])
def depth_calculator():
    results = []
    if request.method == 'POST':
        n_values = request.form.get('n_values', '').split(',')
        t_values = request.form.get('t_values', '').split(',')

        # Validate that the number of n and t values are the same
        if len(n_values) != len(t_values):
            results.append("Error: The number of n and t values must be the same!")
        else:
            for n, t in zip(n_values, t_values):
                try:
                    n = int(n.strip())  # Convert n to integer
                    t = int(t.strip())  # Convert t to integer

                    if n < 2:
                        results.append(f"Invalid n value '{n}'. It should be at least 2.")
                        continue

                    # Calculate depth
                    depth = calculate_depth(n, t)
                    results.append(f"n: {n}, t: {t} => Depth: {depth}")
                except ValueError:
                    results.append(f"Invalid input for n: {n.strip()} or t: {t.strip()}. Please enter only integer values.")
    
    return render_template_string(HTML_TEMPLATE, results=results)

if __name__ == "__main__":
    app.run(debug=True, port=8000)
