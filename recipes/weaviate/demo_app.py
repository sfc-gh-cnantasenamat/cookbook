import streamlit as st

# Constants
NUM_IMAGES_PER_ROW = 5
SEARCH_LIMIT = 10

# Search Mode descriptions
SEARCH_MODES = {
    "Keyword": ("Keyword search (BM25) ranks documents based on the relative frequencies of search terms.", 0),
    "Semantic": ("Semantic (vector) search ranks results based on their similarity to your search query.", 1),
    "Hybrid": ("Hybrid search combines vector and BM25 searches to offer best-of-both-worlds search results.", 0.7),
}

def display_chat_messages():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "images" in message:
                for i in range(0, len(message["images"]), NUM_IMAGES_PER_ROW):
                    cols = st.columns(NUM_IMAGES_PER_ROW)
                    for j, col in enumerate(cols):
                        if i + j < len(message["images"]):
                            col.image(message["images"][i + j], width=200)

def setup_sidebar():
    with st.sidebar:
        st.title("🎥🍿 Movie Magic")
        st.subheader("The RAG Recommender")
        st.markdown("Your Weaviate & AI powered movie recommender. Find the perfect film for any occasion. Just tell us what you're looking for!")
        st.header("Settings")

        mode = st.radio("Search Mode", options=list(SEARCH_MODES.keys()), index=2)
        year_range = st.slider("Year range", min_value=1950, max_value=2024, value=(1990, 2024))
        st.info(SEARCH_MODES[mode][0])
        st.success("Connected to Weaviate", icon="💚")

    return mode, year_range

def display_example_prompts():
    example_prompts = [
        ("sci-fi adventure", "movie night with friends"),
        ("romantic comedy", "date night"),
        ("animated family film", "family viewing"),
        ("classic thriller", "solo watching"),
        ("historical drama", "educational evening"),
        ("indie comedy-drama", "film club discussion"),
    ]

    example_prompts_help = [
        "Search for sci-fi adventure movies suitable for a group viewing",
        "Find romantic comedies perfect for a date night",
        "Look for animated movies great for family entertainment",
        "Discover classic thrillers for a solo movie night",
        "Explore historical dramas for an educational movie experience",
        "Find indie comedy-dramas ideal for film club discussions",
    ]

    st.markdown("---")
    st.write("Select an example prompt or enter your own, then **click `Search`** to get recommendations.")

    button_cols = st.columns(3)
    button_cols_2 = st.columns(3)

    for i, ((movie_type, occasion), help_text) in enumerate(zip(example_prompts, example_prompts_help)):
        col = button_cols[i] if i < 3 else button_cols_2[i-3]
        if col.button(f"{movie_type} for a {occasion}", help=help_text):
            st.session_state.example_movie_type = movie_type
            st.session_state.example_occasion = occasion
            return True
    return False

def main():
    st.title("🎥🍿 Movie Magic")

    mode, year_range = setup_sidebar()

    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.greetings = False

    display_chat_messages()

    if not st.session_state.greetings:
        with st.chat_message("assistant"):
            intro = "👋 Welcome to Movie Magic! I'm your AI movie recommender. Tell me what kind of film you're in the mood for and the occasion, and I'll suggest some great options."
            st.markdown(intro)
            st.session_state.messages.append({"role": "assistant", "content": intro})
            st.session_state.greetings = True

    if "example_movie_type" not in st.session_state:
        st.session_state.example_movie_type = ""
    if "example_occasion" not in st.session_state:
        st.session_state.example_occasion = ""

    example_selected = display_example_prompts()

    movie_type = st.text_input(
        "What movies are you looking for?",
        value=st.session_state.example_movie_type,
        placeholder="E.g., sci-fi adventure, romantic comedy"
    )

    viewing_occasion = st.text_input(
        "What occasion is the movie for?",
        value=st.session_state.example_occasion,
        placeholder="E.g., movie night with friends, date night"
    )

    if st.button("Search") and movie_type and viewing_occasion:
        prompt = f"Searching for: {movie_type} for {viewing_occasion}"
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Placeholder for search results
        st.write("Search results would appear here.")

if __name__ == "__main__":
    main()
