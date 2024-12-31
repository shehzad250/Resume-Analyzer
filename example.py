<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>User Feedback</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background: linear-gradient(135deg, #6a11cb, #2575fc);
            color: white;
            overflow: hidden;
        }

        .dropdown-container {
            position: fixed;
            top: 0;
            right: 0;
            z-index: 100;
        }

        .dropdown-button {
            background: black;
            color: white;
            padding: 10px 15px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }

        .container {
            display: flex;
            justify-content: center;
            align-items: stretch;
            width: 100%;
            height: 100vh;
            overflow: hidden;
        }

        .section {
            background: #ffffff;
            color: #333;
            border-radius: 0;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
            flex: 1;
            padding: 0;
            height: 100vh;
            overflow-y: auto;
            display: none; /* By default, sections are hidden */
        }

        .section.active {
            display: block; /* Only active section is displayed */
        }

        .section h2 {
            text-align: center;
            margin: 0;
            position: sticky;
            top: 0;
            background: #ffffff;
            padding: 10px;
            z-index: 10;
        }

        .pdf-preview {
            height: 50%;
            border: none;
            width: 100%;
            background: #f0f0f0;
        }

        .feedback-section {
            height: 50%;
            overflow-y: auto;
            padding: 10px;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            text-align: left;
        }

        th, td {
            padding: 8px;
            border: 1px solid #ddd;
        }

        th {
            background: #333;
            color: #fff;
            position: sticky;
            top: 40px;
            z-index: 5;
            text-align: center;
        }

        tr:nth-child(even) {
            background: #f9f9f9;
        }

        tr:nth-child(odd) {
            background: #ffffff;
        }

        .delete-button {
            padding: 8px 12px;
            color: #fff;
            background: #dc3545;
            border: none;
            border-radius: 5px;
            cursor: pointer;
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
            <div>
                <!-- PDF Preview Section -->
                <input type="file" id="pdfInput" accept="application/pdf" style="margin: 10px;">
                <iframe id="pdfPreview" class="pdf-preview"></iframe>

                <!-- Feedback Section -->
                <div class="feedback-section">
                    {% if feedback_list and feedback_list|length > 0 %}
                        <strong>Word Count:</strong> {{ feedback_list[0].feedback_text.word_count }}<br>
                        <strong>Keywords Found:</strong> {{ feedback_list[0].feedback_text.keywords_found | join(', ') }}<br>
                        <div class="suggestions">
                            <strong>Suggestions:</strong>
                            <ul>
                                {% for suggestion in feedback_list[0].feedback_text.suggestions %}
                                <li>{{ suggestion }}</li>
                                {% endfor %}
                            </ul>
                        </div>
                    {% else %}
                        <p>No feedback available for the current resume.</p>
                    {% endif %}
                </div>
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
                    {% for feedback in feedback_list[1:] %}
                    <tr>
                        <td>{{ feedback.username }}</td>
                        <td>{{ feedback.date }}</td>
                        <td>
                            <strong>Word Count:</strong> {{ feedback.feedback_text.word_count }}<br>
                            <strong>Keywords Found:</strong> {{ feedback.feedback_text.keywords_found | join(', ') }}<br>
                            <strong>Suggestions:</strong> {{ feedback.feedback_text.suggestions | join('; ') }}
                        </td>
                        <td>
                            <form action="{{ url_for('delete_feedback') }}" method="POST">
                                <input type="hidden" name="username" value="{{ feedback.username }}">
                                <input type="hidden" name="date" value="{{ feedback.date }}">
                                <button type="submit" class="delete-button">Delete</button>
                            </form>
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

        const pdfInput = document.getElementById('pdfInput');
        const pdfPreview = document.getElementById('pdfPreview');

        pdfInput.addEventListener('change', (event) => {
            const file = event.target.files[0];
            if (file) {
                const fileURL = URL.createObjectURL(file);
                pdfPreview.src = fileURL;
            }
        });
    </script>
</body>
</html>