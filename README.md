# Covidômetro

Projeto client/server socket TCP desenvolvido em Python com TKinter como pré-requisito para avaliação da disciplina de **Protocolos de Interconexão de Redes de Computadores** do curso TSI - IFPB, Guarabira/PB.

Tem como objetivo a busca de informações sobre a COVID-19 e demonstração dos dados em formato de dicionário (json) ao cliente, busca esta realizada por meio da api gratuita do Brasil.IO.

## Instalação

1) Clone o projeto:
```bash
git clone https://github.com/alisonsandrade/covidometro-tk.git
```

2) Configure um ambiente virtual:
```bash
python3 -m venv env
source evn/bin/activate
```


3) Instale as dependências do projeto:
```bash
pip install -r requirements.txt
```

## Uso

```bash
# executando o servidor
python server.py

# executando o cliente
python client.py

# A janela tkinter irá executar e basta escolher a cidade e o município para fazer a consulta.
```

## Contribuidores
- [Alison S Andrade](https://github.com/alisonsandrade)
- [Maria Solange](https://github.com/SolangeMeireles)

## Licença
[MIT](https://choosealicense.com/licenses/mit/)