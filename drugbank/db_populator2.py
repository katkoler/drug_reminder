import os
from bs4 import BeautifulSoup
import sqlalchemy

from models import Drug, FoodInteraction, ExternalIdentifier, db, drug_interaction

def populate_drug_interaction_table(filename):
    with open(filename, encoding="utf-8") as f:
        parser = BeautifulSoup(f.read(), "html.parser")

    drug = parser.find("drug")
    if drug:
        target_drug_id = drug.find("drugbank-id")
        drug_interactions_wrapper = drug.find("drug-interactions")
        if drug_interactions_wrapper:
            drug_interactions = drug_interactions_wrapper.find_all("drug-interaction")
            for drug_int in drug_interactions:
                partner_drug_id = drug_int.find("drugbank-id")
                int_desc = drug_int.find("description")
                try:
                    statement = drug_interaction.insert().values(drug_target_id=target_drug_id.string, drug_partner_id=partner_drug_id.string,
                                description=int_desc.string)
                    db.session.execute(statement)
                    db.session.commit()
                except sqlalchemy.exc.IntegrityError:
                    continue

if __name__ == '__main__':
    for filee in os.listdir("file_example"):
        populate_drug_interaction_table(os.path.join("file_example", filee))
