# -*- coding: utf-8 -*-
from flask import Blueprint
from login import login, logout
from add import add, addlink
from create import create, createlink
from vali import vali, getvalicode
from get import get
from tools import getpacket, received
from monitor import monitor, echarts, ad

blueprint = Blueprint('myblueprint', __name__)

blueprint.add_url_rule('/login', view_func=login, methods=['GET', 'POST'])
blueprint.add_url_rule('/logout', view_func=logout, methods=['GET', 'POST'])

blueprint.add_url_rule('/add', view_func=add, methods=['GET'])
blueprint.add_url_rule('/addlink', view_func=addlink, methods=['GET'])

blueprint.add_url_rule('/create', view_func=create, methods=['GET'])
blueprint.add_url_rule('/createlink', view_func=createlink, methods=['GET'])

blueprint.add_url_rule('/vali', view_func=vali, methods=['GET'])
blueprint.add_url_rule('/getvalicode', view_func=getvalicode, methods=['GET'])

blueprint.add_url_rule('/get', view_func=get, methods=['GET'])

blueprint.add_url_rule('/getpacket', view_func=getpacket, methods=['GET'])

blueprint.add_url_rule('/received', view_func=received, methods=['GET'])

blueprint.add_url_rule('/monitor', view_func=monitor, methods=['GET'])
blueprint.add_url_rule('/echarts', view_func=echarts, methods=['GET'])

blueprint.add_url_rule('/ad', view_func=ad, methods=['GET'])
