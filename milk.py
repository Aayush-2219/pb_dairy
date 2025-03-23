from flask import Blueprint, render_template

milk_bp = Blueprint('milk', __name__)

@milk_bp.route('/milk-info')
def milk_info():
    milk_varieties = [
        {"name": "Kesar Milk", "description": "A rich and aromatic saffron-infused milk, known for its health benefits."},
        {"name": "Strawberry Milk", "description": "A sweet and fruity milk with fresh strawberry flavor, loved by all ages."},
        {"name": "Blue Milk", "description": "A unique blue-colored milk inspired by galactic legends, with a creamy vanilla taste."}
    ]
    
    return render_template('milk_info.html', milk_varieties=milk_varieties)
