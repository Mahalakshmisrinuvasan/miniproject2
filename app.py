from flask import Flask, render_template, request, send_file
import pandas as pd


app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/search", methods=["POST"])

def search():
    query = request.form.get("query", "").lower()
    sort = request.form.get("sort", "")
    
    
    df = pd.read_csv("results.csv")
    
    if query:
        df = df[df["name"].str.lower().str.contains(query)]
    def get_category(name):
        if any(x in name.lower() for x in ["iphone", "samsung", "oneplus", "redmi", "mobile"]): return "Mobiles"
        if any(x in name.lower() for x in ["laptop", "macbook", "dell", "lenovo", "asus", "hp"]): return "Laptops"
        if any(x in name.lower() for x in ["airdopes", "headphone", "earphone", "buds", "jbl", "sony"]): return "Headphones"
        if any(x in name.lower() for x in ["watch", "fit", "ninja", "galaxy watch"]): return "Smartwatches"
        if any(x in name.lower() for x in ["fridge", "washing", "ac", "appliance", "mixer", "fryer"]): return "Appliances"
        if any(x in name.lower() for x in ["shoe", "nike", "adidas", "puma", "reebok", "skechers"]): return "Shoes"
        return "Others"

    df["category"] = df["name"].apply(get_category)
    if sort == "price_asc":
        df = df.sort_values(by="price", ascending=True)
    elif sort == "price_desc":
        df = df.sort_values(by="price", ascending=False)
    elif sort == "rating_desc":
        df = df.sort_values(by="rating", ascending=False)

    products = df.to_dict(orient="records")
    return render_template("result.html", products=products, query=query)

@app.route("/download")
def download():
    return send_file("results.csv", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
