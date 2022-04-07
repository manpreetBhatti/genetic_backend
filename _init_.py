from flask import Flask
from genetic_architecture import GeneticAlgorithm

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"





if __name__ == "__main__":
    app.run()