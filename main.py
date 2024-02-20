import os
from src.boot import loadBoot
from src.controller.configController import ConfigController
from src.voice import Voice
from src.listen import Listen
from threading import Thread, Event
from src.queueSpeak import QueueSpeak

if not os.path.isdir('src/db'):
    os.mkdir('src/db')


def main():
    newName = loadBoot()
    configs = ConfigController()
    sysGlobals = {
        "isSpeaking":Event(),
    }

    queueSpeak = QueueSpeak(sysGlobals)
    voice = Voice(configs, sysGlobals=sysGlobals, queueSpeak=queueSpeak)
    listen = Listen(configs, sysGlobals=sysGlobals, queueSpeak=queueSpeak)

    Thread(target=listen.start, args=(newName,)).start()
    voice.start() # por enquanto tem q ser assim pq em thread trava!

    print("Finish!")
    

if __name__ == "__main__":
    main()