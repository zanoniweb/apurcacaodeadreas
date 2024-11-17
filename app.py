# app.py
from flask import Flask, request, jsonify
import pandas as pd
import os

app = Flask(__name__)

# Função para carregar os dados de todas as tabelas
def carregar_dados():
    dados_por_ano = {}
    for ano in range(2020, 2025):
        file_name = f'C:/Users/Usuario/Documents/Acadêmico Juliano Zanoni/Engenharia de Software/Projetos Engenharia/Projetos/Certidão Narrativa Cambé Pr/certpython-protfolio/py/tabela_{ano}.xlsx'
        if os.path.exists(file_name):
            print("entrou no if")
            df = pd.read_excel(file_name)
            print(df)
            dados_por_ano[ano] = df
        else:
            print("nao entrou")

    
    return dados_por_ano

# Função para pesquisar a inscrição
def pesquisar_inscricao(inscricao):
    dados = carregar_dados()
    resultados = []

    for ano, df in dados.items():
        print(df)
        df['Vago'] = df['INSCRICAO'].apply(lambda x: 'Vago' if str(x).endswith('000') else 'Edificado')
        inscricao_data = df[df['INSCRICAO'].astype(str) == inscricao]

        if not inscricao_data.empty:
            for _, row in inscricao_data.iterrows():
                resultados.append({
                    'ano': ano,
                    'inscricao': row['INSCRICAO'],
                    'metragem': row['METRAGEM'],
                    'status': row['Vago']
                })

    return resultados

@app.route('/pesquisar', methods=['GET'])
def pesquisar():
    inscricao = request.args.get('inscricao')
    if not inscricao:
        return jsonify({'error': 'Inscrição não fornecida'}), 400
    
    resultados = pesquisar_inscricao(inscricao)
    if not resultados:
        return jsonify({'message': 'Nenhum resultado encontrado para a inscrição'}), 404

    return jsonify(resultados), 200

if __name__ == '__main__':
    app.run(debug=True)
