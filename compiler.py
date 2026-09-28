# Find the file

# Make the file usable

# 'Compile' the .story file into Python


class LocTreeCorruption(Exception):
    "The location tree has become corrupted and has either too many or too few items. Check to make sure you included a section heading and place."


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
    # If the line is an item in the current dictionary (for example, Places["name"]=...)
    elif line[0] == "#":
        output_str, tab_depth, loc_tree = compile_dict_item(line, tab_depth, loc_tree)
    # If it's a Display class, specifically the speaker-specific one. Because speaker dialogue is used so often, there's
    # shorthand to write it out. Not sure if I'll do that for display-text in general.
    elif line[0:2] == "::":
        output_str, tab_depth, loc_tree = compile_name_speaks(line, tab_depth, loc_tree)
    # If it's any Class. This should accept everything from Flag to Choice. This will be the most broad one to write.
    # Planned syntax:
    # :Display
    # .indent 1
    # This is text to display
    elif line[0] == ":":
        class_called = ""
        print(class_called)  # REMOVE

    return output_str, tab_depth, loc_tree


def compile_header(line, tab_depth, loc_tree) -> tuple[str, int, list]:
    loc_tree = [line[3:]]
    return "", tab_depth, loc_tree


def compile_dict_item(line, tab_depth, loc_tree) -> tuple[str, int, list]:
    # TODO: Add support for People[""] or change to Persons[""]

    # This renders as something like Places["name"] = Place(
    output_str = f'{loc_tree[0]}["{line[1:]}"] = {loc_tree[0][:-1]}('
    tab_depth = 1  # updating tab_depth to be accurate to current tab_depth
    # tab_depth + loc_tree is important for telling when to write textToDisplay= vs. just writing "story text here"
    if len(loc_tree) == 1:
        loc_tree.append(line[1:])
    else:
        loc_tree[1] = line[1:]
    return output_str, tab_depth, loc_tree


def compile_name_speaks(
    line: str, tab_depth: int, loc_tree: list
) -> tuple[str, int, list]:
    output_str = ""

    # If story=[] hasn't been specified yet, which we can tell by the tab depth
    if tab_depth == 1:
        output_str = "\tstory=[\n"
        tab_depth = 2
    # TODO: Figure out how to close the story's opening bracket

    # Adds Display as an item in story, with the speaker set to the current speaker
    # Note that the speaker must be defined within People
    output_str += "\t" * tab_depth + f"Display(speaker=People['{line[2:]}'],"

    # This is because the loc tree needs to get updated when you go up/down
    # Still need to figure out how to remove items from loc_tree cleanly
    if len(loc_tree) == 2:
        loc_tree.append("Display")
    elif len(loc_tree) == 3:
        loc_tree[3] = "Display"
    else:
        print("Context:", line)
        raise LocTreeCorruption

    return output_str, tab_depth, loc_tree


# Write the file as Python


def test_basic_compile():
    # TODO: Organize these more cleanly into different tests to more easily see what breaks
    # Currently tests the file top-down, going from headers, to dictionary items, to story items
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
