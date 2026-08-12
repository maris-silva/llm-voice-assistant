import sys

try:
    from gpiozero import LED

    _led = LED(17)  # Pino BCM 17
except Exception as e:
    _led = None
    print(f"⚠️ Hardware GPIO não inicializado (modo simulação): {e}")


class HardwareController:
    @staticmethod
    def acender_luz():
        if _led:
            _led.on()
        print("💡 [Hardware] Luzes ligadas.")

    @staticmethod
    def apagar_luz():
        if _led:
            _led.off()
        print("🌑 [Hardware] Luzes desligadas.")
