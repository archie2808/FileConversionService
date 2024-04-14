import unittest
import subprocess
import socket


class TestDependencies(unittest.TestCase):
    def test_libreoffice_installed(self):
        """Test if LibreOffice is installed."""
        result = subprocess.run(["libreoffice", "--version"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, "LibreOffice should be installed and return exit code 0")

    def test_unrtf_installed(self):
        """Test if unRTF is installed."""
        result = subprocess.run(["unrtf", "--version"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, "unRTF should be installed and return exit code 0")

    def test_pandoc_installed(self):
        """Test if unRTF is installed."""
        result = subprocess.run(["pandoc", "--version"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, "unRTF should be installed and return exit code 0")
    def test_clamav_network_response(self):
        """Test ClamAV daemon response over network."""
        try:

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            clamav_address = ('clamav', 3310)
            sock.connect(clamav_address)
            sock.send(b'PING\n')
            response = sock.recv(1024)
            sock.close()
            # Check if the response is 'PONG'
            self.assertIn(b'PONG', response)
        except socket.error as e:
            self.fail(f"Connection to ClamAV failed: {e}")


if __name__ == '__main__':
    unittest.main()