"""
object.py – Erzeugt ein OpenBIS-Objekt und schreibt Metadaten.
"""
from config import SPACE, PROJECT, COLLECTION, DEVICE_SERIAL_TO_PARENT


def create_openbis_object(o, metadata: dict):
    """Erstellt und befüllt ein OpenBIS-Objekt aus den Metadaten."""
    code = f"{metadata['Proben ID']}-{metadata['Messdatensatz-Nr.']}"
    my_object = o.new_object(
        type='EXPERIMENTAL_STEP.LASER_DIFF_PSD_MEASUREMENT',
        code=code,
        space=SPACE,
        project=PROJECT,
        collection=COLLECTION,
    )

    # Parent-Device abhängig von Geräte-Seriennummer
    serial = metadata.get('Geräte Seriennr.')
    parent_perm_id = DEVICE_SERIAL_TO_PARENT.get(serial)
    if parent_perm_id:
        parent_dev = o.get_object(parent_perm_id)
        my_object.parents = parent_dev

    # Hilfsfunktionen
    def f2float(s):
        return float(str(s).replace(',', '.'))

    # Name
    probenname_raw = metadata.get('Probenname', '')
    probenname = probenname_raw.split("'")[1] if "'" in probenname_raw else probenname_raw

    # HTML-Seiten
    bemerkung = metadata.get('Bemerkungen', '')
    softwareversion = metadata.get('Softwareversion', '')
    charge = metadata.get('Charge', '')
    auftraggeber = metadata.get('Auftraggeber', '')
    analyse_zeit = metadata.get('Analyse Datum Zeit', '')
    zeit_probenmessung = metadata.get('Zeit Probenmessung', '')
    zeit_hintergrundmessung = metadata.get('Zeit Hintergrundmessung', '')
    ultraschall_extern = metadata.get('Ultraschall extern', '')
    ultraschall_intern = metadata.get('Ultraschall intern', '')
    sonotrode = metadata.get('Sonotrode', '')
    drehzahl = metadata.get('Rührerdrehzahl Erreicht', '')
    analyse_modell = metadata.get('Analyse-Modell', '')
    abschattung_blau = metadata.get('LichtAbschattung - blau', '')
    kugelform = metadata.get('Sind die Partikel nicht kugelförmig?', '')
    konzentration = metadata.get('Konzentration', '')
    modus_0_size = metadata.get('Modus [0]', '')
    modus_0_frac = metadata.get('Modus Prozent [0]', '')
    modus_1_size = metadata.get('Modus [1]', '')
    modus_1_frac = metadata.get('Modus Prozent [1]', '')

    html_description = f"""
<p><strong>Bemerkung:</strong> {bemerkung} </p>
<p><strong>Charge:</strong> {charge} </p>
<p><strong>Auftraggeber:</strong> {auftraggeber} </p>
<p><strong>Zeitpunkt der Analyse:</strong> {analyse_zeit} </p>
<p><strong>Softwareversion:</strong> {softwareversion} </p>
<p><strong>Ultraschall extern:</strong> {ultraschall_extern} </p>
<p><strong>Ultraschall intern:</strong> {ultraschall_intern} </p>
<p><strong>Sonotrode:</strong> {sonotrode} </p>
""".strip()

    html_results = f"""
<p><strong>Zeit Probenmessung [s]:</strong> {zeit_probenmessung} </p>
<p><strong>Zeitpunkt Hintergrundmessung [s]:</strong> {zeit_hintergrundmessung} </p>
<p><strong>Rührerdrehzahl Erreicht [1/min]:</strong> {drehzahl} </p>
<p><strong>Analyse-Modell:</strong> {analyse_modell} </p>
<p><strong>LichtAbschattung - blau [%]:</strong> {abschattung_blau} </p>
<p><strong>Sind die Partikel unregelmäßig geformt?:</strong> {kugelform} </p>
<p><strong>Konzentration [%]:</strong> {konzentration} </p>
<p><strong>Modus [0] [µm]:</strong> {modus_0_size} </p>
<p><strong>Modus[0][%]:</strong> {modus_0_frac} </p>
<p><strong>Modus [1] [µm]:</strong> {modus_1_size} </p>
<p><strong>Modus [1] [%]:</strong> {modus_1_frac} </p>
""".strip()

    # Allgemeine Eigenschaften
    my_object.props['$name'] = probenname
    my_object.props['$show_in_project_overview'] = True
    my_object.props['finished_flag'] = True
    my_object.props['start_date'] = None
    my_object.props['end_date'] = metadata.get('Messung Datum Uhrzeit')
    my_object.props['sample_id'] = metadata.get('Proben ID')
    my_object.props['measurement_id'] = int(metadata.get('Messdatensatz-Nr.', '0'))
    my_object.props['operator'] = metadata.get('Benutzername')

    # ELN-Seiten
    my_object.props['experimental_step.experimental_goals'] = html_description
    my_object.props['experimental_step.experimental_results'] = html_results

    # Streuungs-/Optik-Parameter
    my_object.props['dispersing_medium'] = metadata.get('Dispergiermedium')
    my_object.props['scattering_model_psd_ld'] = metadata.get('Streuungsmodell')
    my_object.props['name_optical_parameterset_sample'] = metadata.get('Partikelname')

    # Numerische Felder (mit Komma als Dezimaltrenner)
    my_object.props['refractive_index_sample'] = f2float(metadata.get('Partikel Brechungsindex', '0'))
    my_object.props['absorption_coeff_sample'] = f2float(metadata.get('Partikel Absorptionswert', '0'))
    my_object.props['refractive_index_blue_sample'] = f2float(metadata.get('Partikel Brechungsindex blaues Licht', '0'))
    my_object.props['absorption_coeff_blue_sample'] = f2float(metadata.get('Partikel Absorptionswert blaues Licht', '0'))
    my_object.props['laser_obscuration'] = f2float(metadata.get('Laserabschattung', '0'))
    my_object.props['weighted_deviation'] = f2float(metadata.get('Gewichtete Abweichung', '0'))
    my_object.props['absolute_deviation'] = f2float(metadata.get('Abweichung', '0'))
    my_object.props['meas_medium_temperature_in_celsius'] = f2float(metadata.get('Temperatur', '0'))
    my_object.props['d_10_in_micrometers'] = f2float(metadata.get('Dx (10)', '0'))
    my_object.props['d_50_in_micrometers'] = f2float(metadata.get('Dx (50)', '0'))
    my_object.props['d_90_in_micrometers'] = f2float(metadata.get('Dx (90)', '0'))
    my_object.props['mode_count'] = int(str(metadata.get('Mode Count', '0')).replace(',', '.'))

    return my_object
