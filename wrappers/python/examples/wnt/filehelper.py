"""
    File helper methods
    ===================

    .. Copyright:
        Copyright Wirepas Ltd 2019 licensed under Apache License, Version 2.0
        See file LICENSE for full license details.
"""
import base64


class FileHelper:
    """File handling helper methods class"""

    @staticmethod
    def read_file_content_as_base64(file_path: str) -> str:
        """Return file content as base64 encoded string

        Args:
            file_path (str): full file path name

        Returns:
            str: File content as base64 string
        """
        file = open(file_path, "rb")
        image_base64 = base64.b64encode(file.read()).decode("utf-8")
        file.close()

        return image_base64

    @staticmethod
    def write_file_content_from_base64(file_path: str, data_base64: str) -> None:
        """Write base64 encoded string data as binary to a file

        Args:
            file_path (str): full file path name
            data_base64 (str): data as base64 encoded string
        """
        file = open(file_path, "wb")
        file.write(base64.b64decode(data_base64))
        file.close()
