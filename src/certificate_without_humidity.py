from _pdf_base import _PDFBase, BASE_DIR
from paragraph_style_gota import ParagraphStylesGota
from reportlab.lib.styles import getSampleStyleSheet
from copy import deepcopy
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib.units import cm
from reportlab.lib import colors
import textwrap
import os


class CertificateWithoutHumidity(_PDFBase):
    """
    Modelo de dados para o certificado sem umidade.
    """
    filename: str = "certificado_sem_umidade.pdf"

    @classmethod
    def content_to_pdf(cls) -> list:
        normal_left = ParagraphStylesGota.normal_left()
        normal_right = ParagraphStylesGota.normal_right()
        normal_adjusted = ParagraphStylesGota.normal_adjusted()
        normal_left_bold = ParagraphStylesGota.normal_left_bold()
        normal_center_bold = ParagraphStylesGota.normal_center_bold()
        title = ParagraphStylesGota.title()
        label_bold_and_value_normal_left = ParagraphStylesGota.paragraph_label_bold_value_normal_left
        max_width_for_table = cls.PageBase.page_width - cls.PageBase.left_margin - cls.PageBase.right_margin

        flowables = []
        
        flowables.append(Paragraph("Certificado de Calibração N° 2290", title))
        flowables.append(Paragraph("Ref. Norma: 04_00", normal_right))
        flowables.append(cls.ElementsPage.line_between_text)
        # flowables.append(Spacer(1, 0.2 * cm))

        # Bloco: Solicitante
        flowables.append(label_bold_and_value_normal_left("Solicitante:", "Hemorio"))
        flowables.append(label_bold_and_value_normal_left("Endereço:", "Rua Frei Caneca, 8 - Centro, Rio de Janeiro - RJ, 20211-030"))
        flowables.append(label_bold_and_value_normal_left("Objeto de calibração:", "Termômetro"))
        flowables.append(label_bold_and_value_normal_left("Marca:", "Senfio"))
        flowables.append(label_bold_and_value_normal_left("Modelo:", "EXPLORER"))
        flowables.append(label_bold_and_value_normal_left("Nº de série:", "0637"))

        flowables.append(cls.ElementsPage.line_between_text)

        # Bloco: Dados da calibração
        dados_calibracao = [
            Paragraph("Dados da calibração", normal_left_bold),
            Paragraph("Data da calibração: 23/05/2024", normal_left),
            Paragraph("Data emissão: 24/04/2025", normal_left),
            Paragraph("Local: Senfio Soluções Tecnológicas", normal_left),
        ]

        # Bloco: Condições ambientais
        condicoes_ambientais = [
            Paragraph("Condições ambientais", normal_left_bold),
            Paragraph("Temperatura: (26,0 ± 1,0)°C", normal_left),
        ]

        # Tabela com duas colunas
        tabela = Table(
            data=[[dados_calibracao, condicoes_ambientais]],
            colWidths=[10 * cm, 7 * cm],  # ajuste conforme necessário
            hAlign='LEFT'
        )

        # Estilo: alinhamento no topo, sem bordas
        tabela.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),  # Alinha conteúdo verticalmente ao topo
            ('LEFTPADDING', (0, 0), (-1, -1), 0),  # Remove espaçamento à esquerda
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),  # Pequeno espaço à direita
            ('TOPPADDING', (0, 0), (-1, -1), 0),   # Sem padding superior
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
            ('BOX', (0, 0), (-1, -1), 0, colors.white),  # Sem bordas
            ('INNERGRID', (0, 0), (-1, -1), 0, colors.white),
        ]))

        flowables.append(tabela)

        flowables.append(cls.ElementsPage.line_between_text)

        flowables.append(Paragraph("Procedimentos", normal_left_bold))
        text_proceed = textwrap.dedent("""\
            A calibração foi conduzida em um meio termostático com incerteza conhecida, onde foram realizadas 
            5 medições em cada ponto. Neste certificado foi representado o valor médio dessas 5 medições. 
            Todas as instruções foram executadas conforme o documento interno Norma-04 da Senfio.
        """)
        flowables.append(Paragraph(text_proceed, normal_adjusted))
        flowables.append(Spacer(1, 0.3 * cm))

        # Bloco: Padrão utilizado
        flowables.append(Paragraph("Padrão utilizado na calibração", normal_left_bold))
        flowables.append(Paragraph("Descrição: Termohigrômetro", normal_left))
        flowables.append(Paragraph("Modelo: Explorer", normal_left))
        flowables.append(Paragraph("Marca: Senfio", normal_left))
        flowables.append(Paragraph("Faixa de uso: -100°C a 100°C", normal_left))
        flowables.append(Paragraph("Certificado de Calibração do Padrão: 7XVH1M24", normal_left))
        flowables.append(Paragraph("Data da Calibração: 23/01/2025", normal_left))
        flowables.append(Paragraph("Número de série: 0112", normal_left))
        flowables.append(Paragraph("Resolução: 0,1°C", normal_left))

        flowables.append(cls.ElementsPage.line_between_text)

        # Bloco: Tabela de resultados
        flowables.append(label_bold_and_value_normal_left("Resultados:", "Temperatura"))

        table_data = [
            [
                Paragraph("VVC (Valor Verdadeiro Convencional)", normal_center_bold),
                Paragraph("VML (Valor Médio das Leituras)", normal_center_bold),
                Paragraph("Erro<br/>(VML-VVC)", normal_center_bold),
                Paragraph("Incerteza combinada<br/>(Uc)", normal_center_bold),
                Paragraph("Fator de abrangência<br/>(K)", normal_center_bold),
                Paragraph("Incerteza expandida<br/>(Ue)", normal_center_bold),
            ],
            [
                Paragraph("(°C)", normal_center_bold),
                Paragraph("(°C)", normal_center_bold),
                Paragraph("(°C)", normal_center_bold),
                Paragraph("(°C)", normal_center_bold),
                Paragraph("", normal_center_bold),
                Paragraph("(°C)", normal_center_bold),
            ],
            ["-20,00", "-21,13", "-1,13", "0,34", "2,00", "0,68"],
            ["0,00", "-0,47", "-0,47", "0,34", "2,00", "0,68"],
            ["20,00", "19,77", "-0,23", "0,34", "2,00", "0,68"],
        ]

        col_widths = [
            0.2*max_width_for_table, 
            0.16*max_width_for_table, 
            0.16*max_width_for_table, 
            0.16*max_width_for_table, 
            0.16*max_width_for_table, 
            0.16*max_width_for_table
        ]

        table = Table(table_data, colWidths=col_widths, hAlign="LEFT")

        table.setStyle(TableStyle([
            # Apenas linhas verticais
            ("LINEBEFORE", (1, 0), (-1, -1), 0.5, colors.HexColor("#d0f0f8")),

            # Background apenas na linha 1 (índice 0) e linha 3 (índice 2)
            ("BACKGROUND", (0, 1), (-1, 1), colors.HexColor("#d0f0f8")),
            ("BACKGROUND", (0, 3), (-1, 3), colors.HexColor("#d0f0f8")),

            # Centraliza o conteúdo
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ]))

        flowables.append(table)

        flowables.append(PageBreak()) # 👉 quebra de página aqui!
        
        # Resumo
        flowables.append(Paragraph("Resumo", normal_left_bold))

        table_data = [
            [
                Paragraph("VVC", normal_center_bold),
                Paragraph("Medição final", normal_center_bold),
            ],
            [
                Paragraph("(°C)", normal_center_bold),
                Paragraph("(°C)", normal_center_bold),
            ],
            ["-20,00", "-21,13 com Uc = 0,34"],
            ["0,00", "-0,47 com Uc = 0,34"],
            ["20,00", "19,77 com Uc = 0,34"],
        ]

        col_widths = [
            0.25*max_width_for_table, 
            0.75*max_width_for_table, 
        ]

        table = Table(table_data, colWidths=col_widths, hAlign="LEFT")

        table.setStyle(TableStyle([
            # Apenas linhas verticais
            ("LINEBEFORE", (1, 0), (-1, -1), 0.5, colors.HexColor("#d0f0f8")),

            # Background apenas na linha 1 (índice 0) e linha 3 (índice 2)
            ("BACKGROUND", (0, 1), (-1, 1), colors.HexColor("#d0f0f8")),
            ("BACKGROUND", (0, 3), (-1, 3), colors.HexColor("#d0f0f8")),

            # Centraliza o conteúdo
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ]))

        flowables.append(table)

        flowables.append(Spacer(1, 0.3 * cm))
        flowables.append(Paragraph("Observações:", normal_left_bold))

        # Corpo do texto, usando HTML básico para formatação
        obs_text_1 = """
        <b>1)</b> As componentes de incerteza consideradas neste certificado englobam além da incerteza das próprias medições, a resolução digital do mostrador do padrão e sua estabilidade térmica.<br/>
        """
        obs_text_2 = """
        <b>2)</b> Este certificado se aplica somente ao instrumento calibrado.<br/>
        """
        obs_text_3 = """
        <b>3)</b> Sua utilização para fins promocionais depende de prévia autorização formal da Senfio. Sua reprodução só pode ser realizada integralmente, sem nenhuma alteração.<br/>
        """
        obs_text_4 = """
        <b>4)</b> A incerteza da calibração (incerteza expandida) é baseada em um fator de abrangência K, para um nível de confiança de 95,45%.
        """

        flowables.append(Paragraph(obs_text_1, normal_adjusted))
        flowables.append(Paragraph(obs_text_2, normal_adjusted))
        flowables.append(Paragraph(obs_text_3, normal_adjusted))
        flowables.append(Paragraph(obs_text_4, normal_adjusted))

        flowables.append(Spacer(1, 1 * cm))
        
        # Bloco: Assinatura
        img = Image(os.path.join(BASE_DIR, "images", "assignElyr.png"), width=5 * cm, height=2 * cm)
        img.hAlign = 'CENTER'

        flowables.append(img)

        return flowables


if __name__ == "__main__":
    pdf = CertificateWithoutHumidity()
    pdf.generate_pdf()
