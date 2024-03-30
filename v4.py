from tkinter import *
import cv2
import base64
from PIL import Image, ImageTk
from openai import OpenAI
import pyttsx3

class CameraApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Camera App")

        # Inicializando a câmera
        self.cap = cv2.VideoCapture(0)

        self.canvas = Canvas(master, width=640, height=480)
        self.canvas.pack()

        self.update()

        # Criando um botão para tirar a foto
        self.btn_capture = Button(master, text="Capturar", command=self.capture)
        self.btn_capture.pack()

    def update(self):
        # Capturando a imagem da câmera
        ret, frame = self.cap.read()

        if ret:
            # Convertendo a imagem para formato tkinter
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.canvas.create_image(0, 0, anchor=NW, image=self.photo)

        # Atualizando o canvas após 10 milissegundos
        self.master.after(10, self.update)

    def capture(self):
    # Capturando a imagem da câmera
      ret, frame = self.cap.read()

      if ret:
        # Salvando a imagem capturada
        cv2.imwrite("temp_image.jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

        # Finalizando a câmera
        self.cap.release()

        # Chamando a função para enviar a imagem para descrição
        self.send_image()


    def send_image(self):
        # Convertendo a imagem para base64
        with open('temp_image.jpg', 'rb') as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

        # Criando a URL da imagem
        image_url = "data:image/jpeg;base64," + encoded_string

        # Criando cliente OpenAI
        client = OpenAI(api_key='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')

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
        description = response.choices[0]
        print("Descrição da imagem:", description)

        # Convertendo texto em fala
        self.convert_text_to_speech(description)

    def convert_text_to_speech(self, text):
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()

root = Tk()
app = CameraApp(root)
root.mainloop()
