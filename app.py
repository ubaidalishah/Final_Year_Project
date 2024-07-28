from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import joblib
import numpy as np

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# Load the model
model = joblib.load('models/model.pkl')

# Database models
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Initialize the database
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/exercises')
@login_required
def exercises():
    return render_template('exercises.html')

@app.route('/bicep')
@login_required
def bicep():
    return render_template('bicep.html')

@app.route('/tricep')
@login_required
def tricep():
    return render_template('tricep.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/predictions')
@login_required
def predictions():
    return render_template('predictions.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            login_user(user)
            flash('Login successful!', 'success')
            if user.is_admin:
                return redirect(url_for('dashboard'))
            else:
                return redirect(url_for('exercises'))
        else:
            flash('Login failed. Check your email and password', 'danger')
    return render_template('login.html')

@app.route('/signup', methods=['POST'])
def signup():
    name = request.form.get('name')
    age = request.form.get('age')
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        user = User(name=name, age=age, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully!', 'success')
        return redirect(url_for('login', show_login='true'))
    except Exception as e:
        flash('Email already exists or other error occurred', 'danger')
        return redirect(url_for('login'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out!', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    if not current_user.is_admin:
        flash('Access denied', 'danger')
        return redirect(url_for('exercises'))
    users = User.query.all()
    return render_template('dashboard.html', users=users)

# Route to receive frontend data
@app.route('/frontend_data', methods=['POST'])
def receive_frontend_data():
    global frontend_data
    if request.method == 'POST':
        try:
            frontend_data = request.get_json()
            print("Frontend data received:", frontend_data)
            return jsonify({'status': 'success'}), 200
        except Exception as e:
            print("Error receiving frontend data:", str(e))
            return jsonify({'error': str(e)}), 400

# Route to receive NodeMCU data
@app.route('/node_data', methods=['POST'])
def receive_node_data():
    global node_data
    if request.method == 'POST':
        try:
            node_data = request.get_json()
            print("NodeMCU data received:", node_data)
            return jsonify({'status': 'success'}), 200
        except Exception as e:
            print("Error receiving NodeMCU data:", str(e))
            return jsonify({'error': str(e)}), 400

# Route to make predictions
@app.route('/predict', methods=['POST'])
def predict():
    global frontend_data, node_data
    if request.method == 'POST':
        try:
            if not frontend_data or not node_data:
                print("Incomplete data: frontend_data:", frontend_data, "node_data:", node_data)
                return jsonify({'error': 'Incomplete data'}), 400

            body_weight = frontend_data.get('body_weight')
            muscle = frontend_data.get('muscle')
            weight_lifted = frontend_data.get('weight_lifted')
            exercise = frontend_data.get('exercise')
            emg_180 = node_data.get('emg_180')
            emg_90 = node_data.get('emg_90')
            emg_20 = node_data.get('emg_20')

            print("Prediction input data:", {
                'body_weight': body_weight,
                'muscle': muscle,
                'weight_lifted': weight_lifted,
                'exercise': exercise,
                'emg_180': emg_180,
                'emg_90': emg_90,
                'emg_20': emg_20
            })

            input_data = np.array([
                [body_weight, muscle, weight_lifted, exercise, emg_180, emg_90, emg_20]
            ], dtype=int)

            prediction = model.predict(input_data)
            print("Prediction result:", prediction)

            # Do not clear data here to ensure it remains available for debugging
            node_data = {}
            # frontend_data = {}

            return jsonify({'prediction': prediction.tolist()}), 200
        except Exception as e:
            print("Error making prediction:", str(e))
            return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)











# from flask import Flask, request, jsonify, render_template
# import joblib
# import numpy as np
# from flask_cors import CORS
# app = Flask(__name__)
# CORS(app)

# # Define paths
# model_path = 'models/model.pkl'  # Adjust path as per your model location

# # Load the model
# model = joblib.load(model_path)

# # Temporary storage for data
# frontend_data = {}
# node_data = {}

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/exercises')
# def exercises():
#     return render_template('exercises.html')

# @app.route('/bicep')
# def bicep():
#     return render_template('bicep.html')

# @app.route('/tricep')
# def tricep():
#     return render_template('tricep.html')

# @app.route('/about')
# def about():
#     return render_template('about.html')

# @app.route('/blog')
# def blog():
#     return render_template('blog.html')

# @app.route('/predictions')
# def predictions():
#     return render_template('predictions.html')

# # Route to receive frontend data
# @app.route('/frontend_data', methods=['POST'])
# def receive_frontend_data():
#     global frontend_data
#     if request.method == 'POST':
#         try:
#             # Process data from frontend (JavaScript)
#             frontend_data = request.get_json()
#             return jsonify({'status': 'success'}), 200
#         except Exception as e:
#             return jsonify({'error': str(e)}), 400

# # Route to receive NodeMCU data and make predictions
# @app.route('/predict', methods=['POST'])
# def predict():
#     global node_data, frontend_data
#     if request.method == 'POST':
#         try:
#             # Process data from NodeMCU (ESP8266)
#             node_data = request.get_json()
            
#             # Ensure both frontend and NodeMCU data are available
#             if not frontend_data or not node_data:
#                 return jsonify({'error': 'Incomplete data'}), 400

#             body_weight = frontend_data.get('body_weight')
#             muscle = frontend_data.get('muscle')
#             weight_lifted = frontend_data.get('weight_lifted')
#             exercise = frontend_data.get('exercise')
#             emg_180 = node_data.get(emg_180)
#             emg_90 = node_data.get(emg_90)
#             emg_20 = node_data.get(emg_20)
            
#             # Combine data for prediction
#             input_data = np.array([
#                 [body_weight, muscle, weight_lifted, exercise, emg_180, emg_90, emg_20]
#             ], dtype=float)

#             # Make prediction using the loaded model
#             prediction = model.predict(input_data)

#             # Clear stored data after prediction
        
#             node_data = {}

#             # Return prediction as JSON response
#             return jsonify({'prediction': prediction.tolist()}),200
            
#         except Exception as e:
#             return jsonify({'error': str(e)}), 400

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8080)
