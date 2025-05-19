
import json
from flask import Flask, request, render_template_string
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    checkbox_label_mapping = {
        'S': 'sexual (S)',
        'H': 'hate (H)',
        'V': 'violence (V)',
        'HR': 'harassment (HR)',
        'SH': 'self-harm (SH)',
        'S3': 'sexual/minors (S3)',
        'H2': 'hate/threatening (H2)',
        'V2': 'violence/graphic (V2)'
    }
    checkboxes = list(checkbox_label_mapping.keys())
    checkbox_values = {checkbox: 'Any' for checkbox in checkboxes}
    matching_lines = []  

    if request.method == 'POST':
        for checkbox in checkboxes:
            checkbox_values[checkbox] = request.form.get(f'radio-{checkbox}', 'Any')
            logging.debug(f"Checkbox {checkbox} value: {checkbox_values[checkbox]}")

        with open('dataset.js', 'r', encoding='utf-8') as f:
            js_content = f.read()
        prefix = 'const dataset = '
        if js_content.startswith(prefix):
            js_content = js_content[len(prefix):]
        js_content = js_content.rstrip(';/\n')
        dataset = json.loads(js_content)

        for record in dataset:
            if all(
                str(record.get(checkbox, 'N/A')) == checkbox_values[checkbox] or
                checkbox_values[checkbox] == 'Any' or
                (
                    checkbox_values[checkbox] == '0 or N/A'
                    and str(record.get(checkbox, 'N/A')) in ['0', 'N/A']
                )
                for checkbox in checkboxes
            ):
                keys_0, keys_1, keys_na = [], [], []
                for checkbox in checkboxes:
                    value = str(record.get(checkbox, 'N/A'))
                    if value == '0':
                        keys_0.append(checkbox_label_mapping[checkbox])
                    elif value == '1':
                        keys_1.append(checkbox_label_mapping[checkbox])
                    else:
                        keys_na.append(checkbox_label_mapping[checkbox])
                record['keys_0'] = ', '.join(keys_0)
                record['keys_1'] = ', '.join(keys_1)
                record['keys_na'] = ', '.join(keys_na)
                matching_lines.append(record)

    return render_template_string("""
        <h1> Explore-wrongthink </h1>
        <style>
            h1, h2 { 
                text-align: center; 
            } 
            table {
                width: 100%;
                table-layout: fixed;
            }
            th, td {
                word-wrap: break-word;
            }
        </style>
        <script>
            function setAllRadioButtons(value) {
                // Get all radio input elements
                var radios = document.querySelectorAll('input[type="radio"]');

                // Loop through each radio input element
                radios.forEach(function(radio) {
                    if (radio.value === value) {
                        radio.checked = true;
                    }
                });
            }
        </script>
        <form method="POST">
        <table border="1">
            <thead>
                <tr>
                    <th>Classification key</th>
<th>
    <button onclick="setAllRadioButtons('0')">Set all values</button> = 0
</th>
<th>
    <button onclick="setAllRadioButtons('1')">Set all values</button> = 1
</th>
<th>
    <button onclick="setAllRadioButtons('Any')">Set all values</button> = Any
</th>
<th>
    <button onclick="setAllRadioButtons('0 or N/A')">Set all values</button> = 0 or N/A
</th>
                    <th>Value on last generation</th>
                </tr>
            </thead>
            <tbody>
{% for checkbox in checkboxes %}
                <tr>
                    <td><label>{{ checkbox_label_mapping[checkbox] }}</label></td>
                    <td><input type="radio" name="radio-{{ checkbox }}" value="0" {% if checkbox_values[checkbox] == '0' %} checked {% endif %}>0</td>
                    <td><input type="radio" name="radio-{{ checkbox }}" value="1" {% if checkbox_values[checkbox] == '1' %} checked {% endif %}>1</td>
                    <td><input type="radio" name="radio-{{ checkbox }}" value="Any" {% if checkbox_values[checkbox] == 'Any' %} checked {% endif %}>Any</td>
                    <td><input type="radio" name="radio-{{ checkbox }}" value="0 or N/A" {% if checkbox_values[checkbox] == '0 or N/A' %} checked {% endif %}>0 or N/A</td>
                    <td>{{ checkbox_values[checkbox] if checkbox_values[checkbox] != 'Any' else 'N/A' }}</td>
                </tr>
{% endfor %}
            </tbody>
        </table>
        <br><input type="submit" value="Generate subset" style="font-size:18px; padding:10px;">
        </form>
        <h2>{{ matching_lines | length }} Matching lines:</h2>
        <table border="1">
            <thead>
                <tr>
                    <th>Prompt</th>
                    <th>Value = 0</th>
                    <th>Value = 1</th>
                    <th>Value = N/A</th>
                </tr>
            </thead>
            <tbody>
                {% for line in matching_lines %}
                <tr>
                    <td>{{ line.get('prompt', 'N/A') }}</td>
                    <td>{{ line.keys_0 }}</td>
                    <td>{{ line.keys_1 }}</td>
                    <td>{{ line.keys_na }}</td>
                </tr>
{% endfor %}
            </tbody>
        </table>
    """, checkboxes=checkboxes, checkbox_values=checkbox_values, matching_lines=matching_lines, checkbox_label_mapping=checkbox_label_mapping)

if __name__ == '__main__':
    app.run(debug=True)
