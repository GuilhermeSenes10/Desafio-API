CREATE TABLE empresas (
    id INTEGER PRIMARY KEY,
    cnpj TEXT UNIQUE NOT NULL,
    situacao TEXT,
    tipo TEXT,
    razao_social TEXT NOT NULL,
    nome_fantasia TEXT,
    estado TEXT NOT NULL,
    municipio TEXT NOT NULL,
    endereco TEXT NOT NULL,
    natureza_juridica TEXT NOT NULL,
    porte TEXT NOT NULL,
    atividade_principal TEXT NOT NULL,
    telefone TEXT,
    numero_funcionarios INTEGER NOT NULL,
    faturamento_anual_estimado REAL NOT NULL,
    vendedor_responsavel TEXT NOT NULL
);