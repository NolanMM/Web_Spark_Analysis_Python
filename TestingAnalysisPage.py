from flask import Flask, render_template, jsonify

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('AnalysisPage.html')


@app.route('/get_data')
def get_data():
    table_data = [
        {
            "VideoID": "1",
            "VideoTitle": "Sample Video 1",
            "ViewCount": 1000,
            "LikeCount": 500,
            "DislikesCount": 50,
            "CommentsCount": 200,
            "AdditionalInformation": "Additional Info 1"
        },
        {
            "VideoID": "2",
            "VideoTitle": "Sample Video 2",
            "ViewCount": 2000,
            "LikeCount": 1000,
            "DislikesCount": 100,
            "CommentsCount": 400,
            "AdditionalInformation": "Additional Info 2"
        },
        {
            "VideoID": "3",
            "VideoTitle": "Sample Video 3",
            "ViewCount": 3000,
            "LikeCount": 1500,
            "DislikesCount": 200,
            "CommentsCount": 600,
            "AdditionalInformation": "Additional Info 3"
        }
    ]
    data = {
        'table_data': table_data,
        'TotalViews': 10000,
        'TotalLikes': 2000,
        'TotalDislikes': 500,
        'TotalEngagement': 1200,
        'labels': ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
                   "November", "December"],
        'views': [1000, 1200, 1300, 1500, 1400, 1600, 1700, 1800, 1900, 2000, 2100, 2200],
        'likes': [200, 220, 230, 250, 240, 260, 270, 280, 290, 300, 310, 320],
        'dislikes': [50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 105],
        'engagement': [120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230]
    }
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True, port=8000)
