from flask import Flask, request, jsonify, render_template
from youtubesearchpython import VideosSearch

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search_youtube_api():
    search_query = request.args.get('query')
    limit = int(request.args.get('limit', 1))  # Default limit is 5 if not specified

    if not search_query:
        return jsonify({'error': 'Query parameter "query" is required'}), 400

    try:
        videos = VideosSearch(search_query, limit=limit)
        results = videos.result()['result']

        formatted_results = []
        for video in results:
            channel = video.get('channel', {})
            thumbnails = channel.get('thumbnails', [])

            formatted_result = {
                'title': video['title'],
                'link': video['link'],
                'videoId': video['id'],
                'thumbnail': thumbnails[0]['url'] if thumbnails else None,
                'duration': video['duration'] if 'duration' in video and video['duration'] else 'Not Available',
                'uploader': channel.get('name', None),
                'channel_icon': thumbnails[0]['url'] if thumbnails else None,
                'channel_link': channel.get('link', None),
                'views': video['viewCount']['short'] if 'viewCount' in video and 'short' in video['viewCount'] else 'Not Available',
            }
            formatted_results.append(formatted_result)

        return jsonify(formatted_results)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
