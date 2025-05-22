from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib import colors
from typing import ClassVar
from pydantic import BaseModel as PydanticBaseModel


class ParagraphStylesGota(PydanticBaseModel):
    font_name: ClassVar[str] = "Helvetica"
    font_bold_name: ClassVar[str] = "Helvetica-Bold"
    
    @classmethod
    def normal_left(cls) -> ParagraphStyle:
        return ParagraphStyle(
            name='NormalLeft',
            fontName=cls.font_name,
            fontSize=10,
            leading=14,
            textColor=colors.black,
            alignment=0,  # Left alignment
        )

    @classmethod
    def normal_right(cls) -> ParagraphStyle:
        return ParagraphStyle(
            name='NormalRight',
            fontName=cls.font_name,
            fontSize=10,
            leading=14,
            textColor=colors.black,
            alignment=2  # Right alignment
        )
        
    @classmethod
    def normal_adjusted(cls) -> ParagraphStyle:
        return ParagraphStyle(
            name='NormalAdjusted',
            fontName=cls.font_name,
            fontSize=10,
            leading=14,
            textColor=colors.black,
            alignment=4,
            firstLineIndent=15,
        )

    @classmethod
    def normal_left_bold(cls) -> ParagraphStyle:
        return ParagraphStyle(
            name='NormalLeftBold',
            fontName=cls.font_bold_name,
            fontSize=10,
            leading=14,
            textColor=colors.black,
            alignment=0,  # Left alignment
        )

    @classmethod
    def normal_center_bold(cls) -> ParagraphStyle:
        return ParagraphStyle(
            name='NormalCenterBold',
            fontName=cls.font_bold_name,
            fontSize=10,
            leading=14,
            textColor=colors.black,
            alignment=1,  # Center alignment
        )

    @classmethod
    def title(cls) -> ParagraphStyle:
        return ParagraphStyle(
            name='Title',
            fontName=cls.font_bold_name,
            fontSize=18,
            leading=22,
            textColor=colors.black,
            alignment=1  # Center alignment
        )

    @classmethod
    def paragraph_label_bold_value_normal_left(cls, label: str, valor: str):
        return Paragraph(f"<b>{label}</b> {valor}", cls.normal_left())
