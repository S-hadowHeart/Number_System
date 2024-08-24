from flask import Flask, render_template, request

app = Flask(__name__)

# Conversion functions here (from the previous Python code)
def bin_to_dec(binary_str):
    return int(binary_str, 2)

def bin_to_oct(binary_str):
    return oct(bin_to_dec(binary_str))[2:]

def bin_to_hex(binary_str):
    return hex(bin_to_dec(binary_str))[2:].upper()

def dec_to_bin(decimal):
    return bin(decimal)[2:]

def dec_to_oct(decimal):
    return oct(decimal)[2:]

def dec_to_hex(decimal):
    return hex(decimal)[2:].upper()

def oct_to_dec(octal_str):
    return int(octal_str, 8)

def oct_to_bin(octal_str):
    return dec_to_bin(oct_to_dec(octal_str))

def oct_to_hex(octal_str):
    return dec_to_hex(oct_to_dec(octal_str))

def hex_to_bin(hex_str):
    return dec_to_bin(int(hex_str, 16))

def hex_to_dec(hex_str):
    return int(hex_str, 16)

def hex_to_oct(hex_str):
    return dec_to_oct(hex_to_dec(hex_str))

def detect_number_type(number_str):
    if number_str.startswith("b{"):
        return "binary", number_str[2:-1]
    elif number_str.startswith("d{"):
        return "decimal", number_str[2:-1]
    elif number_str.startswith("o{"):
        return "octal", number_str[2:-1]
    elif number_str.startswith("h{"):
        return "hexadecimal", number_str[2:-1]
    elif all(c in '01' for c in number_str):
        return "binary", number_str
    elif all(c in '01234567' for c in number_str):
        return "octal", number_str
    elif all(c in '0123456789' for c in number_str):
        return "decimal", number_str
    elif all(c in '0123456789ABCDEFabcdef' for c in number_str):
        return "hexadecimal", number_str
    else:
        return "invalid", None

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        number_str = request.form["number_input"]
        num_type, num_value = detect_number_type(number_str)

        if num_type == "invalid":
            return render_template("index.html", error="Invalid number format!")

        conversions = {}
        if num_type == "binary":
            conversions = {
                "Decimal": bin_to_dec(num_value),
                "Octal": bin_to_oct(num_value),
                "Hexadecimal": bin_to_hex(num_value)
            }
        elif num_type == "decimal":
            decimal_value = int(num_value)
            conversions = {
                "Binary": dec_to_bin(decimal_value),
                "Octal": dec_to_oct(decimal_value),
                "Hexadecimal": dec_to_hex(decimal_value)
            }
        elif num_type == "octal":
            conversions = {
                "Decimal": oct_to_dec(num_value),
                "Binary": oct_to_bin(num_value),
                "Hexadecimal": oct_to_hex(num_value)
            }
        elif num_type == "hexadecimal":
            conversions = {
                "Binary": hex_to_bin(num_value),
                "Decimal": hex_to_dec(num_value),
                "Octal": hex_to_oct(num_value)
            }

        return render_template("index.html", conversions=conversions, num_type=num_type.capitalize(), num_value=num_value)
    
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10001, debug=False)

