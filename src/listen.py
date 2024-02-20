import openai, re, json, time
import speech_recognition as sr
from src.queueSpeak import QueueSpeak
from src.controller.configController import ConfigController
from config import API_KEY

openai.api_key = API_KEY

arrayCancelar = ["cancelar", "cancelar pergunta", "nada", "nada não", "nada deixa pra lá", "nada deixa para lá"]
arrayCommands = ["#ADICIONAR_PESSOA#", "#TROCAR_NOME_ROBO#"]

class Listen:
    def __init__(self, configs:ConfigController, sysGlobals, queueSpeak:QueueSpeak) -> None:
        self.sysGlobals = sysGlobals
        self.configs = configs
        self.queueSpeak = queueSpeak
        self.rec = sr.Recognizer()
        self.chatId = None

    def start(self, newName) -> None:
        if not newName:
            self.robotConfig()

        while True:
            audio = self.getListen()

            if audio:
                try:
                    if audio.lower() == self.configs.NAME.lower():
                        self.robotListen()
                    elif self.configs.NAME.lower() in audio.lower():
                        self.queueSpeak.putWait("Oi, Falou comigo?")
                        quest = self.getListen(timeout=5)

                        if quest:
                            if quest.lower() == "sim":
                                self.robotListen()
                            elif quest.lower() == "não":
                                self.queueSpeak.queue.put("tudo bem!")
                except Exception as e:
                    print("Ocorreu um erro: {}".format(e))

    def robotListen(self) -> None:
        try:
            self.queueSpeak.putWait("oi, no que posso ajudar?")
            text = self.getListen(timeout=5)

            if text:
                if text in arrayCancelar:
                    self.queueSpeak.queue.put("OK!")
                else:
                    self.queueSpeak.queue.put("Aguarde um instante, irei pesquisar...")
                    resp = self.getChatGPT(text)

                    for com in arrayCommands:
                        if com in resp:
                            self.queueSpeak.putWait(resp.replace(com, ""))

                            if com == '#TROCAR_NOME_ROBO#':
                                self.changeName()
                            elif com == '#MAISPARAMETROS...#':
                                self.changeName()
                            
                            return
                            
                    self.queueSpeak.putWait(resp)
            else:
                self.queueSpeak.queue.put("Não compreendi o que deseja.")
        except Exception as e:
            print("Algo deu errado ao executar o metodo robotRun(): {}".format(e))

    def robotConfig(self) -> None:
        try:
            self.queueSpeak.putWait(f"Deseja mudar meu nome agora?")
            newName = self.getListen(text=True)

            if newName.lower() == 'sim':
                self.changeName()
        except Exception as e:
            print("Algo deu errado ao executar o metodo robotConfig(): {}".format(e))

    def changeName(self):
        newName = self.getListen()
        if newName:
            self.configs.setName(newName)
            self.queueSpeak.queue.put(f"Pronto! agora você pode me chamar de {self.configs.NAME}")

    def audio_to_text(self, fileAudio) -> str:
        try:
            resp = self.rec.recognize_google(fileAudio, language="pt-BR")
            return resp
        except Exception as e:
            print("Algo deu errado ao transformar o áudio em texto: {}".format(e))
        
        return False

    def getChatGPT(self, prompt):
        try:
            if self.chatId is None:
                self.chatId = [{
                    "role":"system",
                    "content" :"""
                        Você é um robô assistente com inteligência artificial, sabe responder tudo que lhe for pedido, também tem a capacidade de interagir com seu usuário, então responda sempre como se estivesse falando com algum amigo bem íntimo, o melhor super amigo. 
                        Existe alguns comandos que vão ser executados conforme a intenção do usuário. 
                        Exemplos: Quando perceber que a intenção é adicionar pessoa, você deve responder com uma pergunta de qual o nome e idade da pessoae, no final da frase a TAG '#ADICIONAR_PESSOA#';
                        Quando perceber que a intenção for trocar o nome do assistente, você faz uma pergunda de qual é o novo nome, no final da frase a TAG '#TROCAR_NOME_ROBO#';
                        Quando receber uma mensagem com a TAG '#TROCANDO_NOME_ROBO#', você retorna uma mensagem formatada que contenha o nome e idade informada, exemplo: João Batista Oliveira, 25.
                    """
                }]

            self.chatId.append({
                "role":"user",
                "content":prompt
            })

            response = openai.ChatCompletion.create(
                model = "gpt-3.5-turbo",
                messages=self.chatId,
                n=1,
                stop=None,
                temperature=0.5
            )

            self.chatId.append({
                "role":"assistant",
                "content":response["choices"][0]["message"]["content"]
            })

            return response["choices"][0]["message"]["content"]
        except Exception as e:
            print("Ocorreu um erro ao buscar no chatGPT: {}".format(e))

        return False

    def getListen(self, pause=2, text=True, timeout=3):
        try:
            if self.configs.DEVICEINDEX is None:
                for index, name in enumerate(sr.Microphone.list_microphone_names()):
                    print(f"Checando microfone: {name}")

                    with sr.Microphone(device_index=index) as source:
                        self.rec.adjust_for_ambient_noise(source, duration=0.5)
                        source.pause_threshold = pause
                        
                        try:
                            audio = self.rec.listen(source, phrase_time_limit=1, timeout=1)
                            if audio:
                                self.configs.setDeviceIndex(index)
                                break
                        except Exception as e:
                            print(e)
                            
            with sr.Microphone(device_index=self.configs.DEVICEINDEX) as source:
                self.rec.adjust_for_ambient_noise(source, duration=0.5)
                source.pause_threshold = pause
                audio = self.rec.listen(source, phrase_time_limit=None, timeout=timeout)

                if audio:
                    if text:
                        return self.rec.recognize_google(audio, language="pt-BR")
                    
                    return audio
        except Exception as e:
            print(e)

        return False