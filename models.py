"""Models for REST & JSON APIs"""
from flask_sqlalchemy import SQLAlchemy

default_img= "https://tinyurl.com/demo-cupcake"

db = SQLAlchemy()
def connect_db(app):
    db.app=app
    db.init_app(app)
    app.app_context().push()

class Cupcake(db.Model):
    """This models a cupcake"""

    __tablename__ = "cupcakes"

    id = db.Column(db.Integer,
                   primary_key= True,
                   autoincrement = True)
    flavor = db.Column(db.Text,
                       nullable=False)
    size = db.Column(db.Text,
                     nullable=False)
    rating = db.Column(db.Float,
                       nullable=False)
    image = db.Column(db.Text,
                      nullable= False,
                      default= default_img)
    
    def serialize(self):
        """Returns a dict representation of cupcake which we can turn into JSON"""
        return{
            "id": self.id,
            "flavor": self.flavor,
            "size": self.size,
            "rating": self.rating,
            "image": self.image
        }