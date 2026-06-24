import tkinter as tk
from tkinter import messagebox, PhotoImage
import random
import os
import sys

TOTAL_CASILLAS = 15  
TOTAL_BOMBAS = 3     

class PapaBomba:
    def __init__(self, root):
        self.root = root
        self.root.title("Papa Bomba")
        self.root.geometry("1200x800")
        self.root.configure(bg="#111111")

        self.canvas = tk.Canvas(root, highlightthickness=0)
        self.canvas.place(relwidth=1, relheight=1)
        self.dibujar_degradado()

        self.cargar_imagenes()
        self.mostrar_menu()

    def obtener_ruta_recurso(self, ruta_relativa):
        # Resuelve las rutas de archivos tanto en desarrollo local como al compilar con PyInstaller (.exe/.app)
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, ruta_relativa)

    def cargar_imagenes(self):
        try:
            # Uso de os.path para normalizar separadores de directorios en Windows, Mac o Linux
            self.logo_menu = PhotoImage(file=self.obtener_ruta_recurso(os.path.join("images", "logomenu.png"))).subsample(2,2)
            self.img_vs_cpu = PhotoImage(file=self.obtener_ruta_recurso(os.path.join("images", "vscomputadora.png"))).subsample(2,2)
            self.img_vs_amigo = PhotoImage(file=self.obtener_ruta_recurso(os.path.join("images", "vsamigo.png"))).subsample(2,2)
            self.img_como_jugar = PhotoImage(file=self.obtener_ruta_recurso(os.path.join("images", "comojugar.png"))).subsample(2,2)
            self.img_salir = PhotoImage(file=self.obtener_ruta_recurso(os.path.join("images", "salir.png"))).subsample(2,2)
        except Exception as e:
            print(f"Advertencia: No se pudieron cargar las imágenes. {e}")
            self.logo_menu = self.img_vs_cpu = self.img_vs_amigo = self.img_como_jugar = self.img_salir = None

    def dibujar_degradado(self):
        w, h = 1200, 800
        for i in range(h):
            r = int(255 * (1 - i/h))
            g = int(120 * (1 - i/h))
            color = f"#{r:02x}{g:02x}00"
            self.canvas.create_line(0, i, w, i, fill=color)

    def limpiar(self):
        for w in self.root.winfo_children():
            if w != self.canvas:
                w.destroy()

    def mostrar_menu(self):
        self.limpiar()
        self.canvas.delete("all") 
        self.dibujar_degradado() 

        if self.logo_menu:
            self.logo_id = self.canvas.create_image(600, 180, image=self.logo_menu, anchor="center")
        else:
            self.logo_id = self.canvas.create_text(600, 180, text="¿PAPA O BOMBA?", fill="white", font=("Arial", 46, "bold"), justify="center")

        def crear_boton_menu(y_pos, img, txt, cmd):
            if img:
                btn_id = self.canvas.create_image(600, y_pos, image=img, anchor="center")
                self.canvas.tag_bind(btn_id, "<Button-1>", lambda e: cmd())
            else:
                btn = tk.Button(self.root, text=txt.upper(), command=cmd, font=("Arial", 16, "bold"),
                                bg="black", fg="white", activebackground="#333333", activeforeground="white",
                                bd=2, relief=tk.SOLID, width=46, height=2, highlightthickness=0)
                self.canvas.create_window(600, y_pos, window=btn, anchor="center")

        crear_boton_menu(380, self.img_vs_cpu, "Jugar contra Computadora", lambda: self.iniciar("cpu"))
        crear_boton_menu(475, self.img_vs_amigo, "Jugar contra Amigo", lambda: self.iniciar("amigo"))
        crear_boton_menu(570, self.img_como_jugar, "Cómo jugar", self.como_jugar)
        crear_boton_menu(665, self.img_salir, "Salir", self.root.destroy)

    def como_jugar(self):
        messagebox.showinfo(
            "Cómo jugar",
            f"Cada jugador tiene su propio tablero secreto.\n\n"
            f"Fase 1: Coloca tus {TOTAL_BOMBAS} bombas ocultas en tu tablero.\n"
            f"Fase 2: Por turnos, busca en el tablero del rival para encontrar sus bombas.\n"
            f"¡El primero en encontrar las {TOTAL_BOMBAS} bombas enemigas gana!"
        )

    def iniciar(self, modo):
        self.modo = modo
        self.b1, self.b2 = set(), set()  
        self.i1, self.i2 = set(), set()  
        self.p1 = self.p2 = 0
        self.fase = "colocar1"
        self.crear_tablero()

    def crear_tablero(self):
        self.limpiar()
        self.canvas.delete("all") 
        self.dibujar_degradado() 

        self.canvas.create_text(602, 52, text="BOMBAS ENCONTRADAS", fill="#221100", font=("Arial", 28, "bold"), justify="center")
        self.score_id = self.canvas.create_text(600, 50, text="BOMBAS ENCONTRADAS", fill="white", font=("Arial", 28, "bold"), justify="center")
        
        self.players_id = self.canvas.create_text(600, 105, text="", fill="white", font=("Arial", 22, "bold"), justify="center")
        self.estado_id = self.canvas.create_text(600, 160, text="", fill="white", font=("Arial", 16, "bold"), justify="center")

        self.botones_id = {}
        for i in range(1, TOTAL_CASILLAS + 1):
            fila = (i - 1) // 5
            col = (i - 1) % 5
            
            x1 = 210 + col * (140 + 20)
            y1 = 230 + fila * (140 + 20)
            x2 = x1 + 140
            y2 = y1 + 140

            r = 25  
            shape_id = self.canvas.create_polygon(
                x1+r, y1, x2-r, y1, x2, y1, x2, y1+r, x2, y2-r, x2, y2, x2-r, y2, 
                x1+r, y2, x1, y2, x1, y2-r, x1, y1+r, x1, y1, smooth=True,
                fill="white", outline=""
            )
            
            text_id = self.canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text="🥔", font=("Arial", 38), fill="black")
            
            self.canvas.tag_bind(shape_id, "<Button-1>", lambda event, p=i: self.click(p))
            self.canvas.tag_bind(text_id, "<Button-1>", lambda event, p=i: self.click(p))
            
            self.botones_id[i] = {"shape": shape_id, "text": text_id}

        self.actualizar()

    def actualizar(self):
        rival_nombre = "COMPUTADORA" if self.modo == "cpu" else "JUGADOR 2"
        
        if self.fase == "colocar1":
            texto_estado = "Fase de preparación: JUGADOR 1 coloca sus 3 bombas ocultas"
        elif self.fase == "colocar2":
            texto_estado = "Fase de preparación: JUGADOR 2 coloca sus 3 bombas ocultas"
        elif self.fase == "j1":
            texto_estado = f"Turno activo: JUGADOR 1 buscando bombas de {rival_nombre}"
        elif self.fase == "j2":
            # Se corrigió el salto de línea roto que rompía la sintaxis del string original
            texto_estado = f"Turno activo: JUGADOR 2 buscando bombas de {rival_nombre}"
        else:
            texto_estado = ""

        self.canvas.itemconfig(self.players_id, text=f"JUGADOR 1: {self.p1}    |    {rival_nombre}: {self.p2}")
        self.canvas.itemconfig(self.estado_id, text=texto_estado)

    def renderizar_tablero_ataque(self, intentos_propios, bombas_rival):
        for i, ids in self.botones_id.items():
            if i in intentos_propios:
                if i in bombas_rival:
                    self.canvas.itemconfig(ids["text"], text="💥", fill="white")
                    self.canvas.itemconfig(ids["shape"], fill="red")
                else:
                    self.canvas.itemconfig(ids["text"], text="🚫", fill="white")
                    self.canvas.itemconfig(ids["shape"], fill="#555555")
            else:
                self.canvas.itemconfig(ids["text"], text="🥔", fill="black")
                self.canvas.itemconfig(ids["shape"], fill="white")

    def renderizar_tablero_vacio(self):
        for ids in self.botones_id.values():
            self.canvas.itemconfig(ids["text"], text="🥔", fill="black")
            self.canvas.itemconfig(ids["shape"], fill="white")

    def click(self, pos):
        if self.fase == "colocar1":
            if pos in self.b1: return
            self.b1.add(pos)
            self.canvas.itemconfig(self.botones_id[pos]["text"], text="💣")
            self.canvas.itemconfig(self.botones_id[pos]["shape"], fill="#ffcccc")
            if len(self.b1) == TOTAL_BOMBAS:
                if self.modo == "cpu":
                    self.b2 = set(random.sample(range(1, TOTAL_CASILLAS + 1), TOTAL_BOMBAS))
                    self.fase = "j1"
                    self.renderizar_tablero_ataque(self.i1, self.b2)
                else:
                    self.fase = "colocar2"
                    self.renderizar_tablero_vacio()
                self.actualizar()

        elif self.fase == "colocar2":
            if pos in self.b2: return
            self.b2.add(pos)
            self.canvas.itemconfig(self.botones_id[pos]["text"], text="💣")
            self.canvas.itemconfig(self.botones_id[pos]["shape"], fill="#ffcccc")
            if len(self.b2) == TOTAL_BOMBAS:
                self.fase = "j1"
                self.renderizar_tablero_ataque(self.i1, self.b2)
                self.actualizar()

        elif self.fase == "j1":
            if pos in self.i1: return
            self.i1.add(pos)

            if pos in self.b2:
                self.p1 += 1
                self.canvas.itemconfig(self.botones_id[pos]["text"], text="💥", fill="white")
                self.canvas.itemconfig(self.botones_id[pos]["shape"], fill="red")
            else:
                self.canvas.itemconfig(self.botones_id[pos]["text"], text="🚫", fill="white")
                self.canvas.itemconfig(self.botones_id[pos]["shape"], fill="#555555")

            if self.p1 >= TOTAL_BOMBAS:
                return self.fin("¡Jugador 1 ganó!")

            if self.modo == "cpu":
                self.fase = "cpu"
                self.actualizar()
                self.canvas.itemconfig(self.estado_id, text="La computadora está buscando bombas...")
                self.root.after(1500, self.turno_cpu)
            else:
                self.fase = "j2"
                self.root.after(1000, lambda: [self.renderizar_tablero_ataque(self.i2, self.b1), self.actualizar()])

        elif self.fase == "j2":
            if pos in self.i2: return
            self.i2.add(pos)

            if pos in self.b1:
                self.p2 += 1
                self.canvas.itemconfig(self.botones_id[pos]["text"], text="💥", fill="white")
                self.canvas.itemconfig(self.botones_id[pos]["shape"], fill="red")
            else:
                self.canvas.itemconfig(self.botones_id[pos]["text"], text="🚫", fill="white")
                self.canvas.itemconfig(self.botones_id[pos]["shape"], fill="#555555")

            if self.p2 >= TOTAL_BOMBAS:
                return self.fin("¡Jugador 2 ganó!")

            self.fase = "j1"
            self.root.after(1000, lambda: [self.renderizar_tablero_ataque(self.i1, self.b2), self.actualizar()])

    def turno_cpu(self):
        libres = [x for x in range(1, TOTAL_CASILLAS + 1) if x not in self.i2]
        if not libres: return
        
        p = random.choice(libres)
        self.i2.add(p)

        if p in self.b1:
            self.p2 += 1

        if self.p2 >= TOTAL_BOMBAS:
            return self.fin("La computadora ganó")

        self.fase = "j1"
        self.renderizar_tablero_ataque(self.i1, self.b2)
        self.actualizar()

    def fin(self, msg):
        messagebox.showinfo("Fin", msg)
        self.mostrar_menu()

if __name__ == "__main__":
    root = tk.Tk()
    PapaBomba(root)
    root.mainloop()