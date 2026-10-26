from pathlib import Path
from tempfile import TemporaryDirectory
import xml.etree.ElementTree as ET

from PIL import Image

from make_ascii_svg import make_ascii_svg


with TemporaryDirectory() as directory:
    image = Path(directory) / "input.png"
    output = Path(directory) / "portrait.svg"
    ns = "{http://www.w3.org/2000/svg}"
    for size, brightness in [((80, 80), 0), ((80, 80), 255),
                             ((800, 1), 255), ((10, 100), 255)]:
        Image.new("L", size, brightness).save(image)
        make_ascii_svg(image, output, target_width=80)
        root = ET.parse(output).getroot()
        rows = root.findall(f"{ns}g/{ns}text")
        assert rows, "Portrait must contain ASCII rows"
        expected = " " if brightness == 0 else "@"
        assert all(row.text == expected * 80 for row in rows), "Incorrect brightness mapping"
        assert all(28 < float(row.attrib["y"]) < 308 for row in rows), "Rows exceed the card"
        assert all(row.attrib["x"] == "185" and row.attrib["text-anchor"] == "middle"
                   for row in rows), "Portrait must be centered"
        assert all(row.attrib["{http://www.w3.org/XML/1998/namespace}space"] == "preserve"
                   for row in rows), "ASCII spacing must survive SVG rendering"

print("OK: brightness, wide/tall images, centering, and SVG spacing")
