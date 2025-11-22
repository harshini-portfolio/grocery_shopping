from flask import Flask, request, render_template, redirect, session, url_for, jsonify
app = Flask(__name__)
app.secret_key = "abc"


app.run(debug=True)
