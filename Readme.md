# Setup
1. Create virtual environment with anaconda, venv or similar.
2. Activate environment
3. Install dependencies with ``pip install -r requirements.txt``
4. Setup Configuration as described in Chapter **Setup Configuration**.
5. In activated environment run with ``python core.py``

# Setup Configuration
Explained with the following sample configuration.
```json
{
  "mail": {
    "login": "MAIL_ADDRESS",
    "password": "PASSWORD_MAIL",
    "receivers": ["RECEIVER_MAIL_1", "RECEIVER_MAIL_2"],
    "smtp_host": "smtp.gmail.com",
    "smtp_port": 587
  },
  "checkInterval": 120,
  "vendors": [
    {
      "vendor": "Vendor",
      "url": "Url to product on vendor site",
      "lookfor": "pdp-add-to-cart-button"
    }]
}
```  

**mail.login** : E-mail address used to send notifications.  
**mail.password** : Password for e-mail address.  
**mail.receivers** : List of receiver mail addresses.  
**mail.smtp_host** : The smtp server address of your mail provider. Sample is configured for gmail accounts.  
**mail.smtp_port** : Port of the smtp server.  


**checkInterval** : Interval in seconds in which the product is checked for availability.  


**vendors.vendor** : Name of the vendor.
**vendors.url** : Url to the product of the vendor.
**vendors.lookfor**: Selector of the add to cart or buy button.