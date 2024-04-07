from io import BytesIO
from base_converter import BaseConverter
import tempfile
import subprocess
import os
import io


class DocxToRTFConverter(BaseConverter):
    def convert(self, output_stream: BytesIO):
        try:
            # Use a temporary directory to hold the files
            with tempfile.TemporaryDirectory() as tmpdir:
                input_tmp_path = os.path.join(tmpdir, 'document.docx')
                output_tmp_path = os.path.join(tmpdir, 'document.rtf')

                # Write the input stream content to a temporary file
                with open(input_tmp_path, 'wb') as input_tmp:
                    input_tmp.write(self.input_stream.getvalue())

                # Construct and execute the Pandoc command
                command = ['pandoc', '-s', input_tmp_path, '-o', output_tmp_path]
                subprocess.run(command, check=True)

                # Read the converted RTF content back into an output stream
                output_stream = io.BytesIO()
                with open(output_tmp_path, 'rb') as output_file:
                    output_stream.write(output_file.read())

                output_stream.seek(0)
                return output_stream

        except subprocess.CalledProcessError:
            raise ("Conversion failed: Pandoc encountered an error while converting the document.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
