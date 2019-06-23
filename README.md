# jantarFilosofosDistribuido

## Conceito
A ideia deste código em python é simular o jantar dos filosofos,porém em máquinas diferentes,sendo que,cada máquina possui um garfo e pode consultar a máquina á direita(primeiro indice "á direita" após o índice do ip do máquina no array de IPs) se ela possui um garfo para ser emprestado,um máquina também possui uma thread em que é executado um servidor de garfos,atentando á máquina á esquerda no índice do arrays de IPs caso possua um garfo,caso uma máquina consiga os dois garfos,ela come,em seguida libera o garfo emprestado do filosofo da direita no índice de IPs,e assim sucessivamente

## Funcionamento

o código possui os seguintes atributos:
idFilosofo = um inteiro correspondete ao indice + 1 do ip da máquina no ipFilosofos que será usado para identificar a máquina
ipsFilosofosReal =vetor de IPs de todas as máquinas participantes
ipsFilosofos = mesmo valor de ipsFilosofosReal,porém no índice correspondente ao ip de cada máquina,o ip deverá ser 0.0.0.0
portaJanta = porta usada para emitir e receber mensagem de algum filosofo comendo
portaInicio = porta usada para emitir mensagem do ínicio do programa
situacaoFilosofo = deve começar com 0
meuGarfo = garfo de cada filosofo,deve ser o mesmo valor de início de idFilosofo
garfoAmigo = garfo do filosofo do índice á direita do índice de cada máquina nov etor ipsFilosofos
comecou = flag usada para início do programa,deve estar como 0

Para executar o algoritmo,deve executar em cada máquina o progama,e como pode ser visto no terminal,deverá ser inserio o valor 2 para toda máquina que irá escutar o ínicio do programa e 1 para a máquina que irá dar a largada,após inserir 1,digitar "inicio" e iniciar o espectáculo!
