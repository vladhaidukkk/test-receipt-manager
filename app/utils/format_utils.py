import datetime as dt
from decimal import Decimal

from app.models import PaymentType, Receipt


class ReceiptFormatter:
    def __init__(self, width: int) -> None:
        # You can make this class more configurable by adding more params (e.g., datetime format).
        self.receiver = "ФОП Джонсонюк Борис"
        self.closing_line = "Дякуємо за покупку!"
        self.width = width

    def format(self, receipt: Receipt) -> str:
        content = ""

        content += self.line(self.receiver, center=True)
        content += self.divider()

        for product_idx, product in enumerate(receipt.products, start=1):
            content += self.line(f"{self.number(product.quantity)} x {self.number(product.price)}")

            name = ""
            total = self.number(product.total)

            name_words = product.name.split()
            for word_idx, word in enumerate(name_words, start=1):
                is_too_long = len(name + word + " ") > (self.width - len(total))
                is_last_word = word_idx == len(product.name.split())

                if is_too_long and is_last_word:
                    content += self.line(name)
                    name = word
                elif is_too_long:
                    content += self.line(name + word)
                    name = ""
                elif is_last_word:
                    name += word
                else:
                    name += word + " "
            else:
                content += self.spaced_line(name, total)

            if product_idx != len(receipt.products):
                content += self.divider("-")

        content += self.divider()
        content += self.spaced_line("СУМА", self.number(receipt.total))
        content += self.spaced_line(
            "Готівка" if receipt.payment.type == PaymentType.CASH else "Карта",
            self.number(receipt.payment.amount),
        )
        content += self.spaced_line("Решта", self.number(receipt.rest))

        content += self.divider()
        content += self.line(self.datetime(receipt.created_at), center=True)
        content += self.line(self.closing_line, center=True)

        return content

    def number(self, value: int | float | Decimal) -> str:
        return f"{value:,.2f}".replace(",", " ")

    def datetime(self, value: dt.datetime) -> str:
        return value.strftime("%d.%m.%Y %H:%M")

    def space(self, title: str, value: str) -> str:
        return " " * (self.width - len(title) - len(value))

    def line(self, text: str, *, center: bool = False) -> str:
        content = text
        if center:
            content = content.center(self.width)
        return content + "\n"

    def divider(self, char: str = "=") -> str:
        return char * self.width + "\n"

    def spaced_line(self, title: str, value: str) -> str:
        return self.line(title + self.space(title, value) + value)
