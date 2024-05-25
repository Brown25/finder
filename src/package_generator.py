# src/package_generator.py

import random
import string

class PackageNumberGenerator:
    def generate(self):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
