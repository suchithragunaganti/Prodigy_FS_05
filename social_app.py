
from flask import Flask, render_template_string, request, redirect, url_for
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'  # Folder to store images
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}  # Allowed file types

# In-memory data to store posts
posts = []

# Template for homepage and posting
home_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Mini Social Media</title>
    <style>
        body { font-family: Arial; background: #f4f4f4; padding: 20px; }
        .post { background: white; padding: 15px; margin: 10px 0; border-radius: 5px; }
        .post img { max-width: 100%; border-radius: 5px; }
        form { margin-bottom: 20px; }
        .like-btn, .comment-btn { color: #007BFF; cursor: pointer; }
    </style>
</head>
<body>
    <h2>Welcome to Mini Social Media</h2>
    <form method="post" enctype="multipart/form-data">
        <input name="user" placeholder="Your name" required><br><br>
        <textarea name="text" placeholder="What's on your mind?" rows="3" cols="50" required></textarea><br><br>
        <input type="file" name="image"><br><br>
        <button type="submit">Post</button>
    </form>

    {% for post in posts %}
    <div class="post">
        <strong>{{ post.user }}</strong><br>
        <p>{{ post.text }}</p>
        {% if post.image %}
        <img src="{{ post.image }}" alt="Post image"><br>
        {% endif %}
        <p><span class="like-btn">❤️ {{ post.likes }} Likes</span></p>
        <form method="post" action="/comment/{{ loop.index0 }}">
            <input name="comment" placeholder="Write a comment..." required>
            <button class="comment-btn">Comment</button>
        </form>
        <ul>
            {% for comment in post.comments %}
                <li>{{ comment }}</li>
            {% endfor %}
        </ul>
    </div>
    {% endfor %}
</body>
</html>
"""

# Function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        user = request.form['user']
        text = request.form['text']
        image = request.files.get('image')
        image_path = None

        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            image.save(image_path)
            image_path = '/static/uploads/' + filename  # Path for Flask to serve the image
        
        posts.append({
            'user': user,
            'text': text,
            'image': image_path,
            'likes': 0,
            'comments': []
        })
        return redirect(url_for('home'))
    
    return render_template_string(home_template, posts=posts)

@app.route('/comment/<int:post_id>', methods=['POST'])
def comment(post_id):
    comment_text = request.form['comment']
    posts[post_id]['comments'].append(comment_text)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
