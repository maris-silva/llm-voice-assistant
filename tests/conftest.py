import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

# main.py instancia um Buzzer no import (`buzzer = Buzzer(12)`). Sem isso,
# qualquer teste que importe main.py explode fora de uma Raspberry Pi real.
from gpiozero import Device
from gpiozero.pins.mock import MockFactory

Device.pin_factory = MockFactory()
