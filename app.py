from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from models import db, Hero, Power, HeroPower

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/')
def home():
    return 'Superheroes API'

# GET /heroes
@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    heroes_data = [{"id": hero.id, "name": hero.name, "super_name": hero.super_name} for hero in heroes]
    return jsonify(heroes_data)

# GET /heroes/:id
@app.route('/heroes/<int:id>', methods=['GET'])
def get_hero(id):
    hero = Hero.query.get(id)
    if not hero:
        return jsonify({"error": "Hero not found"}), 404
    
    hero_powers = HeroPower.query.filter_by(hero_id=id).all()
    hero_powers_data = []
    for hp in hero_powers:
        power = Power.query.get(hp.power_id)
        hero_powers_data.append({
            "id": hp.id,
            "hero_id": hp.hero_id,
            "power_id": hp.power_id,
            "strength": hp.strength,
            "power": {
                "id": power.id,
                "name": power.name,
                "description": power.description
            }
        })
    
    hero_data = {
        "id": hero.id,
        "name": hero.name,
        "super_name": hero.super_name,
        "hero_powers": hero_powers_data
    }
    return jsonify(hero_data)

# GET /powers
@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    powers_data = [{"id": power.id, "name": power.name, "description": power.description} for power in powers]
    return jsonify(powers_data)

# GET /powers/:id
@app.route('/powers/<int:id>', methods=['GET'])
def get_power(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({"error": "Power not found"}), 404
    return jsonify({"id": power.id, "name": power.name, "description": power.description})

# PATCH /powers/:id
@app.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({"error": "Power not found"}), 404
    
    data = request.get_json()
    description = data.get('description')
    
    if not description or len(description) < 20:
        return jsonify({"errors": ["Description must be present and at least 20 characters long"]}), 400
    
    power.description = description
    db.session.commit()
    
    return jsonify({
        "id": power.id,
        "name": power.name,
        "description": power.description
    })

# POST /hero_powers
@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json()
    strength = data.get('strength')
    power_id = data.get('power_id')
    hero_id = data.get('hero_id')
    
    valid_strengths = ['Strong', 'Weak', 'Average']
    if strength not in valid_strengths:
        return jsonify({"errors": ["Strength must be one of: 'Strong', 'Weak', 'Average'"]}), 400
    
    hero = Hero.query.get(hero_id)
    power = Power.query.get(power_id)
    
    if not hero or not power:
        return jsonify({"errors": ["Hero or Power not found"]}), 404
    
    hero_power = HeroPower(strength=strength, hero_id=hero_id, power_id=power_id)
    db.session.add(hero_power)
    db.session.commit()
    
    return jsonify({
        "id": hero_power.id,
        "hero_id": hero_power.hero_id,
        "power_id": hero_power.power_id,
        "strength": hero_power.strength,
        "hero": {
            "id": hero.id,
            "name": hero.name,
            "super_name": hero.super_name
        },
        "power": {
            "id": power.id,
            "name": power.name,
            "description": power.description
        }
    }), 201

if __name__ == '__main__':
    app.run(port=5555, debug=True)