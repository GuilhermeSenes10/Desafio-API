from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)

def buscar_dados_receita_federal(cnpj):
    url = f'https://receitaws.com.br/v1/cnpj/{cnpj}'
    response = requests.get(url)
    dados = response.json()
    if response.status_code == 200 and dados['status'] == 'success':
        return dados['data']
    return None

@app.route('/empresas', methods=['POST'])
def criar_empresa():
    cnpj = request.json['cnpj']
    if not cnpj_br.is_valid(cnpj):
        return jsonify({'erro': 'CNPJ inválido'}), 400

    dados_receita = buscar_dados_receita_federal(cnpj)
    if not dados_receita:
        return jsonify({'erro': 'CNPJ inválido'}), 400

    empresa = Empresa(
        cnpj=dados_receita['cnpj'],
        situacao=dados_receita['situacao'],
        tipo=dados_receita['tipo'],
        razao_social=dados_receita['nome'],
        nome_fantasia=dados_receita['fantasia_nome'],
        estado=dados_receita['uf'],
        municipio=dados_receita['municipio'],
        endereco=dados_receita['logradouro'],
        natureza_juridica=dados_receita['atividade_principal'],
        porte=dados_receita['porte'],
        atividade_principal=dados_receita['atividade_principal'],
        telefone=dados_receita['telefone'],
        numero_funcionarios=dados_receita['quantidade_funcionarios'],
        faturamento_anual_estimado=dados_receita['capital_social'],
        vendedor_responsavel=''
    )

    db.session.add(empresa)
    db.session.commit()

    return jsonify({'mensagem': 'Empresa criada com sucesso'}), 201

@app.route('/empresas', methods=['GET'])
def listar_empresas():
    vendedor_responsavel = request.args.get('vendedor_responsavel')

    if vendedor_responsavel:
        empresas = Empresa.query.filter_by(vendedor_responsavel=vendedor_responsavel).all()
    else:
        empresas = Empresa.query.all()

    dados = [
        {
            'cnpj': empresa.cnpj,
            'situacao': empresa.situacao,
            'tipo': empresa.tipo,
            'razao_social': empresa.razao_social,
            'nome_fantasia': empresa.nome_fantasia,
            'estado': empresa.estado,
            'municipio': empresa.municipio,
            'endereco': empresa.endereco,
            'natureza_juridica': empresa.natureza_juridica,
            'porte': empresa.porte,
            'atividade_principal': empresa.atividade_principal,
            'telefone': empresa.telefone,
            'numero_funcionarios': empresa.numero_funcionarios,
            'faturamento_anual_estimado': empresa.faturamento_anual_estimado,
            'vendedor_responsavel': empresa.vendedor_responsavel
       }
        for empresa in empresas
    ]

    return jsonify(dados)

@app.route('/empresas/<int:empresa_id>', methods=['PUT'])
def atualizar_empresa(empresa_id):
    empresa = Empresa.query.get_or_404(empresa_id)

    empresa.vendedor_responsavel = request.json['vendedor_responsavel']
    empresa.numero_funcionarios = request.json['numero_funcionarios']
    empresa.faturamento_anual_estimado = request.json['faturamento_anual_estimado']

    db.session.commit()

    return jsonify({'mensagem': 'Empresa atualizada com sucesso'})

if __name__ == '__main__':
    app.run(debug=True)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///empresas.db'
    db = SQLAlchemy(app)
    db.create_all()

class Empresa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cnpj = db.Column(db.String(14), unique=True)
    situacao = db.Column(db.String(10))
    tipo = db.Column(db.String(10))
    razao_social = db.Column(db.String(100))
    nome_fantasia = db.Column(db.String(100))
    estado = db.Column(db.String(2))
    municipio = db.Column(db.String(50))
    endereco = db.Column(db.String(100))
    natureza_juridica = db.Column(db.String(50))
    porte = db.Column(db.String(10))
    atividade_principal = db.Column(db.String(50))
    telefone = db.Column(db.String(15))
    numero_funcionarios = db.Column(db.Integer)
    faturamento_anual_estimado = db.Column(db.Float)
    vendedor_responsavel = db.Column(db.String(100))

    def __init__(self, cnpj, situacao, tipo, razao_social, nome_fantasia, estado, municipio, endereco, natureza_juridica, porte, atividade_principal, telefone, numero_funcionarios,faturamento_anual_estimado, vendedor_responsavel):
        self.cnpj = cnpj
        self.situacao = situacao
        self.tipo = tipo
        self.razao_social = razao_social
        self.nome_fantasia = nome_fantasia
        self.estado = estado
        self.municipio = municipio
        self.endereco = endereco
        self.natureza_juridica = natureza_juridica
        self.porte = porte
        self.atividade_principal = atividade_principal
        self.telefone = telefone
        self.numero_funcionarios = numero_funcionarios
        self.faturamento_anual_estimado = faturamento_anual_estimado
        self.vendedor_responsavel = vendedor_responsavel