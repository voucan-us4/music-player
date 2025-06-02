from flask import Flask, request, jsonify, render_template
from youtubesearchpython import VideosSearch

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search_youtube_api():
    search_query = request.args.get('query')
    limit = int(request.args.get('limit', 1))

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
                'videoId': video['id'],
            }
            formatted_results.append(formatted_result)

        return jsonify(formatted_results)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
