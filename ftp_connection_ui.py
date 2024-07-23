import os
from ftplib import FTP
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# Función para subir archivos al servidor FTP


def upload_files_to_ftp(ftp_host, ftp_user, ftp_pass, ftp_dir, local_base_dir):
    try:
        ftp = FTP(ftp_host)
        ftp.login(user=ftp_user, passwd=ftp_pass)
        ftp.cwd(ftp_dir)

        local_files = os.listdir(local_base_dir)
        uploaded_files = []
        failed_files = []

        total_files = len(local_files)
        progress_bar['maximum'] = total_files

        for i, file_name in enumerate(local_files):
            local_file_path = os.path.join(local_base_dir, file_name)
            if os.path.isfile(local_file_path):
                try:
                    with open(local_file_path, 'rb') as local_file:
                        ftp.storbinary(f'STOR {file_name}', local_file)
                        uploaded_files.append(file_name)
                        print(f"Archivo subido: {file_name}")
                except Exception as e:
                    failed_files.append((file_name, str(e)))
                    print(f"Error al subir {file_name}: {e}")

            # Actualizar barra de progreso
            progress_bar['value'] = i + 1
            root.update_idletasks()

        ftp.quit()

        # Mostrar resumen
        resumen = f"Archivos subidos correctamente: {len(uploaded_files)}\n"
        resumen += f"Archivos fallidos: {len(failed_files)}\n\n"

        if failed_files:
            resumen += "Detalles de archivos fallidos:\n"
            for file_name, error in failed_files:
                resumen += f"{file_name}: {error}\n"

        messagebox.showinfo("Resumen de la Subida", resumen)

    except Exception as e:
        messagebox.showerror("Error en la conexión FTP", str(e))

# Función para seleccionar la carpeta local


def select_local_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        local_folder_var.set(folder_selected)


# Crear la ventana principal
root = tk.Tk()
root.title("Subir Archivos a FTP")

# Variables
ftp_host_var = tk.StringVar()
ftp_user_var = tk.StringVar()
ftp_pass_var = tk.StringVar()
ftp_dir_var = tk.StringVar(value='/')
local_folder_var = tk.StringVar()

# Etiquetas y campos de entrada
tk.Label(root, text="FTP Host:").grid(
    row=0, column=0, padx=10, pady=5, sticky='e')
tk.Entry(root, textvariable=ftp_host_var).grid(
    row=0, column=1, padx=10, pady=5)

tk.Label(root, text="FTP Usuario:").grid(
    row=1, column=0, padx=10, pady=5, sticky='e')
tk.Entry(root, textvariable=ftp_user_var).grid(
    row=1, column=1, padx=10, pady=5)

tk.Label(root, text="FTP Contraseña:").grid(
    row=2, column=0, padx=10, pady=5, sticky='e')
tk.Entry(root, textvariable=ftp_pass_var,
         show='*').grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Directorio en FTP:").grid(
    row=3, column=0, padx=10, pady=5, sticky='e')
tk.Entry(root, textvariable=ftp_dir_var).grid(row=3, column=1, padx=10, pady=5)

tk.Label(root, text="Carpeta Local:").grid(
    row=4, column=0, padx=10, pady=5, sticky='e')
tk.Entry(root, textvariable=local_folder_var).grid(
    row=4, column=1, padx=10, pady=5)
tk.Button(root, text="Seleccionar", command=select_local_folder).grid(
    row=4, column=2, padx=10, pady=5)

# Barra de progreso
tk.Label(root, text="Progreso:").grid(
    row=5, column=0, padx=10, pady=5, sticky='e')
progress_bar = ttk.Progressbar(
    root, orient='horizontal', length=300, mode='determinate')
progress_bar.grid(row=5, column=1, columnspan=2, padx=10, pady=5)

# Botón para iniciar la subida de archivos
tk.Button(root, text="Subir Archivos", command=lambda: upload_files_to_ftp(
    ftp_host_var.get(),
    ftp_user_var.get(),
    ftp_pass_var.get(),
    ftp_dir_var.get(),
    local_folder_var.get()
)).grid(row=6, column=0, columnspan=3, pady=10)

# Iniciar el bucle de eventos
root.mainloop()
