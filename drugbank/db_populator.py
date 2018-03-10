import os
from bs4 import BeautifulSoup

def print_desired_data(filename):
    with open(filename, encoding="utf-8") as f:
        parser = BeautifulSoup(f.read(), "html.parser")

    drug = parser.find("drug")
    if drug:
        groups_wrapper = drug.find("groups")
        if groups_wrapper is not None:
            groups = groups_wrapper.find_all("group")
            for group in groups:
                print("Group name: " + (group.string or ""))
        
        toxicity = drug.find("toxicity")
        if toxicity:
            print("Toxicity: " + (toxicity.string or ""))
        
        external_identifiers_wr = drug.find("external-identifiers")
        if external_identifiers_wr:
            external_identifiers = external_identifiers_wr.find_all("external-identifier")
            for ext_id in external_identifiers:
                print("Resource ref: " + (ext_id.find("resource").string or ""))
                print("Synonym: " + (ext_id.find("identifier").string or ""))

        food_interactions_wrapper = drug.find("food-interactions")
        if food_interactions_wrapper:
            food_interactions = food_interactions_wrapper.find_all("food-interaction")
            for food_int in food_interactions:
                print("Food interaction: " + (food_int.string or ""))
        
        # drug_interactions_wrapper = drug.find("drug-interactions")
        # if drug_interactions_wrapper:
        #     drug_interactions = drug_interactions_wrapper.find_all("drug-interaction")


# print_desired_data("file_example/line13807858")
# print()
# print_desired_data("file_example/line13809100")
# print()
# print_desired_data("file_example/line13810610")
# print()
for filee in os.listdir("file_example"):
    print_desired_data(os.path.join("file_example", filee))
