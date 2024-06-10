from django.db import models
from django.core.files import File
import qrcode
from io import BytesIO

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=11)
    national_id = models.CharField(max_length=10, null=True)
    birthday = models.DateField(null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Place(models.Model):
    place_name = models.CharField(max_length=50)

    def __str__(self):
        return self.place_name

class Team(models.Model):
    name = models.CharField(max_length=50)


class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    host_team = models.ForeignKey(Team, on_delete=models.CASCADE,  related_name='host_team')
    guest_team = models.ForeignKey(Team, on_delete=models.CASCADE,  related_name='guest_team')
    place = models.ForeignKey(Place, on_delete=models.CASCADE,  related_name='place_ticket')
    buy_date = models.DateField(null=True)
    match_date = models.DateTimeField(null=True)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    qr_code_id = models.IntegerField(blank=False)
    is_used = models.BooleanField(default=False)
    def save(self, *args, **kwargs):
        # Generate QR code data
        qr_data = f"Ticket for {self.user} at {self.place} on {self.buy_date}"
        
        # Create a QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)

        img = qr.make_image(fill='black', back_color='white')

        # Save the image to a BytesIO object
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        img_name = f'qr_code_{self.pk}.png'

        # Save to the ImageField
        self.qr_code.save(img_name, File(buffer), save=False)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Ticket for {self.user} to {self.place} on {self.buy_date}"
