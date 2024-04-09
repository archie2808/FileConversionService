from io import BytesIO
from base_converter import BaseConverter
import tempfile
import subprocess
import os
import io
import logger_config

logger = logger_config.configure_logger(__name__)


class DocxToRTFConverter(BaseConverter):
    def convert(self, output_stream: BytesIO):
        try:
            # Use a temporary directory to hold the files
            with tempfile.TemporaryDirectory() as tmpdir:
                logger.debug("Created temporary directory: %s", tmpdir)

                input_tmp_path = os.path.join(tmpdir, 'document.docx')
                output_tmp_path = os.path.join(tmpdir, 'document.rtf')
                logger.debug("Temporary paths set for input: %s and output: %s", input_tmp_path, output_tmp_path)

                # Write the input stream content to a temporary file
                with open(input_tmp_path, 'wb') as input_tmp:
                    input_tmp.write(self.input_stream.getvalue())
                logger.debug("Wrote input stream to temporary file")

                # Construct and execute the Pandoc command
                command = ['pandoc', '-s', input_tmp_path, '-o', output_tmp_path]
                logger.debug("Executing command: %s", ' '.join(command))
                subprocess.run(command, check=True)
                logger.debug("Pandoc conversion executed successfully")

                # Read the converted RTF content back into an output stream
                with open(output_tmp_path, 'rb') as output_file:
                    file_content = output_file.read()
                    if not file_content:
                        logger.warning("The converted RTF file is empty")
                    output_stream.write(file_content)
                logger.debug("Read converted RTF content back into the output stream")

                output_stream.seek(0)
                return output_stream

        except subprocess.CalledProcessError as e:
            logger.error("Conversion failed: Pandoc encountered an error while converting the document. %s", e)
            raise RuntimeError("Conversion failed: Pandoc encountered an error.") from e
        except Exception as e:
            logger.exception("An unexpected error occurred during the conversion process.")
            raise RuntimeError("An unexpected error occurred.") from e
