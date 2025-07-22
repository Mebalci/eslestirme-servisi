from flask import Flask, request, jsonify
from sentence_transformers import SentenceTransformer, util

app = Flask(__name__)
model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2') 

def build_text(data):
    return f"{data['eşya']} {data.get('renk','')} {data.get('marka','')} {data.get('model','')} {data['şehir']} {data['ilçe']} {data['mahalle']} {data.get('açıklama','')} {data.get('konum','')} {data.get('enlem','')} {data.get('boylam','')}"

def alan_skoru(input_data, item):
    skor = 0
    if item["şehir"] != input_data["şehir"]:
        return 0   

    if item["ilçe"] == input_data["ilçe"]:
        skor += 0.2
    if item["mahalle"] == input_data["mahalle"]:
        skor += 0.1
    if item["eşya"] == input_data["eşya"]:
        skor += 0.15
    if item["marka"] == input_data["marka"]:
        skor += 0.14
    if item["model"] == input_data["model"]:
        skor += 0.06
    if item["renk"] == input_data["renk"]:
        skor += 0.05
    return skor  

@app.route("/match", methods=["POST"])
def match_items():
    data = request.get_json()
    input_text = build_text(data["input"])
    input_embedding = model.encode(input_text, convert_to_tensor=True)

    skorlananlar = []
    for item in data["aday"]:
        if item["şehir"] != data["input"]["şehir"]:
            continue  

        item_text = build_text(item)
        item_embedding = model.encode(item_text, convert_to_tensor=True)
        bert_skor = util.cos_sim(input_embedding, item_embedding).item()   

        alan_skor = alan_skoru(data["input"], item)   

        toplam_skor = round(alan_skor + (bert_skor * 0.3), 3)   
        
        skorlananlar.append({
            "id": item.get("id"),   
            "eşya": item["eşya"],
            "açıklama": item["açıklama"],
            "konum": item["konum"],
            "bert_skor": round(bert_skor, 3),
            "toplam_skor": toplam_skor
        })
     
    skorlananlar.sort(key=lambda x: x["toplam_skor"], reverse=True)
    return jsonify(skorlananlar[:5])

if __name__ == "__main__":
    app.run(debug=True, port=5000)
