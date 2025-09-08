from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contatos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicialização do SQLAlchemy com a aplicação Flask.
db = SQLAlchemy(app)

class Contato(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(40), nullable=False)
    telefone = db.Column(db.String(20), nullable=True)

    def __repr__(self):
        return f'Contato {self.nome}'
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'telefone': self.telefone
        }
    

with app.app_context():
    db.create_all()

#Rotas da API

@app.route('/contatos', methods=['GET', 'POST'])
def handle_contatos():
    if request.method == 'GET':
        contatos = Contato.query.all()
        return jsonify([contato.to_dict() for contato in contatos])
    
    elif request.method == 'POST':
        data = request.get_json()

        #validação
        if not data or 'nome' not in data:
            return jsonify({'message': 'Nome do contato é obrigatório!'}), 400
        
        novo_contato = Contato(nome=data['nome'], telefone=data.get('telefone'))

         # Adiciona o novo contato à sessão do banco de dados.
        db.session.add(novo_contato)

        # Salva as alterações no banco de dados.
        db.session.commit()

        return jsonify(novo_contato.to_dict()), 201 


@app.route('/contatos/<int:contato_id>', methods=['DELETE'])
def delete_contato(contato_id):
    contato = Contato.query.get_or_404(contato_id)

    db.session.delete(contato)
    db.session.commit()

    return "", 204


if __name__ == "__main__":
    app.run(debug=True)

    