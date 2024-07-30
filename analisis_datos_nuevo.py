import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import folium
from folium.plugins import HeatMap
import webbrowser
import seaborn as sns

sns.set(style="whitegrid")

# Datos de coordenadas por departamento
data = {
    'Ubicacion': ['Lima', 'Callao', 'Arequipa', 'Trujillo', 'Chiclayo', 'Piura', 'Huancayo', 'Iquitos', 'Pucallpa', 'Chimbote', 'Tacna', 'Ica', 'Juliaca', 'Cusco', 'Cajamarca', 'Huánuco', 'Sullana', 'Ayacucho', 'Puno', 'Puerto Maldonado'],
    'Latitud': [-12.04318, -12.05659, -16.39889, -8.11599, -6.77137, -5.19449, -12.06513, -3.74912, -8.37915, -9.07508, -18.01465, -14.06777, -15.5, -13.52264, -7.16378, -9.93062, -4.90389, -13.15878, -15.8422, -12.59331],
    'Longitud': [-77.02824, -77.11814, -71.535, -79.02998, -79.84088, -80.63282, -75.20486, -73.25383, -74.55387, -78.59373, -70.25362, -75.72861, -70.13333, -71.96734, -78.50027, -76.24223, -80.68528, -74.22321, -70.0199, -69.18913]
}

df_coordinates = pd.DataFrame(data)

class DataAnalysisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Análisis de Datos de Accidentes de Tránsito")
        self.root.geometry("800x600")
        self.df = None

        # Crear un marco para los botones de carga de datos y gráficos
        self.control_frame = tk.Frame(root, bg='lightgray', pady=10)
        self.control_frame.pack(fill=tk.X)

        # Crear un marco para mostrar los gráficos
        self.display_frame = tk.Frame(root)
        self.display_frame.pack(fill=tk.BOTH, expand=True)

        # Botones para cargar datos y mostrar gráficos
        self.load_button = tk.Button(self.control_frame, text="Cargar Datos", command=self.load_data, bg='#007BFF', fg='white', font=('Arial', 12, 'bold'))
        self.load_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.add_data_button = tk.Button(self.control_frame, text="Agregar Datos", command=self.add_data, state=tk.DISABLED, bg='#28A745', fg='white', font=('Arial', 12, 'bold'))
        self.add_data_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.search_data_button = tk.Button(self.control_frame, text="Buscar Datos de Persona", command=self.search_data, state=tk.DISABLED, bg='#28A745', fg='white', font=('Arial', 12, 'bold'))
        self.search_data_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.plot_buttons = {
            "Clase de Siniestro": tk.Button(self.control_frame, text="Gráfico de Clases de Siniestro", command=self.plot_class_of_accident, state=tk.DISABLED, bg='#17A2B8', fg='white', font=('Arial', 12, 'bold')),
            "Gravedad": tk.Button(self.control_frame, text="Gráfico de Gravedad", command=self.plot_gravity, state=tk.DISABLED, bg='#17A2B8', fg='white', font=('Arial', 12, 'bold')),
            "Tendencias Temporales": tk.Button(self.control_frame, text="Tendencias Temporales", command=self.plot_temporal_trends, state=tk.DISABLED, bg='#17A2B8', fg='white', font=('Arial', 12, 'bold')),
            "Distribución de Edades": tk.Button(self.control_frame, text="Distribución de Edades", command=self.plot_age_distribution, state=tk.DISABLED, bg='#17A2B8', fg='white', font=('Arial', 12, 'bold')),
            "Distribución de Sexo": tk.Button(self.control_frame, text="Distribución de Sexo", command=self.plot_sex_distribution, state=tk.DISABLED, bg='#17A2B8', fg='white', font=('Arial', 12, 'bold')),
            "Mapa de Calor": tk.Button(self.control_frame, text="Mapa de Calor", command=self.plot_heatmap, state=tk.DISABLED, bg='#17A2B8', fg='white', font=('Arial', 12, 'bold'))
        }

        for button in self.plot_buttons.values():
            button.pack(side=tk.LEFT, padx=5, pady=5)

        self.clear_button = tk.Button(self.control_frame, text="Limpiar", command=self.clear_display, state=tk.DISABLED, bg='#DC3545', fg='white', font=('Arial', 12, 'bold'))
        self.clear_button.pack(side=tk.LEFT, padx=5, pady=5)



        self.result_label = tk.Label(root, text="", wraplength=600, font=('Arial', 12))
        self.result_label.pack(pady=10)

    def load_data(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Archivos CSV", "*.csv")],
            title="Selecciona el archivo CSV"
        )
        if file_path:
            try:
                self.df = pd.read_csv(file_path, sep=';', encoding='utf-8')
                self.result_label.config(text=f"Datos cargados exitosamente.\nColumnas disponibles: {', '.join(self.df.columns)}")
                self.add_data_button.config(state=tk.NORMAL)
                self.search_data_button.config(state=tk.NORMAL)
                for button in self.plot_buttons.values():
                    button.config(state=tk.NORMAL)
                self.clear_button.config(state=tk.NORMAL)
            except Exception as e:
                messagebox.showerror("Error", f"Error al cargar los datos: {e}")

    def add_data(self):
        if self.df is not None:
            try:
                # Solicitar datos al usuario
                new_row = {col: simpledialog.askstring("Entrada", col) for col in self.df.columns}
                new_row['EDAD'] = simpledialog.askinteger("Entrada", "Edad")
                
                # Añadir nueva fila al DataFrame
                self.df = self.df.append(new_row, ignore_index=True)
                messagebox.showinfo("Éxito", "Datos añadidos exitosamente.")
            except Exception as e:
                messagebox.showerror("Error", f"Error al añadir datos: {e}")

    def search_data(self):
        if self.df is not None:
            try:
                code = simpledialog.askstring("Buscar Datos de Persona", "Ingrese el Código de Persona:")
                if code:
                    code = code.strip()  # Eliminar espacios en blanco alrededor
                    if 'CÓDIGO PERSONA' in self.df.columns:
                        person_data = self.df[self.df['CÓDIGO PERSONA'].astype(str) == code]
                        if not person_data.empty:
                            person_info = ""
                            for col in person_data.columns:
                                person_info += f"{col}: {person_data.iloc[0][col]}\n"
                            self.show_person_data(person_info)
                        else:
                            self.result_label.config(text="No se encontraron datos para el código de persona proporcionado.")
                    else:
                        self.result_label.config(text="La columna 'CÓDIGO PERSONA' no se encuentra en los datos cargados.")
            except Exception as e:
                messagebox.showerror("Error", f"Error al buscar datos de persona: {e}")

    def show_person_data(self, person_info):
        person_window = tk.Toplevel(self.root)
        person_window.title("Datos de la Persona")
        person_window.geometry("400x400")
        label = tk.Label(person_window, text=person_info, justify=tk.LEFT, wraplength=380, font=('Arial', 12))
        label.pack(pady=10)

    def plot_class_of_accident(self):
        if self.df is not None:
            try:
                fig, ax = plt.subplots(figsize=(10, 6))
                self.df['CLASE DE SINIESTRO'].value_counts().plot(kind='bar', color='skyblue', ax=ax)
                ax.set_title('Frecuencia de Clases de Siniestro')
                ax.set_xlabel('Clase de Siniestro')
                ax.set_ylabel('Cantidad')
                plt.xticks(rotation=45)
                self.display_plot(fig)
            except KeyError:
                messagebox.showerror("Error", "Columna 'CLASE DE SINIESTRO' no encontrada.")
            except Exception as e:
                messagebox.showerror("Error", f"Error al mostrar gráfico de Clase de Siniestro: {e}")

    def plot_gravity(self):
        if self.df is not None:
            try:
                fig, ax = plt.subplots(figsize=(10, 6))
                self.df['GRAVEDAD'].value_counts().plot(kind='bar', color='salmon', ax=ax)
                ax.set_title('Frecuencia de Gravedad de Accidentes')
                ax.set_xlabel('Gravedad')
                ax.set_ylabel('Cantidad')
                plt.xticks(rotation=45)
                self.display_plot(fig)
            except KeyError:
                messagebox.showerror("Error", "Columna 'GRAVEDAD' no encontrada.")
            except Exception as e:
                messagebox.showerror("Error", f"Error al mostrar gráfico de Gravedad: {e}")

    def plot_temporal_trends(self):
        if self.df is not None:
            try:
                self.df['FECHA'] = pd.to_datetime(self.df['FECHA'], errors='coerce')
                temp_trends = self.df.groupby(self.df['FECHA'].dt.to_period('M')).size()
                fig, ax = plt.subplots(figsize=(10, 6))
                temp_trends.plot(kind='bar', color='lightgreen', ax=ax)
                ax.set_title('Tendencias Temporales de Accidentes')
                ax.set_xlabel('Fecha')
                ax.set_ylabel('Cantidad de Accidentes')
                plt.xticks(rotation=45)
                self.display_plot(fig)
            except KeyError:
                messagebox.showerror("Error", "Columna 'FECHA' no encontrada.")
            except Exception as e:
                messagebox.showerror("Error", f"Error al mostrar tendencias temporales: {e}")

    def plot_age_distribution(self):
        if self.df is not None:
            try:
                fig, ax = plt.subplots(figsize=(10, 6))
                self.df['EDAD'] = pd.to_numeric(self.df['EDAD'], errors='coerce')
                self.df['EDAD'].plot(kind='hist', bins=range(0, 101, 5), color='purple', ax=ax)
                ax.set_title('Distribución de Edades de Involucrados')
                ax.set_xlabel('Edad')
                ax.set_ylabel('Cantidad')
                plt.xticks(range(0, 101, 5))
                self.display_plot(fig)
            except KeyError:
                messagebox.showerror("Error", "Columna 'EDAD' no encontrada.")
            except Exception as e:
                messagebox.showerror("Error", f"Error al mostrar distribución de edades: {e}")

    def plot_sex_distribution(self):
        if self.df is not None:
            try:
                fig, ax = plt.subplots(figsize=(10, 6))
                self.df['SEXO'].value_counts().plot(kind='pie', autopct='%1.1f%%', colors=['lightblue', 'lightcoral', 'lightgreen'], ax=ax)
                ax.set_title('Distribución por Sexo de Involucrados')
                ax.set_ylabel('')
                self.display_plot(fig)
            except KeyError:
                messagebox.showerror("Error", "Columna 'SEXO' no encontrada.")
            except Exception as e:
                messagebox.showerror("Error", f"Error al mostrar distribución de sexo: {e}")

    def plot_heatmap(self):
        if self.df is not None:
            try:
                              # Crear el mapa
                m = folium.Map(location=[-9.19, -75.0152], zoom_start=6)

            
                # Agregar el mapa de calor usando las coordenadas proporcionadas
                heat_data = [[row['Latitud'], row['Longitud']] for _, row in df_coordinates.iterrows()]
                HeatMap(heat_data).add_to(m)
                
                # Guardar el mapa en un archivo HTML
                map_file = "heatmap.html"
                m.save(map_file)
                
                # Abrir el mapa en el navegador predeterminado
                webbrowser.open(map_file)
           
            except Exception as e:
                messagebox.showerror("Error", f"Error al mostrar el mapa de calor: {e}")
                messagebox.showerror("Error", f"Error al mostrar el mapa de calor: {e}")

    def display_plot(self, fig):
        for widget in self.display_frame.winfo_children():
            widget.destroy()
        canvas = FigureCanvasTkAgg(fig, master=self.display_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def clear_display(self):
        for widget in self.display_frame.winfo_children():
            widget.destroy()
        self.result_label.config(text="")

    def go_back(self):
        self.clear_display()
        self.result_label.config(text="")

if __name__ == "__main__":
    root = tk.Tk()
    app = DataAnalysisApp(root)
    root.mainloop()
