view_feedback.html GUI
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>User Feedback</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            margin: 0;
            padding: 0;
            background: linear-gradient(135deg, #6a11cb, #2575fc);
            color: white;
        }

        .dropdown-container {
            position: fixed;
            top: 15px;
            right: 20px;
            z-index: 100;
        }

        .dropdown-button {
            background: linear-gradient(45deg, #ff5722, #ffc107);
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 30px;
            cursor: pointer;
            font-weight: bold;
            transition: transform 0.3s, background 0.3s;
        }

        .dropdown-button:hover {
            transform: scale(1.1);
            background: linear-gradient(45deg, #ffc107, #ff5722);
        }

        .container {
            display: flex;
            justify-content: center;
            align-items: stretch;
            width: 100%;
            height: 100vh;
        }

        .section {
            flex: 1;
            padding: 20px;
            background: white;
            color: #333;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
            opacity: 0;
            transform: scale(0.9);
            transition: all 0.5s ease-in-out;
            position: absolute;
            width: 90%;
            height: 90%;
        }

        .section.active {
            opacity: 1;
            transform: scale(1);
            position: static;
        }

        h2 {
            text-align: center;
            margin: 0;
            padding: 10px;
            font-size: 1.5em;
            color: #444;
            background: #f8f8f8;
            border-radius: 8px;
        }

        .pdf-preview {
            height: 60%;
            border: none;
            width: 100%;
            margin-bottom: 10px;
        }

        .feedback-section {
            padding: 10px;
            background: #f9f9f9;
            border-radius: 8px;
            overflow-y: auto;
            height: 35%;
            box-shadow: inset 0 4px 6px rgba(0, 0, 0, 0.1);
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
        }

        th, td {
            padding: 10px;
            border: 1px solid #ddd;
            text-align: center;
        }

        th {
            background: #333;
            color: white;
        }

        tr:nth-child(even) {
            background: #f2f2f2;
        }

        tr:nth-child(odd) {
            background: white;
        }

        .delete-button {
            padding: 8px 15px;
            color: white;
            background: #d9534f;
            border: none;
            border-radius: 20px;
            cursor: pointer;
            transition: transform 0.3s, background 0.3s;
        }

        .delete-button:hover {
            transform: scale(1.1);
            background: #c9302c;
        }
    </style>
</head>
<body>
    <div class="dropdown-container">
        <button id="dropdownButton" class="dropdown-button" onclick="toggleSection()">View Previous Feedback</button>
    </div>

    <div class="container">
        <!-- Current Feedback Section -->
        <div id="currentFeedback" class="section active">
            <h2>Current Resume Feedback</h2>
            {% if uploaded_pdf_path %}
            <iframe class="pdf-preview" src="{{ uploaded_pdf_path }}"></iframe>
            {% else %}
            <p>No resume uploaded.</p>
            {% endif %}
            <div class="feedback-section">
                {% if current_feedback %}
                <strong>Word Count:</strong> {{ current_feedback.word_count }}<br>
                <strong>Keywords Found:</strong> {{ current_feedback.keywords_found | join(', ') }}<br>
                <div>
                    <strong>Suggestions:</strong>
                    <ul>
                        {% for suggestion in current_feedback.suggestions %}
                        <li>{{ suggestion }}</li>
                        {% endfor %}
                    </ul>
                </div>
                {% else %}
                <p>No feedback available for the current resume.</p>
                {% endif %}
            </div>
        </div>

        <!-- Previous Feedback Section -->
        <div id="previousFeedback" class="section">
            <h2>Previous Resumes Feedback</h2>
            <table>
                <thead>
                    <tr>
                        <th>Username</th>
                        <th>Date</th>
                        <th>Feedback</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {% for feedback in feedback_list %}
                    <tr>
                        <td>{{ feedback.username }}</td>
                        <td>{{ feedback.date }}</td>
                        <td>{{ feedback.feedback_text.suggestions | join('; ') }}</td>
                        <td>
                            <button class="delete-button">Delete</button>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>

    <script>
        function toggleSection() {
            const currentSection = document.getElementById('currentFeedback');
            const previousSection = document.getElementById('previousFeedback');
            const dropdownButton = document.getElementById('dropdownButton');

            if (currentSection.classList.contains('active')) {
                currentSection.classList.remove('active');
                previousSection.classList.add('active');
                dropdownButton.textContent = 'View Current Feedback';
            } else {
                currentSection.classList.add('active');
                previousSection.classList.remove('active');
                dropdownButton.textContent = 'View Previous Feedback';
            }
        }
    </script>
</body>
</html>
