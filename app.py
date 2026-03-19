from flask import Flask,request,jsonify
from assistant import process_input
app = Flask(__name__)

@app.route("/UK_english_corrector",methods = ["POST"])

def process():
    try:
        data = request.get_json()
        user_input = data.get("text","")
        mode = data.get("mode","grammar and spelling correction")

        if not user_input:
            return jsonify({"error":"No input text is provided!"})
        
        result = process_input(user_input,mode=mode)
        return jsonify({
            "input":user_input,
            "mode":mode,
            "result":result
        })
    except Exception as e:
        return jsonify({"error":str(e)})
    

if __name__ == "__main__":
    app.run(debug=True)