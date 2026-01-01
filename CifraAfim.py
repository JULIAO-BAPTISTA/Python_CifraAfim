# =====================================================
# Cifra de César Afim com Tkinter + ttk
# Inclui:
# - Botão Limpar
# - Validação dos campos
# - Programação Orientada a Objetos
# =====================================================

import tkinter as tk
from tkinter import ttk, messagebox
import math


class CifraCesarAfim:
    """
    Classe responsável pela lógica da cifra de César Afim
    """

    def __init__(self, a, b):
        """
        Construtor da classe
        :param a: multiplicador (deve ser coprimo com 26)
        :param b: deslocamento
        """
        self.a = a
        self.b = b

        # Verifica se 'a' é válido
        if math.gcd(self.a, 26) != 1:
            raise ValueError("O valor de 'a' deve ser coprimo com 26. Os valores Coprimos de 26 são: 1,3,5,7,9,11,15,17,19,21,23,25")

        # Calcula o inverso multiplicativo de 'a'
        self.inv_a = self._inverso_modular(self.a, 26)

    def _inverso_modular(self, a, m):
        """
        Calcula o inverso multiplicativo de 'a' módulo 'm'
        """
        for i in range(m):
            if (a * i) % m == 1:
                return i
        return None

    def encriptar(self, texto):
        """
        Encripta o texto
        """
        resultado = ""

        for char in texto:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                p = ord(char) - base
                c = (self.a * p + self.b) % 26
                resultado += chr(c + base)
            else:
                resultado += char

        return resultado

    def decriptar(self, texto):
        """
        Decripta o texto
        """
        resultado = ""

        for char in texto:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                c = ord(char) - base
                p = (self.inv_a * (c - self.b)) % 26
                resultado += chr(p + base)
            else:
                resultado += char

        return resultado


class AplicacaoGUI:
    """
    Classe responsável pela interface gráfica
    """

    def __init__(self, root):
        self.root = root
        self.root.title("Cifra de César Afim")
        self.root.geometry("500x450")
        self.root.resizable(False, False)

        # Estilo ttk
        style = ttk.Style()
        style.theme_use("clam")

        # ================== TÍTULO ==================
        ttk.Label(
            root,
            text="Cifra de César Afim",
            font=("Arial", 16, "bold")
        ).pack(pady=10)

        # ================== FRAME DE PARÂMETROS ==================
        frame_params = ttk.LabelFrame(root, text="Parâmetros da Cifra")
        frame_params.pack(fill="x", padx=20, pady=5)

        ttk.Label(frame_params, text="Valor de a (coprimo com 26):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_a = ttk.Entry(frame_params, width=10)
        self.entry_a.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_params, text="Valor de b:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_b = ttk.Entry(frame_params, width=10)
        self.entry_b.grid(row=1, column=1, padx=5, pady=5)

        # ================== TEXTO DE ENTRADA ==================
        ttk.Label(root, text="Texto de entrada:").pack(pady=5)
        self.text_entrada = tk.Text(root, height=4)
        self.text_entrada.pack(fill="x", padx=20)

        # ================== BOTÕES ==================
        frame_botoes = ttk.Frame(root)
        frame_botoes.pack(pady=10)

        ttk.Button(frame_botoes, text="Encriptar", command=self.encriptar).grid(row=0, column=0, padx=5)
        ttk.Button(frame_botoes, text="Decriptar", command=self.decriptar).grid(row=0, column=1, padx=5)
        ttk.Button(frame_botoes, text="Limpar", command=self.limpar).grid(row=0, column=2, padx=5)

        # ================== TEXTO DE SAÍDA ==================
        ttk.Label(root, text="Resultado:").pack(pady=5)
        self.text_saida = tk.Text(root, height=4)
        self.text_saida.pack(fill="x", padx=20)

    # =====================================================
    # Validação e operações
    # =====================================================

    def validar_campos(self):
        """
        Valida se os campos estão corretamente preenchidos
        """
        if not self.entry_a.get() or not self.entry_b.get():
            messagebox.showwarning("Aviso", "Preencha os valores de a e b.")
            return None

        if not self.entry_a.get().isdigit() or not self.entry_b.get().isdigit():
            messagebox.showerror("Erro", "Os valores de a e b devem ser números inteiros.")
            return None

        texto = self.text_entrada.get("1.0", tk.END).strip()
        if not texto:
            messagebox.showwarning("Aviso", "Digite um texto para processar.")
            return None

        try:
            a = int(self.entry_a.get())
            b = int(self.entry_b.get())
            return CifraCesarAfim(a, b)
        except ValueError as erro:
            messagebox.showerror("Erro", str(erro))
            return None

    def encriptar(self):
        """
        Ação do botão Encriptar
        """
        cifra = self.validar_campos()
        if cifra:
            texto = self.text_entrada.get("1.0", tk.END).strip()
            resultado = cifra.encriptar(texto)
            self.mostrar_resultado(resultado)

    def decriptar(self):
        """
        Ação do botão Decriptar
        """
        cifra = self.validar_campos()
        if cifra:
            texto = self.text_entrada.get("1.0", tk.END).strip()
            resultado = cifra.decriptar(texto)
            self.mostrar_resultado(resultado)

    def mostrar_resultado(self, texto):
        """
        Mostra o resultado no campo de saída
        """
        self.text_saida.delete("1.0", tk.END)
        self.text_saida.insert(tk.END, texto)

    def limpar(self):
        """
        Limpa todos os campos da interface
        """
        self.entry_a.delete(0, tk.END)
        self.entry_b.delete(0, tk.END)
        self.text_entrada.delete("1.0", tk.END)
        self.text_saida.delete("1.0", tk.END)


# =====================================================
# Execução do programa
# =====================================================

if __name__ == "__main__":
    root = tk.Tk()
    app = AplicacaoGUI(root)
    root.mainloop()
