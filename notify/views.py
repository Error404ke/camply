from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

@login_required
def notification_list(request):
    return HttpResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Notifications</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: #0a0a2e;
                color: white;
                padding: 20px;
                text-align: center;
            }
            .container {
                max-width: 400px;
                margin: 50px auto;
                background: rgba(255,255,255,0.05);
                padding: 40px;
                border-radius: 20px;
                backdrop-filter: blur(10px);
            }
            .btn {
                display: inline-block;
                padding: 12px 24px;
                background: #f9a825;
                color: white;
                text-decoration: none;
                border-radius: 10px;
                margin-top: 20px;
            }
            .btn:hover {
                background: #ff6f00;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔔 Notifications</h1>
            <p>Your notifications will appear here</p>
            <a href="/" class="btn">Back to Home</a>
        </div>
    </body>
    </html>
    """)
