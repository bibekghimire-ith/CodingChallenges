import sys

class JSONParser:
    def __init__(self):
        self.pos = 0
        self.text = ''

    def parse(self, text):
        self.text = text.strip()
        self.pos = 0
        try:
            result = self._parse_value()
            self._consume_whitespace()
            if self.pos != len(self.text):
                raise ValueError("Extra data after valid JSON")
            print("Valid JSON")
            return 0
        except Exception as e:
            print(f"Invalid JSON: {e}")
            return 1

    def _parse_value(self):
        self._consume_whitespace()
        if self._peek() == '{':
            return self._parse_object()
        elif self._peek() == '[':
            return self._parse_array()
        elif self._peek() == '"':
            return self._parse_string()
        elif self._peek().isdigit() or self._peek() == '-':
            return self._parse_number()
        elif self.text.startswith("true", self.pos):
            self.pos += 4
            return True
        elif self.text.startswith("false", self.pos):
            self.pos += 5
            return False
        elif self.text.startswith("null", self.pos):
            self.pos += 4
            return None
        else:
            raise ValueError(f"Unexpected character at position {self.pos}: '{self._peek()}'")

    def _parse_object(self):
        obj = {}
        self._expect('{')
        self._consume_whitespace()
        if self._peek() == '}':
            self._expect('}')
            return obj
        while True:
            self._consume_whitespace()
            key = self._parse_string()
            self._consume_whitespace()
            self._expect(':')
            self._consume_whitespace()
            value = self._parse_value()
            obj[key] = value
            self._consume_whitespace()
            if self._peek() == '}':
                self._expect('}')
                break
            self._expect(',')
        return obj

    def _parse_array(self):
        arr = []
        self._expect('[')
        self._consume_whitespace()
        if self._peek() == ']':
            self._expect(']')
            return arr
        while True:
            self._consume_whitespace()
            value = self._parse_value()
            arr.append(value)
            self._consume_whitespace()
            if self._peek() == ']':
                self._expect(']')
                break
            self._expect(',')
        return arr

    def _parse_string(self):
        self._expect('"')
        start = self.pos
        while self._peek() != '"':
            if self._peek() == '\\':
                self.pos += 1
            self.pos += 1
            if self.pos >= len(self.text):
                raise ValueError("Unterminated string")
        result = self.text[start:self.pos]
        self._expect('"')
        return result

    def _parse_number(self):
        start = self.pos
        if self._peek() == '-':
            self.pos += 1
        while self._peek().isdigit():
            self.pos += 1
        if self._peek() == '.':
            self.pos += 1
            while self._peek().isdigit():
                self.pos += 1
        return float(self.text[start:self.pos]) if '.' in self.text[start:self.pos] else int(self.text[start:self.pos])

    def _peek(self):
        if self.pos >= len(self.text):
            return ''
        return self.text[self.pos]

    def _expect(self, char):
        if self._peek() != char:
            raise ValueError(f"Expected '{char}' at position {self.pos}")
        self.pos += 1

    def _consume_whitespace(self):
        while self._peek() in ' \t\n\r':
            self.pos += 1


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python jsonParser.py <path_to_json_file>")
        sys.exit(1)

    with open(sys.argv[1], 'r') as f:
        content = f.read()

    parser = JSONParser()
    sys.exit(parser.parse(content))