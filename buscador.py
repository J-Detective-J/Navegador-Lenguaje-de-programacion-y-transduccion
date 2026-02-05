import tkinter as tk
import requests

# ----------------- Estado -----------------
back_stack, forward_stack = [], []
current_query = None

# ----------------- Funciones Auxiliares -----------------
def update_entry(query):
    entry.delete(0, tk.END)
    entry.insert(0, query)

def navigate(direction):
    global current_query
    source_stack = forward_stack if direction == "forward" else back_stack
    target_stack = back_stack if direction == "forward" else forward_stack
    
    if not source_stack:
        text.insert(tk.END, f"No hay páginas para ir hacia {direction}\n")
        return
    
    if current_query:
        target_stack.append(current_query)
    
    current_query = source_stack.pop()
    update_entry(current_query)
    load_results(current_query)

# ----------------- Lógica Principal -----------------
def search(query=None):
    global current_query
    query = query or entry.get() # Usa parámetro o contenido del campo
    
    if not query:
        return
    
    if current_query:
        back_stack.append(current_query)
    
    forward_stack.clear()
    current_query = query
    load_results(query)

def load_results(query):
    text.delete(1.0, tk.END)
    
    try:
        response = requests.get("https://api.duckduckgo.com/", 
                               params={"q": query, "format": "json", "no_redirect": 1, 
                                      "no_html": 1, "kl": "es-es"}, timeout=5)
        results = response.json().get("RelatedTopics", [])
        
        if not results:
            text.insert(tk.END, "No se encontraron resultados\n")
            return
            
        for item in results:
            if "Text" in item:
                text.insert(tk.END, f"• {item['Text']}\n\n")
    except Exception as e:
        text.insert(tk.END, f"Error: {e}\n")

def autocomplete(event):
    query = entry.get()
    listbox.delete(0, tk.END)
    
    if len(query) < 2:
        return
    
    try:
        response = requests.get("https://duckduckgo.com/ac/", params={"q": query})
        for item in response.json():
            listbox.insert(tk.END, item["phrase"])
    except:
        pass

def select_autocomplete(event):
    if listbox.curselection():
        entry.delete(0, tk.END)
        entry.insert(0, listbox.get(listbox.curselection()))
        listbox.delete(0, tk.END)
        search()

def show_recommendations():
    text.delete(1.0, tk.END)
    query = entry.get().strip()
    
    if len(query) < 2:
        text.insert(tk.END, "Escribe al menos 2 letras\n")
        return
    
    try:
        response = requests.get(
            "https://es.wikipedia.org/w/api.php",
            params={"action": "opensearch", "search": query, "limit": 6, 
                   "namespace": 0, "format": "json"},
            headers={"User-Agent": "SimpleBrowser/1.0"},
            timeout=5
        )
        
        sugerencias = response.json()[1]
        
        if len(sugerencias) <= 1:
            text.insert(tk.END, "No se encontraron recomendaciones\n")
            return
        
        text.tag_configure("bold", font=("Arial", 10, "bold"))
        text.insert(tk.END, "Los usuarios que compraron ")
        text.insert(tk.END, f'"{query}"', "bold")
        text.insert(tk.END, " compraron también:\n\n")
        
        for item in sugerencias[1:]:
            text.insert(tk.END, f"• {item}\n")
    except Exception as e:
        text.insert(tk.END, f"Error: {e}\n")

# ----------------- UI Helper -----------------
def create_button(parent, text, command, **kwargs):
    defaults = {
        "font": ("Arial", 11, "bold"),
        "relief": "flat",
        "bd": 0,
        "highlightthickness": 0
    }
    defaults.update(kwargs)
    return tk.Button(parent, text=text, command=command, **defaults)

def add_hover_effect(button, normal_color, hover_color):
    button.bind("<Enter>", lambda e: e.widget.config(bg=hover_color))
    button.bind("<Leave>", lambda e: e.widget.config(bg=normal_color))

# ----------------- Interfaz -----------------
root = tk.Tk()
root.title("Buscador")
root.geometry("700x600")

main_frame = tk.Frame(root)
main_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Top Frame (Navegación + Búsqueda)
top_frame = tk.Frame(main_frame)
top_frame.pack(fill=tk.X, pady=(0, 10))

# Botones de navegación
nav_frame = tk.Frame(top_frame)
nav_frame.pack(side=tk.LEFT)

back_btn = create_button(nav_frame, "←", lambda: navigate("back"), 
                        width=3, height=1, bg="#f0f0f0", font=("Arial", 12, "bold"))
back_btn.pack(side=tk.LEFT, padx=(0, 5))
add_hover_effect(back_btn, "#f0f0f0", "#e0e0e0")

forward_btn = create_button(nav_frame, "→", lambda: navigate("forward"), 
                           width=3, height=1, bg="#f0f0f0", font=("Arial", 12, "bold"))
forward_btn.pack(side=tk.LEFT)
add_hover_effect(forward_btn, "#f0f0f0", "#e0e0e0")

# Barra de búsqueda
search_frame = tk.Frame(top_frame)
search_frame.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)

entry = tk.Entry(search_frame, width=40, font=("Arial", 11))
entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
entry.bind("<Return>", lambda e: search())

search_btn = create_button(search_frame, "🔍", search, 
                          width=3, height=1, bg="#4CAF50", fg="white")
search_btn.pack(side=tk.LEFT, padx=(5, 0))
add_hover_effect(search_btn, "#4CAF50", "#45a049")

# Autocompletado
listbox = tk.Listbox(main_frame, height=5, font=("Arial", 10))
listbox.pack(fill=tk.X, pady=(0, 10))
listbox.bind("<<ListboxSelect>>", select_autocomplete)

# Botón Recomendaciones
recom_btn = create_button(main_frame, "🔄 Recomendaciones", show_recommendations,
                         bg="#2196F3", fg="white", padx=20, pady=8)
recom_btn.pack(pady=(0, 10))
add_hover_effect(recom_btn, "#2196F3", "#1976D2")

# Área de resultados
text = tk.Text(main_frame, wrap=tk.WORD, height=20, font=("Arial", 10),
               bg="white", relief="flat", bd=1, highlightthickness=1, 
               highlightbackground="#ccc")
text.pack(fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(text)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
text.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=text.yview)

# Eventos
entry.bind("<KeyRelease>", autocomplete)

root.mainloop()