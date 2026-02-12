"""EnterpriseManager model contains the logic for CIF validation and JSON processing."""

import json
from EnterpriseManagementException import EnterpriseManagementException
from EnterpriseRequest import EnterpriseRequest

PRE = {"J":0, "A":1, "B":2, "C":3, "D":4, "E":5, "F":6, "G":7, "H":8, "I":9}

class EnterpriseManager:
    """EnterpriseManager class contains the logic for CIF validation."""
    def __init__(self):
        pass

    @staticmethod
    def validate_cif(cif):

        # PLEASE INCLUDE HERE THE CODE FOR VALIDATING THE GUID
        # RETURN TRUE IF THE GUID IS RIGHT, OR FALSE IN OTHER CASE
        if len(cif) != 9 or cif[0] not in PRE or not cif[1:].isdigit():
            return False
        even_pos_sum = 0
        odd_sum = 0
        # Positions 1–7 are digits (skip prefix at position 0)
        for position in range(1, 8):
            num = int(cif[position])

            if position % 2 == 0:  # even position
                even_pos_sum += num
            else:  # odd position
                scaled = num * 2
                odd_sum += scaled if scaled < 10 else (scaled // 10 + scaled % 10)

        total = even_pos_sum + odd_sum
        control_digit = (10 - (total % 10)) % 10

        last_char = cif[8]

        # Last character can be a digit or a letter
        if last_char.isdigit():
            return control_digit == int(last_char)

        return control_digit == PRE.get(last_char, -1)

    def read_product_code_from_json( self, fi ):

        try:
            with open(fi) as f:
                data = json.load(f)
        except FileNotFoundError as e:
            raise EnterpriseManagementException("Wrong file or file path") from e
        except json.JSONDecodeError as e:
            raise EnterpriseManagementException("JSON Decode Error - Wrong JSON Format") from e

        try:
            t_cif = data["cif"]
            t_phone = data["phone"]
            e_name = data["enterprise_name"]
            req = EnterpriseRequest(t_cif, t_phone,e_name)
        except KeyError as e:
            raise EnterpriseManagementException("JSON Decode Error - Invalid JSON Key") from e
        if not self.validate_cif(t_cif) :
            raise EnterpriseManagementException("Invalid FROM IBAN")
        return req

if __name__ == "__main__":
    manager = EnterpriseManager()

    valid_cifs = [
        "A12345674",  # numeric control digit
        "J94058213"  # numeric control digit
    ]

    print("=== VALIDATE_CIF TESTS ===")
    for ex_cif in valid_cifs:
        print(ex_cif, "->", manager.validate_cif(ex_cif))
