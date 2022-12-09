import time
import socket
import configparser
from smtplib import SMTP_SSL
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Mailer:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.ID = 00000 # ID последнего сообщения
        self.MSG = "" # текст последнего письма
        
    def send(self, dest, msg):
        self.MSG = msg
        
        body = MIMEMultipart()
        body['From'] = self.email
        body['To'] = dest
        body['Subject'] = f"[Ticket #{self.generate_token(msg)}] Mailer"
        
        body.attach(MIMEText(msg, 'plain'))

        with SMTP_SSL("smtp.mail.ru", 465) as smtp:
            smtp.login(self.email, self.password)
            text = body.as_string()
            smtp.sendmail(self.email, dest, text)
            smtp.quit()
            
    def generate_token(self, msg):
        self.ID = hash(msg) % 99999
        return self.ID
    
    
class Server:
    def __init__(self):
        self.server = None
        
        self.client_socket = None
        self.address = None
        
        config = configparser.ConfigParser()
        config.read("config.ini")
    
        self.HOST = config["SERVER"]["HOST"]
        self.PORT = int(config["SERVER"]["PORT"])
        self.FREQUENCY = config["SERVER"]["FREQUENCY"]
        self.EMAIL = config["AUTH"]["EMAIL"]
        self.PASSWORD = config["AUTH"]["PASSWORD"]
        
    def connect(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.HOST, self.PORT))
        self.server.listen(4)
        self.client_socket, self.address = self.server.accept()

    def stop(self):
        self.server.close()
        
    def log(self, file, msg):
        with open(file, "w+") as f:
            f.write(f"[{time.time()}] {msg}")
            f.close()
        
    

if __name__ == "__main__":
    server = Server()
    server.connect()
    
    mailer = Mailer(server.EMAIL, server.PASSWORD)
    
    while True:
        try:
            data = server.client_socket.recv(1024)
            mailer.send(data[0], data[1])
            server.log("success_request.log", f"[Token #{mailer.ID}] {mailer.MSG}")
        except TypeError:
            print("TypeError!")
            server.log("error_request.log", str(TypeError))
        except ValueError:
            print("ValueError!")
            server.log("error_request.log", str(ValueError))
            