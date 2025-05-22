from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.utils import ImageReader  # Para ler imagem
import os

PAGE_WIDTH, PAGE_HEIGHT = A4

# Margens ABNT
MARGIN_LEFT = 3 * cm
MARGIN_RIGHT = 2 * cm
MARGIN_TOP = 3 * cm
MARGIN_BOTTOM = 2 * cm

# Área de texto útil
usable_width = PAGE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT
usable_height = PAGE_HEIGHT - MARGIN_TOP - MARGIN_BOTTOM

# Estilos
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="ABNT", fontName="Times-Roman", fontSize=12, leading=14))

# Conteúdo de exemplo
conteudo = [
    "Universidade XYZ",
    "Curso de Ciência da Computação",
    "Disciplina: Projeto de Pesquisa",
    "",
    "Título: Estudo sobre ReportLab com Margens ABNT",
    "",
    "Este é um exemplo de documento PDF gerado com Python e ReportLab, "
    "seguindo as margens padrão da ABNT para trabalhos acadêmicos."
]

# Caminho da imagem do cabeçalho
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HEADER_IMAGE_PATH = os.path.join(BASE_DIR, "images", "Header.png")
HEADER_HEIGHT = 4 * cm  # Ajuste conforme necessário

# Função para desenhar grid e cabeçalho com imagem
def draw_grid(canvas: Canvas, doc):
    canvas.saveState()

    # Desenhar retângulo da área útil (grid de margens)
    canvas.setStrokeColorRGB(1, 0, 0)
    canvas.setLineWidth(0.5)
    canvas.rect(MARGIN_LEFT, MARGIN_BOTTOM, usable_width, usable_height)

    # Desenhar imagem do cabeçalho (ocupando toda a largura da página)
    try:
        header_img = ImageReader(HEADER_IMAGE_PATH)
        img_width, img_height = header_img.getSize()

        aspect = img_height / float(img_width)
        display_width = PAGE_WIDTH
        display_height = display_width * aspect

        # Se ultrapassar a altura máxima desejada, redimensiona
        if display_height > HEADER_HEIGHT:
            display_height = HEADER_HEIGHT
            display_width = display_height / aspect

        x = 0  # Sem margens laterais
        y = PAGE_HEIGHT - display_height  # No topo da página

        canvas.drawImage(
            header_img,
            x,
            y,
            width=display_width,
            height=display_height,
            preserveAspectRatio=True
        )
    except Exception as e:
        print(f"Erro ao carregar imagem do cabeçalho: {e}")

    canvas.restoreState()


# Criar documento
doc = SimpleDocTemplate(
    "exemplo_abnt_grid_com_header.pdf",
    pagesize=A4,
    leftMargin=MARGIN_LEFT,
    rightMargin=MARGIN_RIGHT,
    topMargin=MARGIN_TOP,
    bottomMargin=MARGIN_BOTTOM
)

# Blocos de texto
flowables = []

for linha in conteudo:
    if linha.strip():
        flowables.append(Paragraph(linha, styles["ABNT"]))
    else:
        flowables.append(Spacer(1, 0.5 * cm))

# Montar documento
doc.build(flowables, onFirstPage=draw_grid, onLaterPages=draw_grid)

print("PDF com header e grid gerado com sucesso!")
