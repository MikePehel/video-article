from anthropic import Anthropic
from openai import OpenAI
import os

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
def check_code(article, combined_code):
    #OpenAI API

    #Anthropic client
    # client = Anthropic(api_key=os.environ.get('ANTHROPIC_API_KEY'))

    prompt = f"""
    Audit this Article for the correct and accurate use of the code within it. Use the Combined Code as your primary code reference. If code in the Article looks similar or calls similar functions but is slightly different than the Combined Code, replace it in the final output with the relevant Combined Code snippet supplied in part or in whole, whichever fits best for the task.
  
    If the article's content needs to be slightly modified to fit the code you are replacing it with from Combined Code, do so and only add content that is necessary.

    Article: {article}

    Combined Code: {combined_code if combined_code else "No relevant code found."}

    Return the edited article as your final output.
    """

    system_message = """
    You are a highly skilled technical writer with experience in the PX4 ecosystem including MAVSDK, MAVLink, uORB, QGroundControl ROS, ROS 2, Gazebo, and the Pixhawk open hardware standards. 
    You are editing the content in the article for accuracy and correctness.

    IMPORTANT: Your focus is auditing the code and replacing it if necessary.
    Audit the code based on the Combined Code supplied. If no code is supplied, do nothing. 
    Return the whole edited article.
    Do not add any llm assistant language such as and inclduing "no other edits were made", "Here's the edited article..", "Here's the edited article with the code snippets updated based on the Combined Code provided:" or the "The rest of the article remains unchanged". Only return the edited or non-edited article copy and nothing else.
    """

    #OpenAI Response
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ],
        max_tokens=4000
    )

    return response.choices[0].message.content


    """
    #Anthropic response
    response = client.messages.create(
        model='claude-3-5-sonnet-20240620',
        max_tokens=4000,
        system=system_message,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.content[0].text
    
    """

def check_terms(article, transcript):
    #Anthropic client
    # client = Anthropic(api_key=os.environ.get('ANTHROPIC_API_KEY'))

    prompt = f"""
    Audit this Article for the correct and accurate use of acronyms and trade terms related to the drone industry, aviation, and robotics. If a term in the Article phonetically is similar to an industry term, check the context and replace it with the industry term. For example, "lance" should be replaced with LAANC, if the context was LAANC Authorization. Conversely, if the example was a man named Lance, keep it as Lance.

    Use the Transcript as a context reference only. Your focus is editing the article.
    
    Article: {article}

    Transcript: {transcript}

    Return the edited article as your final output.
    """

    system_message = """
    You are a highly skilled technical writer with experience in the drone industry and aviation regulation including deep knowledge of the FAA, EASA, drone development and manufacturing. 
    Your task is to write a well-structured, engaging, and informative article.
    
    IMPORTANT: Your focus is finding incorrectly spelled or used industry terms and replacing them with accurate ones if necessary. 
    Return the whole edited article.
    Do not add any llm assistant language such as and inclduing "no other edits were made", "Here's the edited article..", "Here's the edited article with the edited terms:" or the "The rest of the article remains unchanged". Only return the edited or non-edited article copy and nothing else.
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ],
        max_tokens=4000
    )

    return response.choices[0].message.content


    """
    response = client.messages.create(
        model='claude-3-5-sonnet-20240620',
        max_tokens=4000,
        system=system_message,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.content[0].text
    """


