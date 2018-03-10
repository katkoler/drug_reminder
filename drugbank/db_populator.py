import os
from bs4 import BeautifulSoup

from models import Drug, FoodInteraction, ExternalIdentifier, db

def get_desired_data(filename):
    with open(filename, encoding="utf-8") as f:
        parser = BeautifulSoup(f.read(), "html.parser")

    drug = parser.find("drug")
    if drug:
        id = drug.find("drugbank-id")

        # Gradaully setting Drug db object...
        new_drug = Drug(id=(id.string or ""))
        
        name = drug.find("name")
        # setting up drug db object
        new_drug.name = name.string or ""

        groups_wrapper = drug.find("groups")
        if groups_wrapper is not None:
            groups = groups_wrapper.find_all("group")
            gp_str = ""
            for group in groups:
                gp_str += (group.string or "")
                # setting up drug db object
                new_drug.group = gp_str
        
        toxicity = drug.find("toxicity")
        if toxicity:
            # setting up drug db object
            new_drug.toxicity = (toxicity.string or "")
            db.session.add(new_drug)
        
        external_identifiers_wr = drug.find("external-identifiers")
        if external_identifiers_wr:
            external_identifiers = external_identifiers_wr.find_all("external-identifier")
            for ext_id in external_identifiers:
                resource = (ext_id.find("resource").string or "")
                identifier = (ext_id.find("identifier").string or "")
                # setting up ExternalIdentifier db object
                new_external_identifier = ExternalIdentifier(resource=resource, name=identifier, drug_id=new_drug.id)
                db.session.add(new_external_identifier)

        food_interactions_wrapper = drug.find("food-interactions")
        if food_interactions_wrapper:
            food_interactions = food_interactions_wrapper.find_all("food-interaction")
            for food_int in food_interactions:
                food_interaction_description = (food_int.string or "")
                # Setting up FoodInteraction db object
                new_food_interaction = FoodInteraction(drug_id=new_drug.id, description=food_interaction_description)
                db.session.add(new_food_interaction)
        
        # Commit all changes to DB!
        db.session.commit()

        # drug_interactions_wrapper = drug.find("drug-interactions")
        # if drug_interactions_wrapper:
        #     drug_interactions = drug_interactions_wrapper.find_all("drug-interaction")



if __name__ == '__main__':
    # get_desired_data("file_example/line13807858")
    # print()
    # get_desired_data("file_example/line13809100")
    # print()
    # get_desired_data("file_example/line13810610")
    # print()
    for filee in os.listdir("file_example"):
        get_desired_data(os.path.join("file_example", filee))
