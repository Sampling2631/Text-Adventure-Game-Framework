# Find the file

# Make the file usable

# 'Compile' the .story file into Python
test_str = """
###Places
#Home
:Display
Hello, my name is James
"""


def compile(line, tab_depth: int = 0, loc_tree: list = []) -> tuple[str, int, list]:
    output_str = ""

    if line[0] == "%":
        return "", tab_depth, loc_tree

    # Checking top-down (headers, then different places/routes/people, then options/things within story)
    # If the line is a header
    if line[0:3] == "###":
        output_str, tab_depth, loc_tree = compile_header(line, tab_depth, loc_tree)
    elif line[0] == "#":
        output_str, tab_depth, loc_tree = compile_dict_item(line, tab_depth, loc_tree)
    elif line[0:2] == "::":
        output_str, tab_depth, loc_tree = compile_name_speaks(line, tab_depth, loc_tree)
    elif line[0] == ":":
        class_called = ""
        print(class_called)  # REMOVE

    return output_str, tab_depth, loc_tree


def compile_header(line, tab_depth, loc_tree) -> tuple[str, int, list]:
    loc_tree = [line[3:]]
    return "", tab_depth, loc_tree


def compile_dict_item(line, tab_depth, loc_tree) -> tuple[str, int, list]:
    output_str = f'{loc_tree[0]}["{line[1:]}"] = {loc_tree[0][:-1]}('
    tab_depth = 1
    if len(loc_tree) == 1:
        loc_tree.append(line[1:])
    else:
        loc_tree[1] = line[1:]
    return output_str, tab_depth, loc_tree


def compile_name_speaks(
    line: str, tab_depth: int, loc_tree: list
) -> tuple[str, int, list]:
    output_str = ""

    if tab_depth == 1:
        output_str = "\tstory=[\n"
        tab_depth = 2

    output_str += "\t" * tab_depth + f"Display(speaker=People['{line[2:]}'],"

    if len(loc_tree) == 2:
        loc_tree.append("Display")
    elif len(loc_tree) == 3:
        loc_tree[3] = "Display"
    else:
        raise Exception(
            f"The location tree has become corrupted. It has either too many or too few items when processing {line}\nCheck to make sure you inluded a Section Heading and Place above it"
        )

    return output_str, tab_depth, loc_tree


# Write the file as Python


def test_basic_compile():
    _, tab_depth, loc_tree_test = compile("###Places")
    test_place_output, tab_depth, loc_tree = compile(
        "#Home", tab_depth, loc_tree_test.copy()
    )
    test_name_output, tab_depth, loc_tree = compile("::James", tab_depth, loc_tree)

    assert loc_tree_test == ["Places"], (
        "Headers don't get compiled correctly into the location tree"
    )
    assert test_place_output == 'Places["Home"] = Place(', (
        "Places no longer get defined correctly"
    )
    assert test_name_output == "\tstory=[\n\t\tDisplay(speaker=People['James'],"


test_basic_compile()
