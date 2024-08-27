import os
from openai import OpenAI
from anthropic import Anthropic
from langchain.text_splitter import RecursiveCharacterTextSplitter

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


# def get_claude_client():
#    return Anthropic(api_key=os.environ.get('ANTHROPIC_API_KEY'))

def parse_transcript(file_path):
    with open(file_path, 'r') as file:
        return file.read()


def derive_topics_from_transcript(transcript):
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=3000,
        chunk_overlap=100,
        length_function=len
    )
    chunks = text_splitter.split_text(transcript)

    # Antropic
    #client = get_claude_client()
    topics = []
    #OpenAI
    for chunk in chunks:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates concise and relevant topic titles."},
                {"role": "user", "content": f"Given the following chunk of text from a transcript, generate a concise and relevant topic title:\n\nChunk:\n{chunk}\n\nTopic Title:"}
            ],
            max_tokens=100
        
        )
        print(response.choices[0].message.content.strip())
        topics.append(response.choices[0].message.content.strip())
        
    """
    # Antrhopic
    message = client.messages.create(
        model='claude-3-sonnet-20240229',
        max_tokens=100,
        messages=[
            {
                "role": "user",
                "content": f"Given the following chunk of text from a transcript, generate a concise and relevant topic title:\n\nChunk:\n{chunk}\n\nTopic Title:"
            }
        ]
    )
    topics.append(message.content[0].text.strip())
    """

    return topics