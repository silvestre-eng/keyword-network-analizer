import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import Counter
from itertools import combinations

class KeywordNetworkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Visualizador de Red de Palabras Clave - RSL")
        self.root.geometry("1100x750")
        
        # Configurar evento al cerrar la ventana para finalizar el proceso completamente
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Panel de controles superior
        control_frame = tk.Frame(self.root, pady=10, bg="#f5f5f5")
        control_frame.pack(side=tk.TOP, fill=tk.X)

        btn_cargar = tk.Button(
            control_frame, 
            text="Cargar Excel (.xlsx)", 
            command=self.cargar_excel,
            bg="#007ACC", 
            fg="white", 
            font=("Arial", 10, "bold"),
            padx=10, 
            pady=4
        )
        btn_cargar.pack(side=tk.LEFT, padx=15)
        
        # 1. Configurar tema y estilo para los controles ttk
        style = ttk.Style()
        style.theme_use('clam') # 'clam' permite personalizar colores y bordes limpiamente
        
        style.configure(
            "TSpinbox",
            arrowsize=16,			# Incrementa el tamaño de los botones de flechas
            padding=5,				# Relleno interno para darle un aspecto más robusto
            fieldbackground="white",
            background="#007ACC",	# Color de los botones de las flechas
            foreground="black"
        )
        
        #Selector de numero de palabras clave principales
        tk.Label(control_frame, text="Top palabras clave:", bg="#f5f5f5", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=(15, 5))
        self.top_n_var = tk.IntVar(value=20)
        
        top_spin = ttk.Spinbox(
            control_frame,
            from_=5,
            to=100,
            textvariable=self.top_n_var,
            width=4,
            font=("Arial", 11, "bold")
        )
        top_spin.pack(side=tk.LEFT, padx=5)
        
        #Boton para actualizar grafico si cambia el Top N
        self.btn_reprocesar = tk.Button(
            control_frame,
            text="Actualizar Red",
            command=self.procesar_y_graficar,
            state=tk.DISABLED,
            font=("Arial", 10, "bold")
            )
        self.btn_reprocesar.pack(side=tk.LEFT, padx=10)
        
        #Boton 3: Guardar PNG
        self.btn_guardar = tk.Button(
            control_frame,
            text="📷 Guardar PNG",
            command=self.guardar_grafico,
            state=tk.DISABLED,
            bg="#28A745",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=8,
            pady=3,
            cursor="hand2"
        )
        self.btn_guardar.pack(side=tk.LEFT, padx=10)
        
        # Contenedor para el gráfico
        self.canvas_frame = tk.Frame(self.root, bg="#ffffff")
        self.canvas_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        self.canvas_widget = None
        self.fig = None				#Guardara referencia de la figura actual
        self.document_keywords = []





    def cargar_excel(self):
        # 1. Selección y lectura del archivo Excel
        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo de Palabras Clave",
            filetypes=[("Archivos Excel", "*.xlsx")]
        )

        if not file_path:
            return

        try:
            # Leer el archivo Excel
            df = pd.read_excel(file_path)

            # Asumimos que la columna se llama 'Keywords' o tomamos la primera columna
            col_name = df.columns[0]
            
            # Limpieza y preparación de datos
            self.document_keywords = []
            for cell in df[col_name].dropna():
                
                cell_text = str(cell)
                
                keywords = [kw.strip().lower() for kw in cell_text.split(';') if kw.strip()]
                if keywords:
                    self.document_keywords.append(keywords)
                
                # Separar por ';' y limpiar espacios en blanco
                #keywords = [kw.strip().lower() for kw.strip().split(';') if kw.strip() != '']   
                

            if not self.document_keywords:
                messagebox.showerror("Error", "No se encontraron palabras clave válidas.")
                return
            
            # Generar y mostrar el gráfico
            self.btn_reprocesar.config(state=tk.NORMAL)
            self.procesar_y_graficar()

        except Exception as e:
            messagebox.showerror("Error al procesar", f"Ocurrió un detalle al leer el archivo:\n{e}")




    def procesar_y_graficar(self):
        if not self.document_keywords:
            return

        # Limpiar gráfico previo
        if self.canvas_widget:
            self.canvas_widget.destroy()
            plt.close('all')

        # 1. Contar frecuencias globales de cada palabra clave
        global_counts = Counter()
        for keywords in self.document_keywords:
            global_counts.update(set(keywords))  # Cuenta presencias por documento

        # Obtener el Top N de palabras
        top_n = self.top_n_var.get()
        top_keywords = set([kw for kw, _ in global_counts.most_common(top_n)])

        # 2. Calcular coocurrencias solo entre las palabras del Top N
        edge_counts = Counter()
        for keywords in self.document_keywords:
            # Filtrar las palabras del artículo que pertenecen al top_n
            filtered = [kw for kw in set(keywords) if kw in top_keywords]
            for u, v in combinations(sorted(filtered), 2):
                edge_counts[(u, v)] += 1

        # Build Graph
        G = nx.Graph()
        for kw in top_keywords:
            G.add_node(kw, count=global_counts[kw])

        for (u, v), weight in edge_counts.items():
            G.add_edge(u, v, weight=weight)

        # 3. Dibujar la red
        self.fig, ax = plt.subplots(figsize=(10, 7), facecolor='#ffffff')
        ax.set_title(f"Top {top_n} Palabras Clave y sus Coocurrencias", fontsize=13, fontweight='bold', pad=12)

        # Algoritmo de distribución (k más alto = más separación entre nodos)
        pos = nx.spring_layout(G, k=1.2, seed=42)

        # Tamaños proporcionales a la frecuencia de aparición
        node_sizes = [G.nodes[node]['count'] * 250 for node in G.nodes()]
        
        # Grosor de bordes por frecuencia de coocurrencia
        edges = G.edges()
        weights = [G[u][v]['weight'] for u, v in edges]
        max_w = max(weights) if weights else 1
        edge_widths = [1 + (w / max_w) * 4 for w in weights]

        # Renderizado de bordes y nodos
        nx.draw_networkx_edges(G, pos, ax=ax, alpha=0.35, width=edge_widths, edge_color="#4A5568")
        nx.draw_networkx_nodes(G, pos, ax=ax, node_size=node_sizes, node_color="#3182CE", alpha=0.85)

        # Renderizado de etiquetas con caja semitransparente para mejor lectura
        for node, (x, y) in pos.items():
            ax.text(
                x, y, 
                s=f"{node}\n({G.nodes[node]['count']})", 
                fontsize=8, 
                fontweight='bold',
                ha='center', 
                va='center',
                bbox=dict(boxstyle="round,pad=0.2", facecolor="white", edgecolor="#CBD5E0", alpha=0.85)
            )

        ax.axis('off')

        # Integrar canvas en Tkinter
        canvas = FigureCanvasTkAgg(self.fig, master=self.canvas_frame)
        self.canvas_widget = canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)
        canvas.draw()
        
        # Habilitar botón de guardar cuando el gráfico esté cargado
        self.btn_guardar.config(state=tk.NORMAL)
 
 
 
 
 
    def guardar_grafico(self):
        """Abre un cuadro de dialogo para guardar la imagen de alta definicion."""
        if not self.fig:
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Guardar grafico de red",
            defaultextension=".png",
            filetypes=[("Imagen PNG", "*.png"), ("Imagen JPEG", "*.jpg"), ("Vector PDF", "*.pdf")]
        )
        
        if file_path:
            try:
                # dpi=300 garantiza alta resolución para publicaciones/tesis
                # bbox_inches='tight' recorta los bordes blancos sobrantes
                self.fig.savefig(file_path, dpi=300, bbox_inches='tight')
                messagebox.showinfo("Exito", f"Grafico guardado correctamente en:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar la imagen:\n{e}")




    def on_closing(self):
        """Maneja el cierre limpio de la ventana y termina el proceso Python."""
        plt.close('all')
        self.root.quit()
        self.root.destroy()
    

if __name__ == "__main__":
    root = tk.Tk()
    app = KeywordNetworkApp(root)
    root.mainloop()