"""
Konfigurationsmodul für OpenBIS/pybis.

Enthält Host und IDs für Space, Project, Collection sowie optional die Zuordnung
von Geräte-Seriennummern zu Parent-Geräten.
"""

# OpenBIS Server
OPENBIS_HOST = 'main.datastore.bam.de'

# ELN/Datastore-Referenzen
SPACE = 'YOUR_SPACE'
PROJECT = 'YOUR_PROJECT'
COLLECTION = 'YOUR_COLLECTION'

# Parent-Device-Zuordnung (Key: Geräte Seriennr., Value: PermID des Geräts)
PARENT_DEVICE_PERM_ID = 'PERM_ID_OF_DESIRED_PARENT_INSTRUMENT'
DEVICE_SERIAL_TO_PARENT = {
    'SERIAL_OF_YOUR_DEVICE': PARENT_DEVICE_PERM_ID,
}
