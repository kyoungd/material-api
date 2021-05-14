from flask import Flask, request, jsonify, abort
from flask_restful import Api, Resource
from transformers import pipeline
from db import get_study
from thinkscript import support_resistance_script, overnight_gapper_script
import logging
from yf_statistics import yf_vitals
from datetime import datetime

app = Flask(__name__)
api = Api(app)


class TextSummary(Resource):

    # /<string:name>/<int:test>
    def get(self):
        return jsonify({"data": request})

    def post(self):
        try:
            summarization = pipeline("summarization")
            data = request.json
            original_text = data["dataset"]
            summary_text = summarization(original_text)[0]['summary_text']
            return jsonify({"result": summary_text})
        except:
            logging.exception()
            abort(500)


class StudySR(Resource):
    def post(self):
        try:
            data = request.json
            symbol = data["symbol"]
            period = data["period"]
            result = get_study("SR", symbol, period)
            return jsonify({"result": result})
        except:
            logging.exception()
            abort(500)


class StudyOG(Resource):
    def post(self):
        try:
            data = request.json
            symbol = data["symbol"]
            result = get_study("OG", symbol, "1d")
            return jsonify({"result": result})
        except:
            logging.exception()
            abort(500)


class ThinkScriptSR(Resource):
    def post(self):
        try:
            data = request.json
            data_list = data["result"]
            result = support_resistance_script(data_list)
            return jsonify({"result": result})
        except:
            logging.exception()
            abort(500)


class ThinkScriptOG(Resource):
    def post(self):
        try:
            data = request.json
            data_list = data["result"]
            result = overnight_gapper_script(data_list)
            return jsonify({"result": result})
        except:
            logging.exception()
            abort(500)


class Vitals(Resource):
    def post(self):
        try:
            data = request.json
            one_date = datetime.today()
            result = yf_vitals(data['symbol'], one_date)
            return result
        except:
            logging.exception()
            abort(500)


api.add_resource(TextSummary, "/summary")
api.add_resource(StudySR, "/study/sr")
api.add_resource(StudyOG, "/study/gf")
api.add_resource(ThinkScriptSR, "/thinkscript/sr")
api.add_resource(ThinkScriptOG, "/thinkscript/gf")
api.add_resource(Vitals, "/vitals")


if __name__ == "__main__":
    app.run(debug=True)
