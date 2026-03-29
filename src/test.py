from flask import Flask, render_template
import folium

app = Flask(__name__)

@app.route("/")
def index():
    # Create a folium map centered on Sydney
    m = folium.Map(location=[-33.8688, 151.2093], zoom_start=12)

    # Add a sample marker
    folium.Marker(
        location=[-33.8688, 151.2093],
        popup="Sydney, Australia",
        tooltip="Click me!",
        icon=folium.Icon(color="blue", icon="info-sign"),
    ).add_to(m)

    # Render the map to an HTML string
    map_html = m._repr_html_()

    return render_template("index.html", map_html=map_html)

if __name__ == "__main__":
    app.run(debug=True)