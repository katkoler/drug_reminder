# Drug:
#   id
#   Name
#   ExternalIdentifiers
#   food interactions
#   drug interactions
#   toxicity

# ExternalIdentifier
#   id
#   drug-id
#   name
#   resource

# Food Interactions
#   id
#   drug-id
#   description
#

# Drug interactions (drug interaction partners)
#  id
#  drug-target-id
#  drug-partner-id
#  description

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\Users\\me1kv\\Desktop\\drug_reminder\\drugbank\\drugs.db'
db = SQLAlchemy(app)

class Drug(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    toxicity = db.Column(db.Text)
    group = db.Column(db.String(100))
    food_interactions = db.relationship("FoodInteraction", backref="drug")

class FoodInteraction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    drug_id = db.Column(db.Integer, db.ForeignKey("drug.id"), nullable=False)
    description = db.Column(db.Text)

class ExternalIdentifier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    drug_id = db.Column(db.Integer, db.ForeignKey("drug.id"), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    resource = db.Column(db.String(150), nullable=False)

drug_interaction = db.Table("drug_interaction",
    db.Column("drug_target_id", db.Integer, db.ForeignKey("drug.id"), primary_key=True),
    db.Column("drug_partner_id", db.Integer, db.ForeignKey("drug.id"), primary_key=True),
    db.Column("description", db.Text)
)
