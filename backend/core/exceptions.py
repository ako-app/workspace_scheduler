# Booking例外規定クラス
class BookingError(Exception):
    pass

# 予約重複エラー
class BookingConflictError(BookingError):
    """予約の時間帯が重複している場合の例外"""
    def __init__(
            self, 
            message: str = "この時間はすでに予約されています"
    ) -> None:
        super().__init__(message)
    