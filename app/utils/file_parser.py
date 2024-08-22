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


def derive_topic_from_content(content):
    """
    # Antrhopic
    client = get_claude_client()
    message = client.messages.create(
        model='claude-3-sonnet-20240229',
        max_tokens=100,
        messages=[
            {
                "role": "user",
                "content": f"Given the following content, generate a concise and relevant topic title:\n\nContent:\n{content}\n\nTopic Title:"
            }
        ]
    )
    return message.content[0].text.strip()
    """
    # Open AI
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates concise and relevant topic titles."},
            {"role": "user", "content": f"Given the following content, generate a concise and relevant topic title:\n\nContent:\n{content}\n\nTopic Title:"}
        ],
        max_tokens=100
    )
    return response.choices[0].message.content.strip()
    


def has_code_indicators(text):
    
    code_indicators = [
    "=", "var", "int", "float", "double", "string", "bool", "char",
    "{", "}", "<head>", "def ", "class ", "function", "import", "from",
    "if", "else", "elif", "for", "while", "do", "switch", "case",
    "try", "catch", "finally", "throw", "throws",
    "public", "private", "protected", "static", "final", "const",
    "return", "void", "null", "true", "false",
    "async", "await", "yield",
    "print", "console.log", "System.out.println",
    "#include", "using namespace", "package",
    "lambda", "->", "=>",
    "[]", "()", "<>", 
    "&&", "||", "!", "==", "!=", "<", ">", "<=", ">=",
    "+", "-", "*", "/", "%", "++", "--",
    "//", "/*", "*/", "#",
    "@", ":", ";", 
    "interface", "enum", "struct", "union",
    "typedef", "namespace", "template",
    "this", "super", "self",
    "new", "delete", "malloc", "free",
    "break", "continue", "goto",
    "virtual", "override", "abstract",
    "extends", "implements", "instanceof"
    ]

    return any(indicator in text for indicator in code_indicators)

def extract_code_snippets(text):
    """
    # Antrhopic
    client = get_claude_client()
    message = client.messages.create(
        model='claude-3-sonnet-20240229',
        max_tokens=1000,
        messages=[
            {
                "role": "user",
                "content": f"Extract and format all code snippets from the following text. Include only the code, not any surrounding text:\n\n{text}"
            }
        ]
    )
    return message.content[0].text.strip()
    """
    #OpenAI
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that extracts and formats code snippets."},
            {"role": "user", "content": f"Extract and format all code snippets from the following text. Include only the code, not any surrounding text:\n\n{text}"}
        ],
        max_tokens=1000
    )
    return response.choices[0].message.content.strip()

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
        print("I'm a CHUNK")
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