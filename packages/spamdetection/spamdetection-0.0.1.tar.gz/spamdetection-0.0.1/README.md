# Introdução

Este diretório contém um projeto Python para solução do problema prático 2 do teste de Inteligência Artificial da Nuveo. Neste problema, solicitou-se a criação de um projeto para servir um modelo de classificação de mensagens de texto em _'ham'_ e _'spam'_. O modelo foi criado utilizando o pacote _scikit-learn_ e disponibilizado como um _pipeline_ contendo um passo de pré-processamento utilizando _TF-IDF_, seguido por um modelo de classificação binária utilizando _Random Forest_.

Para a implementação, foi criado um pacote Python de nome _spamdetection_, que implementa a classe _SpamDetector_, contendo métodos _prob_spam()_ (que retorna a probabilidade de classificação _'spam'_ determinada pelo modelo) e _is_spam()_ (que retorna a classificação). Maiores detalhes sobre o uso do pacote estão disponíveis na seção ___link para uso___ e na documentação ___link para documentação___.

Conforme solicitado no desafio, o pacote também é acompanhado de um módulo de testes unitários, contido na pasta ___link para pasta tests___. Maiores detalhes abaixo, na seção ___link para seção testes___.


# Dependências

Além da biblioteca padrão de Python, os seguintes pacotes são necessários para o uso do pacote _spamdetection_:

sklearn == 0.24.1
pywebio == 1.2.3

Criado em Python 3.8.5

Ambos estão especificados em requirements.txt e podem ser instalados com ___pip install requirements.txt___.

# Instalação

Duas opções estão disponíveis para uso do pacote _spamdetection_:

1. pip install spamdetection (ou pip install nuveo-teste-ia) (Recomendado) - confirmar que está disponível

2. Clonar este repo
	- clonar com git clone ___link - verificar se o link é estável___
	- criar ambiente virtual com venv ou virtualenv
	- à partir da raíz do repositório, instalar dependências com pip install requirements.txt
	- à partir da pasta 02-SMSSpamDetection, acessar o pacote _spamdetection_

Realisticamente falando, a criação do ambiente virtual, apesar de recomendada, provavelmente não é necessária no seu ambiente. As dependências são muito simples e a probabilidade de conflitos é baixíssima. O modelo foi criado com sklearn 0.24.1, mas fiz o desenvolvimento todo com 0.23.2 e não tive problemas (apesar de diversos warnings desencorajando o uso de modelo criado em versão diferente). PyWebIO é um pacote muito simples e também não deve gerar conflitos.

Para poder acessar o pacote à partir de qualquer diretório, adicionar a pasta 02-SMSSpamDetection ao PATH do Python ou clonar o repositório no diretório _sites_ (VERIFICAR SE ISSO É VÁLIDO!!!)


# Uso


modos de operação

Documentação (gerada com pdoc)

1) app


2) pacote + classe etc
classe SpamDetector() na documentação


3) pacote + linha de comando


# Testes

Detalhamento da metodologia de testes