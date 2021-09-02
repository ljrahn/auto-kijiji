from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, abort
from .models import Tracking
from . import db
import json


views = Blueprint('views', __name__)             

@views.route('/', methods=['GET'])
def home_page():
    return render_template('home.html')


@views.route('/find-items', methods=['GET'])
def find_items_page():
    return render_template('find_items.html')
