# COMIDA

> Bot Inteligence Artifical com estratégia de compra/venda à direita

---

**Antes de atualizar o bot, certifique-se de registrar o último preço de compra
na nota. Ele pode perder a configuração ou os registros do último preço de
compra.**

## Como funciona

### Bot de compra/venda de negociação em grade de rastreamento

Este bot usa o conceito de ordem de compra/venda que permite acompanhar a
queda/alta do preço.

> Ordens de Trailing Stop Sobre o conceito de Trailing Stop Orders você pode
> encontrar em
> [Documento oficial da Binance](https://www.binance.com/en/support/faq/360042299292)
>
> Resumo Coloque ordens com um valor fixo ou percentual quando o preço mudar.
> Usando este recurso, você pode comprar pelo menor preço possível ao comprar na
> baixa e vender pelo maior preço possível ao vender na alta.

-O bot suporta múltiplas ordens de compra/venda com base na configuração. -O bot
pode monitorar vários símbolos. Todos os símbolos serão monitorados por segundo.
-O bot usa o MongoDB para fornecer um banco de dados persistente. No entanto,
ele não usa a versão mais recente do MongoDB para suportar o Raspberry Pi de 32
bits. Utilizou a versão do MongoDB. é 3.2.20, que é fornecido por
[apcheamitr](https://hub.docker.com/r/apcheamitru/arm32v7-mongo). -O bot foi
testado e funciona com Linux e Raspberry Pi 4 de 32 bits. Outras plataformas não
foram testadas.

#### Sinal de compra

O bot monitorará continuamente a moeda com base na configuração de negociação da
grade.

Para a negociação de grade nº 1, o bot lançará uma ordem STOP-LOSS-LIMIT para
comprar quando o preço atual atingir o menor preço. Se o preço atual cair
continuamente, o bot cancelará a ordem anterior e substituirá a nova ordem
STOP-LOSS-LIMIT com o novo preço.

Após a negociação na grade nº 1, o bot monitorará a COIN com base no último
preço de compra.

-O bot não colocará uma ordem de compra da negociação de grade nº 1 se tiver
moedas suficientes (normalmente mais de US$ 10) para vender quando atingir o
preço de gatilho para venda. -O bot removerá o último preço de compra se o valor
estimado for menor que o limite de remoção do último preço de compra.

##### Cenário de compra

Digamos que as configurações de negociação da grade de compra estejam definidas
conforme abaixo:

-Número de grades: 2 -Grades | Nº | Porcentagem de gatilho | Porcentagem de
preço de parada | Porcentagem de preço limite | USDT | | --- |
------------------- | --------------------- | ---------------------- | ---- | |
1 | 1 | 1,05 | 1,051 | 50 | | 2 | 0,8 | 1,03 | 1,031 | 100 |

Para facilitar a compreensão, usarei`$`como um símbolo USDT. Para simplificar o
cálculo, não levo em conta a comissão. Em negociações reais, a quantidade pode
ser diferente.

Sua 1ª negociação em grade para compra está configurada conforme abaixo:

-Grade nº: 1 -Porcentagem de gatilho: 1 -Porcentagem de parada: 1,05 (5,00%)
-Porcentagem limite: 1.051 (5,10%) -Valor máximo de compra: $ 50

E o mercado está assim:

-Preço atual: $ 105 -Preço mais baixo: US$ 100 -Preço de gatilho: US$ 100

Quando o preço atual estiver caindo para o preço mais baixo (US$ 100) e abaixo
do preço restrito ATH (máximo histórico), se habilitado, o bot colocará uma nova
ordem STOP-LOSS-LIMIT para compra.

-Preço de parada: $ 100 _ 1,05 = $ 105 -Preço limite: $ 100 _ 1,051 = $ 105,1
-Quantidade: 0,47573

Vamos supor que o mercado mude conforme abaixo:

-Preço atual: $ 95

Em seguida, o bot acompanhará a queda do preço e colocará uma nova ordem
STOP-LOSS-LIMIT conforme abaixo:

-Preço de parada: $ 95 _ 1,05 = $ 99,75 -Preço limite: $ 95 _ 1,051 = $ 99,845
-Quantidade: 0,5

Vamos supor que o mercado mude conforme abaixo:

-Preço atual: US$ 100

Em seguida, o bot executará a primeira compra da moeda. O último preço de compra
será registrado como`$ 99.845`. A quantidade comprada será`0,5`.

Após a compra da moeda, o bot começará a monitorar o sinal de venda e, ao mesmo
tempo, monitorará a próxima grade de negociação para compra.

Sua segunda grade de negociação para compra está configurada conforme abaixo:

-Grade nº: 2 -Último preço de compra atual: $ 99,845 -Porcentagem de gatilho:
0,8 (20%) -Porcentagem de parada: 1,03 (3,00%) -Porcentagem limite: 1.031
(3,10%) -Valor máximo de compra: $ 100

E se o preço atual estiver caindo continuamente para`$ 79.876`(20% menor), então
o bot colocará uma nova ordem STOP-LOSS-LIMIT para a 2ª grade de negociação da
moeda.

Vamos supor que o mercado mude conforme abaixo:

-Preço atual: $ 75

Então o bot acompanhará a queda do preço e colocará uma nova ordem
STOP-LOSS-LIMT conforme abaixo:

-Preço de parada: $ 75 _ 1,03 = $ 77,25 -Preço limite: $ 75 _ 1,031 = $ 77,325
-Quantidade: 1,29

Vamos supor que o mercado mude conforme abaixo:

-Preço atual: $ 78

Em seguida, o bot executará a segunda compra da moeda. O último preço de compra
será recalculado automaticamente conforme abaixo:

-Preço final de compra: ($ 50 + $ 100) / (0,5 COIN + 1,29 COIN) = $ 83,80

### Sinal de venda

Se houver saldo suficiente para vender e o último preço de compra estiver
registrado no bot, o bot começará a monitorar o sinal de venda da operação de
grid nº 1. Assim que o preço atual atingir o preço de gatilho da operação de
grid nº 1, o bot lançará uma ordem STOP-LOSS-LIMIT para vender. Se o preço atual
subir continuamente, o bot cancelará a ordem anterior e substituirá a nova ordem
STOP-LOSS-LIMIT com o novo preço.

-Se o bot não tiver um registro do último preço de compra, o bot não venderá a
moeda. -Se a moeda valer menos que o último limite de remoção do preço de
compra, o bot removerá o último preço de compra. -Se a moeda não valer mais que
o valor nominal mínimo, o bot não fará um pedido.

#### Cenário de Venda

Digamos que as configurações de negociação da grade de vendas estejam definidas
conforme abaixo:

-Número de grades: 2 -Grades | Nº | Porcentagem de gatilho | Porcentagem de
preço de parada | Porcentagem de preço limite | Porcentagem de quantidade de
venda | | --- | ------------------- | --------------------- |
---------------------- |------------------------- | | 1º | 1,05 | 0,97 | 0,969 |
0,5 | | 2º | 1.08 | 0,95 | 0,949 | 1 |

Ao contrário da compra, a configuração de venda usará a porcentagem de uma
quantidade. Se você quiser vender toda a sua quantidade de moedas, basta
configurá-la como`1`(100%).

Das últimas ações de compra, você agora tem os seguintes saldos:

-Quantidade atual: 1,79 -Último preço de compra atual: $ 83,80

Sua 1ª grade de negociação para venda está configurada conforme abaixo:

-Grade nº 1 -Porcentagem de gatilho: 1,05 -Porcentagem de preço de parada: 0,97
-Porcentagem de preço limite: 0,969 -Porcentagem do valor de venda: 0,5

Vamos supor que o mercado mude conforme abaixo:

-Preço atual: $ 88

Como o preço atual é maior que o preço de venda (US$ 87,99), o bot colocará uma
nova ordem STOP-LOSS-LIMIT para venda.

-Preço de parada: $ 88 _ 0,97 = $ 85,36 -Preço limite: $ 88 _ 0,969 = $ 85,272
-Quantidade: 0,895

Vamos supor que o mercado mude conforme abaixo:

-Preço atual: $ 90

Em seguida, o bot acompanhará o aumento do preço e colocará uma nova ordem
STOP-LOSS-LIMIT conforme abaixo:

-Preço de parada: $ 90 _ 0,97 = $ 87,30 -Preço limite: $ 90 _ 0,969 = $ 87,21
-Quantidade: 0,895

Vamos supor que o mercado mude conforme abaixo:

-Preço atual: $ 87

Em seguida, o bot executará a primeira venda da moeda. Em seguida, aguardará o
preço de gatilho da segunda venda (US$ 83,80 \* 1,08 = US$ 90,504).

-Quantidade atual: 0,895 -Último preço de compra atual: $ 83,80

Vamos supor que o mercado mude conforme abaixo:

-Preço atual: $ 91

Então o preço atual ($91) é maior que o segundo preço de gatilho de venda
($90.504), o bot colocará uma nova ordem STOP-LOSS-LIMIT conforme abaixo:

-Preço de parada: $ 91 _ 0,95 = $ 86,45 -Preço limite: $ 91 _ 0,949 = $ 86,359
-Quantidade: 0,895

Vamos supor que o mercado mude conforme abaixo:

-Preço atual: US$ 100

Em seguida, o bot acompanhará o aumento do preço e colocará uma nova ordem
STOP-LOSS-LIMT conforme abaixo:

-Preço de parada: $ 100 _ 0,95 = $ 95 -Preço limite: $ 100 _ 0,949 = $ 94,9
-Quantidade: 0,895

Vamos supor que o mercado mude conforme abaixo:

-Preço atual: $ 94

Então o bot executará a segunda venda da moeda.

O lucro final seria

-1ª venda: $ 94,9 _ 0,895 = $ 84,9355 -2ª venda: $ 87,21 _ 0,895 = $ 78,05295
-Lucro final: $ 162 (lucro de 8%)

-Comércio manual -Converter pequenos saldos em BNB -Negocie todos os símbolos
-Monitoramento de múltiplas moedas simultaneamente -Stop-Loss -Restringir a
compra com preço ATH -Grid Trade para compra/venda -Integrado com a Análise
Técnica do TradingView

### Frontend + WebSocket

Frontend baseado em React.js se comunicando via Web Socket:

-Listar moedas de monitoramento com sinais de compra/venda/ordens abertas -Ver
saldos de contas -Ver negociações abertas/fechadas -Gerenciar configurações
globais/de símbolos -Excluir caches que não são monitorados -Link para URL
pública -Suporte Adicionar à tela inicial -Frontend seguro

## Parâmetros de ambiente

Use os parâmetros do ambiente para ajustar os parâmetros.
Verifique`/config/custom-environment-variables.json`para ver a lista de
parâmetros de ambiente disponíveis

Ou use o frontend para ajustar as configurações após iniciar o aplicativo.

## Como usar

1. Criar `.env`arquivo baseado em`.env.dist`.

## .env ---------------------------

## Live

BINANCE_LIVE_API_KEY=[Sua chave binance] BINANCE_LIVE_SECRET_KEY=[Seu segredo ]

## Test

BINANCE_TEST_API_KEY=[sua mesma chave ] BINANCE_TEST_SECRET_KEY=[Seu mesmo
segredo]

## Slack

BINANCE_SLACK_ENABLED=false BINANCE_SLACK_WEBHOOK_URL= BINANCE_SLACK_CHANNEL=
BINANCE_SLACK_USERNAME=

## Local Tunnel

BINANCE_LOCAL_TUNNEL_ENABLED=false

### A local tunnel makes the bot accessible from the outside.

### Please set the subdomain of the local tunnel as a subdomain that only you can remember.

BINANCE_LOCAL_TUNNEL_SUBDOMAIN=default

## Feature Toggles

BINANCE_FEATURE_TOGGLE_NOTIFY_ORDER_CONFIRM=true
BINANCE_FEATURE_TOGGLE_NOTIFY_DEBUG=false
BINANCE_FEATURE_TOGGLE_NOTIFY_ORDER_EXECUTE=true PORT=8080 NODE_ENV=production

## Authentication

BINANCE_AUTHENTICATION_ENABLED=true

### Please set your own password.

BINANCE_AUTHENTICATION_PASSWORD=[Sua senha real de acesso a binance]
BINANCE_JOBS_TRAILING_TRADE_BOT_OPTIONS_AUTHENTICATION_LOCK_LIST=true
BINANCE_JOBS_TRAILING_TRADE_BOT_OPTIONS_AUTHENTICATION_LOCK_AFTER=120

ATCOIN_API_URL=https://huggingface.co/spaces/amos-fernandes/cripto-model/
ATCOIN_API_KEY=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_mais_minha_super_chave_secreta
BINANCE_API_KEY=['Aqui sua chave'] BINANCE_API_SECRET=['Aqui seu segredo']

#Exportar chaves

##sudo echo $ATCOIN_API_URL ##sudo export
ATCOIN_API_URL="https://huggingface.co/spaces/amos-fernandes/cripto-model/api/v1/predict"

## ---

| Chave do ambiente               | Descrição                                                                                                               | Valor da amostra                                                                                     |
| ------------------------------- | ----------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| BINANCE_LIVE_API_KEY            | Chave da API da Binance para live                                                                                       | (de [Binance](https://binance.zendesk.com/hc/en-us/articles/360002502072-Como-criar-API))            |
| BINANCE_LIVE_SECRET_KEY         | Segredo da API da Binance para live                                                                                     | (de [Binance](https://binance.zendesk.com/hc/en-us/articles/360002502072-Como-criar-API))            |
| BINANCE_TEST_API_KEY            | Chave da API da Binance para teste                                                                                      | (de [Rede de Teste Binance Spot](https://testnet.binance.vision/))                                   |
| BINANCE_TEST_SECRET_KEY         | Segredo da API Binance para teste                                                                                       | (de [Rede de Teste Binance Spot](https://testnet.binance.vision/))                                   |
| BINANCE_SLACK_ENABLED           | Habilitar/desabilitar Slack                                                                                             | verdadeiro                                                                                           |
| BINANCE_SLACK_WEBHOOK_URL       | URL do webhook do Slack                                                                                                 | (de [Folga](https://slack.com/intl/en-au/help/articles/115005265063-Webhooks-de-entrada-para-Slack)) |
| BINANCE_SLACK_CHANNEL           | Canal do Slack                                                                                                          | "#binance"                                                                                           |
| BINANCE_SLACK_USERNAME          | Nome de usuário do Slack                                                                                                | Amos                                                                                                 |
| BINANCE_LOCAL_TUNNEL_ENABLED    | Habilitar/Desabilitar [túnel local](https://github.com/localtunnel/localtunnel)                                         | verdadeiro                                                                                           |
| BINANCE_LOCAL_TUNNEL_SUBDOMAIN  | Subdomínio de URL pública do túnel local                                                                                | binance                                                                                              |
| BINANCE_AUTHENTICATION_ENABLED  | Habilitar/Desabilitar autenticação de frontend                                                                          | true                                                                                                 |
| BINANCE_AUTHENTICATION_PASSWORD | Senha do frontend                                                                                                       | 123456                                                                                               |
| BINANCE_LOG_LEVEL               | Nível de registro. [Valores possíveis descritos na documentação `bunyan`.](https://www.npmjs.com/package/bunyan#levels) | ERRO                                                                                                 |

_Um túnel local torna o bot acessível de fora. Defina o subdomínio do túnel
local como um subdomínio que só você consiga lembrar._ _Você deve alterar a
senha de autenticação; caso contrário, ela será configurada como a senha
padrão._

2.Inicie/atualize o bot com docker-compose

Puxe o código mais recente primeiro:

```bash
  git pull
```

Se quiser o modo de produção/ao vivo, use a imagem de compilação mais recente do
DockerHub:

```bash
  docker-compose -f docker-compose.server.yml puxar
  docker-compose -f docker-compose.server.yml up -d
```

Ou se quiser o modo de desenvolvimento/teste, execute os comandos abaixo:

```bash
  docker-compose up -d --build
```

3.Abra o navegador`http://0.0.0.0:8080`para ver o frontend

-Ao iniciar o aplicativo, ele notificará a URL pública para o Slack. -Se tiver
algum problema com o bot, você pode verificar o log para descobrir o que
aconteceu com ele. Dê uma olhada em [Solução de
problemas](https://github.com/chrisleekr/binance-trading-bot/wiki/Solução de
problemas)

### Instalar via Stackfile

1. Em [Portainer](https://www.portainer.io/) criar nova pilha

2.Copiar conteúdo de`docker-stack.yml`ou carregue o arquivo

3.Definir chaves de ambiente para`binance-bot` no `docker-stack.yml`

4.Inicie e abra o navegador`http://0.0.0.0:8080`para ver o frontend

## Capturas de tela

| Protegido por senha                                                                                                          | Frontend Mobile                                                                                                          |
| ---------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| ![Protegido por senha](https://user-images.githubusercontent.com/5715919/133920104-49d1b590-c2ba-46d7-a294-eb6b24b459f5.png) | ![Frontend Mobile](https://user-images.githubusercontent.com/5715919/137472107-4059fcdf-5174-4282-81af-80cea5b269a0.png) |

| Configuração                                                                                                      | Negociação manual                                                                                                        |
| ----------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| ![Contexto](https://user-images.githubusercontent.com/5715919/127318581-4e422ac9-b145-4e83-a90d-5c05c61d6e2f.png) | ![Comércio manual](https://user-images.githubusercontent.com/5715919/127318630-f2180e1b-3feb-48fa-a083-4cb7f90f743f.png) |

| Frontend Desktop                                                                                                                    | Negócios Fechados                                                                                                             |
| ----------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| ![Área de trabalho front-end](https://user-images.githubusercontent.com/5715919/137472148-7be1e19b-3ce5-4d5a-aa28-18c55b3b48aa.png) | ![Negociações Fechadas](https://user-images.githubusercontent.com/5715919/137472190-a4c6ef0f-3399-44bb-852f-eedb7c67d629.png) |

### Exemplo de comércio

| Gráfico                                                                                                          | Ordens de compra                                                                                                          | Ordens de venda                                                                                                          |
| ---------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| ![Gráfico](https://user-images.githubusercontent.com/5715919/111027391-192db300-8444-11eb-8df4-91c98d0c835b.png) | ![Ordens de compra](https://user-images.githubusercontent.com/5715919/111027403-36628180-8444-11eb-91dc-f3cdabc5a79e.png) | ![Ordens de Venda](https://user-images.githubusercontent.com/5715919/111027411-4b3f1500-8444-11eb-8525-37f02a63de25.png) |

## Changes & Todo

Por favor consulte
[CHANGELOG.md](https://github.com/chrisleekr/binance-trading-bot/blob/master/CHANGELOG.md)
para visualizar as alterações anteriores.

-[ ] Desenvolver tela de configuração simples para segredos -[ ] Permitir
executar stop-loss antes da ação de compra -
[#299](https://github.com/chrisleekr/binance-trading-bot/issues/299) -[ ]
Melhore a estratégia de venda com porcentagem de preço de parada condicional com
base na porcentagem de lucro -
[#94](https://github.com/chrisleekr/binance-trading-bot/issues/94) -[ ]
Adicionar estratégia de compra de queda repentina -
[#67](https://github.com/chrisleekr/binance-trading-bot/issues/67) -[ ]
Gerenciar perfis de configuração (salvar/alterar/carregar?/exportar?) -
[#151](https://github.com/chrisleekr/binance-trading-bot/issues/151) -[ ]
Melhore as notificações com o suporte ao Apprise -
[#106](https://github.com/chrisleekr/binance-trading-bot/issues/106) -[ ]
Suporte o tempo de espera após atingir o preço mais baixo antes de comprar -
[#105](https://github.com/chrisleekr/binance-trading-bot/issues/105) -[ ]
Redefinir a configuração global para a configuração inicial -
[#97](https://github.com/chrisleekr/binance-trading-bot/issues/97) -[ ] Suporte
a frontend multilíngue -
[#56](https://github.com/chrisleekr/binance-trading-bot/issues/56) -[ ] Preço de
parada não linear e função de perseguição -
[#246](https://github.com/chrisleekr/binance-trading-bot/issues/246) -[ ]
Suporte à configuração STOP-LOSS por negociação de grade para venda -
[#261](https://github.com/chrisleekr/binance-trading-bot/issues/261)

## Doações

Se você achar este projeto útil, sinta-se à vontade para fazer uma pequena
[doação](https://github.com/chrisleekr/binance-trading-bot/blob/master/DONATIONS.md)
para o desenvolvedor.

## Agradecimentos

-[@d0x2f](https://github.com/d0x2f) -E muitos outros! Valeu, pessoal!

## Colaboradores

Obrigado a todos os colaboradores :heart:
[Clique para ver nossos heróis](https://github.com/chrisleekr/binance-trading-bot/graphs/contributors)

## Isenção de responsabilidade

Não dou nenhuma garantia e não assumo qualquer responsabilidade pela exatidão ou
integralidade das informações e materiais contidos neste projeto. Em nenhuma
circunstância serei responsabilizado por quaisquer reivindicações, danos,
perdas, despesas, custos ou responsabilidades (incluindo, sem limitação,
quaisquer danos diretos ou indiretos por lucros cessantes, interrupção de
negócios ou perda de informações) resultantes ou decorrentes direta ou
indiretamente do seu uso ou incapacidade de usar este código ou qualquer código
vinculado a ele, ou da sua confiança nas informações e materiais contidos neste
código, mesmo que eu tenha sido avisado da possibilidade de tais danos com
antecedência.

**Então use por sua conta e risco!**
