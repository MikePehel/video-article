import os
#from anthropic import Anthropic
from openai import OpenAI
from app.utils.article_checker import check_code, check_terms

def generate_article(transcript, topics, topic_summaries, combined_code, readme_content, speaker_info, video_title, video_description):
    
    #OpenAi client
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    # Anthropic client
    # client = Anthropic(api_key=os.environ.get('ANTHROPIC_API_KEY'))

    system_message = """
    You are a highly skilled technical writer with experience in the PX4 ecosystem including MAVSDK, MAVLink, uORB, QGroundControl ROS, ROS 2, Gazebo, and the Pixhawk open hardware standards. 
    Your task is to write a well-structured, engaging, and informative article or tutorial.
    """

    prompt = f"""
    Write an 800-word article based on the following information:

    Speaker Information: {speaker_info}

    Session Information:
    Title: {video_title}
    Description: {video_description}

    Transcript:
    {transcript}

    Topics:
    {', '.join(topics)}

    Topic Summaries:
    {', '.join(topic_summaries)}

    README Content:
    {readme_content}

    Relevant Code:
    {combined_code if combined_code else "No relevant code found."}

    Instructions:
    1. Include an introduction and a conclusion.
    2. Use the topics and topic summaries as a framework for the article's content.
    3. Include relevant code snippets from the provided code, explaining each snippet's purpose and functionality.
    4. Avoid code blocks longer than 14 lines. Break them into smaller, logical sections when necessary.
    5. Format the output in markdown.
    6. Aim for a well-structured, engaging, and informative article of approximately 800 words.

    IMPORTANT:
    Avoid using too many bulleted lists. Consolidate some lists into descriptive paragraphs if possible.
    Use ONLY the Relevant Code provided in the prompt. Do not reference or use any code from your training data or external sources.
    When code is relevant, introduce the concepts behind the code, then present the code, and finally describe how it works.
    """

    response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": system_message},
        {"role": "user", "content": prompt}
    ],
    max_tokens=4000
    )

    article = response.choices[0].message.content

    """
    # Anthropic Call
    response = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=4000,
        system=system_message,
        messages=[{"role": "user", "content": prompt}]

    article = response.content[0].text
    """

    # Apply checks
    article = check_code(article, combined_code)
    article = check_terms(article, transcript)

    return article
