from flask import Flask, request, render_template, redirect, url_for
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

# Function to generate the graph based on user data
def generate_graph(height, weight, calories_burned, bmi):
    # Plotting the graph
    labels = ['Height', 'Weight', 'Calories Burned', 'BMI']
    values = [height, weight, calories_burned, bmi]

    plt.bar(labels, values, color=['blue', 'green', 'orange', 'red'])