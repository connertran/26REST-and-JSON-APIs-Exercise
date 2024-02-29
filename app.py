from flask import Flask, request, render_template,redirect, jsonify
from models import db, connect_db, Cupcake

app= Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "abc123"

connect_db(app)


@app.route("/")
def show_HTML_page():
    """Render homepage."""
    cupcakes = Cupcake.query.all()

    return render_template("index.html", cupcakes =cupcakes)

@app.route('/api/cupcakes')
def show_all_cupcakes_json():
    """Returns JSON all cupcakes"""
    cupcakes = Cupcake.query.all()
    all_cupcakes = [cupcake.serialize() for cupcake in cupcakes]
    return jsonify(cupcakes = all_cupcakes)

@app.route('/api/cupcakes/<int:cupcakes_id>')
def show_each_cupcakes_json(cupcakes_id):
    """Returns JSON for one cupcake in particular"""
    the_cupcake= Cupcake.query.get_or_404(cupcakes_id)
    cupcake_dict= the_cupcake.serialize()
    return jsonify(cupcake= cupcake_dict)

@app.route('/api/cupcakes', methods=["POST"])
def create_new_cupcake():
    """Creates a new cupcake and returns JSON of the created cupcake"""
    data = request.json
    # my post request looks like this
    # {
    # 		"flavor": "vani",
    # 		"image": "",
    # 		"rating": 4.0,
    # 		"size": "large"
    # }

    cupcake = Cupcake(
        flavor=data['flavor'],
        rating=data['rating'],
        size=data['size'],
        image=data['image'] or None)
    
    db.session.add(cupcake)
    db.session.commit()
    response_json = jsonify(cupcake= cupcake.serialize())
    return (response_json, 201)

@app.route('/api/cupcakes/<int:cupcake_id>', methods = ["PATCH"])
def update_a_cupcake(cupcake_id):
    """update a particular cupcake and responds JSON of the that updated cupcake"""
    the_cupcake = Cupcake.query.get_or_404(cupcake_id)
    the_cupcake.flavor = request.json.get('flavor', the_cupcake.flavor)
    the_cupcake.size = request.json.get('size', the_cupcake.size)
    the_cupcake.rating = request.json.get('rating', the_cupcake.rating)
    the_cupcake.image = request.json.get('image', the_cupcake.image)

    db.session.commit()
    return jsonify(cupcake= the_cupcake.serialize())

@app.route('/api/cupcakes/<int:cupcake_id>',methods = ["DELETE"])
def delete_a_cupcake(cupcake_id):
    """delete a particular cupcake"""
    the_cupcake = Cupcake.query.get_or_404(cupcake_id)
    db.session.delete(the_cupcake)
    db.session.commit()
    return jsonify(message= 'Deleted')

