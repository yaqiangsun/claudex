"""Hook for voice integration."""


class VoiceIntegration:
    """Manages voice input/output integration."""

    def __init__(self):
        self._enabled = False
        self._speech_recognition = False
        self._text_to_speech = False

    def enable(self, speech_recognition: bool = True, tts: bool = True) -> None:
        """Enable voice integration."""
        self._enabled = True
        self._speech_recognition = speech_recognition
        self._text_to_speech = tts

    def disable(self) -> None:
        """Disable voice integration."""
        self._enabled = False

    def is_enabled(self) -> bool:
        """Check if voice is enabled."""
        return self._enabled

    def is_speech_recognition_available(self) -> bool:
        """Check if speech recognition is available."""
        return self._enabled and self._speech_recognition

    def is_tts_available(self) -> bool:
        """Check if text-to-speech is available."""
        return self._enabled and self._text_to_speech


__all__ = ['VoiceIntegration']