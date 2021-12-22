import socket
import threading
import tkinter
import tkinter.scrolledtext
from tkinter import ttk

from service.api import ApiService


HOST = "127.0.0.1"
PORT = 9091

class Client:
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

        self.gui_done = False
        self.running = True

        gui_thread = threading.Thread(target=self.gui_loop)
        receive_thread = threading.Thread(target=self.receive_loop)

        gui_thread.start()
        receive_thread.start()


    def gui_loop(self):
        self.win = tkinter.Tk()
        self.win.configure(bg="lightgray")
        self.win.title("Covidômetro")

        # Menu principal
        barra_menu = tkinter.Menu(self.win)
        menu_principal = tkinter.Menu(barra_menu)
        menu_principal.add_command(label="Sair", command=self.stop)

        menu_about = tkinter.Menu(barra_menu)
        menu_about.add_command(label="Informações", command=self.gui_about)
        
        barra_menu.add_cascade(label="Principal", menu=menu_principal)
        barra_menu.add_cascade(label="Sobre", menu=menu_about)

        self.win.config(menu=barra_menu)

        # Combo dos Estados
        self.label_state = tkinter.Label(self.win, text="Estado", bg="lightgray")
        self.label_state.config(font=("Arial", 12))
        self.label_state.pack(padx=20, pady=5)

        self.comboBoxState = ttk.Combobox(self.win, width=27, textvariable=tkinter.StringVar())
        self.comboBoxState['values'] = (
            'AC - Acré',
            'AL - Alagoas',
            'AP - Amapá',
            'AM - Amazonas',
            'BA - Bahia',
            'CE - Ceará',
            'DF - Distrito Federal',
            'ES - Espírito Santo',
            'GO - Goiás',
            'MA - Maranhão',
            'MT - Mato Grosso',
            'MS - Mato Grosso do Sul',
            'MG - Minas Gerais',
            'PA - Pará',
            'PB - Paraíba',
            'PR - Paraná',
            'PE - Pernambuco',
            'PI - Piauí',
            'RJ - Rio de Janeiro',
            'RN - Rio Grande do Norte',
            'RS - Rio Grande do Sul',
            'RO - Rondônia',
            'RR - Roraima',
            'SC - Santa Catarina',
            'SP - São Paulo',
            'SE - Sergipe',
            'TO - Tocantins')
                # self.comboBoxState.grid(column=0, row=1)
        self.comboBoxState.current(14)
        self.comboBoxState.pack()

        # Combo das cidades
        self.label_city = tkinter.Label(self.win, text="Município", bg="lightgray")
        self.label_city.config(font=("Arial", 12))
        self.label_city.pack(padx=20, pady=5)

        self.comboBoxCities = ttk.Combobox(self.win, width=27, textvariable=tkinter.StringVar(), postcommand=self.on_select_cities)
        self.comboBoxCities.pack()


        self.chat_label = tkinter.Label(self.win, text="Resultados:", bg="lightgray")
        self.chat_label.config(font=("Arial", 12))
        self.chat_label.pack(padx=20, pady=5)

        self.text_area = tkinter.scrolledtext.ScrolledText(self.win)
        self.text_area.pack(padx=20, pady=5)
        self.text_area.config(state="disabled")

        self.send_button = tkinter.Button(self.win, text="Consultar", command=self.write)
        self.send_button.config(font=("Arial", 12))
        self.send_button.pack(padx=20, pady=5)

        self.gui_done = True

        self.win.protocol("WM_DELETE_WINDOW", self.stop)

        self.win.mainloop()


    def write(self):
        state = self.comboBoxState.get()[0:2]
        city = self.comboBoxCities.get()
        message = f"{state} {city}"

        # message = f"{self.input_area.get('1.0', 'end')}"
        self.sock.send(message.encode("utf-8"))

    
    def on_select_cities(self):
        state_selected = self.comboBoxState.get()[0:2]

        data = ApiService().load_data()
        states = data["estados"]
        cities = data["cidades"]
        

        cities_list = []
        for city in cities:
            if city['estadoId'] == state_selected:
                cities_list.append(city["cidade"])
                
        self.comboBoxCities['values'] = cities_list


    def stop(self):
        self.running = False
        self.win.destroy()
        self.sock.close()
        exit(0)


    def gui_about(self):
        from tkinter import messagebox
        messagebox.showinfo(title="Sobre nós", message="Sistema desenvolvido em Python com TKinter como requisito para obtenção de nota da avaliação de da disciplina de Protocolos de Interconexão de Redes de Computadores do curso TSI - IFPB, Guarabira/PB.\n\nDesenvolvedores:\n- Alison Andrade\n- Maria Solange")


    def receive_loop(self):
        while self.running:
            try:
                message = self.sock.recv(1024)
                print('[*] Servidor:', message.decode("utf-8", "ignore"))
                if self.gui_done:
                    self.text_area.config(state='normal')
                    self.text_area.insert("end", message.decode("utf-8", "ignore"))
                    self.text_area.yview("end")
                    self.text_area.config(state="disabled")
            except ConnectionAbortedError:
                pass
            except:
                print("Ocorreu um erro")
                self.sock.close()
                break


client = Client(HOST, PORT)