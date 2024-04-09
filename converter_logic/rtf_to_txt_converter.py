
import subprocess
import tempfile
from io import BytesIO
from base_converter import BaseConverter
import logger_config


logger = logger_config.configure_logger(__name__)


class RTFToTXTConverter(BaseConverter):
    def convert(self, output_stream: BytesIO):
        with tempfile.NamedTemporaryFile(delete=False, suffix='.rtf', mode='wb') as temp_rtf_file:
            temp_rtf_file.write(self.input_stream.getvalue())
            temp_rtf_file.flush()

        temp_txt_path = temp_rtf_file.name + ".txt"

        command = ['unrtf', '--text', temp_rtf_file.name]

        try:

            result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            with open(temp_txt_path, 'wb') as temp_txt_file:
                temp_txt_file.write(result.stdout)

            with open(temp_txt_path, 'rb') as temp_txt_file:
                output_stream.write(temp_txt_file.read())

            if result.stderr:
                logger.error(f"RTF to TXT conversion stderr: {result.stderr.decode()}")

        except subprocess.CalledProcessError as e:
            logger.error(f"An error occurred during RTF to TXT conversion: {e.stderr.decode()}")
            raise RuntimeError("RTF to TXT conversion failed") from e

        finally:
            if temp_rtf_file:
                temp_rtf_file.close()

        return output_stream
