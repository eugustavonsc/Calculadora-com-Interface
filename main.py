import tkinter as tk
from tkinter import messagebox
import sys
import os

# Resolve caminho de recurso para rodar tanto no projeto quanto no .exe do PyInstaller.
def obter_caminho_recurso(relativo):
	"""Retorna o caminho absoluto de um arquivo empacotado junto da aplicação."""
	try:
		base_path = sys._MEIPASS
		print(f"Pasta temporária: {base_path}")
	except Exception:
		base_path = os.path.abspath(".")
	return os.path.join(base_path, relativo)


def somar(a, b):
	"""Soma dois valores numéricos."""
	return a + b


def subtrair(a, b):
	"""Subtrai o segundo valor do primeiro."""
	return a - b


def multiplicar(a, b):
	"""Multiplica dois valores numéricos."""
	return a * b


def dividir(a, b):
	"""Divide dois valores e protege contra divisão por zero."""
	if b == 0:
		return "Erro: divisão por zero."
	return a / b

# Classe principal da interface gráfica
class CalculadoraGUI:
	def __init__(self, raiz):
		"""Inicializa estado da calculadora e prepara interface + atalhos."""
		self.raiz = raiz
		self.raiz.title("Calculadora")
		self.raiz.resizable(False, False)

		self.valor_atual = "0"
		self.primeiro_numero = None
		self.operacao = None
		self.novo_numero = True

		self.visor_var = tk.StringVar(value=self.valor_atual)

		self._criar_interface()
		self._configurar_atalhos_teclado()

	# Monta layout, visor e botões.
	def _criar_interface(self):
		self.raiz.configure(bg="#06111f")
		try:
			if sys.platform.startswith("win"):
				# Leve transparência para reforçar visual glass no Windows.
				self.raiz.wm_attributes("-alpha", 0.97)
		except tk.TclError:
			pass

		container = tk.Frame(
			self.raiz,
			bg="#0f1b2c",
			padx=14,
			pady=14,
			highlightthickness=1,
			highlightbackground="#486284",
		)
		container.grid()

		for coluna in range(4):
			container.grid_columnconfigure(coluna, weight=1, minsize=70)
		for linha in range(1, 6):
			container.grid_rowconfigure(linha, weight=1, minsize=60)

		visor = tk.Entry(
			container,
			textvariable=self.visor_var,
			font=("Bahnschrift SemiBold", 24),
			justify="right",
			state="readonly",
			readonlybackground="#0a1524",
			fg="#ecf2ff",
			bd=0,
			relief="flat",
			highlightthickness=1,
			highlightbackground="#385170",
			highlightcolor="#5d87b8",
			width=14,
		)
		visor.grid(row=0, column=0, columnspan=4, pady=(0, 12), ipady=10, sticky="nsew")

		botoes = [
			("C", 1, 0, self.limpar_tudo),
			("+/-", 1, 1, self.inverter_sinal),
			("/", 1, 2, lambda: self.definir_operacao("/")),
			("*", 1, 3, lambda: self.definir_operacao("*")),
			("7", 2, 0, lambda: self.adicionar_digito("7")),
			("8", 2, 1, lambda: self.adicionar_digito("8")),
			("9", 2, 2, lambda: self.adicionar_digito("9")),
			("-", 2, 3, lambda: self.definir_operacao("-")),
			("4", 3, 0, lambda: self.adicionar_digito("4")),
			("5", 3, 1, lambda: self.adicionar_digito("5")),
			("6", 3, 2, lambda: self.adicionar_digito("6")),
			("+", 3, 3, lambda: self.definir_operacao("+")),
			("1", 4, 0, lambda: self.adicionar_digito("1")),
			("2", 4, 1, lambda: self.adicionar_digito("2")),
			("3", 4, 2, lambda: self.adicionar_digito("3")),
			("0", 5, 0, lambda: self.adicionar_digito("0")),
			("=", 5, 3, self.calcular_resultado),
		]

		for texto, linha, coluna, comando in botoes:
			botao = self._criar_botao(container, texto, linha, coluna, comando)
			if texto == "+":
				botao.grid_configure(rowspan=2)

		# O botão decimal ocupa 2 colunas para equilibrar a última linha.
		botao_decimal = self._criar_botao(container, ",", 5, 1, lambda: self.adicionar_digito("."))
		botao_decimal.grid(columnspan=2)

	def _criar_botao(self, container, texto, linha, coluna, comando):
		"""Cria botão padrão da calculadora com estilo e efeito hover."""
		estilo = self._obter_estilo_botao(texto)
		botao = tk.Button(
			container,
			text=texto,
			command=comando,
			font=("Bahnschrift", 14, "bold"),
			fg=estilo["fg"],
			bg=estilo["bg"],
			activeforeground=estilo["fg"],
			activebackground=estilo["active_bg"],
			relief="flat",
			bd=0,
			highlightthickness=0,
			cursor="hand2",
			width=5,
			height=2,
		)
		botao.bind("<Enter>", lambda _evento, b=botao, c=estilo["hover_bg"]: b.configure(bg=c))
		botao.bind("<Leave>", lambda _evento, b=botao, c=estilo["bg"]: b.configure(bg=c))
		botao.grid(row=linha, column=coluna, padx=4, pady=4, sticky="nsew")
		return botao

	def _configurar_atalhos_teclado(self):
		"""Liga atalhos do teclado físico às mesmas ações da interface."""
		self.raiz.bind("<Key>", self._ao_tecla_pressionada)
		self.raiz.bind("<Return>", lambda _evento: self.calcular_resultado())
		self.raiz.bind("<KP_Enter>", lambda _evento: self.calcular_resultado())
		self.raiz.bind("<Escape>", lambda _evento: self.limpar_tudo())
		self.raiz.focus_set()

	def _ao_tecla_pressionada(self, evento):
		"""Interpreta tecla pressionada e redireciona para a ação correta."""
		char = evento.char
		tecla = evento.keysym

		if char in "0123456789":
			self.adicionar_digito(char)
			return "break"

		if char in (".", ","):
			self.adicionar_digito(".")
			return "break"

		if char in "+-*/":
			self.definir_operacao(char)
			return "break"

		if char == "=":
			self.calcular_resultado()
			return "break"

		if tecla == "BackSpace":
			self._apagar_ultimo_digito()
			return "break"

		if tecla == "Delete":
			self.limpar_tudo()
			return "break"

	def _apagar_ultimo_digito(self):
		"""Apaga último caractere do valor atual sem quebrar o estado da tela."""
		if self.novo_numero:
			return

		if len(self.valor_atual) > 1:
			self.valor_atual = self.valor_atual[:-1]
		else:
			self.valor_atual = "0"
			self.novo_numero = True

		if self.valor_atual in ("", "-"):
			self.valor_atual = "0"
			self.novo_numero = True

		self.atualizar_visor()

	@staticmethod
	def _obter_estilo_botao(texto):
		"""Define paleta por tipo de botão (operador, ação, número, igual)."""
		if texto in ("/", "*", "-", "+"):
			return {"bg": "#ea7c2b", "hover_bg": "#ff9342", "active_bg": "#d96e1f", "fg": "#ffffff"}
		if texto == "=":
			return {"bg": "#16a36d", "hover_bg": "#22bc7f", "active_bg": "#0f8b59", "fg": "#ffffff"}
		if texto in ("C", "+/-"):
			return {"bg": "#2a3c57", "hover_bg": "#355178", "active_bg": "#223349", "fg": "#dce8ff"}
		return {"bg": "#1a2a43", "hover_bg": "#233a5c", "active_bg": "#16253b", "fg": "#ecf2ff"}

	def atualizar_visor(self):
		"""Atualiza visor em formato de expressão (ex.: '12 +' e '12 + 3')."""
		valor = self.valor_atual.replace(".", ",")
		if self.operacao:
			if self.primeiro_numero is not None:
				primeiro = self._formatar_numero(self.primeiro_numero).replace(".", ",")
				if self.novo_numero:
					self.visor_var.set(f"{primeiro} {self.operacao}")
				else:
					self.visor_var.set(f"{primeiro} {self.operacao} {valor}")
			else:
				self.visor_var.set(f"{valor} {self.operacao}")
		else:
			self.visor_var.set(valor)

	def adicionar_digito(self, digito):
		"""Adiciona dígito/separador ao valor atual respeitando as regras da calculadora."""
		if self.novo_numero:
			self.valor_atual = "0"
			self.novo_numero = False

		if digito == "." and "." in self.valor_atual:
			return

		if self.valor_atual == "0" and digito != ".":
			self.valor_atual = digito
		else:
			self.valor_atual += digito

		self.atualizar_visor()

	def inverter_sinal(self):
		"""Alterna o sinal do número atual (positivo/negativo)."""
		if self.valor_atual == "0":
			return
		if self.valor_atual.startswith("-"):
			self.valor_atual = self.valor_atual[1:]
		else:
			self.valor_atual = "-" + self.valor_atual
		self.atualizar_visor()

	def definir_operacao(self, operacao):
		"""Armazena operação pendente e prepara entrada do próximo número."""
		if self.operacao and not self.novo_numero:
			# Permite encadear operações (ex.: 2 + 3 * 4) mantendo fluxo simples.
			self.calcular_resultado()

		try:
			self.primeiro_numero = float(self.valor_atual)
		except ValueError:
			self.primeiro_numero = 0.0

		self.operacao = operacao
		self.novo_numero = True
		self.atualizar_visor()

	def calcular_resultado(self):
		"""Executa a operação atual com os dois operandos e mostra no visor."""
		if self.operacao is None or self.primeiro_numero is None:
			return

		try:
			segundo_numero = float(self.valor_atual)
		except ValueError:
			segundo_numero = 0.0

		if self.operacao == "+":
			resultado = somar(self.primeiro_numero, segundo_numero)
		elif self.operacao == "-":
			resultado = subtrair(self.primeiro_numero, segundo_numero)
		elif self.operacao == "*":
			resultado = multiplicar(self.primeiro_numero, segundo_numero)
		else:
			resultado = dividir(self.primeiro_numero, segundo_numero)

		if isinstance(resultado, str):
			messagebox.showerror("Erro", resultado)
			self.limpar_tudo()
			return

		self.valor_atual = self._formatar_numero(resultado)
		self.primeiro_numero = resultado
		self.operacao = None
		self.novo_numero = True
		self.atualizar_visor()

	def limpar_tudo(self):
		"""Reseta o estado da calculadora e volta o visor para zero."""
		self.valor_atual = "0"
		self.primeiro_numero = None
		self.operacao = None
		self.novo_numero = True
		self.atualizar_visor()

	@staticmethod
	def _formatar_numero(numero):
		"""Formata saída para evitar ruído de ponto flutuante no visor."""
		# Suaviza artefatos comuns de ponto flutuante e evita exibir -0.
		numero = round(numero, 10)
		if abs(numero) < 1e-10:
			numero = 0.0

		if numero == int(numero):
			return str(int(numero))

		texto = f"{numero:.10f}".rstrip("0").rstrip(".")
		return texto


# Ponto de entrada da aplicação: cria janela, aplica ícone e inicia loop da UI.
def iniciar_calculadora():
	"""Inicializa janela principal e inicia o loop da interface."""

	root = tk.Tk()

	caminho_icone = obter_caminho_recurso("calculadora_pro.ico")

	if os.path.exists(caminho_icone):
		try:
			root.iconbitmap(caminho_icone)
		except Exception as e:
			try:
				img = tk.PhotoImage(file=caminho_icone)
				root.tk.call('wm', 'iconphoto', root._w, img)
			except:
				print(f"Erro ao carregar ícone: {e}")
	else:
		# Mantém execução normal mesmo sem ícone, útil em ambientes de build/teste.
		print("Aviso: Ficheiro de ícone não encontrado no caminho:", caminho_icone)

	CalculadoraGUI(root)

	root.mainloop()

if __name__ == "__main__":
    iniciar_calculadora()
