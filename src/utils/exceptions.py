class FileNotFoundError(Exception):
  def __init__(self, message="File not found. Please check the path and try again."):
      self.message = message
      super().__init__(self.message)



class RuntimeError(Exception):
  def __init__(self, message="An error occurred during runtime. Please check the logs for details."):
      self.message = message
      super().__init__(self.message)


class HTTPException(Exception):
  def __init__(self, status_code=500, detail="An HTTP error occurred."):
      self.status_code = status_code
      self.detail = detail
      super().__init__(f"HTTP {self.status_code}: {self.detail}")      