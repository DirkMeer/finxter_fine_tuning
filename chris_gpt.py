from constants import CLIENT, OUTPUT_DIRECTORY, CHRIS_GPT
import time


leaf_blower = """
Introduction to the AI-powered leaf blower and its innovative features in the realm of yard maintenance equipment.
Description of how the AI technology enhances the efficiency and performance of the leaf blower compared to traditional models.
Overview of the specific AI algorithms and sensors integrated into the leaf blower for optimized leaf collection and debris management.
Real-world application scenarios demonstrating the effectiveness of the AI-powered leaf blower in various landscaping and gardening tasks.
Discussion on the environmental benefits of using the AI-powered leaf blower, such as reduced noise pollution and energy consumption.
Insights into the future development and potential advancements in AI-powered yard maintenance equipment, including further automation and integration with smart home systems.
"""

super_robot = """
new AI-powered robot:
All-in-one household chore solution
Capable of cleaning, laundry, dishwashing, cooking, and car washing
Utilizes advanced AI and robotics technology
Customizable chore scheduling options
Maximizes efficiency and productivity
Seamlessly integrates with smart home systems
"""

sharks = """
Briefly introduce the topic of great white sharks and why you're discussing them.
Describe the appearance and size of great white sharks, highlighting their distinctive features.
Discuss where great white sharks are commonly found and their preferred habitats, such as coastal waters and oceanic regions.
Diet and Feeding Behavior: Explain what great white sharks eat and how they hunt, including their role as apex predators in marine ecosystems.
Provide information about the conservation status of great white sharks, including any threats they face and conservation efforts to protect them.
Discuss human interactions with great white sharks, including encounters in the wild, conservation initiatives, and safety measures for beachgoers and divers.
"""


def chris_gpt(topics: str) -> str:
    response = CLIENT.chat.completions.create(
        model=CHRIS_GPT,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that writes emails for the Finxter email newsletter, adhering perfectly to the style and tone of the Finxter brand and Chris' writing style. You will respond in Simple text format. Don't insert any newline characters and such but use an actual newline. Make sure that the subject makes sense in regards to the content of the email. Keep the email CONCISE AND TO THE POINT, and STAY ON TOPIC. Do not repeat yourself. Don't forget to add Chris' signature emoticons. Also don't make up nonsense terms that do not exist, and make sure you ALWAYS USE CORRECT SPELLING! The user will inform you about the topics of the email:",
            },
            {"role": "user", "content": topics},
        ],
    )

    return (
        response.choices[0].message.content
        or "There was an error with the response. Please try again."
    )


current_unix_time = int(time.time())

filename = f"chris_gpt_output_{current_unix_time}.txt"

with open(OUTPUT_DIRECTORY / filename, "w", encoding="utf-8") as file:
    file.write(chris_gpt(sharks))
