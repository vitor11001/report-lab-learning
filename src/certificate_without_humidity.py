from _pdf_base import _PDFBase
from paragraph_style_gota import ParagraphStylesGota
from reportlab.lib.styles import getSampleStyleSheet
from copy import deepcopy
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
import textwrap


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
        title = ParagraphStylesGota.title()
        label_bold_and_value_normal_left = ParagraphStylesGota.paragraph_label_bold_value_normal_left

        flowables = []
        
        flowables.append(Paragraph("Certificado de Calibração N° 2290", title))
        flowables.append(Paragraph("Ref. Norma: 04_00", normal_right))
        flowables.append(Spacer(1, 0.3 * cm))
        flowables.append(cls.ElementsPage.line_between_text)
        
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

        return flowables

    # @classmethod
    # def content_to_pdf(cls) -> list:
    #     styles = getSampleStyleSheet()
    #     normal = styles["Normal"]
    #     title = styles["Title"]
    #     heading = deepcopy(normal)
    #     heading.fontSize = 10
    #     heading.spaceAfter = 6

    #     bold = deepcopy(normal)
    #     bold.fontName = "Helvetica-Bold"

    #     right_style = deepcopy(normal)
    #     right_style.alignment = 2  # Alinha à direita

    #     flowables = []

    #     # Título e referência
    #     flowables.append(Paragraph("Certificado de Calibração N° 2290", title))
    #     flowables.append(Paragraph("Ref. Norma: 04_00", right_style))
    #     flowables.append(Spacer(1, 0.3 * cm))
    #     flowables.append(cls.line_between_text())

    #     # Bloco: Solicitante
    #     flowables.append(cls.paragrafo_detalhe("Solicitante:", "Hemorio"))
    #     flowables.append(cls.paragrafo_detalhe("Endereço:", "Rua Frei Caneca, 8 - Centro, Rio de Janeiro - RJ, 20211-030"))
    #     flowables.append(cls.paragrafo_detalhe("Objeto de calibração:", "Termômetro"))
    #     flowables.append(cls.paragrafo_detalhe("Marca:", "Senfio"))
    #     flowables.append(cls.paragrafo_detalhe("Modelo:", "EXPLORER"))
    #     flowables.append(cls.paragrafo_detalhe("Nº de série:", "0637"))

    #     flowables.append(Spacer(1, 0.4 * cm))
    #     flowables.append(cls.line_between_text())

    #     # Bloco: Dados da calibração
    #     flowables.append(Paragraph("<b>Dados da calibração</b>", heading))
    #     flowables.append(cls.paragrafo_detalhe("Data da calibração:", "23/05/2024"))
    #     flowables.append(cls.paragrafo_detalhe("Data emissão:", "24/04/2025"))
    #     flowables.append(cls.paragrafo_detalhe("Local:", "Senfio Soluções Tecnológicas"))

    #     flowables.append(Spacer(1, 0.2 * cm))

    #     # Bloco: Condições ambientais
    #     flowables.append(Paragraph("<bCondições ambientais</b>", heading))
    #     flowables.append(cls.paragrafo_detalhe("Temperatura:", "(26,0 ± 1,0)°C"))

    #     flowables.append(Spacer(1, 0.3 * cm))

    #     # Bloco: Procedimentos
    #     texto_proced = (
    #         "A calibração foi conduzida em um meio termostático com incerteza conhecida, onde foram realizadas 5 medições em cada ponto. "
    #         "Neste certificado foi representado o valor médio dessas 5 medições. Todas as instruções foram executadas conforme o documento "
    #         "interno Norma-04 da Senfio."
    #     )
    #     flowables.append(Paragraph("<b>Procedimentos</b>", heading))
    #     flowables.append(Paragraph(texto_proced, normal))
    #     flowables.append(Spacer(1, 0.3 * cm))

    #     # Bloco: Padrão utilizado
    #     flowables.append(Paragraph("<b>Padrão utilizado na calibração</b>", heading))
    #     padrao = [
    #         cls.paragrafo_detalhe("Descrição:", "Termohigrômetro"),
    #         cls.paragrafo_detalhe("Modelo:", "Explorer"),
    #         cls.paragrafo_detalhe("Marca:", "Senfio"),
    #         cls.paragrafo_detalhe("Faixa de uso:", "-100°C a 100°C"),
    #         cls.paragrafo_detalhe("Certificado de Calibração do Padrão:", "7XVH1M24"),
    #         cls.paragrafo_detalhe("Data da Calibração:", "23/01/2025"),
    #         cls.paragrafo_detalhe("Número de série:", "0112"),
    #         cls.paragrafo_detalhe("Resolução:", "0,1°C"),
    #     ]
    #     flowables.extend(padrao)
    #     flowables.append(Spacer(1, 0.3 * cm))

    #     # Bloco: Tabela de resultados
    #     flowables.append(Paragraph("<b>Resultados: Temperatura</b>", heading))

    #     table_data = [
    #         ["VVC (Valor Verdadeiro Convencional)", "VML (Valor Médio das Leituras)", "Erro (VML-VVC)", "Incerteza combinada Uc", "Fator de abrangência (K)", "Incerteza expandida (Ue)"],
    #         ["-20,00", "-21,13", "-1,13", "0,34", "2,00", "0,68"],
    #         ["0,00", "-0,47", "-0,47", "0,34", "2,00", "0,68"],
    #         ["20,00", "19,77", "-0,23", "0,34", "2,00", "0,68"],
    #     ]

    #     col_widths = [4 * cm, 4 * cm, 2.5 * cm, 3 * cm, 3 * cm, 3 * cm]

    #     table = Table(table_data, colWidths=col_widths, hAlign="LEFT")
    #     table.setStyle(TableStyle([
    #         ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
    #         ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#d0f0f8")),
    #         ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    #     ]))

    #     flowables.append(table)

    #     return flowables

    # @staticmethod
    # def paragrafo_detalhe(label: str, valor: str):
    #     styles = getSampleStyleSheet()
    #     normal = styles["Normal"]
    #     return Paragraph(f"<b>{label}</b> {valor}", normal)

    # @staticmethod
    # def line_between_text():
    #     from reportlab.platypus import HRFlowable
    #     return HRFlowable(width="100%", thickness=1, color=colors.black, spaceBefore=0.2 * cm, spaceAfter=0.2 * cm)




if __name__ == "__main__":
    pdf = CertificateWithoutHumidity()
    pdf.generate_pdf()
