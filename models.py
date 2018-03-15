import os
from datetime import datetime, timedelta
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DB_PATH")
db = SQLAlchemy(app)

class Drug(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    toxicity = db.Column(db.Text)
    group = db.Column(db.String(100))
    food_interactions = db.relationship("FoodInteraction", backref="drug")
    external_identifiers = db.relationship("ExternalIdentifier", backref="drug")

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

class TextMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(15))
    drug_name = db.Column(db.String(150))
    message = db.Column(db.Text)

@app.route("/api/drugs")
def get_all_drugs():
    drugs = Drug.query.all()
    return jsonify({"drugs": [drug.name for drug in drugs]})

def add_text_message(values):
    first_name = values.get("firstname")
    last_name = values.get("lastname")
    phone_number = values.get("phone")
    drug_name = values.get("drug-name")
    total_num_tablets = int(values.get("tablets"))
    dosage = int(values.get("dosage"))
    interval = int(values.get("hour"))

    drug_obj = Drug.query.filter_by(name=drug_name).first()

    food_interactions_txt = ", ".join([fi.description for fi in drug_obj.food_interactions])

    di_stmt = drug_interaction.select(whereclause=f"drug_target_id='{drug_obj.id}'")
    results = db.session.execute(di_stmt)
    partner_drugs = []
    for row in results:
        d = Drug.query.filter_by(id=row[1]).first()
        if d:
            partner_drugs.append(d)
    partner_drug_names = ", ".join([drug.name for drug in partner_drugs])


    first_message = """
    Hi {name}, we will reminding you to take {drug_name}. Here's what you should be careful with:
      drug interactions: {drug_interactions}
      food interactions: {food_interactions}
      toxicity: {toxicity}

    We are aware this is very technical. If you have any questions, please consult your doctor.
    """

    general_message = "Hi {name}, don't forget to take {drug_name}"

    last_message = """
    Hi {name}, don't forget to take the last {drug_name}. If you want to use this service again, visit {link}.
    """

    now = datetime.now()
    for count in range(total_num_tablets // dosage):
        if count == 0:
            t = TextMessage(date=now, first_name=first_name, last_name=last_name,
                phone_number=phone_number, drug_name=drug_name,
                message=first_message.format(name=first_name, drug_name=drug_name,
                                             drug_interactions=partner_drug_names,
                                             food_interactions=food_interactions_txt,
                                             toxicity=drug_obj.toxicity))
        elif count == (total_num_tablets // dosage - 1):
            t = TextMessage(date=now + timedelta(minutes=interval * count), first_name=first_name, last_name=last_name,
                            phone_number=phone_number, drug_name=drug_name,
                            message=last_message.format(name=first_name, drug_name=drug_name,
                                                        link="http://drug-reminder.com"))
        else:
            t = TextMessage(date=now + timedelta(minutes=interval * count), first_name=first_name, last_name=last_name,
                            phone_number=phone_number, drug_name=drug_name,
                            message=general_message.format(name=first_name, drug_name=drug_name))
        
        db.session.add(t)
        db.session.commit()

def get_text_messages():
    text_messages = TextMessage.query.all()
    return text_messages

def delete_message(date):
    msg = TextMessage.query.filter_by(date=date).first()
    if msg:
        db.session.delete(msg)
        db.session.commit()

if __name__ == '__main__':
    db.create_all()
    # di = drug_interaction.select(whereclause="drug_target_id='DB00063'")
    # result = db.session.execute(di)
    # for row in result:
    #     print(row)
