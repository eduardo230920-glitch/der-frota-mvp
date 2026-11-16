from datetime import date
from functools import wraps
import os
import secrets
import sqlite3

from flask import (
    Flask, abort, flash, g, redirect, render_template, request,
    session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.path.join(BASE_DIR, "der_frota.db")

app = Flask(__name__)
app.config.update(
    SECRET_KEY=os.environ.get("SECRET_KEY", "troque-esta-chave-em-producao"),
    DATABASE=DATABASE,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
)


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


@app.teardown_appcontext
def close_db(_error=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = sqlite3.connect(app.config["DATABASE"])
    db.execute("PRAGMA foreign_keys = ON")
    db.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS vehicles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            plate TEXT NOT NULL UNIQUE,
            model TEXT NOT NULL,
            year INTEGER NOT NULL,
            asset_number TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS maintenances (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vehicle_id INTEGER NOT NULL,
            description TEXT NOT NULL,
            request_date TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Pendente'
                CHECK(status IN ('Pendente', 'Em andamento', 'Concluída')),
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(vehicle_id) REFERENCES vehicles(id) ON DELETE RESTRICT
        );
    """)
    user = db.execute("SELECT id FROM users WHERE username = ?", ("servidor.der",)).fetchone()
    if user is None:
        db.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            ("servidor.der", generate_password_hash("Der@12345"))
        )
    db.commit()
    db.close()

init_db()

def csrf_token():
    if "_csrf_token" not in session:
        session["_csrf_token"] = secrets.token_hex(16)
    return session["_csrf_token"]


app.jinja_env.globals["csrf_token"] = csrf_token


@app.before_request
def protect_post_requests():
    if request.method == "POST":
        sent = request.form.get("_csrf_token", "")
        expected = session.get("_csrf_token", "")
        if not sent or not expected or not secrets.compare_digest(sent, expected):
            abort(400, description="Token de segurança inválido. Atualize a página e tente novamente.")


def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if "user_id" not in session:
            return redirect(url_for("login", next=request.path))
        return view(**kwargs)
    return wrapped_view


@app.route("/")
def index():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return redirect(url_for("dashboard"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        user = get_db().execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchone()

        if user and check_password_hash(user["password_hash"], password):
            session.clear()
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            flash("Acesso realizado com sucesso.", "success")
            return redirect(url_for("dashboard"))

        flash("Usuário ou senha inválidos.", "danger")

    return render_template("login.html")


@app.post("/logout")
@login_required
def logout():
    session.clear()
    flash("Você saiu do sistema.", "info")
    return redirect(url_for("login"))


@app.route("/dashboard")
@login_required
def dashboard():
    db = get_db()
    counts = {
        "vehicles": db.execute("SELECT COUNT(*) FROM vehicles").fetchone()[0],
        "total": db.execute("SELECT COUNT(*) FROM maintenances").fetchone()[0],
        "pending": db.execute(
            "SELECT COUNT(*) FROM maintenances WHERE status = 'Pendente'"
        ).fetchone()[0],
        "progress": db.execute(
            "SELECT COUNT(*) FROM maintenances WHERE status = 'Em andamento'"
        ).fetchone()[0],
        "done": db.execute(
            "SELECT COUNT(*) FROM maintenances WHERE status = 'Concluída'"
        ).fetchone()[0],
    }
    recent = db.execute("""
        SELECT m.*, v.plate, v.model
        FROM maintenances m
        JOIN vehicles v ON v.id = m.vehicle_id
        ORDER BY m.id DESC LIMIT 5
    """).fetchall()
    return render_template("dashboard.html", counts=counts, recent=recent)


@app.route("/vehicles")
@login_required
def vehicles():
    term = request.args.get("q", "").strip()
    db = get_db()
    if term:
        pattern = f"%{term}%"
        rows = db.execute("""
            SELECT * FROM vehicles
            WHERE plate LIKE ? OR model LIKE ? OR asset_number LIKE ?
            ORDER BY plate
        """, (pattern, pattern, pattern)).fetchall()
    else:
        rows = db.execute("SELECT * FROM vehicles ORDER BY plate").fetchall()
    return render_template("vehicles.html", vehicles=rows, q=term)


@app.route("/vehicles/new", methods=["GET", "POST"])
@login_required
def new_vehicle():
    if request.method == "POST":
        plate = request.form.get("plate", "").strip().upper()
        model = request.form.get("model", "").strip()
        asset_number = request.form.get("asset_number", "").strip()
        year_raw = request.form.get("year", "").strip()

        errors = []
        if not plate or len(plate) > 10:
            errors.append("Informe uma placa válida (até 10 caracteres).")
        if not model:
            errors.append("Informe o modelo do veículo.")
        if not asset_number:
            errors.append("Informe a identificação patrimonial.")
        try:
            year = int(year_raw)
            if year < 1900 or year > date.today().year + 1:
                raise ValueError
        except ValueError:
            errors.append("Informe um ano válido.")

        if errors:
            for error in errors:
                flash(error, "danger")
            return render_template("vehicle_form.html", vehicle=request.form)

        try:
            get_db().execute("""
                INSERT INTO vehicles (plate, model, year, asset_number)
                VALUES (?, ?, ?, ?)
            """, (plate, model, year, asset_number))
            get_db().commit()
        except sqlite3.IntegrityError:
            flash("Já existe um veículo cadastrado com essa placa.", "danger")
            return render_template("vehicle_form.html", vehicle=request.form)

        flash("Veículo cadastrado com sucesso.", "success")
        return redirect(url_for("vehicles"))

    return render_template("vehicle_form.html", vehicle={})


@app.route("/vehicles/<int:vehicle_id>")
@login_required
def vehicle_detail(vehicle_id):
    db = get_db()
    vehicle = db.execute(
        "SELECT * FROM vehicles WHERE id = ?", (vehicle_id,)
    ).fetchone()
    if vehicle is None:
        abort(404)
    history = db.execute("""
        SELECT * FROM maintenances
        WHERE vehicle_id = ?
        ORDER BY request_date DESC, id DESC
    """, (vehicle_id,)).fetchall()
    return render_template("vehicle_detail.html", vehicle=vehicle, history=history)


@app.route("/maintenances")
@login_required
def maintenances():
    status = request.args.get("status", "").strip()
    term = request.args.get("q", "").strip()
    clauses, params = [], []
    if status in ("Pendente", "Em andamento", "Concluída"):
        clauses.append("m.status = ?")
        params.append(status)
    if term:
        pattern = f"%{term}%"
        clauses.append("(v.plate LIKE ? OR v.model LIKE ? OR m.description LIKE ?)")
        params.extend([pattern, pattern, pattern])

    sql = """
        SELECT m.*, v.plate, v.model
        FROM maintenances m JOIN vehicles v ON v.id = m.vehicle_id
    """
    if clauses:
        sql += " WHERE " + " AND ".join(clauses)
    sql += " ORDER BY m.request_date DESC, m.id DESC"
    rows = get_db().execute(sql, params).fetchall()
    return render_template("maintenances.html", maintenances=rows, status=status, q=term)


@app.route("/maintenances/new", methods=["GET", "POST"])
@login_required
def new_maintenance():
    db = get_db()
    vehicle_rows = db.execute("SELECT * FROM vehicles ORDER BY plate").fetchall()
    if request.method == "POST":
        vehicle_id = request.form.get("vehicle_id", "").strip()
        description = request.form.get("description", "").strip()
        request_date = request.form.get("request_date", "").strip()
        try:
            selected_vehicle = int(vehicle_id)
            exists = db.execute(
                "SELECT id FROM vehicles WHERE id = ?", (selected_vehicle,)
            ).fetchone()
            if not exists:
                raise ValueError
        except ValueError:
            flash("Selecione um veículo cadastrado.", "danger")
            return render_template("maintenance_form.html", vehicles=vehicle_rows, form=request.form)

        try:
            parsed_date = date.fromisoformat(request_date)
            if parsed_date > date.today():
                raise ValueError
        except ValueError:
            flash("Informe uma data válida, que não seja futura.", "danger")
            return render_template("maintenance_form.html", vehicles=vehicle_rows, form=request.form)

        if not description or len(description) > 1000:
            flash("Descreva o problema (máximo de 1.000 caracteres).", "danger")
            return render_template("maintenance_form.html", vehicles=vehicle_rows, form=request.form)

        db.execute("""
            INSERT INTO maintenances (vehicle_id, description, request_date)
            VALUES (?, ?, ?)
        """, (selected_vehicle, description, request_date))
        db.commit()
        flash("Solicitação registrada com sucesso. Situação inicial: Pendente.", "success")
        return redirect(url_for("maintenances"))

    return render_template(
        "maintenance_form.html", vehicles=vehicle_rows,
        form={"request_date": date.today().isoformat()}
    )


@app.post("/maintenances/<int:maintenance_id>/status")
@login_required
def update_status(maintenance_id):
    new_status = request.form.get("status", "")
    allowed = ("Pendente", "Em andamento", "Concluída")
    if new_status not in allowed:
        abort(400, description="Situação informada inválida.")

    db = get_db()
    row = db.execute(
        "SELECT id FROM maintenances WHERE id = ?", (maintenance_id,)
    ).fetchone()
    if row is None:
        abort(404)

    db.execute(
        "UPDATE maintenances SET status = ? WHERE id = ?",
        (new_status, maintenance_id)
    )
    db.commit()
    flash("Situação da solicitação atualizada.", "success")
    return redirect(request.referrer or url_for("maintenances"))


@app.errorhandler(400)
def bad_request(error):
    return render_template("error.html", code=400, message=getattr(error, "description", "Solicitação inválida.")), 400


@app.errorhandler(404)
def not_found(_error):
    return render_template("error.html", code=404, message="O registro ou a página solicitada não foi encontrado."), 404


if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1")