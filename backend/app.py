from flask import Flask, render_template, request, jsonify, redirect, session
import pickle
import numpy as np

app = Flask(__name__)
app.secret_key = "house_price_secret"

# Load model
model = pickle.load(open("house_model.pkl", "rb"))

location_factor = {
    "Urban": 1.3,
    "Suburban": 1.1,
    "Rural": 0.9
}

# ---------------- LOGIN ----------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["username"] == "admin" and request.form["password"] == "admin123":
            session["user"] = "admin"
            return redirect("/dashboard")
        return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")
    return render_template("index.html")


# ---------------- OTHER PAGES ----------------
@app.route("/charts")
def charts():
    return render_template("charts.html")

@app.route("/model")
def model_page():
    return render_template("model.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")


# ---------------- PREDICTION (FIXED) ----------------
@app.route("/predict", methods=["POST"])
def predict():
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()

    try:
        area = float(data["area"])
        bedrooms = int(data["bedrooms"])
        bathrooms = int(data["bathrooms"])
        parking = int(data["parking"])
        location = data["location"]

        features = np.array([[area, bedrooms, bathrooms, parking]])
        base_price = model.predict(features)[0]
        final_price = base_price * location_factor.get(location, 1)

        return jsonify({
            "price": round(final_price, 2),
            "explanation": {
                "Area": "High",
                "Bedrooms": "Medium",
                "Bathrooms": "Medium",
                "Parking": "Low"
            }
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)
