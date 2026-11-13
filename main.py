from drafter import *
from dataclasses import dataclass
from bakery import assert_equal


@dataclass
class ClothingItem:
    """Represent a clothing item and the preferences it matches.

    Attributes:
        name: The name of the clothing item.
        category: The type of clothing item.
        weather: The weather the item is suited for.
        occasion: The occasion the item is suited for.
        style: The style the item matches.
        description: A short description of the item.
    """
    name: str
    category: str
    weather: str
    occasion: str
    style: str
    description: str


@dataclass
class State:
    """Store the information used throughout the website.

    Attributes:
        selected_weather: The weather selected by the user.
        selected_occasion: The occasion selected by the user.
        selected_style: The style selected by the user.
        inventory: The list of clothing items available.
        recommendations: The clothing items recommended to the user.
        saved_outfits: The list of outfits saved by the user.
    """
    selected_weather: str
    selected_occasion: str
    selected_style: str
    inventory: list[ClothingItem]
    recommendations: list[ClothingItem]
    saved_outfits: list[str]


# Create the clothing inventory
def make_initial_state() -> State:
    """Create the starting state with default preferences and clothing items.

    Returns:
        State: The initial website state.
    """
    inventory = [
        ClothingItem("Linen Button-Down", "Top", "Hot",
                     "Casual", "Comfortable",
                     "A lightweight shirt for warm days."),

        ClothingItem("Black Going-Out Top", "Top", "Mild",
                     "Going Out", "Trendy",
                     "A stylish top for a night out."),

        ClothingItem("Knit Sweater", "Top", "Cold",
                     "School/Work", "Comfortable",
                     "A cozy sweater for colder weather."),

        ClothingItem("Classic White Tee", "Top", "Any",
                     "Any", "Any",
                     "A simple everyday basic."),

        ClothingItem("Denim Shorts", "Bottoms", "Hot",
                     "Casual", "Trendy",
                     "A casual option for warm weather."),

        ClothingItem("Black Trousers", "Bottoms", "Mild",
                     "School/Work", "Simple",
                     "A polished option for school or work."),

        ClothingItem("Flowy Skirt", "Bottoms", "Mild",
                     "Going Out", "Trendy",
                     "A fun option for going out."),

        ClothingItem("Classic Jeans", "Bottoms", "Any",
                     "Any", "Any",
                     "An everyday wardrobe staple."),

        ClothingItem("Sandals", "Shoes", "Hot",
                     "Casual", "Simple",
                     "Comfortable shoes for warm weather."),

        ClothingItem("Ankle Boots", "Shoes", "Cold",
                     "Going Out", "Trendy",
                     "A stylish choice for colder days."),

        ClothingItem("Rain Boots", "Shoes", "Rainy",
                     "Casual", "Comfortable",
                     "Shoes for rainy weather."),

        ClothingItem("White Sneakers", "Shoes", "Any",
                     "Any", "Any",
                     "Versatile everyday sneakers."),

        ClothingItem("Umbrella", "Accessory", "Rainy",
                     "Casual", "Simple",
                     "An essential accessory for rainy days."),

        ClothingItem("Canvas Tote", "Accessory", "Mild",
                     "School/Work", "Simple",
                     "A practical everyday bag."),

        ClothingItem("Gold Earrings", "Accessory", "Mild",
                     "Going Out", "Trendy",
                     "An accessory to complete an outfit."),

        ClothingItem("Simple Tote Bag", "Accessory", "Any",
                     "Any", "Any",
                     "A versatile everyday accessory.")
    ]

    return State(
        "Mild",
        "Casual",
        "Comfortable",
        inventory,
        [],
        []
    )


def find_matching_items(
    inventory: list[ClothingItem],
    weather: str,
    occasion: str,
    style: str
) -> list[ClothingItem]:
    """Find clothing items that match the user's preferences.

    Args:
        inventory: The list of clothing items to search through.
        weather: The weather selected by the user.
        occasion: The occasion selected by the user.
        style: The style selected by the user.

    Returns:
        list[ClothingItem]: The matching clothing items.
    """
    matching_items = []
    selected_categories = []

    # Find exact matches
    for item in inventory:
        if item.weather == weather:
            if item.occasion == occasion:
                if item.style == style:
                    if item.category not in selected_categories:
                        matching_items.append(item)
                        selected_categories.append(item.category)

    # Add general clothing items if a category is missing
    if len(matching_items) < 4:
        for item in inventory:
            if item.weather == "Any":
                if item.occasion == "Any":
                    if item.style == "Any":
                        if item.category not in selected_categories:
                            matching_items.append(item)
                            selected_categories.append(item.category)

    return matching_items


# ROUTE 1: Home page
@route
def index(state: State) -> Page:
    """Display the home page and navigation buttons.

    Args:
        state: The current website state.

    Returns:
        Page: The home page.
    """
    return Page(state, [
        Header("OUTFIT PICKER"),
        "Find your fit. Dress for your day.",
        "",
        "Having trouble deciding what to wear?",
        "Let us help you put together an outfit!",
        "",
        Button("Find My Outfit", "preferences_page"),
        Button("Saved Outfits", "saved_outfits_page"),
        Button("About", "about_page")
    ])


# ROUTE 2: Preference form
@route
def preferences_page(state: State) -> Page:
    """Display the form for selecting outfit preferences.

    Args:
        state: The current website state.

    Returns:
        Page: The preference selection page.
    """
    return Page(state, [
        Header("Choose Your Preferences"),
        "Select the options that describe your day.",
        "",
        "What is the weather?",
        SelectBox(
            "weather",
            ["Hot", "Cold", "Rainy", "Mild"],
            state.selected_weather
        ),
        "",
        "What is the occasion?",
        SelectBox(
            "occasion",
            ["Casual", "School/Work", "Going Out"],
            state.selected_occasion
        ),
        "",
        "What is your preferred style?",
        SelectBox(
            "style",
            ["Comfortable", "Trendy", "Simple"],
            state.selected_style
        ),
        "",
        Button("Get My Outfit", "update_preferences"),
        Button("Back Home", "index")
    ])


# ROUTE 3: Update user preferences
@route
def update_preferences(
    state: State,
    weather: str,
    occasion: str,
    style: str
) -> Page:
    """Update the user's preferences and generate outfit recommendations.

    Args:
        state: The current website state.
        weather: The weather selected by the user.
        occasion: The occasion selected by the user.
        style: The style selected by the user.

    Returns:
        Page: The recommendation page with the updated state.
    """
    state.selected_weather = weather
    state.selected_occasion = occasion
    state.selected_style = style

    state.recommendations = find_matching_items(
        state.inventory,
        state.selected_weather,
        state.selected_occasion,
        state.selected_style
    )

    return recommendation_page(state)


# ROUTE 4: Recommendation results
@route
def recommendation_page(state: State) -> Page:
    """Display clothing recommendations based on the user's preferences.

    Args:
        state: The current website state containing the recommendations.

    Returns:
        Page: The page displaying the recommended outfit.
    """
    content = [
        Header("Your Outfit"),
        "Here is what we recommend based on your selections!",
        "",
        "Weather: " + state.selected_weather,
        "Occasion: " + state.selected_occasion,
        "Style: " + state.selected_style,
        ""
    ]

    if len(state.recommendations) == 0:
        content.append("No recommendations available.")
    else:
        for item in state.recommendations:
            content.append(
                item.category + ": " + item.name
                + " - " + item.description
            )

    content.extend([
        "",
        Button("Save This Outfit", "save_outfit"),
        Button("Try Different Preferences", "preferences_page"),
        Button("Back Home", "index")
    ])

    return Page(state, content)


# ROUTE 5: Save an outfit
@route
def save_outfit(state: State) -> Page:
    """Save the current outfit to the user's saved outfits list.

    Args:
        state: The current website state containing the outfit.

    Returns:
        Page: The saved outfits page.
    """
    if len(state.recommendations) == 0:
        return recommendation_page(state)

    outfit = (
        state.selected_weather + " | "
        + state.selected_occasion + " | "
        + state.selected_style + " | "
    )

    for item in state.recommendations:
        outfit += item.category + ": " + item.name + "; "

    if outfit not in state.saved_outfits:
        state.saved_outfits.append(outfit)

    return saved_outfits_page(state)


# ROUTE 6: Saved outfits page
@route
def saved_outfits_page(state: State) -> Page:
    """Display the outfits the user has saved.

    Args:
        state: The current website state.

    Returns:
        Page: The page displaying saved outfits.
    """
    content = [
        Header("Saved Outfits"),
        "Your favorite outfit combinations:",
        ""
    ]

    if len(state.saved_outfits) == 0:
        content.append("You have not saved any outfits yet.")
    else:
        for outfit in state.saved_outfits:
            content.append(outfit)
            content.append("")

    content.extend([
        Button("Clear Saved Outfits", "clear_saved_outfits"),
        Button("Find Another Outfit", "preferences_page"),
        Button("Back Home", "index")
    ])

    return Page(state, content)


# ROUTE 7: Clear saved outfits
@route
def clear_saved_outfits(state: State) -> Page:
    """Remove all outfits from the saved outfits list.

    Args:
        state: The current website state.

    Returns:
        Page: The saved outfits page after the list is cleared.
    """
    state.saved_outfits = []

    return saved_outfits_page(state)


# ROUTE 8: About page
@route
def about_page(state: State) -> Page:
    """Display information about the website and how it works.

    Args:
        state: The current website state.

    Returns:
        Page: The about page.
    """
    return Page(state, [
        Header("About The Outfit Edit"),
        "The Outfit Edit helps users decide what to wear.",
        "",
        "How it works:",
        "1. Select your weather.",
        "2. Choose your occasion.",
        "3. Select your preferred style.",
        "4. Receive matching clothing recommendations.",
        "",
        "This project was created using Python and Drafter.",
        "",
        Button("Start Choosing Outfits", "preferences_page"),
        Button("Back Home", "index")
    ])


# UNIT TESTS

# Test home page
home_page = index(make_initial_state())
assert_equal(home_page.state, make_initial_state())

# Test preference page
preference_page = preferences_page(make_initial_state())
assert_equal(preference_page.state.selected_weather, "Mild")

# Test updating preferences
test_state = make_initial_state()

update_preferences(
    test_state, "Hot", "Casual", "Comfortable"
)

assert_equal(test_state.selected_weather, "Hot")
assert_equal(test_state.selected_occasion, "Casual")
assert_equal(test_state.selected_style, "Comfortable")
assert_equal(len(test_state.recommendations), 4)

# Test recommendation page
result_page = recommendation_page(test_state)
assert_equal(result_page.state.selected_weather, "Hot")

# Test saving an outfit
save_test_state = make_initial_state()

save_test_state.recommendations = find_matching_items(
    save_test_state.inventory,
    "Hot",
    "Casual",
    "Comfortable"
)

save_outfit(save_test_state)
assert_equal(len(save_test_state.saved_outfits), 1)

# Test saved outfits page
saved_page = saved_outfits_page(save_test_state)
assert_equal(len(saved_page.state.saved_outfits), 1)

# Test clearing saved outfits
clear_saved_outfits(save_test_state)
assert_equal(len(save_test_state.saved_outfits), 0)

# Test about page
about_test_page = about_page(make_initial_state())
assert_equal(about_test_page.state.selected_weather, "Mild")


# START WEBSITE
start_server(make_initial_state())
