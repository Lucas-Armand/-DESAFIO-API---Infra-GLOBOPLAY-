# [DESAFIO] API - Infra GLOBOPLAY 
Aplicação em Python para atender o desafio de "[Infraestrutura de Integração GloboPlay](https://github.com/Lucas-Armand/-DESAFIO-API---Infra-GLOBOPLAY-/blob/master/docs/DESAFIO%20DE%20INTEGRA%C3%87%C3%83O.pdf)". Esse projeto é de infraestrutura, ou seja, tem como objetivo intermediar outras aplicações. O objetivo é, dado um diretório específico (watchdog) onde são colocados arquivos com dados de entrada que devem ser operados através de APIs, o programa monitora o diretório e, para cada arquivo adicionado, realiza as computações necessárias.

## Instalação

Essa aplicação usa o Conda como ambiente e utiliza as bibliotecas do Projeto Anaconda. Para uma melhor integração recomendo a instalação do Anacoda 3 ou mais recente. Esse programa é baseado em python 3.7 e utiliza as bibliotecas: Sqlite3, rando, panda, logging, datetime, shutil, time, glob, re e os.

Para rodar o programa basta baixar os arquivos do projeto e, na pasta dos "app" do projeto, rodar: 

```
python infra.py
```

## Funcionalidades
Ao executar o programa, caso você tenha tirado todos os arquivos txt da pasta para adicioná-los aos poucos você verá algo como:

![Tela inicial](https://github.com/Lucas-Armand/-DESAFIO-API---Infra-GLOBOPLAY-/blob/master/docs/imgs/Screenshot%20from%202019-02-21%2002-24-40.png)

Nessa exibição é possível ver as primeiras informações do log de execução do programa. Um dos objetivos desse projeto é que o usuário tivesse muito feedback ao longo das etapas do processo, uma vez que o programa de ser usado de maneira contínua.

Caso você simplesmente coloque o programa para rodar com todos os arquivos txt dentro, você terá um resultado como :

![Tela segunda](https://github.com/Lucas-Armand/-DESAFIO-API---Infra-GLOBOPLAY-/blob/master/docs/imgs/Screenshot%20from%202019-02-21%2002-26-31.png)

Nessa tela já podemos ver muitas informações: Novos arquivos encontrados, para cada arquivo, a linha que ele está lendo, etc.

Outras informações importantes estão mais afrente no log:
![Tela terceira](https://github.com/Lucas-Armand/-DESAFIO-API---Infra-GLOBOPLAY-/blob/master/docs/imgs/Screenshot%20from%202019-02-21%2002-26-59.png)

Aqui podemos acompanhar o progresso da "API DE CORTE" e em seguida o feedback do resultado de movimentação e, por fim, os dados que poderiam ser postado na API da GloboPlay em resposta ao requisito deles.

Um diferencial extra deste trabalho foi a construção de um log "log_file_name.log" onde todas as informações que foram postados do log ficam salvas, o que facilita a manutenção e o debug da ferramenta:

![Tela quarta](https://github.com/Lucas-Armand/-DESAFIO-API---Infra-GLOBOPLAY-/blob/master/docs/imgs/Screenshot%20from%202019-02-21%2002-42-43.png)
