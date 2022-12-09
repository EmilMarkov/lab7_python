import socket
import configparser
from smtplib import SMTP


class Mailer:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        
    def send(self, dest, msg):
        with SMTP("smtp.mail.ru", 465) as smtp:
            smtp.ehlo()
            smtp.starttls()
            print(self.email, self.password)
            smtp.login(self.email, self.password)
            smtp.sendmail(self.email, dest, msg)


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config_read = config.read("config.ini")

    HOST = config["SERVER"]["HOST"]
    PORT = int(config["SERVER"]["PORT"])
    FREQUENCY = config["SERVER"]["FREQUENCY"]
    EMAIL = config["AUTH"]["EMAIL"]
    PASSWORD = config["AUTH"]["PASSWORD"]
    
    mailer = Mailer(EMAIL, PASSWORD)
    mailer.send("markovemil2@gmail.com", "Hello, Emil!")

    # server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # server.bind((HOST, PORT))
    # server.listen(4)
    # print("Working...")
    # client_socket, address = server.accept()
    # data = client_socket.recv(1024)

    # print(data.decode("utf-8"))
    # print("Shutdown...")