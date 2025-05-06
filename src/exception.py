import sys

def error_message_detail(error, error_detail: sys):
 _, _, exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    line_number = exc_tb.tb_lineno
    error_msg = f"Error occurred in script: '{file_name}' at line {line_number} | Message: {str(error)}"
    )

class CustomException(Exception):
    def __init__(self, message, error_detail: str = None):
       super().__init__(self.message)
       self.message = message
       self.error_detail = error_detail
        

    def __str__(self):
        if self.error_detail:
            return f"{self.message} | Error Detail: {self.error_detail}"
        return self.message