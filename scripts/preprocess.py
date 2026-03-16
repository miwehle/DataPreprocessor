# Rufe die funktion preprocess in src/api.py auf
# 
# Parameter:
# - an dieses skript (scripts/preprocess.py) wird eine konfig-datei übergeben.
# - darin steht das dataset, config und split
# - mehr muss nicht drinstehen, es sollen die defaults von preprocess genutzt werden
# - beispiel: configs/europarl_config.yaml (fülle diese datei mit inhalt)

# speicherort für die runtergeladene datei:
# - neben dem projektorderner liegt ein ordner artifacts mit unterordner datasets.
# - darin speichern in eime unterordner, der grob den dataset namen angibt.
# - beispiel: artifacts/europarl/raw
#
# Speicherort für das komplett preprozessierten dataset
# - beispiel: artifacts/europarl/preprocessed
# Metadaten: die für das modell und training benötigten metadaten daneben ablegen

# Speicherort für Zwischenergebnisse:
# - beispiel: artifacts/interim
# - für norm, filtered usw. nicht eigene ordner nehmen, sondern im dateinamen die funktion angeben.