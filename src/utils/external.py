import re
import subprocess
import tempfile


def call_nusmv(code: str) -> bool:
    """
    Call the NuSMV binary with the given code and return the result
    :param code: NuSMV code
    :return: LTL specification result
    """
    with tempfile.NamedTemporaryFile() as temp:
        temp.write(code.encode())
        temp.seek(0)
        tmp_path = temp.name

        process = subprocess.run(
            ["nusmv", tmp_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if process.returncode != 0:
            print(process.stderr)
            raise ValueError("nusmv failed to execute")

        pattern = r"specification.*?\sis\s(true|false)"
        results = re.findall(pattern, process.stdout)
        if len(results) == 0:
            raise ValueError("No specification found in the code")

        output = str(results[0])
        if output == "true":
            output = True
        elif output == "false":
            output = False
        else:
            raise ValueError("Invalid specification value")
        return output
