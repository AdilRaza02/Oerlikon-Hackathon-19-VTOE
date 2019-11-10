import calendar
import datetime
import json
from random import randrange
import random, string
import time

import firebase_admin
from firebase_admin import credentials, firestore

BUCKET_ROWS = 9
BUCKET_COLS = 10
BUCKET_STACKS = 3

PIPE_ITEMS = 9
CYLINDER_PIPES = 10
ROTATOR_CYLINDER = 9

MAX_STACK = 12
MAX_ROTATOR = 4

STACK_POSITIONS = ["low", "mid", "high"]
PIPE_POSITIONS = ["low", "mid", "high"]

STAGES_NAME = ["Goods receipt", "Laying-up", "Cleaning", "Batch loading", "Coating", "Post-treatment", "Testing", "Packaging"]

cred = credentials.Certificate("./serviceAccountKey.json")
default_app = firebase_admin.initialize_app(cred)
db = firestore.client()

def setDocument(documentId, documentData):
	doc_ref = db.collection('StaticData').document(documentId)
	doc_ref.set(documentData)

def getDocument(documentId):
	try:
		doc_ref = db.collection('StaticData').document(documentId).get()
	except Exception as e:
		doc_ref = None

	return doc_ref.to_dict()

def generateData(partType = "screw", numParts = 1000, defectRate = 0.5, considerDefect = True):
	stackCapacity = BUCKET_STACKS * BUCKET_ROWS * BUCKET_COLS
	bucketCapacity = BUCKET_ROWS * BUCKET_COLS
	numStacks = int((numParts + stackCapacity - 1) / stackCapacity)

	rotatorCapacity = PIPE_ITEMS * CYLINDER_PIPES * ROTATOR_CYLINDER
	cylinderCapacity = PIPE_ITEMS * CYLINDER_PIPES

	defectCount = 0
	allIds = set()

	ts = calendar.timegm(time.gmtime()) + 3600

	for _part in range(numParts):
		if _part % 30 == 0:
			print(_part)

		# Indexing for Laying Up
		stack_num = int(_part / stackCapacity)
		bucket_num = int(_part / bucketCapacity) % BUCKET_STACKS
		bucket_row_index = int(_part / BUCKET_COLS) % BUCKET_ROWS
		bucket_col_index = int(_part % BUCKET_COLS)
		_stack_pos = STACK_POSITIONS[bucket_num]

		batch_num = int(stack_num / MAX_STACK)
		stack_num = stack_num % MAX_STACK

		# print(stack_num, bucket_num, bucket_row_index, bucket_col_index, _stack_pos)
		laying_str = "Batch " + str(batch_num) + ", " + "Stack " + str(stack_num) + ", " + "Bucket " + str(bucket_num) + ", " + "Row " + str(bucket_row_index) + ", " + "Column " + str(bucket_col_index)

		# Indexing for Coating
		rotator_num = int(_part / rotatorCapacity)
		cylinder_num = int(_part / cylinderCapacity) % ROTATOR_CYLINDER
		pipe_num = int(_part / PIPE_ITEMS) % CYLINDER_PIPES
		pipe_position = int(_part % PIPE_ITEMS)
		_pipe_pos = PIPE_POSITIONS[int(pipe_position / 3)]

		rotator_num = rotator_num % MAX_ROTATOR

		# print(rotator_num, cylinder_num, pipe_num, pipe_position, _pipe_pos)
		coating_str = "Batch " + str(batch_num) + ", " + "Rotator " + str(rotator_num) + ", " + "Cylinder " + str(cylinder_num) + ", " + "Pipe " + str(pipe_num) + ", " + "Height " + str(pipe_position)

		# print(laying_str)
		# print(coating_str)


		full_index = laying_str + "__" + coating_str
		full_position = _stack_pos + "__" + _pipe_pos

		defective = False
		if considerDefect:
			defective = randrange(int(100 / defectRate)) == 0
			if defective: defectCount += 1

		batch_timestamp = ts + batch_num * 3 * 60 * 60 + stack_num * 10 * 60	# 90 Minutes , 6 Minutes

		partJson = {
			"partType": partType,
			"defective": defective,
			"full_index": full_index,
			"full_position": full_position,
			"batch_num": batch_num,
			"timestamp": batch_timestamp,
			"partNum": _part,
			"stages": []
		}

		stageNum = 0

		for _stage in STAGES_NAME:
			_stage_json = {
				"stageNum": stageNum,
				"stageName": _stage,
				"timestamp": batch_timestamp + stageNum * 3 * 60,
				"index": _part,
				"position": None
			}

			if stageNum in (1, 2):
				_stage_json["index"] = laying_str
				_stage_json["position"] = _stack_pos

			if stageNum in (3, 4):
				_stage_json["index"] = coating_str
				_stage_json["position"] = _pipe_pos

			partJson["stages"].append(_stage_json)
			stageNum += 1

		docId = "Unit" + str(_part + 1)
		setDocument(docId, partJson)

	print("Defect Count", defectCount)

def fetchData(docId = "Unit101"):
	docData = getDocument(docId)
	return docData

def fetchBulkData(bulkid = 0):
	try:
		start_idx = 50 * bulkid
		end_idx = start_idx + 50

		data_stream = db.collection('StaticData').where('partNum', '>=', start_idx).where('partNum', '<', end_idx).stream()
		result = []

		for ds in data_stream:
			ds_id = ds.id
			ds_dict = ds.to_dict()

			tmp_dict = {
				"partType": ds_dict["partType"],
				"defective": ds_dict["defective"],
				"full_index": ds_dict["full_index"],
				"full_position": ds_dict["full_position"],
				"batch_num": ds_dict["batch_num"],
				"timestamp": ds_dict["timestamp"],
				"partNum": ds_dict["partNum"],
				"unitid": ds_id
			}
			result.append(tmp_dict)

		return result
	except:
		return None

def getChartData():
	try:
		res = db.collection("Stats").document("chartData").get().to_dict()
		return res
	except:
		return None

# if False:
	# fetchData()

	# t1 = time.time()
	# generateData("screw", 10000, 1.2, True)
	# t2 = time.time()
	# print(t2 - t1)


# --------- Flask Code begins --------- #

#!flask/bin/python
from flask import abort, Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello World!"

@app.route('/getUnitData', methods = ['GET'])
def lifecycleData():
	try:
		tmp = dict(request.args)
		unitid = str(tmp['unitid'])
		unitdata = fetchData(unitid)

		if unitdata != None:
			result = jsonify({
				'result': unitdata,
				'success': True,
				'message': 'ok'
			})

		else:
			result = jsonify({
				'result': unitdata,
				'success': False,
				'message': 'No document found in DB'
			})

	except Exception as e:

		result = jsonify({
			'result': None,
			'success': False,
			'message': "*Error : " + str(e)
		})

	result.headers.add('Access-Control-Allow-Origin', '*')
	return result

@app.route('/getBulkData', methods = ['GET'])
def summarizeBulkData():
	try:
		tmp = dict(request.args)
		bulkid = int(tmp['bulkid'])
		bulkdata = fetchBulkData(bulkid)

		if bulkdata != None:
			result = jsonify({
				'result': bulkdata,
				'success': True,
				'message': 'ok'
			})

		else:
			result = jsonify({
				'result': bulkdata,
				'success': False,
				'message': 'No document found in DB'
			})

	except Exception as e:

		result = jsonify({
			'result': None,
			'success': False,
			'message': "*Error : " + str(e)
		})

	result.headers.add('Access-Control-Allow-Origin', '*')
	return result

@app.route('/getGraphData', methods = ['GET'])
def extractGraphData():
	try:
		res = getChartData()

		if res != None:
			result = jsonify({
				'result': res,
				'success': True,
				'message': 'ok'
			})

		else:
			result = jsonify({
				'result': res,
				'success': False,
				'message': 'No document found in DB'
			})

	except Exception as e:

		result = jsonify({
			'result': None,
			'success': False,
			'message': "*Error : " + str(e)
		})

	result.headers.add('Access-Control-Allow-Origin', '*')
	return result


if __name__ == '__main__':
    app.run(host = '127.0.0.1', port = 8080, debug = True)
