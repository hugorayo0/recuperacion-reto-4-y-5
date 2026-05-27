from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

FICHERO_JSON = "cocineros.json"

# Leo el archivo json con la lista de cocineros, y devuelvo la lista de cocineros
def leer_cocineros():
    with open(FICHERO_JSON, "r", encoding="utf-8") as f:
        cocineros = json.load(f)
    return cocineros

# Guardo la lista en el archivo json de los cocineros
def guardar_cocineros(cocineros):
    with open(FICHERO_JSON, "w", encoding="utf-8") as f:
        json.dump(cocineros, f, ensure_ascii=False, indent=4)

# Página principal - muestra todos los cocineros, con la especialidad y años de experiencia
@app.route("/")
def index():
    cocineros = leer_cocineros()
    return render_template("index.html", cocineros=cocineros)

# Página para añadir un cocinero nuevo
@app.route("/nuevo", methods=["GET", "POST"])
def nuevo_cocinero():
    if request.method == "POST":
        nombre = request.form["nombre"]
        especialidad = request.form["especialidad"]
        experiencia = request.form["experiencia"]

        cocinero = {
            "nombre": nombre,
            "especialidad": especialidad,
            "experiencia": int(experiencia)
        }

        # Añado el nuevo cocinero a la lista y guardo
        cocineros = leer_cocineros()
        cocineros.append(cocinero)
        guardar_cocineros(cocineros)

        return redirect(url_for("index"))

    return render_template("nuevo.html")

# Eliminar un cocinero por su índice
@app.route("/eliminar/<int:id>", methods=["POST"])
def eliminar_cocinero(id):
    cocineros = leer_cocineros()
    if 0 <= id < len(cocineros):
        cocineros.pop(id)
        guardar_cocineros(cocineros)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)