from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    username = request.user.username
    html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Camly - Home</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        /* ===== CSS Variables for Themes ===== */
        :root {{
            --bg-primary: #f5f5f5;
            --bg-secondary: #ffffff;
            --bg-card: #ffffff;
            --text-primary: #1a1a2e;
            --text-secondary: #6b6b7a;
            --text-muted: #9999a8;
            --border-color: #e8e8ef;
            --shadow: 0 2px 12px rgba(0,0,0,0.06);
            --story-border: linear-gradient(135deg, #f9a825, #ff6f00);
            --fab-bg: linear-gradient(135deg, #f9a825, #ff6f00);
            --tab-icon-active: #f9a825;
            --tab-icon-inactive: #9999a8;
            --post-bg: #ffffff;
            --input-bg: #f0f0f5;
            --search-bg: #f0f0f5;
            --like-color: #e74c3c;
            --comment-color: #4a90d9;
            --share-color: #2ecc71;
        }}

        .dark-mode {{
            --bg-primary: #0a0a2e;
            --bg-secondary: #12123a;
            --bg-card: #1a1a4e;
            --text-primary: #f0f0ff;
            --text-secondary: #a8a8c8;
            --text-muted: #6a6a8a;
            --border-color: #2a2a5a;
            --shadow: 0 2px 12px rgba(0,0,0,0.3);
            --post-bg: #1a1a4e;
            --input-bg: #2a2a5a;
            --search-bg: #2a2a5a;
        }}

        /* ===== Reset & Base ===== */
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            min-height: 100vh;
            padding-bottom: 80px;
            transition: background 0.3s, color 0.3s;
        }}

        /* ===== Status Bar (Mock) ===== */
        .status-bar {{
            display: flex;
            justify-content: space-between;
            padding: 8px 20px;
            font-size: 12px;
            color: var(--text-secondary);
            background: var(--bg-secondary);
            border-bottom: 1px solid var(--border-color);
        }}

        /* ===== Header ===== */
        .header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px 20px;
            background: var(--bg-secondary);
            border-bottom: 1px solid var(--border-color);
            position: sticky;
            top: 0;
            z-index: 100;
        }}

        .header h1 {{
            font-size: 22px;
            font-weight: 700;
            color: var(--text-primary);
        }}

        .header h1 i {{
            color: #f9a825;
            margin-right: 6px;
        }}

        .header-actions {{
            display: flex;
            gap: 16px;
            align-items: center;
        }}

        .header-actions button {{
            background: none;
            border: none;
            color: var(--text-secondary);
            font-size: 20px;
            cursor: pointer;
            transition: color 0.3s;
        }}

        .header-actions button:hover {{
            color: var(--text-primary);
        }}

        /* ===== Theme Toggle ===== */
        .theme-toggle-btn {{
            background: none;
            border: none;
            color: var(--text-secondary);
            font-size: 18px;
            cursor: pointer;
            padding: 4px 8px;
            border-radius: 8px;
            transition: all 0.3s;
        }}

        .theme-toggle-btn:hover {{
            background: var(--input-bg);
            color: var(--text-primary);
        }}

        /* ===== Search Bar ===== */
        .search-container {{
            padding: 12px 20px;
            background: var(--bg-secondary);
            border-bottom: 1px solid var(--border-color);
        }}

        .search-bar {{
            display: flex;
            align-items: center;
            background: var(--search-bg);
            border-radius: 12px;
            padding: 10px 16px;
            gap: 10px;
            transition: all 0.3s;
        }}

        .search-bar:focus-within {{
            box-shadow: 0 0 0 2px rgba(249, 168, 37, 0.2);
        }}

        .search-bar i {{
            color: var(--text-muted);
            font-size: 16px;
        }}

        .search-bar input {{
            background: none;
            border: none;
            outline: none;
            color: var(--text-primary);
            font-size: 14px;
            width: 100%;
        }}

        .search-bar input::placeholder {{
            color: var(--text-muted);
        }}

        /* ===== Stories ===== */
        .stories-container {{
            padding: 16px 20px;
            background: var(--bg-secondary);
            border-bottom: 1px solid var(--border-color);
            overflow-x: auto;
            white-space: nowrap;
            display: flex;
            gap: 16px;
            scrollbar-width: none;
        }}

        .stories-container::-webkit-scrollbar {{
            display: none;
        }}

        .story-item {{
            display: inline-flex;
            flex-direction: column;
            align-items: center;
            gap: 4px;
            cursor: pointer;
            min-width: 72px;
        }}

        .story-ring {{
            width: 68px;
            height: 68px;
            border-radius: 50%;
            padding: 3px;
            background: #2d2d2d;
            transition: transform 0.2s;
        }}

        .story-ring:hover {{
            transform: scale(1.05);
        }}

        .story-ring.has-story {{
            background: linear-gradient(135deg, #f9a825, #ff6f00);
        }}

        .story-ring .story-avatar {{
            width: 100%;
            height: 100%;
            border-radius: 50%;
            overflow: hidden;
            border: 2px solid var(--bg-secondary);
            background: var(--bg-primary);
        }}

        .story-ring .story-avatar img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
        }}

        .story-ring .story-avatar .default-avatar {{
            display: flex;
            align-items: center;
            justify-content: center;
            width: 100%;
            height: 100%;
            font-size: 28px;
            color: var(--text-muted);
            background: var(--input-bg);
        }}

        .story-item .story-username {{
            font-size: 11px;
            color: var(--text-secondary);
            max-width: 68px;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }}

        .story-item.add-story .story-ring {{
            background: linear-gradient(135deg, #1a237e, #f9a825);
        }}

        .story-item.add-story .add-icon {{
            position: relative;
        }}

        .story-item.add-story .add-icon::after {{
            content: '+';
            position: absolute;
            bottom: -2px;
            right: -2px;
            background: #f9a825;
            color: white;
            width: 20px;
            height: 20px;
            border-radius: 50%;
            font-size: 14px;
            display: flex;
            align-items: center;
            justify-content: center;
            border: 2px solid var(--bg-secondary);
            font-weight: 700;
        }}

        /* ===== Posts ===== */
        .posts-container {{
            padding: 16px 20px;
            display: flex;
            flex-direction: column;
            gap: 16px;
        }}

        .post {{
            background: var(--post-bg);
            border-radius: 16px;
            padding: 16px;
            box-shadow: var(--shadow);
            border: 1px solid var(--border-color);
            transition: all 0.3s;
        }}

        .post:hover {{
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        }}

        .post-header {{
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 12px;
        }}

        .post-avatar {{
            width: 40px;
            height: 40px;
            border-radius: 50%;
            overflow: hidden;
            background: var(--input-bg);
        }}

        .post-avatar img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
        }}

        .post-avatar .default-avatar {{
            display: flex;
            align-items: center;
            justify-content: center;
            width: 100%;
            height: 100%;
            font-size: 18px;
            color: var(--text-muted);
        }}

        .post-user-info {{
            flex: 1;
        }}

        .post-user-info .post-username {{
            font-weight: 600;
            font-size: 14px;
            color: var(--text-primary);
        }}

        .post-user-info .post-time {{
            font-size: 12px;
            color: var(--text-muted);
        }}

        .post-more {{
            color: var(--text-muted);
            cursor: pointer;
            padding: 4px 8px;
            border-radius: 8px;
            transition: background 0.3s;
        }}

        .post-more:hover {{
            background: var(--input-bg);
        }}

        .post-content {{
            margin-bottom: 12px;
        }}

        .post-content p {{
            font-size: 14px;
            line-height: 1.6;
            color: var(--text-primary);
        }}

        .post-content .see-more {{
            color: #f9a825;
            cursor: pointer;
            font-weight: 500;
        }}

        .post-actions {{
            display: flex;
            gap: 20px;
            padding-top: 12px;
            border-top: 1px solid var(--border-color);
        }}

        .post-action {{
            display: flex;
            align-items: center;
            gap: 6px;
            color: var(--text-secondary);
            cursor: pointer;
            transition: all 0.2s;
            font-size: 14px;
        }}

        .post-action:hover {{
            color: var(--text-primary);
        }}

        .post-action i {{
            font-size: 16px;
        }}

        .post-action.liked {{
            color: #e74c3c;
        }}

        .post-action.liked i {{
            font-weight: 900;
        }}

        .post-action .count {{
            font-size: 13px;
        }}

        /* ===== Floating Action Button ===== */
        .fab {{
            position: fixed;
            bottom: 100px;
            right: 24px;
            width: 56px;
            height: 56px;
            border-radius: 50%;
            background: var(--fab-bg);
            color: white;
            border: none;
            font-size: 24px;
            cursor: pointer;
            box-shadow: 0 4px 20px rgba(249, 168, 37, 0.3);
            transition: all 0.3s;
            z-index: 1000;
        }}

        .fab:hover {{
            transform: scale(1.1) rotate(90deg);
            box-shadow: 0 6px 30px rgba(249, 168, 37, 0.4);
        }}

        /* ===== Bottom Tab Bar ===== */
        .tab-bar {{
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background: var(--bg-secondary);
            border-top: 1px solid var(--border-color);
            display: flex;
            justify-content: space-around;
            padding: 8px 0;
            padding-bottom: env(safe-area-inset-bottom);
            z-index: 1000;
        }}

        .tab-item {{
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 2px;
            color: var(--tab-icon-inactive);
            cursor: pointer;
            padding: 4px 16px;
            transition: all 0.3s;
            text-decoration: none;
            position: relative;
        }}

        .tab-item i {{
            font-size: 22px;
            transition: all 0.3s;
        }}

        .tab-item span {{
            font-size: 10px;
            font-weight: 500;
        }}

        .tab-item.active {{
            color: var(--tab-icon-active);
        }}

        .tab-item.active i {{
            transform: translateY(-2px);
        }}

        .tab-item:hover {{
            color: var(--tab-icon-active);
        }}

        .tab-item .badge {{
            position: absolute;
            top: 0;
            right: 4px;
            background: #e74c3c;
            color: white;
            font-size: 10px;
            padding: 2px 6px;
            border-radius: 12px;
            min-width: 18px;
            text-align: center;
        }}

        /* ===== Responsive ===== */
        @media (max-width: 600px) {{
            .header {{
                padding: 10px 16px;
            }}
            
            .header h1 {{
                font-size: 18px;
            }}
            
            .search-container {{
                padding: 8px 16px;
            }}
            
            .stories-container {{
                padding: 12px 16px;
                gap: 12px;
            }}
            
            .story-ring {{
                width: 60px;
                height: 60px;
            }}
            
            .story-item {{
                min-width: 60px;
            }}
            
            .posts-container {{
                padding: 12px 16px;
                gap: 12px;
            }}
            
            .post {{
                padding: 14px;
            }}
            
            .tab-item {{
                padding: 4px 12px;
            }}
            
            .tab-item i {{
                font-size: 18px;
            }}
            
            .fab {{
                width: 48px;
                height: 48px;
                font-size: 20px;
                bottom: 80px;
                right: 16px;
            }}
        }}
    </style>
</head>
<body>
    <!-- ===== Status Bar ===== -->
    <div class="status-bar">
        <span>9:41</span>
        <span><i class="fas fa-signal"></i> <i class="fas fa-wifi"></i> <i class="fas fa-battery-full"></i></span>
    </div>

    <!-- ===== Header ===== -->
    <header class="header">
        <h1><i class="fas fa-graduation-cap"></i>Camly</h1>
        <div class="header-actions">
            <button onclick="toggleTheme()" class="theme-toggle-btn" id="themeToggle">
                <i class="fas fa-moon" id="themeIcon"></i>
            </button>
            <button onclick="location.href='/notify/'">
                <i class="fas fa-bell"></i>
                <span class="badge" style="position:absolute;top:8px;right:64px;background:#e74c3c;color:#fff;font-size:10px;padding:1px 6px;border-radius:12px;min-width:18px;text-align:center;">3</span>
            </button>
        </div>
    </header>

    <!-- ===== Search ===== -->
    <div class="search-container">
        <div class="search-bar">
            <i class="fas fa-search"></i>
            <input type="text" placeholder="Search for people, posts, groups..." id="searchInput">
        </div>
    </div>

    <!-- ===== Stories ===== -->
    <div class="stories-container" id="storiesContainer">
        <!-- Your Story -->
        <div class="story-item add-story" onclick="openStoryUpload()">
            <div class="story-ring">
                <div class="story-avatar add-icon">
                    <div class="default-avatar">
                        <i class="fas fa-plus"></i>
                    </div>
                </div>
            </div>
            <span class="story-username">Your Story</span>
        </div>
        
        <!-- Story 1 -->
        <div class="story-item" onclick="viewStory(1)">
            <div class="story-ring has-story">
                <div class="story-avatar">
                    <div class="default-avatar">👤</div>
                </div>
            </div>
            <span class="story-username">James_doe</span>
        </div>
        
        <!-- Story 2 -->
        <div class="story-item" onclick="viewStory(2)">
            <div class="story-ring has-story">
                <div class="story-avatar">
                    <div class="default-avatar">👤</div>
                </div>
            </div>
            <span class="story-username">Phillips joe</span>
        </div>
        
        <!-- Story 3 -->
        <div class="story-item" onclick="viewStory(3)">
            <div class="story-ring has-story">
                <div class="story-avatar">
                    <div class="default-avatar">👤</div>
                </div>
            </div>
            <span class="story-username">Jane Clark</span>
        </div>
        
        <!-- Story 4 -->
        <div class="story-item" onclick="viewStory(4)">
            <div class="story-ring has-story">
                <div class="story-avatar">
                    <div class="default-avatar">👤</div>
                </div>
            </div>
            <span class="story-username">Matthew</span>
        </div>
    </div>

    <!-- ===== Posts ===== -->
    <div class="posts-container">
        <!-- Post 1 -->
        <div class="post">
            <div class="post-header">
                <div class="post-avatar">
                    <div class="default-avatar">👤</div>
                </div>
                <div class="post-user-info">
                    <div class="post-username">James Clinton</div>
                    <div class="post-time">2h ago</div>
                </div>
                <div class="post-more">
                    <i class="fas fa-ellipsis-h"></i>
                </div>
            </div>
            <div class="post-content">
                <p>Designing with intention beats chasing trends. This is what I've learned so far... <span class="see-more">see more</span></p>
            </div>
            <div class="post-actions">
                <div class="post-action" onclick="toggleLike(this)">
                    <i class="far fa-heart"></i>
                    <span class="count">105</span>
                </div>
                <div class="post-action" onclick="toggleComment(this)">
                    <i class="far fa-comment"></i>
                    <span class="count">15</span>
                </div>
                <div class="post-action" onclick="sharePost(this)">
                    <i class="far fa-share-alt"></i>
                    <span class="count">50</span>
                </div>
            </div>
        </div>

        <!-- Post 2 -->
        <div class="post">
            <div class="post-header">
                <div class="post-avatar">
                    <div class="default-avatar">👤</div>
                </div>
                <div class="post-user-info">
                    <div class="post-username">Priya Dehnia</div>
                    <div class="post-time">2h ago</div>
                </div>
                <div class="post-more">
                    <i class="fas fa-ellipsis-h"></i>
                </div>
            </div>
            <div class="post-content">
                <p>Designing with intention beats chasing trends. This is what I've learned so far... <span class="see-more">see more</span></p>
            </div>
            <div class="post-actions">
                <div class="post-action" onclick="toggleLike(this)">
                    <i class="far fa-heart"></i>
                    <span class="count">105</span>
                </div>
                <div class="post-action" onclick="toggleComment(this)">
                    <i class="far fa-comment"></i>
                    <span class="count">15</span>
                </div>
                <div class="post-action" onclick="sharePost(this)">
                    <i class="far fa-share-alt"></i>
                    <span class="count">50</span>
                </div>
            </div>
        </div>

        <!-- Post 3 -->
        <div class="post">
            <div class="post-header">
                <div class="post-avatar">
                    <div class="default-avatar">👤</div>
                </div>
                <div class="post-user-info">
                    <div class="post-username">Phillips James</div>
                    <div class="post-time">2h ago</div>
                </div>
                <div class="post-more">
                    <i class="fas fa-ellipsis-h"></i>
                </div>
            </div>
            <div class="post-content">
                <p>Designing with intention beats chasing trends. This is what I've learned so far... <span class="see-more">see more</span></p>
            </div>
            <div class="post-actions">
                <div class="post-action" onclick="toggleLike(this)">
                    <i class="far fa-heart"></i>
                    <span class="count">105</span>
                </div>
                <div class="post-action" onclick="toggleComment(this)">
                    <i class="far fa-comment"></i>
                    <span class="count">15</span>
                </div>
                <div class="post-action" onclick="sharePost(this)">
                    <i class="far fa-share-alt"></i>
                    <span class="count">50</span>
                </div>
            </div>
        </div>
    </div>

    <!-- ===== Floating Action Button ===== -->
    <button class="fab" onclick="createPost()">
        <i class="fas fa-plus"></i>
    </button>

    <!-- ===== Bottom Tab Bar ===== -->
    <nav class="tab-bar">
        <a href="/" class="tab-item active">
            <i class="fas fa-home"></i>
            <span>Home</span>
        </a>
        <a href="/inbox/" class="tab-item">
            <i class="fas fa-inbox"></i>
            <span>Inbox</span>
            <span class="badge">5</span>
        </a>
        <a href="/notifications/" class="tab-item">
            <i class="fas fa-bell"></i>
            <span>Notifications</span>
            <span class="badge">3</span>
        </a>
        <a href="/profile/" class="tab-item">
            <i class="fas fa-user"></i>
            <span>Profile</span>
        </a>
    </nav>

    <!-- ===== JavaScript ===== -->
    <script>
        // ===== Theme Toggle =====
        function toggleTheme() {{
            const body = document.body;
            const icon = document.getElementById('themeIcon');
            body.classList.toggle('dark-mode');
            if (body.classList.contains('dark-mode')) {{
                icon.className = 'fas fa-sun';
                localStorage.setItem('theme', 'dark');
            }} else {{
                icon.className = 'fas fa-moon';
                localStorage.setItem('theme', 'light');
            }}
        }}

        // Load saved theme
        document.addEventListener('DOMContentLoaded', function() {{
            const savedTheme = localStorage.getItem('theme');
            const icon = document.getElementById('themeIcon');
            if (savedTheme === 'dark') {{
                document.body.classList.add('dark-mode');
                icon.className = 'fas fa-sun';
            }}
        }});

        // ===== Story Functions =====
        function viewStory(id) {{
            window.location.href = `/stories/${{id}}/`;
        }}

        function openStoryUpload() {{
            // Create file input
            const input = document.createElement('input');
            input.type = 'file';
            input.accept = 'image/*';
            input.onchange = function(e) {{
                if (this.files && this.files[0]) {{
                    const formData = new FormData();
                    formData.append('image', this.files[0]);
                    fetch('/stories/create/', {{
                        method: 'POST',
                        body: formData,
                        headers: {{
                            'X-CSRFToken': '{{ csrf_token }}',
                        }},
                    }})
                    .then(response => response.json())
                    .then(data => {{
                        if (data.success) {{
                            location.reload();
                        }}
                    }});
                }}
            }};
            input.click();
        }}

        // ===== Post Functions =====
        function toggleLike(element) {{
            const icon = element.querySelector('i');
            const count = element.querySelector('.count');
            let num = parseInt(count.textContent);
            if (icon.classList.contains('far')) {{
                icon.classList.remove('far');
                icon.classList.add('fas');
                element.classList.add('liked');
                num++;
            }} else {{
                icon.classList.remove('fas');
                icon.classList.add('far');
                element.classList.remove('liked');
                num--;
            }}
            count.textContent = num;
        }}

        function toggleComment(element) {{
            // Scroll to comment section or open modal
            alert('Comment section coming soon!');
        }}

        function sharePost(element) {{
            if (navigator.share) {{
                navigator.share({{
                    title: 'Camly Post',
                    text: 'Check out this post on Camly!',
                    url: window.location.href,
                }});
            }} else {{
                alert('Share functionality coming soon!');
            }}
        }}

        function createPost() {{
            window.location.href = '/posts/create/';
        }}

        // ===== Search Function =====
        document.getElementById('searchInput').addEventListener('input', function(e) {{
            const query = e.target.value.toLowerCase();
            const posts = document.querySelectorAll('.post');
            posts.forEach(post => {{
                const text = post.textContent.toLowerCase();
                post.style.display = text.includes(query) ? 'block' : 'none';
            }});
        }});

        // ===== Smooth Story Scrolling =====
        const storiesContainer = document.getElementById('storiesContainer');
        let isDown = false;
        let startX;
        let scrollLeft;

        storiesContainer.addEventListener('mousedown', (e) => {{
            isDown = true;
            startX = e.pageX - storiesContainer.offsetLeft;
            scrollLeft = storiesContainer.scrollLeft;
        }});

        storiesContainer.addEventListener('mouseleave', () => {{
            isDown = false;
        }});

        storiesContainer.addEventListener('mouseup', () => {{
            isDown = false;
        }});

        storiesContainer.addEventListener('mousemove', (e) => {{
            if (!isDown) return;
            e.preventDefault();
            const x = e.pageX - storiesContainer.offsetLeft;
            const walk = (x - startX) * 2;
            storiesContainer.scrollLeft = scrollLeft - walk;
        }});
    </script>
</body>
</html>
"""
    return HttpResponse(html)
