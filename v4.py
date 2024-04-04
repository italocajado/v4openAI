from tkinter import *
import cv2
import base64
from PIL import Image, ImageTk
from openai import OpenAI
import pyttsx3

client = OpenAI(api_key='')

class CameraApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Camera App")

        # Inicializando a câmera
        self.cap = cv2.VideoCapture(0)
        self.canvas = Canvas(master, width=640, height=480)
        self.canvas.pack()
        self.update()

        # botão para tirar a foto
        self.btn_capture = Button(master, text="Capturar", command=self.capture)
        self.btn_capture.pack()
        
        self.descriptionText = Text(master, height = 10, width = 100)
        self.descriptionText.pack(padx= 5, pady= 5)

    def update(self):
        ret, frame = self.cap.read()

        if ret:
            # Convertendo a imagem para formato tkinter
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.canvas.create_image(0, 0, anchor=NW, image=self.photo)

        # Atualizando o canvas após 10 milissegundos
        self.master.after(10, self.update)

    def capture(self):
        ret, frame = self.cap.read()

        if ret:
            # Salvando a imagem capturada sem conversão de cores
            cv2.imwrite("temp_image.jpg", frame)  # Salva a imagem em BGR
            self.cap.release()
            # Chamando a função para enviar a imagem para descrição
            self.send_image()


    def send_image(self):
        # Convertendo a imagem para base64
        with open('temp_image.jpg', 'rb') as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

        # Criando a URL da imagem
        image_url = "data:image/jpeg;base64," + encoded_string
        
        # Enviando a imagem para descrição
        response = client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "descreva essa imagem?"},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": image_url,
                            },
                        },
                    ],
                }
            ],
            max_tokens=300,
        )

        # Obtendo a descrição da imagem
        if response.choices[0].message:
            description = response.choices[0].message.content
        else:
            description = "Não foi possivel  obter uma descrição."
        print("Descrição da imagem: ", description)
        self.descriptionText.delete(1.0, END)
        self.descriptionText.insert(END, description)

        # Convertendo texto em fala
        self.convert_text_to_speech(description)

    def convert_text_to_speech(self, text):
        engine = pyttsx3.init()
        engine.say(text)
        engine.setProperty('rate', 1.5)
        engine.runAndWait()

root = Tk()
app = CameraApp(root)
root.mainloop()
