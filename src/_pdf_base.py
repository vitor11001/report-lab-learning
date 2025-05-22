import os
from abc import ABC, abstractmethod
from copy import deepcopy
from dataclasses import dataclass
from typing import ClassVar

from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict, field_validator
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import (Frame, HRFlowable, Image, Paragraph,
                                SimpleDocTemplate, Spacer, Table, TableStyle)

# Tamanho da página A4
PAGE_WIDTH, PAGE_HEIGHT = A4

# Margens ABNT
MARGIN_LEFT = 3 * cm
MARGIN_RIGHT = 2 * cm
MARGIN_TOP = 3 * cm
MARGIN_BOTTOM = 2 * cm

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class _PDFBase(PydanticBaseModel, ABC):
    filename: str

    class PageBase(PydanticBaseModel):
        """
        Estrutura da página com margens e áreas definidas.
        """

        pagesize: ClassVar[tuple] = A4
        page_width: ClassVar[float] = PAGE_WIDTH
        page_height: ClassVar[float] = PAGE_HEIGHT
        left_margin: ClassVar[float] = MARGIN_LEFT
        right_margin: ClassVar[float] = MARGIN_RIGHT
        top_margin: ClassVar[float] = MARGIN_TOP
        bottom_margin: ClassVar[float] = MARGIN_BOTTOM

        class Header(PydanticBaseModel):
            """
            Estrutura do cabeçalho.
            """

            image_path: ClassVar[str] = os.path.join(
                BASE_DIR, "images", "Header_Modificado.png"
            )  # Caminho da imagem do cabeçalho
            header_height: ClassVar[float] = 4 * cm  # Altura do cabeçalho

        class Footer(PydanticBaseModel):
            """
            Estrutura do rodapé.
            """

            image_path: ClassVar[str] = os.path.join(
                BASE_DIR, "images", "Footer.jpeg"
            )  # Caminho da imagem do rodapé
            footer_height: ClassVar[float] = 4 * cm  # Altura do rodapé

        @staticmethod
        def _validate_image_path(value: str) -> str:
            if not os.path.exists(value):
                print(f"Imagem não encontrada: {value}")
                raise FileNotFoundError(
                    f"A imagem não existe no caminho especificado: {value}"
                )
            return value

        @classmethod
        def _generate_header(cls, canvas: Canvas):
            header_image = ImageReader(cls.Header.image_path)
            img_width, img_height = header_image.getSize()

            aspect = img_height / float(img_width)
            display_width = cls.page_width
            display_height = display_width * aspect

            # Se ultrapassar a altura máxima desejada, redimensiona
            if display_height > cls.Header.header_height:
                display_height = cls.Header.header_height
                display_width = display_height / aspect

            x = 0  # Sem margens laterais
            y = PAGE_HEIGHT - display_height  # No topo da página

            canvas.drawImage(
                image=header_image,
                x=x,
                y=y,
                width=display_width,
                height=display_height,
                preserveAspectRatio=True,
                mask="auto",
            )

        @classmethod
        def generate_header(cls, canvas: Canvas, doc: SimpleDocTemplate = None):
            """
            Desenha a imagem do cabeçalho centralizada horizontalmente,
            ocupando toda a altura do cabeçalho proporcionalmente.
            """
            try:
                cls._validate_image_path(cls.Header.image_path)
                cls._generate_header(canvas)
            except Exception as error:
                print(f"Erro ao gerar o Header: {error}")

        @classmethod
        def _generate_footer(cls, canvas: Canvas):
            footer_image = ImageReader(cls.Footer.image_path)
            img_width, img_height = footer_image.getSize()

            aspect = img_height / float(img_width)

            # Definir margens
            margin_x = 0.2 * cm
            available_width = cls.page_width - 2 * margin_x

            display_width = available_width
            display_height = display_width * aspect

            # Redimensiona se ultrapassar a altura máxima
            if display_height > cls.Footer.footer_height:
                display_height = cls.Footer.footer_height
                display_width = display_height / aspect
                # Reajusta a margem lateral para centralizar a imagem menor
                margin_x = (cls.page_width - display_width) / 2

            x = margin_x
            y = 0.3 * cm  # Altura do rodapé (um pequeno deslocamento vertical)

            canvas.drawImage(
                image=footer_image,
                x=x,
                y=y,
                width=display_width,
                height=display_height,
                preserveAspectRatio=True,
                mask="auto",
            )

        @classmethod
        def generate_footer(cls, canvas: Canvas, doc: SimpleDocTemplate = None):
            """
            Desenha o rodapé na parte inferior da página.
            """
            try:
                cls._validate_image_path(cls.Footer.image_path)
                cls._generate_footer(canvas)
            except Exception as error:
                print(f"Erro ao gerar o Footer: {error}")

        @classmethod
        def add_header_and_footer(cls, canvas: Canvas, doc: SimpleDocTemplate = None):
            """
            Adiciona o cabeçalho e rodapé ao documento.
            """
            cls.generate_header(canvas, doc)
            cls.generate_footer(canvas, doc)

    class ElementsPage(PydanticBaseModel):
        line_between_text: ClassVar[HRFlowable] = HRFlowable(
            width="100%",
            thickness=1,
            color=colors.HexColor("#d4eced"),
            spaceBefore=0.3 * cm,
            spaceAfter=0.3 * cm,
        )

    def base_template_pdf(self, filename: str) -> SimpleDocTemplate:
        """
        Gera a configuração base do PDF com margens ABNT.
        :param filename: Caminho do arquivo PDF a ser gerado.
        :return: Instância do SimpleDocTemplate configurada.
        """
        doc = SimpleDocTemplate(
            filename=filename,
            pagesize=self.PageBase.pagesize,
            leftMargin=self.PageBase.left_margin,
            rightMargin=self.PageBase.right_margin,
            topMargin=self.PageBase.top_margin,
            bottomMargin=self.PageBase.bottom_margin,
        )
        return doc

    @classmethod
    @abstractmethod
    def content_to_pdf(cls) -> list:
        pass

    def generate_pdf(self):
        """
        Gera um PDF com margens ABNT e áreas definidas para conteúdo.
        :param filename: Caminho do arquivo PDF a ser gerado.
        """
        # Configura o documento
        doc = self.base_template_pdf(self.filename)

        # Conteúdo do PDF
        content = self.content_to_pdf()

        # Cria o PDF
        doc.build(
            content,
            onFirstPage=self.PageBase.add_header_and_footer,
            onLaterPages=self.PageBase.add_header_and_footer,
        )


if __name__ == "__main__":
    pdf = _PDFBase()
    pdf.generate_pdf("output.pdf")
