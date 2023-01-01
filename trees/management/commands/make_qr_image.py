import qrcode

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Make a QR code image'

    def handle(self, *args, **kwargs):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        # qr.add_data('http://mwalker.info')
        qr.add_data('https://texastreeplanting.tamu.edu/Display_Onetree.aspx?tid=63')
        qr.make(fit=True)
        image = qr.make_image(fill_color='green', back_color='white').convert('RGB')
        image.save('qr.png')
