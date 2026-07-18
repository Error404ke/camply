from django.shortcuts import render
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
            --bg-primary: rgba(255, 255, 255, 0.12);
            --bg-secondary: rgba(255, 255, 255, 0.08);
            --bg-card: rgba(255, 255, 255, 0.1);
            --text-primary: #1a1a2e;
            --text-secondary: #2d2d44;
            --text-muted: #555577;
            --border-color: rgba(255, 255, 255, 0.15);
            --shadow: 0 8px 32px rgba(0,0,0,0.15);
            --input-bg: rgba(255, 255, 255, 0.1);
            --hover-bg: rgba(255, 255, 255, 0.08);
            --online-color: #2ecc71;
            --accent-color: #f9a825;
            --tab-icon-active: #00bcd4;
            --tab-icon-inactive: rgba(255, 255, 255, 0.5);
            --story-border: linear-gradient(135deg, #f9a825, #ff6f00);
            --like-color: #e74c3c;
            --glass-blur: 20px;
            --glass-border: rgba(255, 255, 255, 0.15);
            --glass-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
            --glass-glow: rgba(255, 255, 255, 0.05);
            --status-bar-bg: rgba(255, 255, 255, 0.08);
            --overlay-color: rgba(0, 0, 0, 0.3);
            --nav-color: rgba(0, 188, 212, 0.15);
            --nav-border: rgba(0, 188, 212, 0.2);
            --nav-glow: rgba(0, 188, 212, 0.3);
            --post-glass-bg: rgba(255, 255, 255, 0.15);
            --post-glass-border: rgba(255, 255, 255, 0.2);
            --post-glass-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
        }}

        .dark-mode {{
            --bg-primary: rgba(10, 10, 46, 0.25);
            --bg-secondary: rgba(10, 10, 46, 0.2);
            --bg-card: rgba(10, 10, 46, 0.25);
            --text-primary: #f0f0ff;
            --text-secondary: #c8c8e8;
            --text-muted: #8888aa;
            --border-color: rgba(255, 255, 255, 0.08);
            --shadow: 0 8px 32px rgba(0,0,0,0.3);
            --input-bg: rgba(255, 255, 255, 0.05);
            --hover-bg: rgba(255, 255, 255, 0.05);
            --tab-icon-inactive: rgba(255, 255, 255, 0.3);
            --glass-border: rgba(255, 255, 255, 0.05);
            --status-bar-bg: rgba(10, 10, 46, 0.2);
            --overlay-color: rgba(0, 0, 0, 0.5);
            --nav-color: rgba(0, 188, 212, 0.1);
            --nav-border: rgba(0, 188, 212, 0.15);
            --nav-glow: rgba(0, 188, 212, 0.2);
            --post-glass-bg: rgba(255, 255, 255, 0.05);
            --post-glass-border: rgba(255, 255, 255, 0.08);
            --post-glass-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
            --glass-glow: rgba(255, 255, 255, 0.02);
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            min-height: 100vh;
            padding-bottom: 70px;
            transition: background 0.5s ease, color 0.3s ease;
            background: var(--bg-primary);
            color: var(--text-primary);
            position: relative;
            overflow-x: hidden;
        }}

        /* ===== City Background ===== */
        .city-background {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
            background-image: url('https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?w=1920');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            transition: all 0.8s ease;
        }}

        .city-background::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(180deg, 
                rgba(0, 0, 0, 0.15) 0%,
                rgba(0, 0, 0, 0.05) 30%,
                rgba(0, 0, 0, 0.1) 60%,
                rgba(0, 0, 0, 0.3) 100%
            );
        }}

        .dark-mode .city-background {{
            background-image: url('https://images.unsplash.com/photo-1519501025264-65ba15a82390?w=1920');
        }}

        .dark-mode .city-background::before {{
            background: linear-gradient(180deg, 
                rgba(0, 0, 0, 0.4) 0%,
                rgba(0, 0, 0, 0.3) 30%,
                rgba(0, 0, 0, 0.4) 60%,
                rgba(0, 0, 0, 0.7) 100%
            );
        }}

        /* ===== City Lights Animation ===== */
        .city-lights {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
            pointer-events: none;
            overflow: hidden;
        }}

        .light {{
            position: absolute;
            width: 4px;
            height: 4px;
            background: rgba(255, 215, 0, 0.3);
            border-radius: 50%;
            animation: twinkleLight 2s ease-in-out infinite;
        }}

        .light:nth-child(1) {{ top: 20%; left: 10%; animation-delay: 0s; width: 6px; height: 6px; }}
        .light:nth-child(2) {{ top: 15%; left: 25%; animation-delay: 0.5s; }}
        .light:nth-child(3) {{ top: 25%; left: 40%; animation-delay: 1s; width: 8px; height: 8px; background: rgba(255, 255, 255, 0.4); }}
        .light:nth-child(4) {{ top: 10%; left: 55%; animation-delay: 1.5s; }}
        .light:nth-child(5) {{ top: 30%; left: 70%; animation-delay: 0.3s; width: 5px; height: 5px; }}
        .light:nth-child(6) {{ top: 18%; left: 85%; animation-delay: 0.8s; }}
        .light:nth-child(7) {{ top: 35%; left: 15%; animation-delay: 1.2s; width: 7px; height: 7px; background: rgba(255, 200, 100, 0.5); }}
        .light:nth-child(8) {{ top: 22%; left: 50%; animation-delay: 0.2s; }}
        .light:nth-child(9) {{ top: 28%; left: 75%; animation-delay: 1.8s; width: 4px; height: 4px; }}
        .light:nth-child(10) {{ top: 12%; left: 95%; animation-delay: 0.7s; }}

        .dark-mode .light {{
            background: rgba(255, 215, 0, 0.6);
        }}

        .dark-mode .light:nth-child(1) {{ background: rgba(255, 215, 0, 0.8); }}
        .dark-mode .light:nth-child(3) {{ background: rgba(255, 255, 255, 0.7); }}
        .dark-mode .light:nth-child(7) {{ background: rgba(255, 200, 100, 0.8); }}

        @keyframes twinkleLight {{
            0%, 100% {{ opacity: 0.2; transform: scale(0.5); }}
            50% {{ opacity: 1; transform: scale(1.5); }}
        }}

        /* ===== Liquid Glass Effect ===== */
        .glass {{
            background: var(--bg-card);
            backdrop-filter: blur(var(--glass-blur));
            -webkit-backdrop-filter: blur(var(--glass-blur));
            border: 1px solid var(--glass-border);
            box-shadow: var(--glass-shadow);
        }}

        /* ===== Enhanced Post Glass ===== */
        .glass-post {{
            background: var(--post-glass-bg);
            backdrop-filter: blur(24px) saturate(1.2);
            -webkit-backdrop-filter: blur(24px) saturate(1.2);
            border: 1px solid var(--post-glass-border);
            box-shadow: var(--post-glass-shadow), inset 0 1px 0 var(--glass-glow);
            border-radius: 16px;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        }}

        .glass-post:hover {{
            background: var(--post-glass-bg);
            backdrop-filter: blur(28px) saturate(1.4);
            -webkit-backdrop-filter: blur(28px) saturate(1.4);
            box-shadow: var(--post-glass-shadow), 0 12px 48px rgba(0, 0, 0, 0.15), inset 0 1px 0 var(--glass-glow);
            transform: translateY(-4px);
        }}

        /* ===== Cyan Glass Navigation ===== */
        .glass-nav {{
            background: var(--nav-color);
            backdrop-filter: blur(var(--glass-blur));
            -webkit-backdrop-filter: blur(var(--glass-blur));
            border-bottom: 1px solid var(--nav-border);
            box-shadow: 0 4px 30px var(--nav-glow), 0 2px 10px rgba(0, 188, 212, 0.1);
            transition: all 0.5s ease;
        }}

        .glass-nav:hover {{
            box-shadow: 0 4px 40px var(--nav-glow), 0 2px 20px rgba(0, 188, 212, 0.15);
        }}

        .glass-nav .brand {{
            color: var(--text-primary);
            text-shadow: 0 0 20px rgba(0, 188, 212, 0.1);
        }}

        .glass-nav .brand i {{
            color: #00bcd4;
            text-shadow: 0 0 20px rgba(0, 188, 212, 0.3);
        }}

        .glass-nav .header-actions button {{
            background: rgba(0, 188, 212, 0.05);
            border: 1px solid rgba(0, 188, 212, 0.1);
        }}

        .glass-nav .header-actions button:hover {{
            background: rgba(0, 188, 212, 0.1);
            border-color: rgba(0, 188, 212, 0.2);
            box-shadow: 0 0 20px rgba(0, 188, 212, 0.1);
        }}

        .glass-nav .profile-trigger {{
            border-color: rgba(0, 188, 212, 0.15);
            background: rgba(0, 188, 212, 0.05);
        }}

        .glass-nav .profile-trigger:hover {{
            border-color: rgba(0, 188, 212, 0.4);
            box-shadow: 0 0 30px rgba(0, 188, 212, 0.15);
        }}

        .glass-nav .profile-trigger .avatar {{
            background: linear-gradient(135deg, #00bcd4, #0097a7);
        }}

        .glass-nav .theme-toggle {{
            border-color: rgba(0, 188, 212, 0.15);
            background: rgba(0, 188, 212, 0.05);
        }}

        .glass-nav .theme-toggle .toggle-option.active {{
            background: #00bcd4;
            color: white;
            box-shadow: 0 2px 10px rgba(0, 188, 212, 0.4);
        }}

        /* ===== Status Bar ===== */
        .status-bar {{
            display: flex;
            justify-content: space-between;
            padding: 6px 20px;
            font-size: 12px;
            color: var(--text-secondary);
            background: var(--status-bar-bg);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border-bottom: 1px solid var(--border-color);
        }}

        /* ===== Header ===== */
        .header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 20px;
            position: sticky;
            top: 0;
            z-index: 100;
        }}

        .header .brand {{
            font-size: 20px;
            font-weight: 700;
            color: var(--text-primary);
            text-decoration: none;
        }}

        .header .brand i {{
            color: #00bcd4;
            margin-right: 6px;
        }}

        .header-actions {{
            display: flex;
            align-items: center;
            gap: 12px;
        }}

        .header-actions button {{
            font-size: 16px;
            cursor: pointer;
            padding: 6px 10px;
            border-radius: 30px;
            transition: all 0.3s;
            position: relative;
        }}

        .header-actions .badge {{
            position: absolute;
            top: -4px;
            right: -4px;
            background: #00bcd4;
            color: white;
            font-size: 9px;
            padding: 1px 5px;
            border-radius: 50%;
            min-width: 16px;
            text-align: center;
        }}

        /* ===== Theme Toggle ===== */
        .theme-toggle {{
            border-radius: 30px;
            padding: 4px;
            display: flex;
            gap: 4px;
            cursor: pointer;
            transition: all 0.3s;
        }}

        .theme-toggle .toggle-option {{
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 12px;
            color: var(--text-muted);
            transition: all 0.3s;
            background: none;
            border: none;
            cursor: pointer;
        }}

        .theme-toggle .toggle-option.active {{
            color: white;
        }}

        /* ===== Profile Trigger ===== */
        .profile-trigger {{
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 2px 8px 2px 2px;
            border-radius: 30px;
            transition: all 0.3s;
            cursor: pointer;
        }}

        .profile-trigger .avatar {{
            width: 32px;
            height: 32px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: 600;
            font-size: 14px;
        }}

        .profile-trigger .username {{
            font-size: 13px;
            font-weight: 500;
            color: var(--text-primary);
        }}

        .profile-trigger i {{
            color: var(--text-muted);
            font-size: 11px;
        }}

        /* ===== Dropdown Menu ===== */
        .dropdown-menu {{
            display: none;
            position: absolute;
            top: calc(100% + 8px);
            right: 0;
            min-width: 220px;
            background: var(--bg-secondary);
            backdrop-filter: blur(var(--glass-blur));
            border: 1px solid var(--glass-border);
            border-radius: 16px;
            box-shadow: var(--glass-shadow);
            padding: 8px 0;
            z-index: 200;
            animation: dropdownIn 0.2s ease-out;
        }}

        .dropdown-menu.show {{
            display: block;
        }}

        @keyframes dropdownIn {{
            from {{ opacity: 0; transform: translateY(-10px) scale(0.95); }}
            to {{ opacity: 1; transform: translateY(0) scale(1); }}
        }}

        .dropdown-header {{
            padding: 8px 16px 12px;
            border-bottom: 1px solid var(--border-color);
        }}

        .dropdown-header .user-name {{
            font-weight: 600;
            font-size: 14px;
            color: var(--text-primary);
        }}

        .dropdown-header .user-email {{
            font-size: 12px;
            color: var(--text-muted);
        }}

        .dropdown-item {{
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 10px 16px;
            color: var(--text-primary);
            text-decoration: none;
            transition: all 0.2s;
            cursor: pointer;
            border: none;
            background: none;
            width: 100%;
            text-align: left;
            font-size: 14px;
        }}

        .dropdown-item:hover {{
            background: var(--hover-bg);
            backdrop-filter: blur(10px);
            transform: translateX(4px);
        }}

        .dropdown-item i {{
            width: 20px;
            color: var(--text-muted);
            font-size: 16px;
        }}

        .dropdown-item.danger {{
            color: #e74c3c;
        }}

        .dropdown-item.danger i {{
            color: #e74c3c;
        }}

        .dropdown-divider {{
            height: 1px;
            background: var(--border-color);
            margin: 4px 0;
        }}

        .profile-container {{
            position: relative;
        }}

        /* ===== Stories ===== */
        .stories-container {{
            padding: 12px 16px;
            background: var(--bg-secondary);
            backdrop-filter: blur(var(--glass-blur));
            -webkit-backdrop-filter: blur(var(--glass-blur));
            border-bottom: 1px solid var(--glass-border);
            overflow-x: auto;
            white-space: nowrap;
            display: flex;
            gap: 14px;
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
            min-width: 68px;
        }}

        .story-ring {{
            width: 64px;
            height: 64px;
            border-radius: 50%;
            padding: 3px;
            background: rgba(255, 255, 255, 0.1);
            transition: transform 0.2s;
            backdrop-filter: blur(5px);
        }}

        .story-ring.has-story {{
            background: linear-gradient(135deg, #f9a825, #ff6f00);
            box-shadow: 0 0 20px rgba(249, 168, 37, 0.2);
        }}

        .story-ring:hover {{
            transform: scale(1.05);
        }}

        .story-thumbnail {{
            width: 100%;
            height: 100%;
            border-radius: 50%;
            overflow: hidden;
            border: 2px solid var(--bg-secondary);
            background: var(--bg-primary);
        }}

        .story-thumbnail img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
        }}

        .story-thumbnail .default-avatar {{
            display: flex;
            align-items: center;
            justify-content: center;
            width: 100%;
            height: 100%;
            font-size: 24px;
            color: var(--text-muted);
            background: var(--input-bg);
        }}

        .story-username {{
            font-size: 10px;
            color: var(--text-secondary);
            max-width: 64px;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
            text-align: center;
        }}

        .add-story .story-ring {{
            background: linear-gradient(135deg, #1a237e, #f9a825);
            box-shadow: 0 0 20px rgba(249, 168, 37, 0.15);
        }}

        .add-story .add-icon {{
            position: relative;
        }}

        .add-story .add-icon::after {{
            content: '+';
            position: absolute;
            bottom: -2px;
            right: -2px;
            background: var(--accent-color);
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
            box-shadow: 0 2px 10px rgba(249, 168, 37, 0.3);
        }}

        /* ===== Feed Container ===== */
        .feed-container {{
            max-width: 600px;
            margin: 0 auto;
            padding: 12px 16px;
        }}

        /* ===== Enhanced Posts ===== */
        .post-card {{
            padding: 16px;
            margin-bottom: 16px;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }}

        /* Glass shine effect */
        .post-card::before {{
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle at 30% 30%, rgba(255, 255, 255, 0.03), transparent 60%);
            pointer-events: none;
            z-index: 1;
        }}

        .post-card::after {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(135deg, 
                rgba(255, 255, 255, 0.02) 0%,
                transparent 50%,
                rgba(255, 255, 255, 0.02) 100%
            );
            pointer-events: none;
            z-index: 1;
        }}

        .post-card .post-content,
        .post-card .post-header,
        .post-card .post-actions {{
            position: relative;
            z-index: 2;
        }}

        .post-card:hover {{
            transform: translateY(-4px) scale(1.01);
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
            position: relative;
            z-index: 2;
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
            position: relative;
            z-index: 2;
        }}

        .post-username {{
            font-weight: 600;
            font-size: 14px;
            color: var(--text-primary);
        }}

        .post-time {{
            font-size: 11px;
            color: var(--text-muted);
        }}

        .post-more {{
            color: var(--text-muted);
            cursor: pointer;
            padding: 4px 8px;
            border-radius: 8px;
            transition: background 0.3s;
            position: relative;
            z-index: 2;
        }}

        .post-more:hover {{
            background: var(--input-bg);
        }}

        .post-content {{
            margin-bottom: 12px;
            position: relative;
            z-index: 2;
        }}

        .post-content p {{
            font-size: 14px;
            line-height: 1.6;
            color: var(--text-primary);
        }}

        .post-content .see-more {{
            color: var(--accent-color);
            cursor: pointer;
            font-weight: 500;
        }}

        .post-image {{
            width: 100%;
            border-radius: 12px;
            margin: 8px 0;
            max-height: 400px;
            object-fit: cover;
            position: relative;
            z-index: 2;
        }}

        .post-actions {{
            display: flex;
            gap: 20px;
            padding-top: 12px;
            border-top: 1px solid var(--border-color);
            position: relative;
            z-index: 2;
        }}

        .post-action {{
            display: flex;
            align-items: center;
            gap: 6px;
            color: var(--text-secondary);
            cursor: pointer;
            transition: all 0.2s;
            font-size: 14px;
            background: none;
            border: none;
            padding: 4px 8px;
            border-radius: 8px;
        }}

        .post-action:hover {{
            background: var(--input-bg);
            color: var(--text-primary);
            transform: translateY(-2px);
        }}

        .post-action i {{
            font-size: 16px;
        }}

        .post-action.liked {{
            color: var(--like-color);
        }}

        .post-action .count {{
            font-size: 13px;
        }}

        /* ===== Reels Section ===== */
        .reels-section {{
            margin: 20px 0;
        }}

        .section-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
        }}

        .section-header h3 {{
            font-size: 16px;
            color: var(--text-primary);
        }}

        .section-header a {{
            color: var(--accent-color);
            font-size: 13px;
            text-decoration: none;
        }}

        .reels-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 8px;
        }}

        .reel-item {{
            position: relative;
            aspect-ratio: 9/16;
            border-radius: 12px;
            overflow: hidden;
            background: var(--bg-card);
            cursor: pointer;
            transition: all 0.3s;
            border: 1px solid var(--glass-border);
            backdrop-filter: blur(10px);
        }}

        .reel-item:hover {{
            transform: scale(1.03);
            box-shadow: 0 8px 30px rgba(0,0,0,0.2);
        }}

        .reel-item video {{
            width: 100%;
            height: 100%;
            object-fit: cover;
            pointer-events: none;
        }}

        .reel-item .reel-overlay {{
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            padding: 16px;
            background: linear-gradient(to top, rgba(0,0,0,0.6), transparent);
            color: white;
        }}

        .reel-item .reel-overlay .reel-views {{
            font-size: 11px;
            opacity: 0.7;
        }}

        .reel-item .reel-play-icon {{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            color: white;
            font-size: 2.5rem;
            opacity: 0.5;
            text-shadow: 0 2px 10px rgba(0,0,0,0.5);
        }}

        .reel-item:hover .reel-play-icon {{
            opacity: 0.8;
            transform: translate(-50%, -50%) scale(1.1);
        }}

        /* ===== Tab Bar ===== */
        .tab-bar {{
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            display: flex;
            justify-content: space-around;
            align-items: center;
            padding: 6px 0;
            padding-bottom: env(safe-area-inset-bottom);
            z-index: 1000;
            flex-direction: row !important;
        }}

        .tab-item {{
            display: flex !important;
            flex-direction: column !important;
            align-items: center !important;
            justify-content: center !important;
            gap: 2px;
            color: var(--tab-icon-inactive);
            cursor: pointer;
            padding: 4px 16px;
            transition: all 0.3s;
            text-decoration: none;
            position: relative;
            background: none;
            border: none;
            font-size: 10px;
            min-width: 50px;
        }}

        .tab-item i {{
            font-size: 22px;
            transition: all 0.3s;
            display: block;
        }}

        .tab-item span {{
            font-size: 10px;
            font-weight: 500;
            display: block;
        }}

        .tab-item.active {{
            color: #00bcd4;
        }}

        .tab-item.active i {{
            transform: translateY(-2px);
            text-shadow: 0 0 20px rgba(0, 188, 212, 0.4);
        }}

        .tab-item:hover {{
            color: #00bcd4;
        }}

        .tab-item .badge {{
            position: absolute;
            top: 0;
            right: 4px;
            background: #00bcd4;
            color: white;
            font-size: 9px;
            padding: 1px 5px;
            border-radius: 50%;
            min-width: 16px;
            text-align: center;
        }}

        /* ===== Toast ===== */
        .toast {{
            position: fixed;
            bottom: 80px;
            left: 50%;
            transform: translateX(-50%);
            background: var(--bg-secondary);
            backdrop-filter: blur(var(--glass-blur));
            -webkit-backdrop-filter: blur(var(--glass-blur));
            color: var(--text-primary);
            padding: 10px 20px;
            border-radius: 16px;
            box-shadow: var(--glass-shadow);
            z-index: 1000;
            font-size: 14px;
            display: none;
            border: 1px solid var(--glass-border);
        }}

        .toast.show {{
            display: block;
            animation: toastIn 0.4s ease-out;
        }}

        @keyframes toastIn {{
            from {{ opacity: 0; transform: translateX(-50%) translateY(20px) scale(0.9); }}
            to {{ opacity: 1; transform: translateX(-50%) translateY(0) scale(1); }}
        }}

        
        @media (max-width: 600px) {{
            .header {{
                padding: 8px 16px;
            }}
            .header .brand {{
                font-size: 18px;
            }}
            .profile-trigger .username {{
                display: none;
            }}
            .feed-container {{
                padding: 8px 12px;
            }}
            .story-ring {{
                width: 56px;
                height: 56px;
            }}
            .story-item {{
                min-width: 56px;
            }}
            .story-username {{
                font-size: 9px;
                max-width: 56px;
            }}
            .reels-grid {{
                grid-template-columns: repeat(3, 1fr);
                gap: 6px;
            }}
            .tab-item {{
                padding: 4px 8px;
                min-width: 40px;
            }}
            .tab-item i {{
                font-size: 18px;
            }}
            .tab-item span {{
                font-size: 9px;
            }}
            .theme-toggle .toggle-option {{
                padding: 2px 8px;
                font-size: 10px;
            }}
            .post-card {{
                padding: 14px;
            }}
        }}

        @media (max-width: 400px) {{
            .reels-grid {{
                grid-template-columns: repeat(3, 1fr);
            }}
            .post-card {{
                padding: 12px;
            }}
            .tab-item {{
                padding: 4px 6px;
                min-width: 35px;
            }}
            .tab-item i {{
                font-size: 16px;
            }}
            .tab-item span {{
                font-size: 8px;
            }}
        }}
    </style>
</head>
<body>
    <!-- ===== City Background ===== -->
    <div class="city-background"></div>
    
    <!-- ===== City Lights ===== -->
    <div class="city-lights">
        <div class="light"></div>
        <div class="light"></div>
        <div class="light"></div>
        <div class="light"></div>
        <div class="light"></div>
        <div class="light"></div>
        <div class="light"></div>
        <div class="light"></div>
        <div class="light"></div>
        <div class="light"></div>
    </div>

    <!-- ===== Status Bar ===== -->
    <div class="status-bar">
        <span>9:41</span>
        <span><i class="fas fa-signal"></i> <i class="fas fa-wifi"></i> <i class="fas fa-battery-full"></i></span>
    </div>

    <!-- ===== Header ===== -->
    <header class="header glass-nav">
        <a href="/" class="brand">
            <i class="fas fa-graduation-cap"></i>Camly
        </a>
        <div class="header-actions">
            <!-- Theme Toggle -->
            <div class="theme-toggle" onclick="toggleTheme()">
                <button class="toggle-option active" id="lightToggle">
                    <i class="fas fa-sun"></i>
                </button>
                <button class="toggle-option" id="darkToggle">
                    <i class="fas fa-moon"></i>
                </button>
            </div>
            
            <button onclick="window.location.href='/notifications/'" title="Notifications">
                <i class="fas fa-bell"></i>
                <span class="badge">3</span>
            </button>
            
            <!-- Profile Dropdown -->
            <div class="profile-container">
                <button class="profile-trigger" onclick="toggleDropdown()">
                    <div class="avatar">{username[0].upper()}</div>
                    <span class="username">{username}</span>
                    <i class="fas fa-chevron-down"></i>
                </button>
                
                <div class="dropdown-menu" id="profileDropdown">
                    <div class="dropdown-header">
                        <div class="user-name">{username}</div>
                        <div class="user-email">{username}@camly.com</div>
                    </div>
                    <a href="/profile/view/" class="dropdown-item">
                        <i class="fas fa-user"></i> View Profile
                    </a>
                    <a href="/profile/edit/" class="dropdown-item">
                        <i class="fas fa-edit"></i> Edit Profile
                    </a>
                    <a href="/profile/settings/" class="dropdown-item">
                        <i class="fas fa-cog"></i> Settings
                    </a>
                    <div class="dropdown-divider"></div>
                    <a href="/profile/add-account/" class="dropdown-item">
                        <i class="fas fa-user-plus"></i> Add Account
                    </a>
                    <div class="dropdown-divider"></div>
                    <a href="/accounts/logout/" class="dropdown-item danger" onclick="return confirmLogout()">
                        <i class="fas fa-sign-out-alt"></i> Logout
                    </a>
                </div>
            </div>
        </div>
    </header>

    <!-- ===== Stories ===== -->
    <div class="stories-container glass">
        <!-- Your Story -->
        <div class="story-item add-story" onclick="openStoryUpload()">
            <div class="story-ring has-story">
                <div class="story-thumbnail add-icon">
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
                <div class="story-thumbnail">
                    <div class="default-avatar">👤</div>
                </div>
            </div>
            <span class="story-username">James_doe</span>
        </div>
        
        <!-- Story 2 -->
        <div class="story-item" onclick="viewStory(2)">
            <div class="story-ring has-story">
                <div class="story-thumbnail">
                    <div class="default-avatar">👤</div>
                </div>
            </div>
            <span class="story-username">Phillips joe</span>
        </div>
        
        <!-- Story 3 -->
        <div class="story-item" onclick="viewStory(3)">
            <div class="story-ring has-story">
                <div class="story-thumbnail">
                    <div class="default-avatar">👤</div>
                </div>
            </div>
            <span class="story-username">Jane Clark</span>
        </div>
        
        <!-- Story 4 -->
        <div class="story-item" onclick="viewStory(4)">
            <div class="story-ring has-story">
                <div class="story-thumbnail">
                    <div class="default-avatar">👤</div>
                </div>
            </div>
            <span class="story-username">Matthew</span>
        </div>
        
        <!-- Story 5 -->
        <div class="story-item" onclick="viewStory(5)">
            <div class="story-ring has-story">
                <div class="story-thumbnail">
                    <div class="default-avatar">👤</div>
                </div>
            </div>
            <span class="story-username">Sarah</span>
        </div>
    </div>

    <!-- ===== Feed ===== -->
    <div class="feed-container">
        <!-- Post 1 -->
        <div class="post-card glass-post">
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
                <button class="post-action" onclick="toggleLike(this)">
                    <i class="far fa-heart"></i>
                    <span class="count">105</span>
                </button>
                <button class="post-action" onclick="toggleComment(this)">
                    <i class="far fa-comment"></i>
                    <span class="count">15</span>
                </button>
                <button class="post-action" onclick="sharePost(this)">
                    <i class="far fa-share-alt"></i>
                    <span class="count">50</span>
                </button>
            </div>
        </div>

        <!-- Post 2 -->
        <div class="post-card glass-post">
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
                <button class="post-action" onclick="toggleLike(this)">
                    <i class="far fa-heart"></i>
                    <span class="count">105</span>
                </button>
                <button class="post-action" onclick="toggleComment(this)">
                    <i class="far fa-comment"></i>
                    <span class="count">15</span>
                </button>
                <button class="post-action" onclick="sharePost(this)">
                    <i class="far fa-share-alt"></i>
                    <span class="count">50</span>
                </button>
            </div>
        </div>

        <!-- ===== Reels Section ===== -->
        <div class="reels-section">
            <div class="section-header">
                <h3>Reels</h3>
                <a href="/reels/">See All</a>
            </div>
            <div class="reels-grid">
                <div class="reel-item" onclick="viewReel(1)">
                    <div class="reel-play-icon"><i class="fas fa-play"></i></div>
                    <div class="reel-overlay">
                        <div class="reel-views">12.5k views</div>
                    </div>
                </div>
                <div class="reel-item" onclick="viewReel(2)">
                    <div class="reel-play-icon"><i class="fas fa-play"></i></div>
                    <div class="reel-overlay">
                        <div class="reel-views">8.2k views</div>
                    </div>
                </div>
                <div class="reel-item" onclick="viewReel(3)">
                    <div class="reel-play-icon"><i class="fas fa-play"></i></div>
                    <div class="reel-overlay">
                        <div class="reel-views">5.7k views</div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Post 3 -->
        <div class="post-card glass-post">
            <div class="post-header">
                <div class="post-avatar">
                    <div class="default-avatar">👤</div>
                </div>
                <div class="post-user-info">
                    <div class="post-username">Phillips James</div>
                    <div class="post-time">3h ago</div>
                </div>
                <div class="post-more">
                    <i class="fas fa-ellipsis-h"></i>
                </div>
            </div>
            <div class="post-content">
                <p>Designing with intention beats chasing trends. This is what I've learned so far... <span class="see-more">see more</span></p>
            </div>
            <div class="post-actions">
                <button class="post-action" onclick="toggleLike(this)">
                    <i class="far fa-heart"></i>
                    <span class="count">105</span>
                </button>
                <button class="post-action" onclick="toggleComment(this)">
                    <i class="far fa-comment"></i>
                    <span class="count">15</span>
                </button>
                <button class="post-action" onclick="sharePost(this)">
                    <i class="far fa-share-alt"></i>
                    <span class="count">50</span>
                </button>
            </div>
        </div>
    </div>

    <!-- ===== Tab Bar ===== -->
    <nav class="tab-bar glass-nav">
        <a href="/" class="tab-item active">
            <i class="fas fa-home"></i>
            <span>Home</span>
        </a>
        <a href="/chat/" class="tab-item">
            <i class="fas fa-comment-dots"></i>
            <span>Chat</span>
            <span class="badge">5</span>
        </a>
        <a href="/events/" class="tab-item">
            <i class="fas fa-calendar"></i>
            <span>Events</span>
        </a>
        <a href="/housing/" class="tab-item">
            <i class="fas fa-home"></i>
            <span>Housing</span>
        </a>
        <a href="/resources/" class="tab-item">
            <i class="fas fa-book"></i>
            <span>Resources</span>
        </a>
    </nav>

    <!-- ===== Toast ===== -->
    <div class="toast" id="toast"></div>

    <script>
        // ===== Theme Toggle =====
        function toggleTheme() {{
            const body = document.body;
            const isDark = body.classList.contains('dark-mode');
            
            body.classList.toggle('dark-mode');
            
            // Update toggle buttons
            document.getElementById('lightToggle').classList.toggle('active', !isDark);
            document.getElementById('darkToggle').classList.toggle('active', isDark);
            
            // Save preference
            localStorage.setItem('theme', isDark ? 'light' : 'dark');
        }}

        // ===== Dropdown Functions =====
        function toggleDropdown() {{
            document.getElementById('profileDropdown').classList.toggle('show');
        }}

        document.addEventListener('click', function(e) {{
            var container = document.querySelector('.profile-container');
            if (container && !container.contains(e.target)) {{
                document.getElementById('profileDropdown').classList.remove('show');
            }}
        }});

        function confirmLogout() {{
            return confirm('Are you sure you want to logout?');
        }}

        // ===== Story Functions =====
        function viewStory(id) {{
            showToast('📸 Opening story...');
        }}

        function openStoryUpload() {{
            const input = document.createElement('input');
            input.type = 'file';
            input.accept = 'image/*';
            input.onchange = function(e) {{
                if (this.files && this.files[0]) {{
                    showToast('📸 Story uploaded!');
                }}
            }};
            input.click();
        }}

        // ===== Post Functions =====
        function toggleLike(btn) {{
            const icon = btn.querySelector('i');
            const count = btn.querySelector('.count');
            let num = parseInt(count.textContent);
            if (icon.classList.contains('far')) {{
                icon.classList.remove('far');
                icon.classList.add('fas');
                btn.classList.add('liked');
                num++;
            }} else {{
                icon.classList.remove('fas');
                icon.classList.add('far');
                btn.classList.remove('liked');
                num--;
            }}
            count.textContent = num;
        }}

        function toggleComment(btn) {{
            showToast('💬 Comment section coming soon!');
        }}

        function sharePost(btn) {{
            if (navigator.share) {{
                navigator.share({{
                    title: 'Camly Post',
                    text: 'Check out this post on Camly!',
                    url: window.location.href,
                }});
            }} else {{
                showToast('📤 Share functionality coming soon!');
            }}
        }}

        // ===== Reel Functions =====
        function viewReel(id) {{
            showToast('🎬 Opening reel...');
        }}

        // ===== Toast Function =====
        function showToast(message) {{
            var toast = document.getElementById('toast');
            toast.textContent = message;
            toast.classList.add('show');
            setTimeout(function() {{
                toast.classList.remove('show');
            }}, 3000);
        }}

        
        document.addEventListener('DOMContentLoaded', function() {{
            const savedTheme = localStorage.getItem('theme');
            const isDark = savedTheme === 'dark';
            
            if (isDark) {{
                document.body.classList.add('dark-mode');
                document.getElementById('darkToggle').classList.add('active');
                document.getElementById('lightToggle').classList.remove('active');
            }} else {{
                document.getElementById('lightToggle').classList.add('active');
                document.getElementById('darkToggle').classList.remove('active');
            }}
            
            showToast('🌆 Welcome to Camly!');
        }});
    </script>
</body>
</html>
"""
    return HttpResponse(html)
