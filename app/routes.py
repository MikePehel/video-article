from flask import Blueprint, render_template, request, jsonify
from app.utils.file_parser import derive_topics_from_transcript
from app.utils.github_analyzer import analyze_github_repo
from app.utils.article_generator import generate_article
from app.utils.youtube_retriever import get_youtube_transcript
import markdown2

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print("Form data received:")
        for key, value in request.form.items():
            print(f"{key}: {value}")
        # Get form data
        speaker_name = request.form['speaker_name']
        speaker_bio = request.form['speaker_bio']
        video_title = request.form['video_title']
        video_description = request.form['video_description']
        github_url = request.form.get('github_url', '')
        youtube_url = request.form.get('youtube_url', '')

        # Handle transcript file
        transcript_text = ""
        if youtube_url:
            try:
                transcript_text = get_youtube_transcript(youtube_url)
            except Exception as e:
                return jsonify({'error': str(e)}), 400

        if not transcript_text:
            return jsonify({'error': 'No transcript provided or file not found'}), 400

        # Initialize topics and topic_summaries
        topics, topic_summaries = [], []

        topics = derive_topics_from_transcript(transcript_text)
        topic_summaries = [""] * len(topics)

        # Analyze GitHub repo if URL provided
        github_code = ""
        readme_content = ""
        repo_size_mb = 0
        if github_url:
            github_code, readme_content = analyze_github_repo(github_url)


        speaker_info = speaker_name + "\n " + speaker_bio

        # Generate article
        article = generate_article(
            transcript_text, topics, topic_summaries, 
            github_code, readme_content,
            speaker_info,
            video_title, video_description, 
        )

        article_html = markdown2.markdown(article)

        return render_template('article.html', article=article_html)

    return render_template('index.html')