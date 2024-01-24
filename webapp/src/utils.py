import enum

def generate_enum(enumClass, enumDict):
    """
    Generates python code for an Enum
    """

    enum_template = """
@unique
class {enumClass}(enum.Enum):
{enumBody}
"""

    enumBody = '\n'.join([f"    {name} = '{value}'" for (name,value) in enumDict.items()])

    return enum_template.format(enumClass=enumClass,enumBody=enumBody)