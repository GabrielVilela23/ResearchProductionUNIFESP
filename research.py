import os
from google.cloud import bigquery
import customtkinter as ctk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import pandas as pd

# Construir o caminho para o arquivo de credenciais automaticamente
current_dir = os.path.dirname(os.path.abspath(_file_))
credentials_path = os.path.join(current_dir, 'credenciais.json')
print(credentials_path)

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path

def manipula():
    def executar_insercao():
        sql_query = query_textbox.get("1.0", "end-1c")
        client = bigquery.Client()

        try:
            query_job = client.query(sql_query)
            query_job.result()
            messagebox.showinfo("Sucesso", "O comando SQL foi executado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", str(e))
    app = ctk.CTkToplevel()
    app.title("Manipulação de Dados no BigQuery")
    app.geometry("370x410")
    ctk.set_appearance_mode("dark")

    query_textbox = ctk.CTkTextbox(app, width=300, height=200)
    query_textbox.pack(pady=20)

    send_button = ctk.CTkButton(app, text="Enviar Comando de Manipulação SQL", command=executar_insercao, width=200, height=60)
    send_button.pack(pady=5)

    image_path = os.path.join(current_dir, "imagem.png")
    image = Image.open(image_path)
    photo = ImageTk.PhotoImage(image)

    image_label = ctk.CTkLabel(app, image=photo, text="")
    #image_label.image = photo 
    image_label.pack(side="right", anchor="se", padx=10, pady=10)

    image2_path = os.path.join(current_dir, "imagem2.png")
    image2 = Image.open(image2_path)
    photo2 = ImageTk.PhotoImage(image2)

    image2_label = ctk.CTkLabel(app, image=photo2, text="")
    #image2_label.image = photo2 
    image2_label.pack(side="left", anchor="sw", padx=10, pady=20)

    app.mainloop()

def consulta():
    def executar_consulta():
        sql_query = query_textbox.get("1.0", "end-1c")
        client = bigquery.Client()

        try:
            query_job = client.query(sql_query)
            results = query_job.result()

            output_file = 'resultado_consulta.csv'

            rows = [dict(row) for row in results]
            df = pd.DataFrame(rows)
            df.to_csv(output_file, index=False, encoding='utf-8-sig')

            mostrar_resultados(df)

        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def mostrar_resultados(df):
        result_window = ctk.CTkToplevel()
        result_window.title("Resultados da Consulta")
        result_window.geometry("500x500")

        tree = ttk.Treeview(result_window)
        tree.pack(expand=True, fill="both")

        tree["column"] = list(df.columns)
        tree["show"] = "headings"

        for col in df.columns:
            tree.heading(col, text=col, anchor="center")
            tree.column(col, minwidth=50, width=100, anchor="center")

        for index, row in df.iterrows():
            tree.insert("", "end", values=list(row))

    app = ctk.CTkToplevel()
    app.title("Visualização de Dados no BigQuery")
    app.geometry("370x410")

    ctk.set_appearance_mode("dark")

    query_textbox = ctk.CTkTextbox(app, width=300, height=200)
    query_textbox.pack(pady=20)

    send_button = ctk.CTkButton(app, text="Enviar Comando de Visualização SQL", command=executar_consulta,  width=200, height=60)
    send_button.pack(pady=5)

    image_path = os.path.join(current_dir, "imagem.png")
    image = Image.open(image_path)
    photo = ImageTk.PhotoImage(image)

    image_label = ctk.CTkLabel(app, image=photo, text="")
    image_label.image = photo  # Para evitar que a imagem seja coletada pelo garbage collector
    image_label.pack(side="right", anchor="se", padx=10, pady=10)

    image2_path = os.path.join(current_dir, "imagem2.png")
    image2 = Image.open(image2_path)
    photo2 = ImageTk.PhotoImage(image2)

    image2_label = ctk.CTkLabel(app, image=photo2, text="")
    image2_label.image = photo2  # Para evitar que a imagem seja coletada pelo garbage collector
    image2_label.pack(side="left", anchor="sw", padx=10, pady=20)

    app.mainloop()

def main_menu():
    app = ctk.CTk()
    app.title("Menu Principal")
    app.geometry("270x380")
    ctk.set_appearance_mode("dark")

    manipula_button = ctk.CTkButton(app, text="Manipulação de Dados", command=manipula, width=200, height=100)
    manipula_button.pack(pady=20)

    consulta_button = ctk.CTkButton(app, text="Visualização de Dados", command=consulta, width=200, height=100)
    consulta_button.pack(pady=7)

    # Adicionando o label no centro inferior
    credit_label = ctk.CTkLabel(app, text=(
        "Projeto desenvolvido por:\nGabriel Vilela\nLivia Canuto\nJoão Pedro Mariano\nGabrielly Vieira\n\nCom auxilio da Profª Drª Daniela Musa"
    ))
    credit_label.pack(side="bottom", pady=10)

    app.mainloop()

main_menu()