from inspect import getsource

from pyspark.sql.functions import pandas_udf


class hopsworksUdf:
    def __init__(self, func, return_type=None, name=None, module_imports=""):
        self.udf_function = func
        self.udf_type = "pandas"
        if name is None:
            self.function_name = func.__name__
        else:
            self.function_name = name
        self.return_type = return_type
        self.module_imports = module_imports
        self.function_source = (
            self.module_imports
            + "\n" * 2
            + self.remove_argument(self.udf_function, "statistics")
        )

    def remove_argument(self, func, arg_to_remove):
        # Get source code of the original function
        if isinstance(func, str):
            source_lines = func.split("\n")
        else:
            source_lines = getsource(func).split("\n")

        # Find the line where the function signature is defined
        for i, line in enumerate(source_lines):
            if line.strip().startswith("def "):
                signature_line = i
                break

        # Parse the function signature to remove the specified argument
        signature = source_lines[signature_line]
        arg_list = signature.split("(")[1].split(")")[0].split(",")
        arg_list = [
            arg.strip()
            for arg in arg_list
            if (
                arg_to_remove not in list(map(str.strip, arg.split(" ")))
                and arg_to_remove not in list(map(str.strip, arg.split(":")))
                and arg.strip() != arg_to_remove
            )
        ]

        # Reconstruct the function signature
        new_signature = (
            signature.split("(")[0]
            + "("
            + ", ".join(arg_list)
            + ")"
            + signature.split(")")[1]
        )

        # Modify the source code to reflect the changes
        source_lines[signature_line] = new_signature

        # Removing test before function signatre since they are decorators
        source_lines = source_lines[signature_line:]

        # Reconstruct the modified function as a string
        modified_source = "\n".join(source_lines)

        # Define a new function with the modified source code
        return modified_source

    def hopsworksUdf_wrapper(self, statistics):
        scope = __import__("__main__").__dict__
        scope.update(locals())
        exec(self.function_source, scope)
        return eval(self.function_name, scope)

    def __call__(self, statistics):
        return pandas_udf(
            f=self.hopsworksUdf_wrapper(statistics=statistics),
            returnType=self.return_type,
        )


def hopsworks_udf(return_type):
    def wrapper(func):
        hudf = hopsworksUdf(func=func, return_type=return_type)
        return hudf

    return wrapper
