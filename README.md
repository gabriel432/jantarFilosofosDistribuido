# jantarDosFilosofosDistribuido

## Conceito
A ideia deste projeto é simular o jantar dos filosofos, porém em máquinas diferentes, sendo que, cada máquina possui um garfo e pode consultar a máquina a direita (primeiro indice "á direita" após o índice do ip do máquina no array de IPs) se ela possuir um garfo para ser emprestado, uma máquina também possui uma thread em que é executado um servidor de garfos, atendendo a máquina á esquerda no índice do arrays de IPs; caso possua um garfo,caso uma máquina consiga os dois garfos, ela "come", em seguida libera o garfo emprestado do filosofo da direita no índice de IPs, e assim sucessivamente.

## Funcionamento

o código possui os seguintes atributos:
idFilosofo = um inteiro correspondete ao indice + 1 do ip da máquina no ipFilosofos que será usado para identificar a máquina
ipsFilosofosReal = vetor de IPs de todas as máquinas participantes
ipsFilosofos = mesmo valor de ipsFilosofosReal, porém no índice correspondente ao ip de cada máquina, o ip deverá ser 0.0.0.0
portaJanta = porta usada para emitir e receber mensagem de algum filosofo comendo
portaInicio = porta usada para emitir mensagem do ínicio do programa
situacaoFilosofo = deve começar com 0
meuGarfo = garfo de cada filosofo,deve ser o mesmo valor de início de idFilosofo
garfoAmigo = garfo do filosofo do índice á direita do índice de cada máquina nov etor ipsFilosofos
comecou = flag usada para início do programa, deve estar como 0

Para executar o algoritmo, deve executar em cada máquina o progama, e como pode ser visto no terminal (ao executar o código), deverá ser inserio o valor 2 para toda máquina que irá escutar o ínicio do programa e 1 para a máquina que irá dar a largada, após inserir 1, digitar "inicio" e iniciar o espectáculo!

## Observação
O python não realiza um processamento realmente paraleo entre threads, sendo um pseudo-paralelo, onde cada thread é executada sequencialmente, por causa do Global Interpreter Lock (arquitetura interna da linguagem), ao contrário dos processos, onde a execução é realmente paralela, por este motivo, como o código foi implementado com threads, caso uma thread não esteja "escutando" na porta setada (por outra thread do código estar sendo executada no momento), os pacotes enviados pela thread que fez a requsição se perderão, e a mesma não terá uma resposta, por isso, em todas as threads que fazem requisições á outras threads, foi implementado uma confirmaçao de que o pacote enviado realmente foi recebido pela thread de destino, reenviando o pacote pela thread de origem caso o mesmo não tenha sido entregue.
