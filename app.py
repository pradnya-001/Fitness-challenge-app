from flask import Flask, request, render_template, redirect, url_for
import matplotlib.pyplot as plt

app = Flask(__name__)

# Function to generate the graph based on user data
def generate_graph(height, weight, calories_burned, bmi):
    # Plotting the graph
    labels = ['Height', 'Weight', 'Calories Burned', 'BMI']
    values = [height, weight, calories_burned, bmi]

    plt.bar(labels, values, color=['blue', 'green', 'orange', 'red'])
    plt.xlabel('Metrics')
    plt.ylabel('Values')
    plt.title('User Metrics')

    # Save the plot to a file
    graph_path = 'static/graph.png'
    plt.savefig(graph_path)

    return graph_path

# Calculate BMI function
def calculate_bmi(height, weight):
    # Convert height from cm to meters
    height_meters = height / 100.0
    # Calculate BMI
    bmi = weight / (height_meters ** 2)
    return bmi

# Function to suggest challenge and health tips based on BMI
def suggest_challenge_and_tips(bmi):
    suggestion = ""
    tips = ""
    if bmi < 18.5:
        suggestion = "Your BMI indicates that you are underweight. Consider a challenge to gain healthy weight."
        tips = "Consume a balanced diet rich in proteins and healthy fats. Include strength training exercises in your routine to build muscle mass."
    elif 18.5 <= bmi < 25:
        suggestion = "Your BMI falls within the normal range. Maintain your current weight with a balanced lifestyle."
        tips = "Continue with your healthy habits. Regular exercise and a balanced diet are key to maintaining your weight."
    elif 25 <= bmi < 30:
        suggestion = "Your BMI indicates that you are overweight. Consider a challenge to lose weight and improve your health."
        tips = "Focus on portion control and choose nutrient-rich foods. Incorporate aerobic exercises like walking, jogging, or swimming into your routine."
    else:
        suggestion = "Your BMI indicates that you are obese. It's important to take steps to improve your health."
        tips = "Seek guidance from a healthcare professional to create a personalized weight loss plan. Incorporate regular physical activity and make dietary changes to achieve a healthier weight."

    return suggestion, tips

# Routes
@app.route('/', methods=['GET', 'POST']) 
def home():
    if request.method == 'POST':
        if request.form['action'] == 'register':
            return redirect(url_for('user_registration'))
    return render_template('home.html')

@app.route('/user_registration', methods=['GET', 'POST'])
def user_registration():
    if request.method == 'POST':
        # Process the registration form data
        # Assuming the registration is successful
        # Retrieve user details from the form 
        name = request.form['name']
        age = request.form['age']
        weight = float(request.form['weight'])
        height = float(request.form['height'])

        # Calculate BMI
        bmi = calculate_bmi(height, weight)

        # Redirect to create challenge page
        return redirect(url_for('create_challenge', name=name, age=age, weight=weight, height=height, bmi=bmi))
    return render_template('user_registration.html')

@app.route('/create_challenge', methods=['GET', 'POST'])
def create_challenge():
    if request.method == 'POST':
        # Process the create challenge form data
        # Assuming the challenge is created successfully
        return redirect(url_for('track_activity'))
    return render_template('create_challenge.html')

@app.route('/track_activity', methods=['GET', 'POST'])
def track_activity():
    if request.method == 'POST':
        # Process the track activity form data
        # Assuming the activity is tracked successfully
        # For now, let's assume we have these data
        height = float(request.form['height'])
        weight = float(request.form['weight'])
        calories_burned = float(request.form['calories_burned'])

        # Calculate BMI
        bmi = calculate_bmi(height, weight)

        # Generate the graph based on user data
        graph_path = generate_graph(height, weight, calories_burned, bmi)

        # Redirect to the output page with user data
        return redirect(url_for('output', height=height, weight=weight, calories_burned=calories_burned, bmi=bmi, graph_path=graph_path))
    
    return render_template('track_activity.html')

@app.route('/output')
def output():
    # Retrieve user data and graph path from the query parameters
    name = request.args.get('name')
    age = request.args.get('age')
    weight = request.args.get('weight')
    height = request.args.get('height')
    calories_burned = request.args.get('calories_burned')
    bmi = request.args.get('bmi')
    graph_path = request.args.get('graph_path')

    # Get challenge suggestion and health tips based on BMI
    suggestion, tips = suggest_challenge_and_tips(float(bmi))

    # Render the output.html template with user data, graph path, challenge suggestion, and health tips
    return render_template('output.html', name=name, age=age, weight=weight, height=height, calories_burned=calories_burned, bmi=bmi, graph_path=graph_path, suggestion=suggestion, tips=tips)

if __name__ == '__main__':
    app.run(debug=True)
