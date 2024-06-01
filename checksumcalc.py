import hashlib

def calculate_checksum(filename):
    """Calculates the SHA-256 checksum of a file."""
    sha256_hash = hashlib.sha256()
    with open(filename, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

if __name__ == "__main__":
    filename = "main.py"  # Specify the name of your main script
    checksum = calculate_checksum(filename)
    print(f"SHA-256 checksum of {filename}: {checksum}")
