import nlu
import requests 

modelhub_json_url = 'https://nlp.johnsnowlabs.com/models.json'
data = requests.get(modelhub_json_url).json()
list_of_missing_refrenes = []

def NLP_ref_to_NLU_ref(nlp_ref,lang) -> str :
    """Resolve a Spark NLP reference to a NLU reference"""
    nlu_namespaces_to_check = [nlu.Spellbook.pretrained_pipe_references, nlu.Spellbook.pretrained_models_references, nlu.Spellbook.pretrained_healthcare_model_references, nlu.Spellbook.licensed_storage_ref_2_nlu_ref , nlu.Spellbook.storage_ref_2_nlu_ref]
    for dict_ in nlu_namespaces_to_check:
        if lang in dict_.keys():
            for reference in dict_[lang]:
                if dict_[lang][reference] == nlp_ref:
                    return reference

def get_missing_NLP_models() -> list:
    for model in data : 
        if NLP_ref_to_NLU_ref(model['name'],model['language']) == None: 
            list_of_missing_refrenes.append([f"https://nlp.johnsnowlabs.com/{model['url']}"])
            return list_of_missing_refrenes

miss = get_missing_NLP_models()

print(miss, sep='\n')
