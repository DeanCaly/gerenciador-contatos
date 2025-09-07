from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contatos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicialização do SQLAlchemy com a aplicação Flask.
db = SQLAlchemy(app)

class Contato(db.model):
    id = db.Column(db.Integer, primary_Key=True)
    nome = db.Column(db.String(20), nullable=False)
    telefone = db.Column(db.Integer, nullable=True)


    def toDict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'fone': self.telefone
        }
    

with app.app_context():
    db.create_all()

#Rotas da API

@app.route('/contatos', methods=["GET", "POST"])

def handle_contatos():
    if request.method == "GET":
        contatos = Contato.query.all()
        return jsonify([contato.toDict() for contato in contatos])
    elif request.method == "POST":
        data = request.get_json()

        #validação
        if not data or not 'nome' in data:
            return jsonify({'message': 'Nome do contato é obrigatório!'}), 400
        
        novo_contato = Contato(nome=data.get('nome'), telefone=data.get('telefone'))

         # Adiciona o novo contato à sessão do banco de dados.
        db.session.add(novo_contato)

        # Salva as alterações no banco de dados.
        db.session.commit()

        return jsonify(novo_contato.toDict())
    

