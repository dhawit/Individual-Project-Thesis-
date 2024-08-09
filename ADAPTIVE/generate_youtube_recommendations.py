# import requests

# # Replace with your YouTube Data API key
# API_KEY = 'YOUR_YOUTUBE_API_KEY'

# # Video IDs and titles
# VIDEO_IDS = {
#     'Flutter Course for Beginners': 'VPvVD8t02U8',
#     'Flutter Basic Training': '1xipg02Wu8s',
#     'Flutter Tutorial For Beginners': 'CD1Y2DmL5JM',
#     'React Tutorial for Beginners': 'SqcY0GlETPk',
#     'Cyber Security In 7 Minutes': 'inWWhr5tnEA'
# }

# def get_video_details(video_id):
#     """
#     Fetch video details from YouTube Data API.
#     """
#     url = f'https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={API_KEY}'
#     response = requests.get(url).json()
#     if 'items' in response and len(response['items']) > 0:
#         item = response['items'][0]
#         title = item['snippet']['title']
#         thumbnail_url = item['snippet']['thumbnails']['high']['url']
#         return title, thumbnail_url
#     return None, None

# def generate_html_recommendations():
#     """
#     Generate HTML content with video recommendations and thumbnails.
#     """
#     recommendations = generate_recommendations()
#     html_content = '''
#     <!DOCTYPE html>
#     <html lang="en">
#     <head>
#         <meta charset="UTF-8">
#         <meta name="viewport" content="width=device-width, initial-scale=1.0">
#         <title>YouTube Recommendations</title>
#         <style>
#             body {
#                 font-family: Arial, sans-serif;
#                 line-height: 1.6;
#             }
#             .recommendation {
#                 margin: 20px 0;
#             }
#             .recommendation img {
#                 width: 320px;
#                 height: 180px;
#                 object-fit: cover;
#                 border: 1px solid #ddd;
#                 border-radius: 4px;
#             }
#             .recommendation a {
#                 text-decoration: none;
#                 color: #333;
#             }
#             .recommendation a:hover {
#                 color: #007bff;
#             }
#         </style>
#     </head>
#     <body>
#         <h1>YouTube Recommendations</h1>
#     '''
    
#     recommendations = generate_recommendations()
    
#     for rec in recommendations:
#         html_content += f'''
#         <div class="recommendation">
#             <a href="{rec['url']}" target="_blank">
#                 <img src="{rec['thumbnail']}" alt="{rec['title']}">
#                 <p>{rec['title']}</p>
#             </a>
#         </div>
#         '''
    
#     html_content += '''
#     </body>
#     </html>
#     '''
    
#     with open('recommendations.html', 'w') as file:
#         file.write(html_content)

# # Fetch video recommendations
# def generate_recommendations():
#     """
#     Generate recommendations with titles and thumbnails.
#     """
#     recommendations = []
#     for title, video_id in VIDEO_IDS.items():
#         video_title, thumbnail_url = get_video_details(video_id)
#         if video_title and thumbnail_url:
#             recommendations.append({
#                 'title': video_title,
#                 'thumbnail': thumbnail_url,
#                 'url': f'https://www.youtube.com/watch?v={video_id}'
#             })
#     return recommendations

# # Generate and save the HTML file
# generate_html_recommendations()
