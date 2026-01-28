"""
openbis.py – Login bei OpenBIS/pybis und Upload von Objekt & Attachments.
"""
from pybis import Openbis
import getpass
from config import OPENBIS_HOST, COLLECTION


def login(username: str | None = None, password: str | None = None,
          save_token: bool = True, pat_name: str | None = None):
    """Meldet sich bei OpenBIS an. Optional: erstellt/holt einen PAT."""
    o = Openbis(OPENBIS_HOST)
    if username is None:
        username = input('Bitte Username eingeben // Please input username: ')
    if password is None:
        password = getpass.getpass(prompt='Bitte Passwort eingeben // Please enter password: ')

    o.login(username, password, save_token=save_token)
    if pat_name:
        _ = o.get_or_create_personal_access_token(pat_name)
    return o


def upload(o, my_object, attachment_files: list[str], preview_file: str):
    """Speichert das Objekt und lädt Attachments & Preview als Datasets hoch."""
    # Objekt speichern
    my_object.save()

    # ATTACHMENT Dataset
    user_dataset = o.new_dataset(
        type='ATTACHMENT',
        collection=COLLECTION,
        object=my_object,
        files=list(attachment_files),
    )
    user_dataset.save()

    # ELN_PREVIEW Dataset
    user_preview = o.new_dataset(
        type='ELN_PREVIEW',
        object=my_object,
        files=[preview_file],
    )
    user_preview.save()

    return user_dataset, user_preview
