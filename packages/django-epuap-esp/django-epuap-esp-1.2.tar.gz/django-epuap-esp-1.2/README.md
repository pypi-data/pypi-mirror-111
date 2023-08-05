django-epuap-esp
================
`django-epuap-esp` is a Django application providing integration with Polish Public Administration Services electronic inbox. `django-epuap-esp` is not related to Profil Zaufany authentication workflow, use django-epuap instead.

Installation
------------
To get `django-epuap-esp` please follow the steps below:

- obtain ePUAP Service Certificate
  (https://int.epuap.gov.pl/wps/portal/strefa-urzednika/katalog-spraw/udostepnianie-uslug/najczesciej-zalatwiane-sprawy/wniosek-o-certyfikat-do-srodowiska-integracyjnego)
- download ePUAP Server Certificate (from Strefa urzędnika→Pomoc)
- pip install django-epuap-esp
- add following options to settings.py:
  - `EPUAP_ESP_SUBJECT = ` ePUAP Public Administration Subject identification string
  - `EPUAP_ESP_BOX = ` ePUAP Public Administration box name
  - `EPUAP_ESP_ADDRESS = ` ePUAP Public Administration box address
  - `EPUAP_ESP_SYSTEM_CERT = ` ePUAP Service Certificate PEM-encoded file name
  - `EPUAP_ESP_SYSTEM_KEY = ` ePUAP Service Certificate private key PEM-encoded file name
  - `EPUAP_ESP_WS_CERT = ` ePUAP Server Certificate PEM-encoded file name
- use an interface in view or module.
  `epuapesp.epuap.EPuap.pull()` should be invoked periodically. Ex.
  ```python
  from epuapesp import epuap
  document = epuap.EPuap.pull()
  #process document.content
  epuap.EPuap.acknowledge(document.sha256)
  ```

Current state
-------------
`django-epuap-esp` provides integration with ePUAP test environment. Currently only document receiver (pull) works. A document delivery is still WiP.
