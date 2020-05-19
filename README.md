# jantarDosFilosofosDistribuido

## Conceito
A ideia deste projeto é simular o jantar dos filosofos, porém em máquinas diferentes, sendo que, cada máquina possui um garfo e pode consultar a máquina a direita (primeiro indice "á direita" após o índice do ip do máquina no array de IPs) se ela possuir um garfo para ser emprestado, uma máquina também possui uma thread em que é executado um servidor de garfos, atendendo a máquina á esquerda no índice do arrays de IPs; caso possua um garfo,caso uma máquina consiga os dois garfos, ela "come", em seguida libera o garfo emprestado do filosofo da direita no índice de IPs, e assim sucessivamente.

## Funcionamento

O código possui os seguintes parâmetros: 
* idFilosofo - Um inteiro correspondete ao indice + 1 do ip da máquina no ipFilosofos que será usado para identificar a máquina
* ipsFilosofosReal - Vetor de IPs de todas as máquinas participantes
* ipsFilosofos - Mesmo valor de ipsFilosofosReal, porém no índice correspondente ao ip de cada máquina, o ip deverá ser 0.0.0.0
* portaJanta - Porta usada para emitir e receber mensagem de algum filosofo comendo
* portaInicio - Porta usada para emitir mensagem do ínicio do programa
* situacaoFilosofo - Deve começar com 0
* meuGarfo - Garfo de cada filosofo,deve ser o mesmo valor de início de idFilosofo
* garfoAmigo - Garfo do filosofo do índice á direita do índice de cada máquina nov etor ipsFilosofos
* comecou - Flag usada para início do programa, deve estar como 0

Para executar o algoritmo, deve executar em cada máquina o progama, e como pode ser visto no terminal (ao executar o código), deverá ser inserio o valor 2 para toda máquina que irá escutar o ínicio do programa e 1 para a máquina que irá dar a largada, após inserir 1, digitar "inicio" e iniciar o espectáculo!

## Observação
O python não realiza um processamento realmente paralelo entre threads, sendo um pseudo-paralelo, onde cada thread é executada sequencialmente, por causa do Global Interpreter Lock (arquitetura interna da linguagem), ao contrário dos processos, onde a execução é realmente paralela, por este motivo, como o código foi implementado com threads, caso uma thread não esteja "escutando" na porta setada (por outra thread do código estar sendo executada no momento), os pacotes enviados pela thread que fez a requsição se perderão, e a mesma não terá uma resposta, por isso, em todas as threads que fazem requisições á outras threads, foi implementado uma confirmaçao de que o pacote enviado realmente foi recebido pela thread de destino, reenviando o pacote pela thread de origem caso o mesmo não tenha sido entregue.
