import google.generativeai as genai

# Store the API key as a variable
api_key = "AIzaSyAi1jAyprJ-yyjKzBFgQXoGkfORQ1avvvg"  # Replace with your actual API key

# Configure the library with your API key
genai.configure(api_key=api_key)

# Create an instance of the GenerativeModel
model = genai.GenerativeModel("gemini-1.5-flash")

# Function to generate response based on user query and top-k context
def generate_response(user_query, top_k_context):
    # Combine user query with context
    combined_prompt = f"Context: {top_k_context}\n\nUser Query: {user_query}\n\nResponse:"

    # Generate the response
    response = model.generate_content(combined_prompt)

    # Check if the response contains valid content
    if response.candidates and len(response.candidates) > 0:
        return response.candidates[0].content
    else:
        return "No valid content was returned. Please adjust your prompt or try again."

# Example usage
user_query = "Explain ramayana in 50 words"
top_k_context = "The Mahabharata is one of the two major Sanskrit epics of ancient Indian literature, attributed to the sage Vyasa, and is one of the longest epics in world literature, consisting of about 100,000 shlokas (verses). It primarily tells the story of the Kurukshetra War, a great battle between two factions of a royal family—the Pandavas and the Kauravas—arising from a dispute over the throne of Hastinapura. Key characters include the five Pandavas (Yudhishthira, Bhima, Arjuna, Nakula, and Sahadeva) and their cousins, the Kauravas, led by Duryodhana, with Krishna serving as Arjuna's charioteer and advisor, who imparts the teachings of the Bhagavad Gita during the war. Central themes include duty (dharma), moral dilemmas, fate and free will, and the internal conflicts faced by the characters, emphasizing human emotions, desires, and ethical choices. The Mahabharata has profoundly influenced Indian culture, philosophy, art, and literature, inspiring numerous adaptations in various forms and continues to be studied for its rich moral and ethical lessons, offering guidance on navigating the complexities of life, making it a timeless work that resonates with audiences to this day. , The Ramayana is one of the two major ancient Indian epics, the other being the Mahabharata, and is traditionally attributed to the sage Valmiki, often regarded as the Adi Kavi or the first poet. The epic consists of about 24,000 shlokas (verses) and narrates the life and adventures of Prince Rama, the seventh avatar of the god Vishnu. The story begins in the kingdom of Ayodhya, where Rama, the eldest son of King Dasharatha, is destined to inherit the throne. However, due to the machinations of his stepmother Kaikeyi, he is exiled to the forest for fourteen years. Accompanied by his devoted wife Sita and loyal brother Lakshmana, Rama embarks on a journey filled with trials and tribulations. The narrative unfolds as Sita is abducted by the demon king Ravana, ruler of Lanka, leading Rama and Lakshmana to ally with the monkey god Hanuman and his army to rescue her. The Ramayana explores profound themes of duty (dharma), honor, loyalty, and the struggle between good and evil, emphasizing the moral dilemmas faced by its characters. The epic culminates in a fierce battle between Rama's forces and Ravana's army, resulting in Rama's victory and the rescue of Sita. Upon their return to Ayodhya, Rama is crowned king, but their journey is not without challenges; doubts about Sita's purity lead to her exile, highlighting the rigid societal norms of the time. The Ramayana is not only a story of heroism and adventure but also serves as a guide to ethical living and righteousness. Its influence extends far beyond literature, shaping art, culture, and spiritual thought across India and other parts of Southeast Asia. The epic has been adapted into countless performances, films, and modern interpretations, making it a central text in the Hindu tradition, where Rama and Sita are revered as ideals of virtue and fidelity. Through its rich narrative and multifaceted characters, the Ramayana continues to resonate with audiences, offering timeless lessons on love, sacrifice, and the importance of following one's dharma in the face of adversity."

# Get the response from the LLM
result = generate_response(user_query, top_k_context)

# Print the result
print(result)
