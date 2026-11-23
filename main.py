# ==========================================================
# PROJECT: AI TUTOR CHATBOT USING PROMPT ENGINEERING
# ==========================================================

# STEP 1: IMPORT REQUIRED PACKAGES & MODULES
# ==========================================================

from dotenv import load_dotenv
import os
import json
from groq import Groq


# STEP 2: LOAD ENVIRONMENT VARIABLES
# ==========================================================

load_dotenv()


# STEP 3: GET THE API KEY
# ==========================================================

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("API key not found! Check your .env file.")


# STEP 4: CREATE THE GROQ CLIENT
# ==========================================================

client = Groq(api_key=api_key)


# STEP 5: SYSTEM INSTRUCTION
# ==========================================================

system_message = {
    "role": "system",
    "content": """
    You are a friendly and professional AI tutor.

    ROLE:
    Act as an experienced teacher.

    CONTEXT:
    You are teaching beginners who have basic computer knowledge.

    TASK:
    Help users understand technical and non-technical concepts.

    PROMPT ENGINEERING RULES:

    1. Role Prompting:
       Act as a friendly AI tutor.

    2. Context Prompting:
       Understand that the user is a beginner.

    3. Task Prompting:
       Explain concepts clearly with examples.

    4. Constraint Prompting:
       - Use simple English.
       - Avoid unnecessary technical words.
       - Keep answers clear.
       - Give practical examples.
       - Do not provide unrelated information.

    5. Output Formatting:
       - Definition
       - Explanation
       - Example
       - Practical Application

    6. Few-Shot Prompting:

       Example Question:
       What is a variable?

       Example Answer:
       A variable is a container used to store data.

       Example:
       name = "Abitha"

       Here, name is a variable that stores the value Abitha.

    IMPORTANT:
    Use previous conversation context when relevant.
    """
}


# STEP 6: LOAD PREVIOUS CONVERSATION FROM JSON
# ==========================================================

if os.path.exists("chat_history.json"):

    with open("chat_history.json", "r", encoding="utf-8") as file:

        try:

            messages = json.load(file)

        except json.JSONDecodeError:

            messages = [system_message]

else:

    messages = [system_message]


# STEP 7: MAKE SURE SYSTEM INSTRUCTION EXISTS
# ==========================================================

if not messages or messages[0].get("role") != "system":

    messages.insert(0, system_message)

else:

    messages[0] = system_message


# STEP 8: PROMPT ENGINEERING FUNCTION
# ==========================================================

def create_prompt(user_input):

    prompt = f"""
    ROLE:
    Act as a friendly and professional AI tutor.

    CONTEXT:
    The user is a beginner who wants to learn new concepts.

    USER QUESTION:
    {user_input}

    TASK:
    Explain the given question clearly.

    CONSTRAINTS:
    - Use simple English.
    - Explain step by step.
    - Give a real-time example.
    - Avoid unnecessary information.
    - Keep the answer beginner-friendly.

    OUTPUT FORMAT:
    1. Definition
    2. Simple Explanation
    3. Practical Example
    4. Real-Time Application

    INSTRUCTION:
    Answer the user's actual question.
    Do not force headings when they are not suitable.
    """

    return prompt


# STEP 9: START CHATBOT LOOP
# ==========================================================

while True:

    print("\n" + "=" * 50)
    print("             AI TUTOR CHATBOT")
    print("=" * 50)

    user_input = input("\nYou: ").strip()


    # STEP 10: EXIT COMMAND
    # ======================================================

    if user_input.lower() == "bye bye":

        print("\nAI: Goodbye! Happy Learning!")

        break


    # STEP 11: CHECK EMPTY INPUT
    # ======================================================

    if not user_input:

        print("\nPlease enter a question.")

        continue


    # STEP 12: CREATE ENGINEERED PROMPT
    # ======================================================

    engineered_prompt = create_prompt(user_input)


    # STEP 13: ADD USER MESSAGE TO HISTORY
    # ======================================================

    messages.append(
        {
            "role": "user",
            "content": engineered_prompt
        }
    )


    try:

        # STEP 14: KEEP RECENT CONVERSATION CONTEXT
        # ==================================================

        recent_messages = [system_message] + messages[1:][-10:]


        # STEP 15: SEND REQUEST WITH STREAMING ENABLED
        # ==================================================

        response = client.chat.completions.create(

            model="openai/gpt-oss-20b",

            messages=recent_messages,

            stream=True,

            include_reasoning=False

        )


        # STEP 16: STORE THE STREAMED RESPONSE
        # ==================================================

        answer = ""


        # STEP 17: DISPLAY RESPONSE CHUNK BY CHUNK
        # ==================================================

        print("\nAI: ", end="", flush=True)

        for chunk in response:

            content = chunk.choices[0].delta.content

            if content:

                print(
                    content,
                    end="",
                    flush=True
                )

                answer += content

        print()


        # STEP 18: ADD AI RESPONSE TO HISTORY
        # ==================================================

        messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )


        # STEP 19: SAVE CONVERSATION IN JSON FILE
        # ==================================================

        with open("chat_history.json", "w", encoding="utf-8") as file:

            json.dump(
                messages,
                file,
                indent=4,
                ensure_ascii=False
            )

        print("\n[Conversation saved successfully!]")


    # STEP 20: HANDLE ERRORS
    # ======================================================

    except Exception as error:

        print("\nError:", error)

        # Remove failed user message
        if messages and messages[-1]["role"] == "user":

            messages.pop()


# ==========================================================
# END OF PROJECT
# ==========================================================