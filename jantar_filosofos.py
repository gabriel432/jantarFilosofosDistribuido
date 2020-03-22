import time
import random
import socket
from threading import Thread, RLock

lock = RLock()
idFilosofo = 2  ''' 1,2,3,4 ou 5 #if do filosofo precisa corresponder ao indice
no array de ips de seu respectivo ip'''
ipsFilosofosReal = list(["200.239.138.232", "200.239.138.237",
                         "200.239.138.92", "200.239.138.205",
                         "200.239.138.234"])
ipsFilosofos = list(["200.239.138.232", "0.0.0.0", "200.239.138.92",
                    "200.239.138.205", "200.239.138.234"])

portaInicio = 5052
portaJanta = 5053
situacaoFilosofo = 0  # 1 p comendo 0 p pensando
meuGarfo = 2
garfoAmigo = 0  # 0,1,2,3,4,5
comecou = 0


class Filosofo(Thread):
    op = 0

    def __init__(self, cond):
        Thread.__init__(self)
        self.op = cond

    def comer(self):
        global idFilosofo, ipsFilosofos, ipsFilosofosReal, portaInicio, \
            portaJanta, situacaoFilosofo, meuGarfo, garfoAmigo, comecou
        print("comer")
        situacaoFilosofo = 1
        time.sleep(random.random())  # comendo por tempo indeterminado
        situacaoFilosofo = 0
        for i in ipsFilosofos:
            array = ["Filosofo ", ipsFilosofosReal[idFilosofo - 1],
                     " comendo com garfos ", str(meuGarfo), " e ",
                     str(garfoAmigo)]
            self.enviaDado(i, portaJanta, "".join(array))

    def pegarGarfoAmigo(self):
        global idFilosofo, ipsFilosofos, ipsFilosofosReal, portaInicio, \
            portaJanta, situacaoFilosofo, meuGarfo, garfoAmigo, comecou
        print("pegarGarfoAmigo")
        if(garfoAmigo != 0):
            return True
        self.enviaDado(ipsFilosofos[idFilosofo % len(ipsFilosofos)], 5060,
                       str("1|-1"))  # 1 para pegar garfo
        print("pegarGarfoAmigo | msg enviada ao amigo,esperando...")
        try:
            msg, ipFilosofoAmigo = self.recebeDado(ipsFilosofos[idFilosofo - 1], 5061, 1)
            print("pegarGarfoAmigo | msg recebida, msg = " + msg)
            lock.acquire()
            garfoAmigo = int(msg[2])
            lock.release()
        except socket.timeout:
            print("pegarGarfoAmigo | tempo excedido!")
            return False
        self.enviaDado(ipsFilosofos[idFilosofo % len(ipsFilosofos)], 5060,
                       str("ok"))
        print("Garfo Amigo " + str(garfoAmigo) + ", meu garfo " + str(meuGarfo)
              + " mensagem " + msg)

        if(garfoAmigo):
            return True
        else:
            return False

    def devolverGarfoAmigo(self):
        global idFilosofo, ipsFilosofos, ipsFilosofosReal, portaInicio,\
             portaJanta, situacaoFilosofo, meuGarfo, garfoAmigo, comecou
        print("devolverGarfoAmigo")
        array = ["2|", str(garfoAmigo)]
        self.enviaDado(ipsFilosofos[idFilosofo % len(ipsFilosofos)], 5060,
                       "".join(array))  # 2 para devolver
        try:
            msg, ipFilosofoComFome = self.recebeDado(
                ipsFilosofos[idFilosofo - 1], 5001, 1)
            if(msg == "ok"):
                self.enviaDado(ipFilosofoComFome[0], 5060, "ok")
                msg, ipFilosofoComFome = self.recebeDado(
                    ipsFilosofos[idFilosofo - 1], 5001, 1)
                if(msg == "ok"):
                    garfoAmigo = 0

                return True
        except socket.timeout:
            return False

    def dormir(self):
        print("dormir")
        time.sleep(random.random())  # random de 0 a 1 segundo

    def viver(self):
        global idFilosofo, ipsFilosofos, ipsFilosofosReal, portaInicio,\
             portaJanta, situacaoFilosofo, meuGarfo, garfoAmigo, comecou
        print("viver")
        tentativas = 0
        while(True):
            self.dormir()
            tentativas += 1
            print("meuGarfo : " + str(meuGarfo) + "  garfoAmigo : " +
                  str(garfoAmigo))
            if(self.pegarGarfoAmigo() and meuGarfo):
                self.comer()
                if(garfoAmigo != 0):
                    self.devolverGarfoAmigo()
                tentativas = 1
            elif(tentativas >= 3 and garfoAmigo != 0):
                print("meuGarfo : " + str(meuGarfo) + "  garfoAmigo : " +
                      str(garfoAmigo))
                self.devolverGarfoAmigo()
                tentativas = 1

    def atendeFilosofoAmigo(self):
        global idFilosofo, ipsFilosofos, ipsFilosofosReal, portaInicio, \
            portaJanta, situacaoFilosofo, meuGarfo, garfoAmigo, comecou
        print("atendeFilosofoAmigo")
        msg, ipFilosofoComFome = self.recebeDado(
            ipsFilosofos[idFilosofo - 1], 5060, 0)
        if(situacaoFilosofo == 0 and msg[0] == "1" and meuGarfo != 0):
            array = ["2|", str(meuGarfo)]
            print("atendeFilosofoAmigo | msg a enviar : " + "".join(array))
            self.enviaDado(ipFilosofoComFome[0], 5061, "".join(array))
            try:
                msg, ipFilosofoComFome = self.recebeDado(
                    ipsFilosofos[idFilosofo - 1], 5060, 1)
                if(msg == "ok"):
                    lock.acquire()
                    meuGarfo = 0
                    lock.release()
                    return True
            except socket.timeout:
                return False
        elif(msg[0] == "2"):
            print("atendeFilosofoAmigo | garfo devolvido,  meu garfo = " + msg)
            self.enviaDado(ipFilosofoComFome[0], 5001, "ok")
            try:
                msg, ipFilosofoComFome = self.recebeDado(
                    ipsFilosofos[idFilosofo - 1], 5060, 1)
                if(msg == "ok"):
                    lock.acquire()
                    meuGarfo = idFilosofo
                    self.enviaDado(ipFilosofoComFome[0], 5001, "ok")
                    lock.release()
                    return True
            except socket.timeout:
                return False

    def imprimeJantar(self):
        global idFilosofo, ipsFilosofos, ipsFilosofosReal, portaInicio, \
            portaJanta, situacaoFilosofo, meuGarfo, garfoAmigo, comecou
        print("imprimeJantar")
        msg, ipFilosofo = self.recebeDado(
            ipsFilosofos[idFilosofo - 1], portaJanta, 0)
        print(msg)

    def enviaDado(self, ipFilosofoDestino, portaRequisicao, dado):
        for i in range(3):
            try:
                tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                dest = (str(ipFilosofoDestino), int(portaRequisicao))
                tcp.connect(dest)
                tcp.send(dado)
                tcp.close()
                return True
            except Exception as e:
                pass

    def recebeDado(self, ipFilosofo, portaAtendimento, cond):
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        orig = (str(ipFilosofo), int(portaAtendimento))
        tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        if(cond):
            tcp.settimeout(0.5)
        tcp.bind(orig)
        tcp.listen(1)
        objSocket, ipFilosofoComFome = tcp.accept()
        msg = objSocket.recv(1024)
        tcp.close()
        return msg, ipFilosofoComFome

    def inicio(self):
        global idFilosofo, ipsFilosofos, ipsFilosofosReal, portaInicio, \
            portaJanta, situacaoFilosofo, meuGarfo, garfoAmigo, comecou
        cond = int(input("1 para ouvir e 2 para executar: "))
        if(cond == 1):
            msg, ipFilosofoAmigo = self.recebeDado(
                ipsFilosofos[idFilosofo - 1], portaInicio, 0)
            if(msg == "inicio"):
                print("comecou!!")
                comecou = 1
        elif(cond == 2):
            msg = input("Digite inicio para comecar: ")
            for i in ipsFilosofos:
                print(i)
                if(i != ipsFilosofos[idFilosofo - 1]):
                    self.enviaDado(i, portaInicio, msg)
            comecou = 1

    def run(self):
        while(True):
            if(self.op == 0 and comecou == 0):
                self.inicio()
            if(self.op == 1 and comecou == 1):
                self.atendeFilosofoAmigo()
            if(self.op == 2 and comecou == 1):
                self.viver()
            if(self.op == 3 and comecou == 1):
                self.imprimeJantar()


for i in range(4):
    Filosofo(i).start()
