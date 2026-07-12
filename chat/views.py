from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
import base64

@login_required
def chat_home(request):
    username = request.user.username
    html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Camly - Messages</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        /* All CSS styles - keeping it concise with group chat additions */
        :root {{
            --bg-primary: #f5f5f5;
            --bg-secondary: #ffffff;
            --bg-chat-own: #f9a825;
            --bg-chat-other: #f0f0f5;
            --text-primary: #1a1a2e;
            --text-secondary: #6b6b7a;
            --text-muted: #9999a8;
            --border-color: #e8e8ef;
            --input-bg: #f0f0f5;
            --online-color: #2ecc71;
            --chat-sidebar-width: 340px;
            --wallpaper-url: url('https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800');
            --wallpaper-opacity: 0.3;
            --group-color: #4a90d9;
        }}
        .dark-mode {{
            --bg-primary: #0a0a2e;
            --bg-secondary: #12123a;
            --bg-chat-own: #f9a825;
            --bg-chat-other: #2a2a5a;
            --text-primary: #f0f0ff;
            --text-secondary: #a8a8c8;
            --text-muted: #6a6a8a;
            --border-color: #2a2a5a;
            --input-bg: #2a2a5a;
            --wallpaper-url: url('https://images.unsplash.com/photo-1519681393784-d120267933ba?w=800');
        }}
        /* Existing styles - keeping it concise */
        * {{ margin:0; padding:0; box-sizing:border-box; }}
        body {{ font-family: -apple-system, sans-serif; background: var(--bg-primary); color: var(--text-primary); height: 100vh; overflow: hidden; display: flex; flex-direction: column; }}
        .status-bar {{ display: flex; justify-content: space-between; padding: 4px 20px; font-size: 12px; color: var(--text-secondary); background: var(--bg-secondary); border-bottom: 1px solid var(--border-color); flex-shrink: 0; }}
        .header {{ display: flex; justify-content: space-between; align-items: center; padding: 10px 20px; background: var(--bg-secondary); border-bottom: 1px solid var(--border-color); flex-shrink: 0; }}
        .header-left {{ display: flex; align-items: center; gap: 12px; }}
        .back-btn {{ background: none; border: none; color: var(--text-primary); font-size: 20px; cursor: pointer; padding: 4px; }}
        .header h1 {{ font-size: 20px; font-weight: 700; color: var(--text-primary); }}
        .header-actions {{ display: flex; gap: 16px; align-items: center; }}
        .header-actions button {{ background: none; border: none; color: var(--text-secondary); font-size: 18px; cursor: pointer; padding: 4px; }}
        .settings-btn, .group-btn {{ background: none; border: none; color: var(--text-secondary); font-size: 18px; cursor: pointer; padding: 4px 8px; border-radius: 8px; }}
        .settings-btn:hover, .group-btn:hover {{ background: var(--input-bg); color: var(--text-primary); }}
        .chat-container {{ display: flex; flex: 1; overflow: hidden; height: calc(100vh - 100px); }}
        .chat-sidebar {{ width: var(--chat-sidebar-width); min-width: var(--chat-sidebar-width); background: var(--bg-secondary); border-right: 1px solid var(--border-color); display: flex; flex-direction: column; overflow: hidden; flex-shrink: 0; }}
        .chat-sidebar .search-container {{ padding: 12px 16px; background: var(--bg-secondary); border-bottom: 1px solid var(--border-color); flex-shrink: 0; }}
        .chat-sidebar .search-bar {{ display: flex; align-items: center; background: var(--input-bg); border-radius: 12px; padding: 8px 14px; gap: 10px; }}
        .chat-sidebar .search-bar i {{ color: var(--text-muted); font-size: 14px; }}
        .chat-sidebar .search-bar input {{ background: none; border: none; outline: none; color: var(--text-primary); font-size: 14px; width: 100%; }}
        .chat-sidebar .search-bar input::placeholder {{ color: var(--text-muted); }}
        .chat-list {{ flex: 1; overflow-y: auto; padding: 8px 0; }}
        .chat-section-header {{ padding: 10px 16px 4px; font-size: 11px; font-weight: 600; color: var(--text-muted); text-transform: uppercase; display: flex; justify-content: space-between; align-items: center; }}
        .chat-section-header .see-all {{ color: #f9a825; font-size: 10px; cursor: pointer; }}
        .chat-item {{ display: flex; align-items: center; padding: 10px 16px; cursor: pointer; transition: background 0.2s; border-left: 3px solid transparent; position: relative; }}
        .chat-item:hover {{ background: rgba(0,0,0,0.03); }}
        .chat-item.active {{ background: rgba(0,0,0,0.03); border-left-color: #f9a825; }}
        .dark-mode .chat-item:hover {{ background: rgba(255,255,255,0.03); }}
        .dark-mode .chat-item.active {{ background: rgba(255,255,255,0.03); }}
        .chat-item.group-chat .chat-avatar {{ background: var(--group-color); color: white; }}
        .chat-item.group-chat .chat-avatar i {{ font-size: 20px; }}
        .chat-avatar {{ width: 44px; height: 44px; border-radius: 50%; overflow: hidden; background: var(--input-bg); flex-shrink: 0; margin-right: 12px; display: flex; align-items: center; justify-content: center; font-size: 18px; color: var(--text-muted); position: relative; }}
        .chat-avatar .online-indicator {{ position: absolute; bottom: 0; right: 0; width: 12px; height: 12px; border-radius: 50%; background: var(--online-color); border: 2px solid var(--bg-secondary); }}
        .chat-info {{ flex: 1; min-width: 0; }}
        .chat-info .chat-name {{ font-weight: 600; font-size: 14px; color: var(--text-primary); }}
        .chat-info .chat-preview {{ font-size: 12px; color: var(--text-muted); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
        .chat-info .chat-members {{ font-size: 10px; color: var(--text-muted); }}
        .chat-meta {{ text-align: right; flex-shrink: 0; margin-left: 8px; }}
        .chat-meta .chat-time {{ font-size: 10px; color: var(--text-muted); }}
        .chat-meta .unread-badge {{ background: #f9a825; color: #fff; font-size: 10px; padding: 1px 7px; border-radius: 12px; display: inline-block; font-weight: 600; }}
        .chat-meta .pinned-icon {{ color: #f9a825; font-size: 10px; }}
        .chat-close-btn {{ position: absolute; right: 8px; top: 50%; transform: translateY(-50%); background: none; border: none; color: var(--text-muted); font-size: 14px; cursor: pointer; padding: 4px 8px; border-radius: 8px; opacity: 0; background: var(--bg-secondary); }}
        .chat-item:hover .chat-close-btn {{ opacity: 1; }}
        .chat-close-btn:hover {{ color: #e74c3c; background: rgba(231,76,60,0.1); }}
        .chat-main {{ flex: 1; display: flex; flex-direction: column; background: var(--bg-primary); min-width: 0; position: relative; }}
        .chat-main.hidden {{ display: none; }}
        .chat-wallpaper {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; background-image: var(--wallpaper-url); background-size: cover; background-position: center; opacity: var(--wallpaper-opacity); z-index: 0; transition: opacity 0.3s ease; }}
        .dark-mode .chat-wallpaper {{ opacity: calc(var(--wallpaper-opacity) * 0.5); }}
        .chat-main-header {{ display: flex; justify-content: space-between; align-items: center; padding: 12px 20px; background: var(--bg-secondary); border-bottom: 1px solid var(--border-color); flex-shrink: 0; z-index: 1; position: relative; }}
        .chat-main-header .chat-user-info {{ display: flex; align-items: center; gap: 12px; }}
        .chat-main-header .chat-user-info .chat-avatar-sm {{ width: 36px; height: 36px; border-radius: 50%; background: var(--input-bg); display: flex; align-items: center; justify-content: center; font-size: 16px; position: relative; }}
        .chat-main-header .chat-user-info .chat-avatar-sm .online-dot-small {{ position: absolute; bottom: 0; right: 0; width: 10px; height: 10px; border-radius: 50%; background: var(--online-color); border: 2px solid var(--bg-secondary); }}
        .chat-main-header .chat-user-info .chat-name {{ font-weight: 600; font-size: 15px; }}
        .chat-main-header .chat-user-info .chat-status {{ font-size: 11px; color: var(--text-muted); }}
        .chat-main-header .chat-actions {{ display: flex; gap: 12px; align-items: center; }}
        .chat-main-header .chat-actions button {{ background: none; border: none; color: var(--text-secondary); font-size: 16px; cursor: pointer; padding: 4px; }}
        .chat-main-header .chat-actions .close-chat-div-btn {{ color: var(--text-muted); font-size: 18px; }}
        .chat-main-header .chat-actions .close-chat-div-btn:hover {{ color: #e74c3c; transform: rotate(90deg); }}
        .chat-messages {{ flex: 1; overflow-y: auto; padding: 16px 20px; display: flex; flex-direction: column; gap: 8px; z-index: 1; position: relative; }}
        .bubble-style-1 .message.own {{ background: var(--bg-chat-own); color: #ffffff; border-bottom-right-radius: 4px; }}
        .bubble-style-1 .message.other {{ background: var(--bg-chat-other); color: var(--text-primary); border-bottom-left-radius: 4px; }}
        .bubble-style-2 .message.own {{ background: #4a90d9; color: #fff; border-radius: 20px 20px 4px 20px; }}
        .bubble-style-2 .message.other {{ background: #e8e8ef; color: #1a1a2e; border-radius: 20px 20px 20px 4px; }}
        .dark-mode .bubble-style-2 .message.other {{ background: #2a2a5a; color: #f0f0ff; }}
        .bubble-style-3 .message.own {{ background: #2ecc71; color: #fff; border-radius: 16px 16px 4px 16px; }}
        .bubble-style-3 .message.other {{ background: #f0f0f5; color: #1a1a2e; border-radius: 16px 16px 16px 4px; }}
        .dark-mode .bubble-style-3 .message.other {{ background: #2a2a5a; color: #f0f0ff; }}
        .bubble-style-4 .message.own {{ background: #e74c3c; color: #fff; border-radius: 24px 24px 4px 24px; }}
        .bubble-style-4 .message.other {{ background: #f0f0f5; color: #1a1a2e; border-radius: 24px 24px 24px 4px; }}
        .dark-mode .bubble-style-4 .message.other {{ background: #2a2a5a; color: #f0f0ff; }}
        .bubble-style-5 .message.own {{ background: linear-gradient(135deg, #f9a825, #ff6f00); color: #fff; border-radius: 20px 4px 20px 4px; }}
        .bubble-style-5 .message.other {{ background: linear-gradient(135deg, #f0f0f5, #e8e8ef); color: #1a1a2e; border-radius: 4px 20px 4px 20px; }}
        .dark-mode .bubble-style-5 .message.other {{ background: linear-gradient(135deg, #2a2a5a, #1a1a4e); color: #f0f0ff; }}
        .message {{ max-width: 70%; padding: 10px 14px; border-radius: 14px; font-size: 14px; line-height: 1.5; word-wrap: break-word; animation: messageIn 0.3s ease-out; }}
        @keyframes messageIn {{ from {{ opacity: 0; transform: translateY(10px); }} to {{ opacity: 1; transform: translateY(0); }} }}
        .message.own {{ align-self: flex-end; }}
        .message.other {{ align-self: flex-start; }}
        .message .message-time {{ font-size: 10px; opacity: 0.6; margin-top: 4px; display: block; text-align: right; }}
        .message.sticker {{ padding: 4px; max-width: 200px; background: none !important; }}
        .message.sticker img {{ width: 100%; height: auto; border-radius: 12px; }}
        .message.file {{ padding: 8px 12px; background: var(--bg-secondary) !important; border: 1px solid var(--border-color); border-radius: 12px; max-width: 280px; }}
        .message.file .file-icon {{ font-size: 32px; margin-right: 8px; }}
        .message.file .file-name {{ font-weight: 500; font-size: 13px; }}
        .message.file .file-size {{ font-size: 11px; color: var(--text-muted); }}
        .message.image-message {{ padding: 4px; max-width: 300px; background: none !important; }}
        .message.image-message img {{ width: 100%; height: auto; border-radius: 12px; max-height: 300px; object-fit: contain; }}
        .chat-input-area {{ display: flex; align-items: center; gap: 10px; padding: 10px 16px; background: var(--bg-secondary); border-top: 1px solid var(--border-color); flex-shrink: 0; z-index: 1; position: relative; }}
        .chat-input-area input {{ flex: 1; padding: 10px 16px; background: var(--input-bg); border: none; border-radius: 20px; color: var(--text-primary); font-size: 14px; outline: none; }}
        .chat-input-area input::placeholder {{ color: var(--text-muted); }}
        .chat-input-area .input-actions {{ display: flex; gap: 4px; align-items: center; }}
        .chat-input-area .input-actions button {{ background: none; border: none; color: var(--text-secondary); font-size: 18px; cursor: pointer; padding: 6px; border-radius: 50%; width: 36px; height: 36px; display: flex; align-items: center; justify-content: center; position: relative; }}
        .chat-input-area .input-actions button:hover {{ background: var(--input-bg); color: var(--text-primary); }}
        .chat-input-area .input-actions button .badge {{ position: absolute; top: 0; right: 0; background: #e74c3c; color: white; font-size: 9px; padding: 1px 5px; border-radius: 50%; }}
        .send-btn {{ width: 40px; height: 40px; border-radius: 50%; background: #f9a825; border: none; color: #fff; font-size: 16px; cursor: pointer; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }}
        .send-btn:hover {{ transform: scale(1.05); box-shadow: 0 4px 16px rgba(249,168,37,0.3); }}
        .file-preview {{ display: none; position: absolute; bottom: 70px; left: 16px; right: 16px; max-height: 200px; background: var(--bg-secondary); border-radius: 16px; border: 1px solid var(--border-color); box-shadow: 0 8px 30px rgba(0,0,0,0.2); z-index: 999; padding: 16px; overflow-y: auto; }}
        .file-preview.active {{ display: block; }}
        .file-preview .file-item {{ display: flex; align-items: center; gap: 12px; padding: 8px; border-radius: 8px; background: var(--input-bg); margin-bottom: 8px; }}
        .file-preview .file-item .file-icon {{ font-size: 28px; }}
        .file-preview .file-item .file-info {{ flex: 1; }}
        .file-preview .file-item .file-info .file-name {{ font-size: 13px; font-weight: 500; }}
        .file-preview .file-item .file-info .file-size {{ font-size: 11px; color: var(--text-muted); }}
        .file-preview .file-item .remove-file {{ background: none; border: none; color: var(--text-muted); cursor: pointer; padding: 4px 8px; }}
        .file-preview .file-item .remove-file:hover {{ color: #e74c3c; }}
        
        /* Emoji Picker */
        .emoji-picker {{ display: none; position: absolute; bottom: 70px; left: 16px; right: 16px; max-height: 350px; background: var(--bg-secondary); border-radius: 16px; border: 1px solid var(--border-color); box-shadow: 0 8px 30px rgba(0,0,0,0.2); z-index: 1000; overflow: hidden; flex-direction: column; }}
        .emoji-picker.active {{ display: flex; }}
        .emoji-picker-header {{ display: flex; border-bottom: 1px solid var(--border-color); flex-shrink: 0; }}
        .emoji-picker-header button {{ flex: 1; padding: 10px; background: none; border: none; border-bottom: 3px solid transparent; cursor: pointer; color: var(--text-muted); font-size: 14px; font-weight: 500; transition: all 0.3s; }}
        .emoji-picker-header button.active {{ border-bottom-color: #f9a825; color: var(--text-primary); }}
        .emoji-picker-content {{ overflow-y: auto; padding: 12px; flex: 1; }}
        .emoji-grid {{ display: grid; grid-template-columns: repeat(8, 1fr); gap: 4px; }}
        .emoji-grid .emoji {{ font-size: 28px; text-align: center; padding: 6px; cursor: pointer; border-radius: 8px; transition: all 0.2s; }}
        .emoji-grid .emoji:hover {{ background: var(--input-bg); transform: scale(1.1); }}
        .sticker-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; }}
        .sticker-grid .sticker {{ padding: 4px; cursor: pointer; border-radius: 8px; transition: all 0.2s; text-align: center; }}
        .sticker-grid .sticker:hover {{ background: var(--input-bg); transform: scale(1.05); }}
        .sticker-grid .sticker img {{ width: 100%; height: auto; border-radius: 8px; }}
        .sticker-grid .sticker .emoji-sticker {{ font-size: 48px; display: block; padding: 8px; }}
        .create-sticker-btn {{ padding: 12px; background: #f9a825; color: white; border: none; border-radius: 8px; cursor: pointer; font-weight: 600; margin-top: 8px; width: 100%; }}
        .create-sticker-btn:hover {{ background: #ff6f00; }}
        
        /* ===== Group Chat Modal ===== */
        .group-modal {{ display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.7); z-index: 2000; align-items: center; justify-content: center; }}
        .group-modal.active {{ display: flex; }}
        .group-modal-content {{ background: var(--bg-secondary); border-radius: 20px; padding: 24px; max-width: 500px; width: 90%; max-height: 80vh; overflow-y: auto; }}
        .group-modal-content .group-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }}
        .group-modal-content .group-header h2 {{ color: var(--text-primary); }}
        .group-modal-content .group-header .close-btn {{ background: none; border: none; color: var(--text-secondary); font-size: 24px; cursor: pointer; }}
        .group-modal-content .group-field {{ margin-bottom: 16px; }}
        .group-modal-content .group-field label {{ display: block; color: var(--text-secondary); font-size: 13px; font-weight: 500; margin-bottom: 4px; }}
        .group-modal-content .group-field input {{ width: 100%; padding: 10px 14px; background: var(--input-bg); border: 1px solid var(--border-color); border-radius: 10px; color: var(--text-primary); font-size: 14px; outline: none; }}
        .group-modal-content .group-field input:focus {{ border-color: #f9a825; box-shadow: 0 0 0 2px rgba(249,168,37,0.1); }}
        .group-modal-content .member-search {{ position: relative; }}
        .group-modal-content .member-search input {{ width: 100%; padding: 10px 14px; background: var(--input-bg); border: 1px solid var(--border-color); border-radius: 10px; color: var(--text-primary); font-size: 14px; outline: none; }}
        .group-modal-content .member-search .search-results {{ position: absolute; top: 100%; left: 0; right: 0; background: var(--bg-secondary); border: 1px solid var(--border-color); border-radius: 10px; max-height: 150px; overflow-y: auto; display: none; z-index: 10; }}
        .group-modal-content .member-search .search-results.active {{ display: block; }}
        .group-modal-content .member-search .search-results .result-item {{ padding: 8px 14px; cursor: pointer; display: flex; align-items: center; gap: 10px; transition: background 0.2s; }}
        .group-modal-content .member-search .search-results .result-item:hover {{ background: var(--input-bg); }}
        .group-modal-content .member-search .search-results .result-item .result-avatar {{ width: 28px; height: 28px; border-radius: 50%; background: var(--input-bg); display: flex; align-items: center; justify-content: center; font-size: 12px; }}
        .group-modal-content .member-search .search-results .result-item .result-name {{ font-size: 13px; color: var(--text-primary); }}
        .group-modal-content .selected-members {{ display: flex; flex-wrap: wrap; gap: 6px; padding: 8px 0; }}
        .group-modal-content .selected-members .member-tag {{ display: flex; align-items: center; gap: 4px; background: rgba(249,168,37,0.15); padding: 4px 10px; border-radius: 20px; font-size: 12px; color: var(--text-primary); }}
        .group-modal-content .selected-members .member-tag .remove-member {{ background: none; border: none; color: var(--text-muted); cursor: pointer; font-size: 12px; padding: 0 4px; }}
        .group-modal-content .selected-members .member-tag .remove-member:hover {{ color: #e74c3c; }}
        .group-modal-content .create-group-btn {{ width: 100%; padding: 12px; background: #f9a825; color: white; border: none; border-radius: 10px; font-size: 16px; font-weight: 600; cursor: pointer; transition: all 0.3s; }}
        .group-modal-content .create-group-btn:hover {{ background: #ff6f00; transform: scale(1.02); }}
        .group-modal-content .create-group-btn:disabled {{ opacity: 0.5; cursor: not-allowed; }}
        
        /* Modals */
        .settings-modal, .bubble-modal, .delete-modal, .wallpaper-modal, .sticker-modal {{ display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.7); z-index: 2000; align-items: center; justify-content: center; }}
        .settings-modal.active, .bubble-modal.active, .delete-modal.active, .wallpaper-modal.active, .sticker-modal.active {{ display: flex; }}
        .settings-modal-content, .bubble-modal-content, .delete-modal-content, .wallpaper-modal-content, .sticker-modal-content {{ background: var(--bg-secondary); border-radius: 20px; padding: 24px; max-width: 500px; width: 90%; max-height: 80vh; overflow-y: auto; }}
        .settings-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }}
        .settings-header h2 {{ color: var(--text-primary); }}
        .settings-header .close-btn {{ background: none; border: none; color: var(--text-secondary); font-size: 24px; cursor: pointer; }}
        .settings-section {{ margin-bottom: 24px; }}
        .settings-section .section-title {{ font-size: 13px; font-weight: 600; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 12px; padding-bottom: 8px; border-bottom: 1px solid var(--border-color); }}
        .settings-option {{ display: flex; justify-content: space-between; align-items: center; padding: 12px 0; border-bottom: 1px solid var(--border-color); cursor: pointer; }}
        .settings-option:last-child {{ border-bottom: none; }}
        .settings-option .option-info {{ display: flex; align-items: center; gap: 12px; }}
        .settings-option .option-info i {{ color: var(--text-muted); font-size: 18px; width: 24px; }}
        .settings-option .option-info .option-label {{ color: var(--text-primary); font-size: 14px; }}
        .settings-option .option-info .option-desc {{ color: var(--text-muted); font-size: 12px; display: block; }}
        .settings-option .option-value {{ color: var(--text-secondary); font-size: 13px; display: flex; align-items: center; gap: 8px; }}
        .opacity-slider-container {{ display: flex; align-items: center; gap: 12px; padding: 4px 0; }}
        .opacity-slider-container input[type="range"] {{ flex: 1; -webkit-appearance: none; appearance: none; height: 4px; border-radius: 2px; background: var(--border-color); outline: none; }}
        .opacity-slider-container input[type="range"]::-webkit-slider-thumb {{ -webkit-appearance: none; appearance: none; width: 16px; height: 16px; border-radius: 50%; background: #f9a825; cursor: pointer; }}
        .opacity-value {{ min-width: 40px; font-size: 13px; color: var(--text-secondary); text-align: center; }}
        .language-dropdown {{ padding: 6px 12px; border-radius: 8px; border: 1px solid var(--border-color); background: var(--input-bg); color: var(--text-primary); font-size: 13px; cursor: pointer; outline: none; }}
        .bubble-style-picker {{ display: flex; gap: 8px; flex-wrap: wrap; }}
        .bubble-style-option {{ width: 50px; height: 50px; border-radius: 12px; border: 3px solid transparent; cursor: pointer; display: flex; align-items: center; justify-content: center; position: relative; }}
        .bubble-style-option:hover {{ transform: scale(1.05); }}
        .bubble-style-option.active {{ border-color: #f9a825; }}
        .bubble-style-option.active::after {{ content: '✓'; position: absolute; top: -8px; right: -8px; background: #f9a825; color: white; width: 18px; height: 18px; border-radius: 50%; font-size: 10px; display: flex; align-items: center; justify-content: center; }}
        .bubble-preview-own {{ background: #f9a825; color: white; padding: 4px 8px; border-radius: 8px; font-size: 10px; }}
        .bubble-preview-other {{ background: var(--bg-chat-other); color: var(--text-primary); padding: 4px 8px; border-radius: 8px; font-size: 10px; }}
        .toast {{ position: fixed; bottom: 80px; left: 50%; transform: translateX(-50%); background: var(--bg-secondary); color: var(--text-primary); padding: 12px 24px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.2); z-index: 3000; font-size: 14px; font-weight: 500; display: none; border: 1px solid var(--border-color); }}
        .toast.show {{ display: block; animation: toastIn 0.3s ease-out; }}
        @keyframes toastIn {{ from {{ opacity: 0; transform: translateX(-50%) translateY(20px); }} to {{ opacity: 1; transform: translateX(-50%) translateY(0); }} }}
        .delete-modal-content .icon {{ font-size: 48px; color: #e74c3c; margin-bottom: 16px; text-align: center; }}
        .delete-modal-content h2 {{ text-align: center; margin-bottom: 8px; }}
        .delete-modal-content p {{ text-align: center; color: var(--text-secondary); font-size: 14px; margin-bottom: 24px; }}
        .delete-modal-actions {{ display: flex; gap: 12px; }}
        .delete-modal-actions button {{ flex: 1; padding: 12px; border: none; border-radius: 10px; font-size: 14px; font-weight: 600; cursor: pointer; }}
        .delete-modal-actions .cancel-btn {{ background: var(--input-bg); color: var(--text-secondary); }}
        .delete-modal-actions .delete-btn {{ background: #e74c3c; color: white; }}
        .wallpaper-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-bottom: 16px; }}
        .wallpaper-option {{ aspect-ratio: 16/9; border-radius: 12px; cursor: pointer; border: 3px solid transparent; background-size: cover; background-position: center; }}
        .wallpaper-option:hover {{ transform: scale(1.05); }}
        .wallpaper-option.selected {{ border-color: #f9a825; }}
        .wallpaper-option.default-wall {{ background-image: url('https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=400'); }}
        .wallpaper-option.dark-wall {{ background-image: url('https://images.unsplash.com/photo-1519681393784-d120267933ba?w=400'); }}
        .wallpaper-option.beach-wall {{ background-image: url('https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=400'); }}
        .wallpaper-option.mountain-wall {{ background-image: url('https://images.unsplash.com/photo-1519681393784-d120267933ba?w=400'); }}
        .wallpaper-option.forest-wall {{ background-image: url('https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=400'); }}
        .wallpaper-option.city-wall {{ background-image: url('https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?w=400'); }}
        .wallpaper-modal-close {{ padding: 10px 24px; background: #f9a825; border: none; border-radius: 10px; color: white; cursor: pointer; font-size: 14px; font-weight: 600; }}
        
        .sticker-modal-content .sticker-preview {{ width: 100px; height: 100px; border-radius: 12px; border: 2px dashed var(--border-color); display: flex; align-items: center; justify-content: center; margin: 12px auto; font-size: 48px; background: var(--input-bg); }}
        .sticker-modal-content input[type="file"] {{ display: none; }}
        .sticker-modal-content .upload-label {{ display: block; padding: 10px; background: var(--input-bg); border-radius: 8px; cursor: pointer; text-align: center; color: var(--text-secondary); font-size: 14px; }}
        .sticker-modal-content .upload-label:hover {{ background: var(--border-color); }}
        .sticker-modal-content .emoji-options {{ display: flex; gap: 8px; flex-wrap: wrap; justify-content: center; margin: 12px 0; }}
        .sticker-modal-content .emoji-options span {{ font-size: 32px; cursor: pointer; padding: 4px 8px; border-radius: 8px; transition: all 0.2s; }}
        .sticker-modal-content .emoji-options span:hover {{ background: var(--input-bg); transform: scale(1.2); }}
        .sticker-modal-content .sticker-name-input {{ width: 100%; padding: 10px; border: 1px solid var(--border-color); border-radius: 8px; background: var(--input-bg); color: var(--text-primary); font-size: 14px; margin: 8px 0; }}
        .sticker-modal-content .save-sticker-btn {{ padding: 10px 24px; background: #f9a825; color: white; border: none; border-radius: 8px; cursor: pointer; font-weight: 600; width: 100%; }}
        .sticker-modal-content .save-sticker-btn:hover {{ background: #ff6f00; }}
        
        @media (max-width: 1024px) {{ .chat-sidebar {{ width: 100%; min-width: 100%; border-right: none; border-bottom: 1px solid var(--border-color); max-height: 50vh; }} .chat-container {{ flex-direction: column; }} .chat-main {{ max-height: 50vh; }} .message {{ max-width: 85%; }} .wallpaper-grid {{ grid-template-columns: repeat(2, 1fr); }} }}
        @media (max-width: 768px) {{ .header {{ padding: 8px 16px; }} .header h1 {{ font-size: 18px; }} .chat-avatar {{ width: 40px; height: 40px; font-size: 16px; }} .chat-close-btn {{ opacity: 1 !important; }} .emoji-grid {{ grid-template-columns: repeat(6, 1fr); }} }}
        @media (max-width: 480px) {{ .header {{ padding: 8px 12px; }} .header h1 {{ font-size: 16px; }} .chat-avatar {{ width: 36px; height: 36px; font-size: 14px; }} .chat-messages {{ padding: 10px 12px; }} .chat-input-area {{ padding: 8px 12px; }} .settings-modal-content {{ padding: 16px; }} .opacity-slider-container {{ flex-wrap: wrap; }} .emoji-grid {{ grid-template-columns: repeat(5, 1fr); }} .sticker-grid {{ grid-template-columns: repeat(3, 1fr); }} .message.file {{ max-width: 200px; }} .message.image-message {{ max-width: 200px; }} .group-modal-content {{ padding: 16px; }} }}
    </style>
</head>
<body>
    <div class="status-bar"><span>9:41</span><span></span></div>
    <header class="header">
        <div class="header-left">
            <button class="back-btn" onclick="window.location.href='/'"><i class="fas fa-arrow-left"></i></button>
            <h1>Messages</h1>
        </div>
        <div class="header-actions">
            <button class="group-btn" onclick="openGroupModal()" title="New Group Chat"><i class="fas fa-users"></i></button>
            <button class="settings-btn" onclick="openSettings()" title="Settings"><i class="fas fa-cog"></i></button>
            <button onclick="toggleTheme()" class="theme-toggle-btn" id="themeToggle"><i class="fas fa-moon" id="themeIcon"></i></button>
            <button onclick="openWallpaperPicker()" title="Change Wallpaper"><i class="fas fa-image"></i></button>
        </div>
    </header>
    <div class="chat-container">
        <div class="chat-sidebar">
            <div class="search-container">
                <div class="search-bar">
                    <i class="fas fa-search"></i>
                    <input type="text" placeholder="Search Message" id="searchInput">
                </div>
            </div>
            <div class="chat-list" id="chatList">
                <div class="chat-section-header"><span>Pinned</span><span class="see-all">See All</span></div>
                <div class="chat-item active" data-name="Shanti Thapa" data-id="1">
                    <div class="chat-avatar">👤<span class="online-indicator"></span></div>
                    <div class="chat-info"><div class="chat-name">Shanti Thapa</div><div class="chat-preview">Thanks.</div></div>
                    <div class="chat-meta"><div class="chat-time">2 Mins ago</div><div class="pinned-icon"><i class="fas fa-thumbtack"></i></div></div>
                    <button class="chat-close-btn" onclick="event.stopPropagation(); openDeleteModal('Shanti Thapa', 1)"><i class="fas fa-times"></i></button>
                </div>
                <div class="chat-item group-chat" data-name="Camping Team" data-id="4">
                    <div class="chat-avatar"><i class="fas fa-users"></i></div>
                    <div class="chat-info">
                        <div class="chat-name">Camping Team</div>
                        <div class="chat-preview">I'll be taking the tents...</div>
                        <div class="chat-members">5 members</div>
                    </div>
                    <div class="chat-meta"><div class="chat-time">Yesterday</div><div class="unread-badge">3</div></div>
                    <button class="chat-close-btn" onclick="event.stopPropagation(); openDeleteModal('Camping Team', 4)"><i class="fas fa-times"></i></button>
                </div>
                <div class="chat-item" data-name="Santosh Limbu" data-id="2">
                    <div class="chat-avatar">👤<span class="online-indicator"></span></div>
                    <div class="chat-info"><div class="chat-name">Santosh Limbu</div><div class="chat-preview">I will let you know by this evening.</div></div>
                    <div class="chat-meta"><div class="chat-time">12 Mins ago</div></div>
                    <button class="chat-close-btn" onclick="event.stopPropagation(); openDeleteModal('Santosh Limbu', 2)"><i class="fas fa-times"></i></button>
                </div>
                <div class="chat-section-header"><span>All Messages</span><span class="see-all">See All</span></div>
                <div class="chat-item" data-name="Kala Shrestha" data-id="3">
                    <div class="chat-avatar">👤</div>
                    <div class="chat-info"><div class="chat-name">Kala Shrestha</div><div class="chat-preview">Ok.</div></div>
                    <div class="chat-meta"><div class="chat-time">12 Mins ago</div></div>
                    <button class="chat-close-btn" onclick="event.stopPropagation(); openDeleteModal('Kala Shrestha', 3)"><i class="fas fa-times"></i></button>
                </div>
                <div class="chat-item" data-name="Riya Shrestha" data-id="5">
                    <div class="chat-avatar">👤</div>
                    <div class="chat-info"><div class="chat-name">Riya Shrestha</div><div class="chat-preview">Please do not forget to bring the herbs...</div></div>
                    <div class="chat-meta"><div class="chat-time">Yesterday</div></div>
                    <button class="chat-close-btn" onclick="event.stopPropagation(); openDeleteModal('Riya Shrestha', 5)"><i class="fas fa-times"></i></button>
                </div>
                <div class="chat-item" data-name="Punam Limbu" data-id="6">
                    <div class="chat-avatar">👤</div>
                    <div class="chat-info"><div class="chat-name">Punam Limbu</div><div class="chat-preview">I was wondering, if you are free this Sat...</div></div>
                    <div class="chat-meta"><div class="chat-time">Yesterday</div></div>
                    <button class="chat-close-btn" onclick="event.stopPropagation(); openDeleteModal('Punam Limbu', 6)"><i class="fas fa-times"></i></button>
                </div>
                <div class="chat-item" data-name="Mausam Kafle" data-id="7">
                    <div class="chat-avatar">👤</div>
                    <div class="chat-info"><div class="chat-name">Mausam Kafle</div><div class="chat-preview">Ok.</div></div>
                    <div class="chat-meta"><div class="chat-time">Yesterday</div></div>
                    <button class="chat-close-btn" onclick="event.stopPropagation(); openDeleteModal('Mausam Kafle', 7)"><i class="fas fa-times"></i></button>
                </div>
                <div class="chat-item group-chat" data-name="Basketball Team" data-id="8">
                    <div class="chat-avatar"><i class="fas fa-users"></i></div>
                    <div class="chat-info">
                        <div class="chat-name">Basketball Team</div>
                        <div class="chat-preview">We will do our best.</div>
                        <div class="chat-members">8 members</div>
                    </div>
                    <div class="chat-meta"><div class="chat-time">Yesterday</div></div>
                    <button class="chat-close-btn" onclick="event.stopPropagation(); openDeleteModal('Basketball Team', 8)"><i class="fas fa-times"></i></button>
                </div>
                <div class="chat-item" data-name="Office Buddies" data-id="9">
                    <div class="chat-avatar">👤</div>
                    <div class="chat-info"><div class="chat-name">Office Buddies</div><div class="chat-preview">...</div></div>
                    <div class="chat-meta"><div class="chat-time">Yesterday</div></div>
                    <button class="chat-close-btn" onclick="event.stopPropagation(); openDeleteModal('Office Buddies', 9)"><i class="fas fa-times"></i></button>
                </div>
            </div>
        </div>
        <div class="chat-main" id="chatMain">
            <div class="chat-wallpaper" id="chatWallpaper"></div>
            <div class="chat-main-header">
                <div class="chat-user-info">
                    <div class="chat-avatar-sm">👤<span class="online-dot-small"></span></div>
                    <div><div class="chat-name">Santosh Limbu</div><div class="chat-status">Active Now</div></div>
                </div>
                <div class="chat-actions">
                    <button onclick="alert('Voice call coming soon!')"><i class="fas fa-phone"></i></button>
                    <button onclick="alert('Video call coming soon!')"><i class="fas fa-video"></i></button>
                    <button class="close-chat-div-btn" onclick="closeChatDiv()" title="Close Chat"><i class="fas fa-times"></i></button>
                </div>
            </div>
            <div class="chat-messages" id="chatMessages">
                <div class="message other">Hello Santosh. Are you free this Saturday.<span class="message-time">2:23 PM</span></div>
                <div class="message own">Hi, I have some plans but if you looking for any help. I can manage my time.<span class="message-time">2:25 PM</span></div>
                <div class="message other">Actually, me and my friends were planning for going on a camp this Saturday. And I am wondering, Would you be able to join us.<span class="message-time">2:25 PM</span></div>
                <div class="message own">Oh, I would love to<br>What's the time of leaving?<span class="message-time">2:27 PM</span></div>
                <div class="message other">We will be leaving around 4 at the evening.<span class="message-time">2:30 PM</span></div>
                <div class="message own">I'll let you know by this evening.<span class="message-time">Just Now</span></div>
            </div>
            <div class="chat-input-area" id="chatInputArea">
                <div class="input-actions">
                    <button class="emoji-toggle-btn" onclick="toggleEmojiPicker()" title="Emoji & Stickers"><i class="fas fa-smile"></i></button>
                    <button onclick="document.getElementById('fileInput').click()" title="Attach file" id="attachBtn">
                        <i class="fas fa-paperclip"></i>
                        <span class="badge" id="fileBadge" style="display:none;">1</span>
                    </button>
                    <input type="file" id="fileInput" style="display:none" multiple accept="image/*,.pdf,.doc,.docx,.txt,.zip,.rar,.mp3,.mp4,.xls,.xlsx,.ppt,.pptx" onchange="handleFileSelect(this)">
                </div>
                <input type="text" placeholder="Your message here" id="messageInput">
                <button class="send-btn" onclick="sendMessage()"><i class="fas fa-paper-plane"></i></button>
                
                <div class="file-preview" id="filePreview">
                    <div id="filePreviewContent"></div>
                    <button class="create-sticker-btn" onclick="clearFiles()" style="margin-top:8px;">Clear All</button>
                </div>
                
                <div class="emoji-picker" id="emojiPicker">
                    <div class="emoji-picker-header">
                        <button class="active" onclick="switchEmojiTab('emoji', this)">😊 Emoji</button>
                        <button onclick="switchEmojiTab('stickers', this)">📸 Stickers</button>
                        <button onclick="switchEmojiTab('custom', this)">✨ Custom</button>
                    </div>
                    <div class="emoji-picker-content" id="emojiContent"></div>
                </div>
            </div>
        </div>
    </div>

    <!-- Group Chat Modal -->
    <div class="group-modal" id="groupModal">
        <div class="group-modal-content">
            <div class="group-header">
                <h2>New Group Chat</h2>
                <button class="close-btn" onclick="closeGroupModal()"><i class="fas fa-times"></i></button>
            </div>
            <div class="group-field">
                <label>Group Name</label>
                <input type="text" id="groupName" placeholder="Enter group name..." maxlength="50">
            </div>
            <div class="group-field">
                <label>Add Members</label>
                <div class="member-search">
                    <input type="text" id="memberSearch" placeholder="Search for people..." oninput="searchMembers(this.value)">
                    <div class="search-results" id="searchResults"></div>
                </div>
            </div>
            <div class="selected-members" id="selectedMembers"></div>
            <button class="create-group-btn" onclick="createGroup()" id="createGroupBtn">Create Group</button>
        </div>
    </div>

    <!-- Settings Modal -->
    <div class="settings-modal" id="settingsModal">
        <div class="settings-modal-content">
            <div class="settings-header"><h2>Settings</h2><button class="close-btn" onclick="closeSettings()"><i class="fas fa-times"></i></button></div>
            <div class="settings-section">
                <div class="section-title">Appearance</div>
                <div class="settings-option">
                    <div class="option-info"><i class="fas fa-palette"></i><div><span class="option-label">Chat Bubble Style</span><span class="option-desc">Change how messages appear</span></div></div>
                    <div class="option-value" onclick="openBubblePicker()"><span id="currentBubbleLabel">Default</span><i class="fas fa-chevron-right"></i></div>
                </div>
                <div class="settings-option">
                    <div class="option-info"><i class="fas fa-image"></i><div><span class="option-label">Wallpaper Opacity</span><span class="option-desc">Adjust wallpaper transparency</span></div></div>
                    <div class="option-value"><div class="opacity-slider-container"><input type="range" id="opacitySlider" min="0" max="80" value="30" oninput="updateOpacity(this.value)"><span class="opacity-value" id="opacityValue">30%</span></div></div>
                </div>
                <div class="settings-option" onclick="toggleTheme()">
                    <div class="option-info"><i class="fas fa-moon"></i><div><span class="option-label">Dark Mode</span><span class="option-desc">Switch between light and dark</span></div></div>
                    <div class="option-value" id="themeStatus"><span>Light</span><i class="fas fa-toggle-off" id="themeToggleIcon"></i></div>
                </div>
            </div>
            <div class="settings-section">
                <div class="section-title">Privacy</div>
                <div class="settings-option" onclick="togglePrivacy('online')">
                    <div class="option-info"><i class="fas fa-eye"></i><div><span class="option-label">Show Online Status</span><span class="option-desc">Let others see when you're online</span></div></div>
                    <div class="option-value"><span id="privacyOnline">On</span><i class="fas fa-toggle-on" id="privacyOnlineIcon"></i></div>
                </div>
                <div class="settings-option" onclick="togglePrivacy('read')">
                    <div class="option-info"><i class="fas fa-check-double"></i><div><span class="option-label">Read Receipts</span><span class="option-desc">Show when you've read messages</span></div></div>
                    <div class="option-value"><span id="privacyRead">On</span><i class="fas fa-toggle-on" id="privacyReadIcon"></i></div>
                </div>
                <div class="settings-option" onclick="togglePrivacy('typing')">
                    <div class="option-info"><i class="fas fa-keyboard"></i><div><span class="option-label">Typing Indicator</span><span class="option-desc">Show when you're typing</span></div></div>
                    <div class="option-value"><span id="privacyTyping">On</span><i class="fas fa-toggle-on" id="privacyTypingIcon"></i></div>
                </div>
                <div class="settings-option" onclick="togglePrivacy('group_invite')">
                    <div class="option-info"><i class="fas fa-user-plus"></i><div><span class="option-label">Group Invites</span><span class="option-desc">Who can add you to groups</span></div></div>
                    <div class="option-value" id="groupInviteValue"><span>Everyone</span><i class="fas fa-chevron-right"></i></div>
                </div>
            </div>
            <div class="settings-section">
                <div class="section-title">Language</div>
                <div class="settings-option">
                    <div class="option-info"><i class="fas fa-globe"></i><div><span class="option-label">App Language</span><span class="option-desc">Choose your preferred language</span></div></div>
                    <div class="option-value"><select class="language-dropdown" id="languageDropdown" onchange="changeLanguage(this.value)"><option value="en">English</option><option value="es">Spanish</option><option value="fr">French</option><option value="de">German</option><option value="zh">Chinese</option><option value="ja">Japanese</option><option value="ar">Arabic</option><option value="hi">Hindi</option><option value="pt">Portuguese</option><option value="ru">Russian</option></select></div>
                </div>
            </div>
            <div class="settings-section">
                <div class="section-title">App</div>
                <div class="settings-option" onclick="checkUpdates()">
                    <div class="option-info"><i class="fas fa-download"></i><div><span class="option-label">Check for Updates</span><span class="option-desc">Get the latest features and fixes</span></div></div>
                    <div class="option-value"><span id="updateStatus">v1.0.0</span><i class="fas fa-chevron-right"></i></div>
                </div>
                <div class="settings-option" onclick="showAppInfo()">
                    <div class="option-info"><i class="fas fa-info-circle"></i><div><span class="option-label">About</span><span class="option-desc">App version and information</span></div></div>
                    <div class="option-value"><i class="fas fa-chevron-right"></i></div>
                </div>
            </div>
        </div>
    </div>

    <!-- Group Invite Privacy Modal -->
    <div class="settings-modal" id="groupInviteModal">
        <div class="settings-modal-content">
            <div class="settings-header">
                <h2>Group Invite Privacy</h2>
                <button class="close-btn" onclick="closeGroupInviteModal()"><i class="fas fa-times"></i></button>
            </div>
            <div class="settings-section">
                <div class="settings-option" onclick="setGroupInviteSetting('everyone')">
                    <div class="option-info">
                        <i class="fas fa-globe"></i>
                        <div>
                            <span class="option-label">Everyone</span>
                            <span class="option-desc">Anyone can add you to groups</span>
                        </div>
                    </div>
                    <div class="option-value" id="inviteEveryone"><i class="fas fa-check-circle" style="color:#f9a825;"></i></div>
                </div>
                <div class="settings-option" onclick="setGroupInviteSetting('contacts')">
                    <div class="option-info">
                        <i class="fas fa-address-book"></i>
                        <div>
                            <span class="option-label">My Contacts</span>
                            <span class="option-desc">Only people in your contacts</span>
                        </div>
                    </div>
                    <div class="option-value" id="inviteContacts"><i class="fas fa-circle" style="color:var(--text-muted);"></i></div>
                </div>
                <div class="settings-option" onclick="setGroupInviteSetting('none')">
                    <div class="option-info">
                        <i class="fas fa-user-slash"></i>
                        <div>
                            <span class="option-label">Nobody</span>
                            <span class="option-desc">No one can add you to groups</span>
                        </div>
                    </div>
                    <div class="option-value" id="inviteNone"><i class="fas fa-circle" style="color:var(--text-muted);"></i></div>
                </div>
            </div>
        </div>
    </div>

    <!-- Bubble Picker Modal -->
    <div class="bubble-modal" id="bubblePickerModal">
        <div class="bubble-modal-content">
            <div class="settings-header"><h2>Chat Bubble Style</h2><button class="close-btn" onclick="closeBubblePicker()"><i class="fas fa-times"></i></button></div>
            <div class="settings-section"><div class="section-title">Choose a style</div><div class="bubble-style-picker" id="bubbleStylePicker"></div></div>
        </div>
    </div>

    <!-- Sticker Creation Modal -->
    <div class="sticker-modal" id="stickerModal">
        <div class="sticker-modal-content">
            <div class="settings-header"><h2>Create Sticker</h2><button class="close-btn" onclick="closeStickerModal()"><i class="fas fa-times"></i></button></div>
            <div class="sticker-preview" id="stickerPreview">😊</div>
            <div class="emoji-options">
                <span onclick="selectStickerEmoji('😊')">😊</span>
                <span onclick="selectStickerEmoji('😂')">😂</span>
                <span onclick="selectStickerEmoji('❤️')">❤️</span>
                <span onclick="selectStickerEmoji('🔥')">🔥</span>
                <span onclick="selectStickerEmoji('🌟')">🌟</span>
                <span onclick="selectStickerEmoji('💯')">💯</span>
                <span onclick="selectStickerEmoji('🎉')">🎉</span>
                <span onclick="selectStickerEmoji('👍')">👍</span>
            </div>
            <input type="text" class="sticker-name-input" id="stickerName" placeholder="Sticker name (optional)">
            <label class="upload-label" onclick="document.getElementById('stickerFileInput').click()">
                <i class="fas fa-upload"></i> Upload image (PNG, JPG)
            </label>
            <input type="file" id="stickerFileInput" accept="image/*" onchange="handleStickerUpload(this)">
            <button class="save-sticker-btn" onclick="saveSticker()">Save Sticker</button>
        </div>
    </div>

    <!-- Delete Modal -->
    <div class="delete-modal" id="deleteModal">
        <div class="delete-modal-content">
            <div class="icon"><i class="fas fa-exclamation-circle"></i></div>
            <h2>Close Chat?</h2>
            <p>Are you sure you want to close the chat with <strong id="deleteChatName">this user</strong>? This will remove the chat from your list.</p>
            <div class="delete-modal-actions"><button class="cancel-btn" onclick="closeDeleteModal()">Cancel</button><button class="delete-btn" onclick="confirmDeleteChat()">Close Chat</button></div>
        </div>
    </div>

    <!-- Toast -->
    <div class="toast" id="toast"></div>

    <!-- Wallpaper Modal -->
    <div class="wallpaper-modal" id="wallpaperModal">
        <div class="wallpaper-modal-content">
            <h2>Choose Wallpaper</h2>
            <div class="wallpaper-grid">
                <div class="wallpaper-option default-wall selected" onclick="changeWallpaper('default')" data-wall="default"></div>
                <div class="wallpaper-option dark-wall" onclick="changeWallpaper('dark')" data-wall="dark"></div>
                <div class="wallpaper-option beach-wall" onclick="changeWallpaper('beach')" data-wall="beach"></div>
                <div class="wallpaper-option mountain-wall" onclick="changeWallpaper('mountain')" data-wall="mountain"></div>
                <div class="wallpaper-option forest-wall" onclick="changeWallpaper('forest')" data-wall="forest"></div>
                <div class="wallpaper-option city-wall" onclick="changeWallpaper('city')" data-wall="city"></div>
            </div>
            <button class="wallpaper-modal-close" onclick="closeWallpaperPicker()">Close</button>
        </div>
    </div>

    <script>
        // ===== Group Chat Variables =====
        var selectedGroupMembers = [];
        var groupInviteSetting = localStorage.getItem('groupInviteSetting') || 'everyone';

        // ===== Group Modal Functions =====
        function openGroupModal() {{
            document.getElementById('groupModal').classList.add('active');
            document.getElementById('selectedMembers').innerHTML = '';
            selectedGroupMembers = [];
            document.getElementById('groupName').value = '';
            document.getElementById('memberSearch').value = '';
            document.getElementById('searchResults').classList.remove('active');
            updateCreateGroupBtn();
        }}

        function closeGroupModal() {{
            document.getElementById('groupModal').classList.remove('active');
        }}

        function searchMembers(query) {{
            var results = document.getElementById('searchResults');
            if (query.length < 2) {{
                results.classList.remove('active');
                return;
            }}
            // Sample contacts - in real app, fetch from server
            var contacts = [
                {{ name: 'John Doe', id: 10 }},
                {{ name: 'Jane Smith', id: 11 }},
                {{ name: 'Mike Johnson', id: 12 }},
                {{ name: 'Sarah Williams', id: 13 }},
                {{ name: 'David Brown', id: 14 }},
                {{ name: 'Emily Davis', id: 15 }}
            ];
            var filtered = contacts.filter(function(c) {{
                return c.name.toLowerCase().includes(query.toLowerCase()) &&
                    !selectedGroupMembers.some(function(m) {{ return m.id === c.id; }});
            }});
            if (filtered.length === 0) {{
                results.innerHTML = '<div style=\"padding:8px 14px;color:var(--text-muted);font-size:13px;\">No contacts found</div>';
                results.classList.add('active');
                return;
            }}
            var html = '';
            filtered.forEach(function(contact) {{
                html += '<div class=\"result-item\" onclick=\"addMember(' + contact.id + ', \\'' + contact.name + '\\')\">' +
                    '<div class=\"result-avatar\">👤</div>' +
                    '<span class=\"result-name\">' + contact.name + '</span>' +
                    '</div>';
            }});
            results.innerHTML = html;
            results.classList.add('active');
        }}

        function addMember(id, name) {{
            selectedGroupMembers.push({{ id: id, name: name }});
            updateSelectedMembers();
            document.getElementById('memberSearch').value = '';
            document.getElementById('searchResults').classList.remove('active');
            updateCreateGroupBtn();
        }}

        function removeMember(id) {{
            selectedGroupMembers = selectedGroupMembers.filter(function(m) {{ return m.id !== id; }});
            updateSelectedMembers();
            updateCreateGroupBtn();
        }}

        function updateSelectedMembers() {{
            var container = document.getElementById('selectedMembers');
            if (selectedGroupMembers.length === 0) {{
                container.innerHTML = '<span style=\"color:var(--text-muted);font-size:13px;\">No members selected</span>';
                return;
            }}
            var html = '';
            selectedGroupMembers.forEach(function(member) {{
                html += '<div class=\"member-tag\">' +
                    '👤 ' + member.name +
                    ' <button class=\"remove-member\" onclick=\"removeMember(' + member.id + ')\"><i class=\"fas fa-times\"></i></button>' +
                    '</div>';
            }});
            container.innerHTML = html;
        }}

        function updateCreateGroupBtn() {{
            var btn = document.getElementById('createGroupBtn');
            var name = document.getElementById('groupName').value.trim();
            if (name && selectedGroupMembers.length > 0) {{
                btn.disabled = false;
                btn.textContent = 'Create Group (' + (selectedGroupMembers.length + 1) + ' members)';
            }} else {{
                btn.disabled = true;
                btn.textContent = 'Create Group';
            }}
        }}

        document.getElementById('groupName').addEventListener('input', updateCreateGroupBtn);

        function createGroup() {{
            var name = document.getElementById('groupName').value.trim();
            if (!name || selectedGroupMembers.length === 0) return;
            // In real app, send to server
            var memberNames = selectedGroupMembers.map(function(m) {{ return m.name; }}).join(', ');
            var groupItem = document.createElement('div');
            groupItem.className = 'chat-item group-chat';
            groupItem.setAttribute('data-name', name);
            groupItem.setAttribute('data-id', 'group_' + Date.now());
            groupItem.innerHTML = '<div class=\"chat-avatar\"><i class=\"fas fa-users\"></i></div>' +
                '<div class=\"chat-info\">' +
                '<div class=\"chat-name\">' + name + '</div>' +
                '<div class=\"chat-preview\">Group created with ' + memberNames + '</div>' +
                '<div class=\"chat-members\">' + (selectedGroupMembers.length + 1) + ' members</div>' +
                '</div>' +
                '<div class=\"chat-meta\"><div class=\"chat-time\">Just now</div></div>' +
                '<button class=\"chat-close-btn\" onclick=\"event.stopPropagation(); openDeleteModal(\\'' + name + '\\', \\'group_' + Date.now() + '\\')\"><i class=\"fas fa-times\"></i></button>';
            document.getElementById('chatList').appendChild(groupItem);
            showToast('Group "' + name + '" created successfully! 🎉');
            closeGroupModal();
        }}

        // ===== Group Invite Privacy Functions =====
        function openGroupInviteModal() {{
            document.getElementById('groupInviteModal').classList.add('active');
            updateGroupInviteUI();
        }}

        function closeGroupInviteModal() {{
            document.getElementById('groupInviteModal').classList.remove('active');
        }}

        function setGroupInviteSetting(setting) {{
            groupInviteSetting = setting;
            localStorage.setItem('groupInviteSetting', setting);
            updateGroupInviteUI();
            var valueDisplay = document.querySelector('#groupInviteValue span');
            if (valueDisplay) {{
                var labels = {{ 'everyone': 'Everyone', 'contacts': 'My Contacts', 'none': 'Nobody' }};
                valueDisplay.textContent = labels[setting] || 'Everyone';
            }}
            showToast('Group invite setting updated to ' + (labels[setting] || 'Everyone'));
            closeGroupInviteModal();
        }}

        function updateGroupInviteUI() {{
            var options = ['everyone', 'contacts', 'none'];
            options.forEach(function(opt) {{
                var icon = document.getElementById('invite' + opt.charAt(0).toUpperCase() + opt.slice(1));
                if (icon) {{
                    if (opt === groupInviteSetting) {{
                        icon.innerHTML = '<i class=\"fas fa-check-circle\" style=\"color:#f9a825;\"></i>';
                    }} else {{
                        icon.innerHTML = '<i class=\"fas fa-circle\" style=\"color:var(--text-muted);\"></i>';
                    }}
                }}
            }});
        }}

        // Override privacy toggle to include group invite
        var originalTogglePrivacy = togglePrivacy;
        function togglePrivacy(setting) {{
            if (setting === 'group_invite') {{
                openGroupInviteModal();
                return;
            }}
            originalTogglePrivacy(setting);
        }}

        // ===== File Attachment Variables =====
        var selectedFiles = [];

        function handleFileSelect(input) {{
            var files = input.files;
            for (var i = 0; i < files.length; i++) {{
                selectedFiles.push(files[i]);
            }}
            updateFilePreview();
            updateFileBadge();
            input.value = '';
        }}

        function updateFilePreview() {{
            var preview = document.getElementById('filePreview');
            var content = document.getElementById('filePreviewContent');
            if (selectedFiles.length === 0) {{
                preview.classList.remove('active');
                return;
            }}
            preview.classList.add('active');
            content.innerHTML = '';
            selectedFiles.forEach(function(file, index) {{
                var item = document.createElement('div');
                item.className = 'file-item';
                var icon = getFileIcon(file.type);
                var size = formatFileSize(file.size);
                item.innerHTML = `
                    <div class=\"file-icon\">${{icon}}</div>
                    <div class=\"file-info\">
                        <div class=\"file-name\">${{file.name}}</div>
                        <div class=\"file-size\">${{size}}</div>
                    </div>
                    <button class=\"remove-file\" onclick=\"removeFile(${{index}})\"><i class=\"fas fa-times\"></i></button>
                `;
                content.appendChild(item);
            }});
        }}

        function removeFile(index) {{
            selectedFiles.splice(index, 1);
            updateFilePreview();
            updateFileBadge();
            if (selectedFiles.length === 0) {{
                document.getElementById('filePreview').classList.remove('active');
            }}
        }}

        function clearFiles() {{
            selectedFiles = [];
            updateFilePreview();
            updateFileBadge();
            document.getElementById('filePreview').classList.remove('active');
        }}

        function updateFileBadge() {{
            var badge = document.getElementById('fileBadge');
            if (selectedFiles.length > 0) {{
                badge.style.display = 'inline';
                badge.textContent = selectedFiles.length;
            }} else {{
                badge.style.display = 'none';
            }}
        }}

        function getFileIcon(type) {{
            if (type.startsWith('image/')) return '🖼️';
            if (type === 'application/pdf') return '📄';
            if (type.includes('word') || type.includes('doc')) return '📝';
            if (type.includes('excel') || type.includes('sheet')) return '📊';
            if (type.includes('powerpoint') || type.includes('ppt')) return '📽️';
            if (type.includes('zip') || type.includes('rar')) return '📦';
            if (type.includes('audio')) return '🎵';
            if (type.includes('video')) return '🎬';
            return '📎';
        }}

        function formatFileSize(bytes) {{
            if (bytes < 1024) return bytes + ' B';
            if (bytes < 1048576) return (bytes / 1024).toFixed(1) + ' KB';
            return (bytes / 1048576).toFixed(1) + ' MB';
        }}

        // ===== Settings Functions =====
        function openSettings() {{
            document.getElementById('settingsModal').classList.add('active');
            updateSettingsUI();
            updateOpacityUI();
            updateLanguageUI();
            updateGroupInviteUI();
        }}
        function closeSettings() {{ document.getElementById('settingsModal').classList.remove('active'); }}
        
        function updateSettingsUI() {{
            var isDark = document.body.classList.contains('dark-mode');
            var themeStatus = document.getElementById('themeStatus');
            var themeIcon = document.getElementById('themeToggleIcon');
            if (isDark) {{
                themeStatus.querySelector('span').textContent = 'Dark';
                themeIcon.className = 'fas fa-toggle-on';
            }} else {{
                themeStatus.querySelector('span').textContent = 'Light';
                themeIcon.className = 'fas fa-toggle-off';
            }}
            // Update group invite display
            var valueDisplay = document.querySelector('#groupInviteValue span');
            if (valueDisplay) {{
                var labels = {{ 'everyone': 'Everyone', 'contacts': 'My Contacts', 'none': 'Nobody' }};
                valueDisplay.textContent = labels[groupInviteSetting] || 'Everyone';
            }}
        }}

        // ===== Opacity Functions =====
        function updateOpacity(value) {{
            document.getElementById('chatWallpaper').style.opacity = value / 100;
            localStorage.setItem('wallpaperOpacity', value);
            document.getElementById('opacityValue').textContent = value + '%';
        }}
        function updateOpacityUI() {{
            var saved = localStorage.getItem('wallpaperOpacity') || '30';
            document.getElementById('opacitySlider').value = saved;
            document.getElementById('chatWallpaper').style.opacity = saved / 100;
            document.getElementById('opacityValue').textContent = saved + '%';
        }}

        // ===== Language Functions =====
        function changeLanguage(value) {{
            var languages = {{'en':'English','es':'Spanish','fr':'French','de':'German','zh':'Chinese','ja':'Japanese','ar':'Arabic','hi':'Hindi','pt':'Portuguese','ru':'Russian'}};
            localStorage.setItem('appLanguage', value);
            showToast('Language changed to ' + (languages[value] || value));
            // Simple UI translation
            var translations = {{
                'en': {{'Messages':'Messages','Search Message':'Search Message','Pinned':'Pinned','See All':'See All','All Messages':'All Messages','Active Now':'Active Now','Settings':'Settings'}},
                'es': {{'Messages':'Mensajes','Search Message':'Buscar mensaje','Pinned':'Fijados','See All':'Ver todo','All Messages':'Todos los mensajes','Active Now':'Activo ahora','Settings':'Configuración'}},
                'fr': {{'Messages':'Messages','Search Message':'Rechercher','Pinned':'Épinglés','See All':'Voir tout','All Messages':'Tous les messages','Active Now':'Actif maintenant','Settings':'Paramètres'}},
                'de': {{'Messages':'Nachrichten','Search Message':'Nachricht suchen','Pinned':'Angepinnt','See All':'Alle anzeigen','All Messages':'Alle Nachrichten','Active Now':'Aktiv jetzt','Settings':'Einstellungen'}},
                'zh': {{'Messages':'消息','Search Message':'搜索消息','Pinned':'已置顶','See All':'查看全部','All Messages':'所有消息','Active Now':'在线','Settings':'设置'}},
                'ja': {{'Messages':'メッセージ','Search Message':'メッセージを検索','Pinned':'ピン留め','See All':'すべて表示','All Messages':'すべてのメッセージ','Active Now':'オンライン','Settings':'設定'}},
                'ar': {{'Messages':'الرسائل','Search Message':'بحث عن رسالة','Pinned':'مثبت','See All':'عرض الكل','All Messages':'جميع الرسائل','Active Now':'نشط الآن','Settings':'الإعدادات'}},
                'hi': {{'Messages':'संदेश','Search Message':'संदेश खोजें','Pinned':'पिन किया हुआ','See All':'सभी देखें','All Messages':'सभी संदेश','Active Now':'अभी ऑनलाइन','Settings':'सेटिंग्स'}},
                'pt': {{'Messages':'Mensagens','Search Message':'Buscar mensagem','Pinned':'Fixados','See All':'Ver todos','All Messages':'Todas as mensagens','Active Now':'Ativo agora','Settings':'Configurações'}},
                'ru': {{'Messages':'Сообщения','Search Message':'Поиск сообщений','Pinned':'Закрепленные','See All':'Смотреть все','All Messages':'Все сообщения','Active Now':'В сети','Settings':'Настройки'}}
            }};
            var t = translations[value] || translations['en'];
            var headerH1 = document.querySelector('.header h1');
            if (headerH1) headerH1.textContent = t['Messages'] || 'Messages';
            var searchInput = document.querySelector('.search-bar input');
            if (searchInput) searchInput.placeholder = t['Search Message'] || 'Search Message';
            var pinnedHeaders = document.querySelectorAll('.chat-section-header span');
            if (pinnedHeaders.length > 0) pinnedHeaders[0].textContent = t['Pinned'] || 'Pinned';
            if (pinnedHeaders.length > 1) {{
                var seeAlls = document.querySelectorAll('.chat-section-header .see-all');
                if (seeAlls.length > 0) seeAlls[0].textContent = t['See All'] || 'See All';
                if (pinnedHeaders.length > 2) pinnedHeaders[2].textContent = t['All Messages'] || 'All Messages';
                if (seeAlls.length > 1) seeAlls[1].textContent = t['See All'] || 'See All';
            }}
            var statusEl = document.querySelector('.chat-status');
            if (statusEl) statusEl.textContent = t['Active Now'] || 'Active Now';
            var settingsTitle = document.querySelector('.settings-header h2');
            if (settingsTitle) settingsTitle.textContent = t['Settings'] || 'Settings';
        }}
        function updateLanguageUI() {{
            var saved = localStorage.getItem('appLanguage') || 'en';
            document.getElementById('languageDropdown').value = saved;
        }}

        // ===== Bubble Style Functions =====
        var bubbleStyles = [
            {{ id: 'style-1', name: 'Default', class: 'bubble-style-1' }},
            {{ id: 'style-2', name: 'Modern', class: 'bubble-style-2' }},
            {{ id: 'style-3', name: 'Green', class: 'bubble-style-3' }},
            {{ id: 'style-4', name: 'Red', class: 'bubble-style-4' }},
            {{ id: 'style-5', name: 'Gradient', class: 'bubble-style-5' }}
        ];
        var currentBubbleStyle = localStorage.getItem('bubbleStyle') || 'style-1';

        function openBubblePicker() {{
            var picker = document.getElementById('bubbleStylePicker');
            picker.innerHTML = '';
            bubbleStyles.forEach(function(style) {{
                var div = document.createElement('div');
                div.className = 'bubble-style-option' + (style.id === currentBubbleStyle ? ' active' : '');
                div.setAttribute('data-style', style.id);
                div.innerHTML = '<div style=\"display:flex;flex-direction:column;align-items:center;gap:4px;width:100%;\"><div class=\"bubble-preview-own\" style=\"font-size:8px;padding:2px 6px;\">Hi</div><div class=\"bubble-preview-other\" style=\"font-size:8px;padding:2px 6px;\">Hey</div></div>';
                div.onclick = function() {{ selectBubbleStyle(style.id); }};
                picker.appendChild(div);
            }});
            document.getElementById('bubblePickerModal').classList.add('active');
        }}
        function closeBubblePicker() {{ document.getElementById('bubblePickerModal').classList.remove('active'); }}
        function selectBubbleStyle(styleId) {{
            var chatMessages = document.getElementById('chatMessages');
            bubbleStyles.forEach(function(s) {{ chatMessages.classList.remove(s.class); }});
            var selected = bubbleStyles.find(function(s) {{ return s.id === styleId; }});
            if (selected) chatMessages.classList.add(selected.class);
            currentBubbleStyle = styleId;
            localStorage.setItem('bubbleStyle', styleId);
            document.querySelectorAll('.bubble-style-option').forEach(function(el) {{
                el.classList.remove('active');
                if (el.getAttribute('data-style') === styleId) el.classList.add('active');
            }});
            document.getElementById('currentBubbleLabel').textContent = selected ? selected.name : 'Default';
            closeBubblePicker();
            showToast('Bubble style updated to ' + (selected ? selected.name : 'Default'));
        }}
        function loadBubbleStyle() {{
            var saved = localStorage.getItem('bubbleStyle') || 'style-1';
            var style = bubbleStyles.find(function(s) {{ return s.id === saved; }});
            if (style) {{ document.getElementById('chatMessages').classList.add(style.class); currentBubbleStyle = saved; }}
        }}

        // ===== Privacy Functions =====
        var privacySettings = {{ online: true, read: true, typing: true }};
        function togglePrivacy(setting) {{
            if (setting === 'group_invite') {{
                openGroupInviteModal();
                return;
            }}
            privacySettings[setting] = !privacySettings[setting];
            var status = document.getElementById('privacy' + setting.charAt(0).toUpperCase() + setting.slice(1));
            var icon = document.getElementById('privacy' + setting.charAt(0).toUpperCase() + setting.slice(1) + 'Icon');
            if (privacySettings[setting]) {{
                status.textContent = 'On';
                icon.className = 'fas fa-toggle-on';
            }} else {{
                status.textContent = 'Off';
                icon.className = 'fas fa-toggle-off';
            }}
            showToast(setting.charAt(0).toUpperCase() + setting.slice(1) + ' ' + (privacySettings[setting] ? 'enabled' : 'disabled'));
        }}

        // ===== Update Functions =====
        function checkUpdates() {{
            var status = document.getElementById('updateStatus');
            status.textContent = 'Checking...';
            setTimeout(function() {{ status.textContent = 'v1.0.0 (Latest)'; showToast('✓ App is up to date!'); }}, 1500);
        }}
        function showAppInfo() {{ showToast('Camly v1.0.0 | © 2026 Camly Community Platform'); }}

        // ===== Theme Toggle =====
        function toggleTheme() {{
            var body = document.body;
            var icon = document.getElementById('themeIcon');
            body.classList.toggle('dark-mode');
            if (body.classList.contains('dark-mode')) {{
                icon.className = 'fas fa-sun';
                localStorage.setItem('theme', 'dark');
            }} else {{
                icon.className = 'fas fa-moon';
                localStorage.setItem('theme', 'light');
            }}
            updateSettingsUI();
            updateOpacityUI();
        }}

        // ===== Wallpaper Functions =====
        var wallpapers = {{
            'default': 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800',
            'dark': 'https://images.unsplash.com/photo-1519681393784-d120267933ba?w=800',
            'beach': 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800',
            'mountain': 'https://images.unsplash.com/photo-1519681393784-d120267933ba?w=800',
            'forest': 'https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=800',
            'city': 'https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?w=800'
        }};
        function changeWallpaper(name) {{
            var wallpaperEl = document.getElementById('chatWallpaper');
            var url = wallpapers[name];
            if (url) {{
                wallpaperEl.style.backgroundImage = 'url(' + url + ')';
                localStorage.setItem('chatWallpaper', name);
                document.querySelectorAll('.wallpaper-option').forEach(function(el) {{ el.classList.remove('selected'); }});
                var selected = document.querySelector('.wallpaper-option[data-wall=\"' + name + '\"]');
                if (selected) selected.classList.add('selected');
                showToast('Wallpaper updated');
            }}
        }}
        function openWallpaperPicker() {{ document.getElementById('wallpaperModal').classList.add('active'); }}
        function closeWallpaperPicker() {{ document.getElementById('wallpaperModal').classList.remove('active'); }}

        // ===== Close Chat Div =====
        function closeChatDiv() {{ document.getElementById('chatMain').classList.add('hidden'); showToast('Chat closed'); }}

        // ===== Delete Functions =====
        var deleteTarget = null;
        function openDeleteModal(name, id) {{
            deleteTarget = {{ name: name, id: id }};
            document.getElementById('deleteChatName').textContent = name;
            document.getElementById('deleteModal').classList.add('active');
        }}
        function closeDeleteModal() {{ document.getElementById('deleteModal').classList.remove('active'); deleteTarget = null; }}
        function confirmDeleteChat() {{
            if (deleteTarget) {{
                var chatItems = document.querySelectorAll('.chat-item');
                chatItems.forEach(function(item) {{
                    if (item.getAttribute('data-id') == deleteTarget.id) {{
                        item.style.transition = 'all 0.3s ease';
                        item.style.opacity = '0';
                        item.style.transform = 'translateX(50px)';
                        setTimeout(function() {{
                            item.remove();
                            showToast('Chat with ' + deleteTarget.name + ' closed');
                            if (document.querySelectorAll('.chat-item').length === 0) {{
                                document.getElementById('chatMain').classList.add('hidden');
                            }}
                        }}, 300);
                    }}
                }});
                closeDeleteModal();
            }}
        }}

        // ===== Toast Function =====
        function showToast(message) {{
            var toast = document.getElementById('toast');
            toast.textContent = message;
            toast.classList.add('show');
            setTimeout(function() {{ toast.classList.remove('show'); }}, 3000);
        }}

        // ===== Search Function =====
        document.getElementById('searchInput').addEventListener('input', function(e) {{
            var query = e.target.value.toLowerCase();
            document.querySelectorAll('.chat-item').forEach(function(chat) {{
                var text = chat.getAttribute('data-name') ? chat.getAttribute('data-name').toLowerCase() : '';
                chat.style.display = text.includes(query) ? 'flex' : 'none';
            }});
            document.querySelectorAll('.chat-section-header').forEach(function(section) {{
                var hasVisible = false;
                var sibling = section.nextElementSibling;
                while (sibling && sibling.classList.contains('chat-item')) {{
                    if (sibling.style.display !== 'none') {{ hasVisible = true; break; }}
                    sibling = sibling.nextElementSibling;
                }}
                section.style.display = hasVisible ? 'flex' : 'none';
            }});
        }});

        // ===== Send Message with Files =====
        function sendMessage() {{
            var input = document.getElementById('messageInput');
            var message = input.value.trim();
            
            if (!message && selectedFiles.length === 0) {{
                return;
            }}
            
            var messages = document.getElementById('chatMessages');
            
            if (message) {{
                var messageDiv = document.createElement('div');
                messageDiv.className = 'message own';
                var now = new Date();
                var time = now.getHours().toString().padStart(2, '0') + ':' + now.getMinutes().toString().padStart(2, '0');
                messageDiv.innerHTML = message.replace(/\\n/g, '<br>') + '<span class=\"message-time\">' + time + '</span>';
                messages.appendChild(messageDiv);
                input.value = '';
            }}
            
            selectedFiles.forEach(function(file) {{
                var reader = new FileReader();
                reader.onload = function(e) {{
                    var messageDiv = document.createElement('div');
                    var now = new Date();
                    var time = now.getHours().toString().padStart(2, '0') + ':' + now.getMinutes().toString().padStart(2, '0');
                    
                    if (file.type.startsWith('image/')) {{
                        messageDiv.className = 'message image-message';
                        messageDiv.innerHTML = '<img src=\"' + e.target.result + '\" alt=\"' + file.name + '\"><span class=\"message-time\">' + time + '</span>';
                    }} else {{
                        var icon = getFileIcon(file.type);
                        var size = formatFileSize(file.size);
                        messageDiv.className = 'message file';
                        messageDiv.innerHTML = `
                            <div style=\"display:flex;align-items:center;gap:8px;\">
                                <span class=\"file-icon\">${{icon}}</span>
                                <div>
                                    <div class=\"file-name\">${{file.name}}</div>
                                    <div class=\"file-size\">${{size}}</div>
                                </div>
                            </div>
                            <span class=\"message-time\">${{time}}</span>
                        `;
                    }}
                    messages.appendChild(messageDiv);
                    messages.scrollTop = messages.scrollHeight;
                }};
                reader.readAsDataURL(file);
            }});
            
            clearFiles();
            messages.scrollTop = messages.scrollHeight;
            closeEmojiPicker();
        }}
        
        document.getElementById('messageInput').addEventListener('keypress', function(e) {{ if (e.key === 'Enter' && !e.shiftKey) {{ e.preventDefault(); sendMessage(); }} }});

        // ===== Active Chat Highlight =====
        document.querySelectorAll('.chat-item').forEach(function(item) {{
            item.addEventListener('click', function(e) {{
                if (e.target.closest('.chat-close-btn')) return;
                document.querySelectorAll('.chat-item').forEach(function(i) {{ i.classList.remove('active'); }});
                this.classList.add('active');
                document.getElementById('chatMain').classList.remove('hidden');
                document.getElementById('chatMessages').scrollTop = document.getElementById('chatMessages').scrollHeight;
            }});
        }});

        // ===== Close Modals on Outside Click =====
        ['deleteModal', 'wallpaperModal', 'settingsModal', 'bubblePickerModal', 'stickerModal', 'groupModal', 'groupInviteModal'].forEach(function(id) {{
            document.getElementById(id).addEventListener('click', function(e) {{
                if (e.target === this) {{
                    if (id === 'deleteModal') closeDeleteModal();
                    else if (id === 'wallpaperModal') closeWallpaperPicker();
                    else if (id === 'settingsModal') closeSettings();
                    else if (id === 'bubblePickerModal') closeBubblePicker();
                    else if (id === 'stickerModal') closeStickerModal();
                    else if (id === 'groupModal') closeGroupModal();
                    else if (id === 'groupInviteModal') closeGroupInviteModal();
                }}
            }});
        }});

        // Close emoji picker on outside click
        document.addEventListener('click', function(e) {{
            var picker = document.getElementById('emojiPicker');
            var btn = document.querySelector('.emoji-toggle-btn');
            if (picker.classList.contains('active') && !picker.contains(e.target) && !btn.contains(e.target)) {{
                closeEmojiPicker();
            }}
            var filePreview = document.getElementById('filePreview');
            var attachBtn = document.getElementById('attachBtn');
            if (filePreview.classList.contains('active') && !filePreview.contains(e.target) && !attachBtn.contains(e.target)) {{
                // Don't close file preview on click outside
            }}
        }});

        // ===== Emoji & Sticker Data =====
        var emojis = ['😀','😁','😂','🤣','😃','😄','😅','😆','😉','😊','😋','😎','😍','🥰','😘','😗','😙','😚','☺️','🙂','🤗','🤩','🤔','🤨','😐','😑','😶','🙄','😏','😣','😥','😮','🤐','😯','😪','😫','😴','😌','😛','😜','😝','🤤','😒','😓','😔','😕','🙃','🤑','😲','☹️','🙁','😖','😞','😟','😤','😢','😭','😦','😧','😨','😩','🤯','😬','😰','😱','🥵','🥶','😳','🤪','😵','🥴','😠','😡','🤬','😷','🤒','🤕','🤢','🤮','🤧','😇','🤠','🤡','🥳','🥺','🤥','🤫','🤭','🧐','🤓','😈','👿','👹','👺','💀','☠️','👋','🤚','🖐️','✋','🖖','👌','🤌','🤏','✌️','🤞','🤟','🤘','👈','👉','👆','🖕','👇','☝️','👍','👎','👊','✊','🤛','🤜','👏','🙌','👐','🤲','🤝','🙏','✍️','💅','🤳','💪'];
        
        var stickerPacks = [
            {{ name: 'Popular', stickers: ['😊','😂','❤️','🔥','🌟','💯','🎉','👍'] }},
            {{ name: 'Animals', stickers: ['🐶','🐱','🐭','🐹','🐰','🦊','🐻','🐼'] }},
            {{ name: 'Food', stickers: ['🍕','🍔','🍟','🌭','🍿','🧁','🍩','🍪'] }},
            {{ name: 'Activities', stickers: ['⚽','🏀','🎮','🎵','🎶','🎨','🏃','🏊'] }}
        ];
        
        var customStickers = JSON.parse(localStorage.getItem('customStickers') || '[]');
        var stickerPreviewValue = '😊';
        var stickerFileData = null;

        // ===== Emoji Picker Functions =====
        function toggleEmojiPicker() {{
            var picker = document.getElementById('emojiPicker');
            var btn = document.querySelector('.emoji-toggle-btn');
            picker.classList.toggle('active');
            btn.classList.toggle('active');
            if (picker.classList.contains('active')) {{
                switchEmojiTab('emoji', document.querySelector('.emoji-picker-header button.active'));
            }}
        }}

        function switchEmojiTab(tab, btn) {{
            document.querySelectorAll('.emoji-picker-header button').forEach(function(b) {{ b.classList.remove('active'); }});
            btn.classList.add('active');
            var content = document.getElementById('emojiContent');
            content.innerHTML = '';
            
            if (tab === 'emoji') {{
                var grid = document.createElement('div');
                grid.className = 'emoji-grid';
                emojis.forEach(function(emoji) {{
                    var span = document.createElement('span');
                    span.className = 'emoji';
                    span.textContent = emoji;
                    span.onclick = function() {{ insertEmoji(emoji); }};
                    grid.appendChild(span);
                }});
                content.appendChild(grid);
            }} else if (tab === 'stickers') {{
                var grid = document.createElement('div');
                grid.className = 'sticker-grid';
                stickerPacks.forEach(function(pack) {{
                    var header = document.createElement('div');
                    header.style.cssText = 'grid-column: 1 / -1; font-weight: 600; color: var(--text-secondary); padding: 8px 0; font-size: 13px;';
                    header.textContent = pack.name;
                    grid.appendChild(header);
                    pack.stickers.forEach(function(sticker) {{
                        var div = document.createElement('div');
                        div.className = 'sticker';
                        var span = document.createElement('span');
                        span.className = 'emoji-sticker';
                        span.textContent = sticker;
                        div.appendChild(span);
                        div.onclick = function() {{ insertEmoji(sticker); }};
                        grid.appendChild(div);
                    }});
                }});
                if (customStickers.length > 0) {{
                    var header = document.createElement('div');
                    header.style.cssText = 'grid-column: 1 / -1; font-weight: 600; color: var(--text-secondary); padding: 8px 0; font-size: 13px;';
                    header.textContent = '✨ Custom';
                    grid.appendChild(header);
                    customStickers.forEach(function(sticker) {{
                        var div = document.createElement('div');
                        div.className = 'sticker';
                        if (sticker.type === 'emoji') {{
                            var span = document.createElement('span');
                            span.className = 'emoji-sticker';
                            span.textContent = sticker.value;
                            div.appendChild(span);
                        }} else {{
                            var img = document.createElement('img');
                            img.src = sticker.value;
                            img.alt = sticker.name || 'Sticker';
                            div.appendChild(img);
                        }}
                        div.onclick = function() {{ insertSticker(sticker); }};
                        grid.appendChild(div);
                    }});
                }}
                var createBtn = document.createElement('button');
                createBtn.className = 'create-sticker-btn';
                createBtn.textContent = '➕ Create New Sticker';
                createBtn.onclick = function() {{ closeEmojiPicker(); openStickerModal(); }};
                content.appendChild(createBtn);
                content.appendChild(grid);
            }} else if (tab === 'custom') {{
                var container = document.createElement('div');
                if (customStickers.length === 0) {{
                    var empty = document.createElement('p');
                    empty.style.cssText = 'text-align: center; color: var(--text-muted); padding: 20px;';
                    empty.textContent = 'No custom stickers yet. Create your first sticker!';
                    container.appendChild(empty);
                }} else {{
                    var grid = document.createElement('div');
                    grid.className = 'sticker-grid';
                    customStickers.forEach(function(sticker) {{
                        var div = document.createElement('div');
                        div.className = 'sticker';
                        if (sticker.type === 'emoji') {{
                            var span = document.createElement('span');
                            span.className = 'emoji-sticker';
                            span.textContent = sticker.value;
                            div.appendChild(span);
                        }} else {{
                            var img = document.createElement('img');
                            img.src = sticker.value;
                            img.alt = sticker.name || 'Sticker';
                            div.appendChild(img);
                        }}
                        div.onclick = function() {{ insertSticker(sticker); }};
                        grid.appendChild(div);
                    }});
                    container.appendChild(grid);
                }}
                var createBtn = document.createElement('button');
                createBtn.className = 'create-sticker-btn';
                createBtn.textContent = '➕ Create New Sticker';
                createBtn.onclick = function() {{ closeEmojiPicker(); openStickerModal(); }};
                container.appendChild(createBtn);
                content.appendChild(container);
            }}
        }}

        function insertEmoji(emoji) {{
            var input = document.getElementById('messageInput');
            input.value += emoji;
            input.focus();
            closeEmojiPicker();
        }}

        function insertSticker(sticker) {{
            var messages = document.getElementById('chatMessages');
            var messageDiv = document.createElement('div');
            messageDiv.className = 'message sticker';
            if (sticker.type === 'emoji') {{
                messageDiv.innerHTML = '<span style=\"font-size:64px;display:block;\">' + sticker.value + '</span>';
            }} else {{
                messageDiv.innerHTML = '<img src=\"' + sticker.value + '\" alt=\"' + (sticker.name || 'Sticker') + '\">';
            }}
            var now = new Date();
            var time = now.getHours().toString().padStart(2, '0') + ':' + now.getMinutes().toString().padStart(2, '0');
            var timeSpan = document.createElement('span');
            timeSpan.className = 'message-time';
            timeSpan.textContent = time;
            messageDiv.appendChild(timeSpan);
            messages.appendChild(messageDiv);
            messages.scrollTop = messages.scrollHeight;
            closeEmojiPicker();
        }}

        function closeEmojiPicker() {{
            document.getElementById('emojiPicker').classList.remove('active');
            document.querySelector('.emoji-toggle-btn').classList.remove('active');
        }}

        // ===== Sticker Creation Functions =====
        function openStickerModal() {{
            document.getElementById('stickerModal').classList.add('active');
        }}

        function closeStickerModal() {{
            document.getElementById('stickerModal').classList.remove('active');
            stickerFileData = null;
            document.getElementById('stickerFileInput').value = '';
        }}

        function selectStickerEmoji(emoji) {{
            stickerPreviewValue = emoji;
            document.getElementById('stickerPreview').textContent = emoji;
            document.getElementById('stickerPreview').style.fontSize = '48px';
            stickerFileData = null;
        }}

        function handleStickerUpload(input) {{
            var file = input.files[0];
            if (file) {{
                var reader = new FileReader();
                reader.onload = function(e) {{
                    stickerFileData = e.target.result;
                    document.getElementById('stickerPreview').innerHTML = '<img src=\"' + e.target.result + '\" style=\"width:100px;height:100px;object-fit:contain;\">';
                }};
                reader.readAsDataURL(file);
            }}
        }}

        function saveSticker() {{
            var name = document.getElementById('stickerName').value.trim() || 'Custom Sticker';
            var sticker;
            if (stickerFileData) {{
                sticker = {{ type: 'image', value: stickerFileData, name: name }};
            }} else {{
                sticker = {{ type: 'emoji', value: stickerPreviewValue, name: name }};
            }}
            customStickers.push(sticker);
            localStorage.setItem('customStickers', JSON.stringify(customStickers));
            showToast('Sticker created successfully! 🎉');
            closeStickerModal();
        }}

        // ===== Initialize =====
        document.addEventListener('DOMContentLoaded', function() {{
            var savedTheme = localStorage.getItem('theme');
            var icon = document.getElementById('themeIcon');
            if (savedTheme === 'dark') {{
                document.body.classList.add('dark-mode');
                icon.className = 'fas fa-sun';
            }}
            var savedWallpaper = localStorage.getItem('chatWallpaper') || 'default';
            changeWallpaper(savedWallpaper);
            loadBubbleStyle();
            updateOpacityUI();
            updateLanguageUI();
            updateGroupInviteUI();
            switchEmojiTab('emoji', document.querySelector('.emoji-picker-header button'));
            document.getElementById('chatMessages').scrollTop = document.getElementById('chatMessages').scrollHeight;
            updateCreateGroupBtn();
        }});
    </script>
</body>
</html>
"""
    return HttpResponse(html)

@login_required
def chat_detail(request, chat_id):
    username = request.user.username
    chat_names = {
        1: 'Shanti Thapa', 2: 'Santosh Limbu', 3: 'Kala Shrestha',
        4: 'Camping Team', 5: 'Riya Shrestha', 6: 'Punam Limbu',
        7: 'Mausam Kafle', 8: 'Basketball Team', 9: 'Office Buddies'
    }
    chat_name = chat_names.get(chat_id, 'Unknown')
    
    html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Camly - Chat with {chat_name}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        /* Same styles as chat_home */
        :root {{
            --bg-primary: #f5f5f5;
            --bg-secondary: #ffffff;
            --bg-chat-own: #f9a825;
            --bg-chat-other: #f0f0f5;
            --text-primary: #1a1a2e;
            --text-secondary: #6b6b7a;
            --text-muted: #9999a8;
            --border-color: #e8e8ef;
            --input-bg: #f0f0f5;
            --online-color: #2ecc71;
            --status-bar-bg: #f8f8f8;
            --wallpaper-url: url('https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800');
            --wallpaper-opacity: 0.3;
        }}
        .dark-mode {{
            --bg-primary: #0a0a2e;
            --bg-secondary: #12123a;
            --bg-chat-own: #f9a825;
            --bg-chat-other: #2a2a5a;
            --text-primary: #f0f0ff;
            --text-secondary: #a8a8c8;
            --text-muted: #6a6a8a;
            --border-color: #2a2a5a;
            --input-bg: #2a2a5a;
            --status-bar-bg: #0a0a2e;
            --wallpaper-url: url('https://images.unsplash.com/photo-1519681393784-d120267933ba?w=800');
        }}
        * {{ margin:0; padding:0; box-sizing:border-box; }}
        body {{ font-family: -apple-system, sans-serif; background: var(--bg-primary); color: var(--text-primary); height: 100vh; display: flex; flex-direction: column; transition: background 0.3s, color 0.3s; }}
        .status-bar {{ display: flex; justify-content: space-between; padding: 4px 20px; font-size: 12px; color: var(--text-secondary); background: var(--status-bar-bg); border-bottom: 1px solid var(--border-color); flex-shrink: 0; }}
        .header {{ display: flex; justify-content: space-between; align-items: center; padding: 10px 20px; background: var(--bg-secondary); border-bottom: 1px solid var(--border-color); flex-shrink: 0; }}
        .header-left {{ display: flex; align-items: center; gap: 12px; }}
        .back-btn {{ background: none; border: none; color: var(--text-primary); font-size: 20px; cursor: pointer; padding: 4px; }}
        .chat-user-info {{ display: flex; flex-direction: column; }}
        .chat-user-info .chat-name {{ font-weight: 600; font-size: 16px; color: var(--text-primary); }}
        .chat-user-info .chat-status {{ font-size: 11px; color: var(--text-muted); display: flex; align-items: center; gap: 4px; }}
        .online-dot {{ width: 6px; height: 6px; border-radius: 50%; background: var(--online-color); display: inline-block; animation: pulse 2s infinite; }}
        @keyframes pulse {{ 0%,100% {{ opacity:1; }} 50% {{ opacity:0.4; }} }}
        .header-actions {{ display: flex; gap: 16px; align-items: center; }}
        .header-actions button {{ background: none; border: none; color: var(--text-secondary); font-size: 18px; cursor: pointer; padding: 4px; }}
        .theme-toggle-btn {{ background: none; border: none; color: var(--text-secondary); font-size: 18px; cursor: pointer; padding: 4px 8px; border-radius: 8px; }}
        .theme-toggle-btn:hover {{ background: var(--input-bg); color: var(--text-primary); }}
        .chat-main {{ flex: 1; display: flex; flex-direction: column; background: var(--bg-primary); min-width: 0; position: relative; }}
        .chat-wallpaper {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; background-image: var(--wallpaper-url); background-size: cover; background-position: center; opacity: var(--wallpaper-opacity); z-index: 0; transition: opacity 0.3s ease; }}
        .dark-mode .chat-wallpaper {{ opacity: calc(var(--wallpaper-opacity) * 0.5); }}
        .chat-messages {{ flex: 1; overflow-y: auto; padding: 16px 20px; display: flex; flex-direction: column; gap: 8px; position: relative; z-index: 1; }}
        .bubble-style-1 .message.own {{ background: var(--bg-chat-own); color: var(--text-chat-own); border-bottom-right-radius: 4px; }}
        .bubble-style-1 .message.other {{ background: var(--bg-chat-other); color: var(--text-chat-other); border-bottom-left-radius: 4px; }}
        .bubble-style-2 .message.own {{ background: #4a90d9; color: #fff; border-radius: 20px 20px 4px 20px; }}
        .bubble-style-2 .message.other {{ background: #e8e8ef; color: #1a1a2e; border-radius: 20px 20px 20px 4px; }}
        .dark-mode .bubble-style-2 .message.other {{ background: #2a2a5a; color: #f0f0ff; }}
        .bubble-style-3 .message.own {{ background: #2ecc71; color: #fff; border-radius: 16px 16px 4px 16px; }}
        .bubble-style-3 .message.other {{ background: #f0f0f5; color: #1a1a2e; border-radius: 16px 16px 16px 4px; }}
        .dark-mode .bubble-style-3 .message.other {{ background: #2a2a5a; color: #f0f0ff; }}
        .bubble-style-4 .message.own {{ background: #e74c3c; color: #fff; border-radius: 24px 24px 4px 24px; }}
        .bubble-style-4 .message.other {{ background: #f0f0f5; color: #1a1a2e; border-radius: 24px 24px 24px 4px; }}
        .dark-mode .bubble-style-4 .message.other {{ background: #2a2a5a; color: #f0f0ff; }}
        .bubble-style-5 .message.own {{ background: linear-gradient(135deg, #f9a825, #ff6f00); color: #fff; border-radius: 20px 4px 20px 4px; }}
        .bubble-style-5 .message.other {{ background: linear-gradient(135deg, #f0f0f5, #e8e8ef); color: #1a1a2e; border-radius: 4px 20px 4px 20px; }}
        .dark-mode .bubble-style-5 .message.other {{ background: linear-gradient(135deg, #2a2a5a, #1a1a4e); color: #f0f0ff; }}
        .message {{ max-width: 70%; padding: 10px 14px; border-radius: 14px; font-size: 14px; line-height: 1.5; word-wrap: break-word; animation: messageIn 0.3s ease-out; }}
        @keyframes messageIn {{ from {{ opacity:0; transform:translateY(10px); }} to {{ opacity:1; transform:translateY(0); }} }}
        .message.own {{ align-self: flex-end; }}
        .message.other {{ align-self: flex-start; }}
        .message .message-time {{ font-size: 10px; opacity: 0.6; margin-top: 4px; display: block; text-align: right; }}
        .message.sticker {{ padding: 4px; max-width: 200px; background: none !important; }}
        .message.sticker img {{ width: 100%; height: auto; border-radius: 12px; }}
        .message.file {{ padding: 8px 12px; background: var(--bg-secondary) !important; border: 1px solid var(--border-color); border-radius: 12px; max-width: 280px; }}
        .message.file .file-icon {{ font-size: 32px; margin-right: 8px; }}
        .message.file .file-name {{ font-weight: 500; font-size: 13px; }}
        .message.file .file-size {{ font-size: 11px; color: var(--text-muted); }}
        .message.image-message {{ padding: 4px; max-width: 300px; background: none !important; }}
        .message.image-message img {{ width: 100%; height: auto; border-radius: 12px; max-height: 300px; object-fit: contain; }}
        .chat-input-area {{ display: flex; align-items: center; gap: 10px; padding: 10px 16px; background: var(--bg-secondary); border-top: 1px solid var(--border-color); flex-shrink: 0; position: relative; z-index: 1; }}
        .chat-input-area input {{ flex: 1; padding: 10px 16px; background: var(--input-bg); border: none; border-radius: 20px; color: var(--text-primary); font-size: 14px; outline: none; }}
        .chat-input-area input:focus {{ box-shadow: 0 0 0 2px rgba(249,168,37,0.15); }}
        .chat-input-area input::placeholder {{ color: var(--text-muted); }}
        .chat-input-area .input-actions {{ display: flex; gap: 4px; align-items: center; }}
        .chat-input-area .input-actions button {{ background: none; border: none; color: var(--text-secondary); font-size: 18px; cursor: pointer; padding: 6px; border-radius: 50%; width: 36px; height: 36px; display: flex; align-items: center; justify-content: center; position: relative; }}
        .chat-input-area .input-actions button:hover {{ background: var(--input-bg); color: var(--text-primary); }}
        .chat-input-area .input-actions button .badge {{ position: absolute; top: 0; right: 0; background: #e74c3c; color: white; font-size: 9px; padding: 1px 5px; border-radius: 50%; }}
        .send-btn {{ width: 40px; height: 40px; border-radius: 50%; background: #f9a825; border: none; color: #fff; font-size: 16px; cursor: pointer; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }}
        .send-btn:hover {{ transform: scale(1.05); box-shadow: 0 4px 16px rgba(249,168,37,0.3); }}
        .file-preview {{ display: none; position: absolute; bottom: 70px; left: 16px; right: 16px; max-height: 200px; background: var(--bg-secondary); border-radius: 16px; border: 1px solid var(--border-color); box-shadow: 0 8px 30px rgba(0,0,0,0.2); z-index: 999; padding: 16px; overflow-y: auto; }}
        .file-preview.active {{ display: block; }}
        .file-preview .file-item {{ display: flex; align-items: center; gap: 12px; padding: 8px; border-radius: 8px; background: var(--input-bg); margin-bottom: 8px; }}
        .file-preview .file-item .file-icon {{ font-size: 28px; }}
        .file-preview .file-item .file-info {{ flex: 1; }}
        .file-preview .file-item .file-info .file-name {{ font-size: 13px; font-weight: 500; }}
        .file-preview .file-item .file-info .file-size {{ font-size: 11px; color: var(--text-muted); }}
        .file-preview .file-item .remove-file {{ background: none; border: none; color: var(--text-muted); cursor: pointer; padding: 4px 8px; }}
        .file-preview .file-item .remove-file:hover {{ color: #e74c3c; }}
        .emoji-picker {{ display: none; position: absolute; bottom: 70px; left: 16px; right: 16px; max-height: 350px; background: var(--bg-secondary); border-radius: 16px; border: 1px solid var(--border-color); box-shadow: 0 8px 30px rgba(0,0,0,0.2); z-index: 1000; overflow: hidden; flex-direction: column; }}
        .emoji-picker.active {{ display: flex; }}
        .emoji-picker-header {{ display: flex; border-bottom: 1px solid var(--border-color); flex-shrink: 0; }}
        .emoji-picker-header button {{ flex: 1; padding: 10px; background: none; border: none; border-bottom: 3px solid transparent; cursor: pointer; color: var(--text-muted); font-size: 14px; font-weight: 500; transition: all 0.3s; }}
        .emoji-picker-header button.active {{ border-bottom-color: #f9a825; color: var(--text-primary); }}
        .emoji-picker-content {{ overflow-y: auto; padding: 12px; flex: 1; }}
        .emoji-grid {{ display: grid; grid-template-columns: repeat(8, 1fr); gap: 4px; }}
        .emoji-grid .emoji {{ font-size: 28px; text-align: center; padding: 6px; cursor: pointer; border-radius: 8px; transition: all 0.2s; }}
        .emoji-grid .emoji:hover {{ background: var(--input-bg); transform: scale(1.1); }}
        .sticker-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; }}
        .sticker-grid .sticker {{ padding: 4px; cursor: pointer; border-radius: 8px; transition: all 0.2s; text-align: center; }}
        .sticker-grid .sticker:hover {{ background: var(--input-bg); transform: scale(1.05); }}
        .sticker-grid .sticker img {{ width: 100%; height: auto; border-radius: 8px; }}
        .sticker-grid .sticker .emoji-sticker {{ font-size: 48px; display: block; padding: 8px; }}
        .create-sticker-btn {{ padding: 12px; background: #f9a825; color: white; border: none; border-radius: 8px; cursor: pointer; font-weight: 600; margin-top: 8px; width: 100%; }}
        .create-sticker-btn:hover {{ background: #ff6f00; }}
        .sticker-modal {{ display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.7); z-index: 2000; align-items: center; justify-content: center; }}
        .sticker-modal.active {{ display: flex; }}
        .sticker-modal-content {{ background: var(--bg-secondary); border-radius: 20px; padding: 24px; max-width: 500px; width: 90%; max-height: 80vh; overflow-y: auto; }}
        .sticker-modal-content .sticker-preview {{ width: 100px; height: 100px; border-radius: 12px; border: 2px dashed var(--border-color); display: flex; align-items: center; justify-content: center; margin: 12px auto; font-size: 48px; background: var(--input-bg); }}
        .sticker-modal-content input[type="file"] {{ display: none; }}
        .sticker-modal-content .upload-label {{ display: block; padding: 10px; background: var(--input-bg); border-radius: 8px; cursor: pointer; text-align: center; color: var(--text-secondary); font-size: 14px; }}
        .sticker-modal-content .upload-label:hover {{ background: var(--border-color); }}
        .sticker-modal-content .emoji-options {{ display: flex; gap: 8px; flex-wrap: wrap; justify-content: center; margin: 12px 0; }}
        .sticker-modal-content .emoji-options span {{ font-size: 32px; cursor: pointer; padding: 4px 8px; border-radius: 8px; transition: all 0.2s; }}
        .sticker-modal-content .emoji-options span:hover {{ background: var(--input-bg); transform: scale(1.2); }}
        .sticker-modal-content .sticker-name-input {{ width: 100%; padding: 10px; border: 1px solid var(--border-color); border-radius: 8px; background: var(--input-bg); color: var(--text-primary); font-size: 14px; margin: 8px 0; }}
        .sticker-modal-content .save-sticker-btn {{ padding: 10px 24px; background: #f9a825; color: white; border: none; border-radius: 8px; cursor: pointer; font-weight: 600; width: 100%; }}
        .sticker-modal-content .save-sticker-btn:hover {{ background: #ff6f00; }}
        @media (max-width: 480px) {{ .header {{ padding: 8px 12px; }} .chat-messages {{ padding: 10px 12px; }} .message {{ max-width: 85%; font-size: 13px; padding: 8px 12px; }} .chat-input-area {{ padding: 8px 12px; }} .emoji-grid {{ grid-template-columns: repeat(5, 1fr); }} .sticker-grid {{ grid-template-columns: repeat(3, 1fr); }} .message.file {{ max-width: 200px; }} .message.image-message {{ max-width: 200px; }} }}
    </style>
</head>
<body>
    <div class="status-bar"><span>9:41</span><span></span></div>
    <header class="header">
        <div class="header-left">
            <button class="back-btn" onclick="window.location.href='/chat/'"><i class="fas fa-arrow-left"></i></button>
            <div class="chat-user-info">
                <div class="chat-name">{chat_name}</div>
                <div class="chat-status"><span class="online-dot"></span> Active Now</div>
            </div>
        </div>
        <div class="header-actions">
            <button onclick="toggleTheme()" class="theme-toggle-btn" id="themeToggle"><i class="fas fa-moon" id="themeIcon"></i></button>
            <button onclick="alert('Video call coming soon!')"><i class="fas fa-video"></i></button>
            <button onclick="alert('Phone call coming soon!')"><i class="fas fa-phone"></i></button>
        </div>
    </header>
    <div class="chat-main">
        <div class="chat-wallpaper" id="chatWallpaper"></div>
        <div class="chat-messages" id="chatMessages">
            <div class="message other">Hello Santosh. Are you free this Saturday.<span class="message-time">2:23 PM</span></div>
            <div class="message own">Hi, I have some plans but if you looking for any help. I can manage my time.<span class="message-time">2:25 PM</span></div>
            <div class="message other">Actually, me and my friends were planning for going on a camp this Saturday. And I am wondering, Would you be able to join us.<span class="message-time">2:25 PM</span></div>
            <div class="message own">Oh, I would love to<br>What's the time of leaving?<span class="message-time">2:27 PM</span></div>
            <div class="message other">We will be leaving around 4 at the evening.<span class="message-time">2:30 PM</span></div>
            <div class="message own">I'll let you know by this evening.<span class="message-time">Just Now</span></div>
        </div>
        <div class="chat-input-area">
            <div class="input-actions">
                <button class="emoji-toggle-btn" onclick="toggleEmojiPicker()" title="Emoji & Stickers"><i class="fas fa-smile"></i></button>
                <button onclick="document.getElementById('fileInput').click()" title="Attach file" id="attachBtn">
                    <i class="fas fa-paperclip"></i>
                    <span class="badge" id="fileBadge" style="display:none;">1</span>
                </button>
                <input type="file" id="fileInput" style="display:none" multiple accept="image/*,.pdf,.doc,.docx,.txt,.zip,.rar,.mp3,.mp4,.xls,.xlsx,.ppt,.pptx" onchange="handleFileSelect(this)">
            </div>
            <input type="text" placeholder="Your message here" id="messageInput">
            <button class="send-btn" onclick="sendMessage()"><i class="fas fa-paper-plane"></i></button>
            
            <div class="file-preview" id="filePreview">
                <div id="filePreviewContent"></div>
                <button class="create-sticker-btn" onclick="clearFiles()" style="margin-top:8px;">Clear All</button>
            </div>
            
            <div class="emoji-picker" id="emojiPicker">
                <div class="emoji-picker-header">
                    <button class="active" onclick="switchEmojiTab('emoji', this)">😊 Emoji</button>
                    <button onclick="switchEmojiTab('stickers', this)">📸 Stickers</button>
                    <button onclick="switchEmojiTab('custom', this)">✨ Custom</button>
                </div>
                <div class="emoji-picker-content" id="emojiContent"></div>
            </div>
        </div>
    </div>

    <!-- Sticker Creation Modal -->
    <div class="sticker-modal" id="stickerModal">
        <div class="sticker-modal-content">
            <div class="settings-header"><h2>Create Sticker</h2><button class="close-btn" onclick="closeStickerModal()"><i class="fas fa-times"></i></button></div>
            <div class="sticker-preview" id="stickerPreview">😊</div>
            <div class="emoji-options">
                <span onclick="selectStickerEmoji('😊')">😊</span>
                <span onclick="selectStickerEmoji('😂')">😂</span>
                <span onclick="selectStickerEmoji('❤️')">❤️</span>
                <span onclick="selectStickerEmoji('🔥')">🔥</span>
                <span onclick="selectStickerEmoji('🌟')">🌟</span>
                <span onclick="selectStickerEmoji('💯')">💯</span>
                <span onclick="selectStickerEmoji('🎉')">🎉</span>
                <span onclick="selectStickerEmoji('👍')">👍</span>
            </div>
            <input type="text" class="sticker-name-input" id="stickerName" placeholder="Sticker name (optional)">
            <label class="upload-label" onclick="document.getElementById('stickerFileInput').click()">
                <i class="fas fa-upload"></i> Upload image (PNG, JPG)
            </label>
            <input type="file" id="stickerFileInput" accept="image/*" onchange="handleStickerUpload(this)">
            <button class="save-sticker-btn" onclick="saveSticker()">Save Sticker</button>
        </div>
    </div>

    <script>
        var wallpapers = {{
            'default': 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800',
            'dark': 'https://images.unsplash.com/photo-1519681393784-d120267933ba?w=800',
            'beach': 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800',
            'mountain': 'https://images.unsplash.com/photo-1519681393784-d120267933ba?w=800',
            'forest': 'https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=800',
            'city': 'https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?w=800'
        }};
        
        // File attachment variables
        var selectedFiles = [];
        
        function handleFileSelect(input) {{
            var files = input.files;
            for (var i = 0; i < files.length; i++) {{
                selectedFiles.push(files[i]);
            }}
            updateFilePreview();
            updateFileBadge();
            input.value = '';
        }}
        
        function updateFilePreview() {{
            var preview = document.getElementById('filePreview');
            var content = document.getElementById('filePreviewContent');
            if (selectedFiles.length === 0) {{
                preview.classList.remove('active');
                return;
            }}
            preview.classList.add('active');
            content.innerHTML = '';
            selectedFiles.forEach(function(file, index) {{
                var item = document.createElement('div');
                item.className = 'file-item';
                var icon = getFileIcon(file.type);
                var size = formatFileSize(file.size);
                item.innerHTML = `
                    <div class=\"file-icon\">${{icon}}</div>
                    <div class=\"file-info\">
                        <div class=\"file-name\">${{file.name}}</div>
                        <div class=\"file-size\">${{size}}</div>
                    </div>
                    <button class=\"remove-file\" onclick=\"removeFile(${{index}})\"><i class=\"fas fa-times\"></i></button>
                `;
                content.appendChild(item);
            }});
        }}
        
        function removeFile(index) {{
            selectedFiles.splice(index, 1);
            updateFilePreview();
            updateFileBadge();
            if (selectedFiles.length === 0) {{
                document.getElementById('filePreview').classList.remove('active');
            }}
        }}
        
        function clearFiles() {{
            selectedFiles = [];
            updateFilePreview();
            updateFileBadge();
            document.getElementById('filePreview').classList.remove('active');
        }}
        
        function updateFileBadge() {{
            var badge = document.getElementById('fileBadge');
            if (selectedFiles.length > 0) {{
                badge.style.display = 'inline';
                badge.textContent = selectedFiles.length;
            }} else {{
                badge.style.display = 'none';
            }}
        }}
        
        function getFileIcon(type) {{
            if (type.startsWith('image/')) return '🖼️';
            if (type === 'application/pdf') return '📄';
            if (type.includes('word') || type.includes('doc')) return '📝';
            if (type.includes('excel') || type.includes('sheet')) return '📊';
            if (type.includes('powerpoint') || type.includes('ppt')) return '📽️';
            if (type.includes('zip') || type.includes('rar')) return '📦';
            if (type.includes('audio')) return '🎵';
            if (type.includes('video')) return '🎬';
            return '📎';
        }}
        
        function formatFileSize(bytes) {{
            if (bytes < 1024) return bytes + ' B';
            if (bytes < 1048576) return (bytes / 1024).toFixed(1) + ' KB';
            return (bytes / 1048576).toFixed(1) + ' MB';
        }}
        
        // ===== Emoji & Sticker Data =====
        var emojis = ['😀','😁','😂','🤣','😃','😄','😅','😆','😉','😊','😋','😎','😍','🥰','😘','😗','😙','😚','☺️','🙂','🤗','🤩','🤔','🤨','😐','😑','😶','🙄','😏','😣','😥','😮','🤐','😯','😪','😫','😴','😌','😛','😜','😝','🤤','😒','😓','😔','😕','🙃','🤑','😲','☹️','🙁','😖','😞','😟','😤','😢','😭','😦','😧','😨','😩','🤯','😬','😰','😱','🥵','🥶','😳','🤪','😵','🥴','😠','😡','🤬','😷','🤒','🤕','🤢','🤮','🤧','😇','🤠','🤡','🥳','🥺','🤥','🤫','🤭','🧐','🤓','😈','👿','👹','👺','💀','☠️','👋','🤚','🖐️','✋','🖖','👌','🤌','🤏','✌️','🤞','🤟','🤘','👈','👉','👆','🖕','👇','☝️','👍','👎','👊','✊','🤛','🤜','👏','🙌','👐','🤲','🤝','🙏','✍️','💅','🤳','💪'];
        
        var stickerPacks = [
            {{ name: 'Popular', stickers: ['😊','😂','❤️','🔥','🌟','💯','🎉','👍'] }},
            {{ name: 'Animals', stickers: ['🐶','🐱','🐭','🐹','🐰','🦊','🐻','🐼'] }},
            {{ name: 'Food', stickers: ['🍕','🍔','🍟','🌭','🍿','🧁','🍩','🍪'] }},
            {{ name: 'Activities', stickers: ['⚽','🏀','🎮','🎵','🎶','🎨','🏃','🏊'] }}
        ];
        
        var customStickers = JSON.parse(localStorage.getItem('customStickers') || '[]');
        var stickerPreviewValue = '😊';
        var stickerFileData = null;
        
        function loadBubbleStyle() {{
            var saved = localStorage.getItem('bubbleStyle') || 'style-1';
            var styles = [
                {{ id: 'style-1', class: 'bubble-style-1' }},
                {{ id: 'style-2', class: 'bubble-style-2' }},
                {{ id: 'style-3', class: 'bubble-style-3' }},
                {{ id: 'style-4', class: 'bubble-style-4' }},
                {{ id: 'style-5', class: 'bubble-style-5' }}
            ];
            var style = styles.find(function(s) {{ return s.id === saved; }});
            if (style) document.getElementById('chatMessages').classList.add(style.class);
        }}
        
        function updateOpacityUI() {{
            var saved = localStorage.getItem('wallpaperOpacity') || '30';
            document.getElementById('chatWallpaper').style.opacity = saved / 100;
        }}
        
        function toggleTheme() {{
            var body = document.body;
            var icon = document.getElementById('themeIcon');
            body.classList.toggle('dark-mode');
            if (body.classList.contains('dark-mode')) {{
                icon.className = 'fas fa-sun';
                localStorage.setItem('theme', 'dark');
            }} else {{
                icon.className = 'fas fa-moon';
                localStorage.setItem('theme', 'light');
            }}
            updateWallpaper();
            updateOpacityUI();
        }}
        
        function updateWallpaper() {{
            var wallpaperEl = document.getElementById('chatWallpaper');
            var saved = localStorage.getItem('chatWallpaper') || 'default';
            var url = wallpapers[saved];
            if (url) wallpaperEl.style.backgroundImage = 'url(' + url + ')';
        }}
        
        function showToast(message) {{
            var toast = document.getElementById('toast');
            toast.textContent = message;
            toast.classList.add('show');
            setTimeout(function() {{ toast.classList.remove('show'); }}, 3000);
        }}
        
        function sendMessage() {{
            var input = document.getElementById('messageInput');
            var message = input.value.trim();
            
            if (!message && selectedFiles.length === 0) {{
                return;
            }}
            
            var messages = document.getElementById('chatMessages');
            
            if (message) {{
                var messageDiv = document.createElement('div');
                messageDiv.className = 'message own';
                var now = new Date();
                var time = now.getHours().toString().padStart(2, '0') + ':' + now.getMinutes().toString().padStart(2, '0');
                messageDiv.innerHTML = message.replace(/\\n/g, '<br>') + '<span class=\"message-time\">' + time + '</span>';
                messages.appendChild(messageDiv);
                input.value = '';
            }}
            
            selectedFiles.forEach(function(file) {{
                var reader = new FileReader();
                reader.onload = function(e) {{
                    var messageDiv = document.createElement('div');
                    var now = new Date();
                    var time = now.getHours().toString().padStart(2, '0') + ':' + now.getMinutes().toString().padStart(2, '0');
                    
                    if (file.type.startsWith('image/')) {{
                        messageDiv.className = 'message image-message';
                        messageDiv.innerHTML = '<img src=\"' + e.target.result + '\" alt=\"' + file.name + '\"><span class=\"message-time\">' + time + '</span>';
                    }} else {{
                        var icon = getFileIcon(file.type);
                        var size = formatFileSize(file.size);
                        messageDiv.className = 'message file';
                        messageDiv.innerHTML = `
                            <div style=\"display:flex;align-items:center;gap:8px;\">
                                <span class=\"file-icon\">${{icon}}</span>
                                <div>
                                    <div class=\"file-name\">${{file.name}}</div>
                                    <div class=\"file-size\">${{size}}</div>
                                </div>
                            </div>
                            <span class=\"message-time\">${{time}}</span>
                        `;
                    }}
                    messages.appendChild(messageDiv);
                    messages.scrollTop = messages.scrollHeight;
                }};
                reader.readAsDataURL(file);
            }});
            
            clearFiles();
            messages.scrollTop = messages.scrollHeight;
            closeEmojiPicker();
        }}
        
        document.getElementById('messageInput').addEventListener('keypress', function(e) {{ if (e.key === 'Enter' && !e.shiftKey) {{ e.preventDefault(); sendMessage(); }} }});
        
        // ===== Emoji Picker Functions =====
        function toggleEmojiPicker() {{
            var picker = document.getElementById('emojiPicker');
            var btn = document.querySelector('.emoji-toggle-btn');
            picker.classList.toggle('active');
            btn.classList.toggle('active');
            if (picker.classList.contains('active')) {{
                switchEmojiTab('emoji', document.querySelector('.emoji-picker-header button.active'));
            }}
        }}
        
        function switchEmojiTab(tab, btn) {{
            document.querySelectorAll('.emoji-picker-header button').forEach(function(b) {{ b.classList.remove('active'); }});
            btn.classList.add('active');
            var content = document.getElementById('emojiContent');
            content.innerHTML = '';
            
            if (tab === 'emoji') {{
                var grid = document.createElement('div');
                grid.className = 'emoji-grid';
                emojis.forEach(function(emoji) {{
                    var span = document.createElement('span');
                    span.className = 'emoji';
                    span.textContent = emoji;
                    span.onclick = function() {{ insertEmoji(emoji); }};
                    grid.appendChild(span);
                }});
                content.appendChild(grid);
            }} else if (tab === 'stickers') {{
                var grid = document.createElement('div');
                grid.className = 'sticker-grid';
                stickerPacks.forEach(function(pack) {{
                    var header = document.createElement('div');
                    header.style.cssText = 'grid-column: 1 / -1; font-weight: 600; color: var(--text-secondary); padding: 8px 0; font-size: 13px;';
                    header.textContent = pack.name;
                    grid.appendChild(header);
                    pack.stickers.forEach(function(sticker) {{
                        var div = document.createElement('div');
                        div.className = 'sticker';
                        var span = document.createElement('span');
                        span.className = 'emoji-sticker';
                        span.textContent = sticker;
                        div.appendChild(span);
                        div.onclick = function() {{ insertEmoji(sticker); }};
                        grid.appendChild(div);
                    }});
                }});
                if (customStickers.length > 0) {{
                    var header = document.createElement('div');
                    header.style.cssText = 'grid-column: 1 / -1; font-weight: 600; color: var(--text-secondary); padding: 8px 0; font-size: 13px;';
                    header.textContent = '✨ Custom';
                    grid.appendChild(header);
                    customStickers.forEach(function(sticker) {{
                        var div = document.createElement('div');
                        div.className = 'sticker';
                        if (sticker.type === 'emoji') {{
                            var span = document.createElement('span');
                            span.className = 'emoji-sticker';
                            span.textContent = sticker.value;
                            div.appendChild(span);
                        }} else {{
                            var img = document.createElement('img');
                            img.src = sticker.value;
                            img.alt = sticker.name || 'Sticker';
                            div.appendChild(img);
                        }}
                        div.onclick = function() {{ insertSticker(sticker); }};
                        grid.appendChild(div);
                    }});
                }}
                var createBtn = document.createElement('button');
                createBtn.className = 'create-sticker-btn';
                createBtn.textContent = '➕ Create New Sticker';
                createBtn.onclick = function() {{ closeEmojiPicker(); openStickerModal(); }};
                content.appendChild(createBtn);
                content.appendChild(grid);
            }} else if (tab === 'custom') {{
                var container = document.createElement('div');
                if (customStickers.length === 0) {{
                    var empty = document.createElement('p');
                    empty.style.cssText = 'text-align: center; color: var(--text-muted); padding: 20px;';
                    empty.textContent = 'No custom stickers yet. Create your first sticker!';
                    container.appendChild(empty);
                }} else {{
                    var grid = document.createElement('div');
                    grid.className = 'sticker-grid';
                    customStickers.forEach(function(sticker) {{
                        var div = document.createElement('div');
                        div.className = 'sticker';
                        if (sticker.type === 'emoji') {{
                            var span = document.createElement('span');
                            span.className = 'emoji-sticker';
                            span.textContent = sticker.value;
                            div.appendChild(span);
                        }} else {{
                            var img = document.createElement('img');
                            img.src = sticker.value;
                            img.alt = sticker.name || 'Sticker';
                            div.appendChild(img);
                        }}
                        div.onclick = function() {{ insertSticker(sticker); }};
                        grid.appendChild(div);
                    }});
                    container.appendChild(grid);
                }}
                var createBtn = document.createElement('button');
                createBtn.className = 'create-sticker-btn';
                createBtn.textContent = '➕ Create New Sticker';
                createBtn.onclick = function() {{ closeEmojiPicker(); openStickerModal(); }};
                container.appendChild(createBtn);
                content.appendChild(container);
            }}
        }}
        
        function insertEmoji(emoji) {{
            var input = document.getElementById('messageInput');
            input.value += emoji;
            input.focus();
            closeEmojiPicker();
        }}
        
        function insertSticker(sticker) {{
            var messages = document.getElementById('chatMessages');
            var messageDiv = document.createElement('div');
            messageDiv.className = 'message sticker';
            if (sticker.type === 'emoji') {{
                messageDiv.innerHTML = '<span style=\"font-size:64px;display:block;\">' + sticker.value + '</span>';
            }} else {{
                messageDiv.innerHTML = '<img src=\"' + sticker.value + '\" alt=\"' + (sticker.name || 'Sticker') + '\">';
            }}
            var now = new Date();
            var time = now.getHours().toString().padStart(2, '0') + ':' + now.getMinutes().toString().padStart(2, '0');
            var timeSpan = document.createElement('span');
            timeSpan.className = 'message-time';
            timeSpan.textContent = time;
            messageDiv.appendChild(timeSpan);
            messages.appendChild(messageDiv);
            messages.scrollTop = messages.scrollHeight;
            closeEmojiPicker();
        }}
        
        function closeEmojiPicker() {{
            document.getElementById('emojiPicker').classList.remove('active');
            document.querySelector('.emoji-toggle-btn').classList.remove('active');
        }}
        
        function openStickerModal() {{
            document.getElementById('stickerModal').classList.add('active');
        }}
        
        function closeStickerModal() {{
            document.getElementById('stickerModal').classList.remove('active');
            stickerFileData = null;
            document.getElementById('stickerFileInput').value = '';
        }}
        
        function selectStickerEmoji(emoji) {{
            stickerPreviewValue = emoji;
            document.getElementById('stickerPreview').textContent = emoji;
            document.getElementById('stickerPreview').style.fontSize = '48px';
            stickerFileData = null;
        }}
        
        function handleStickerUpload(input) {{
            var file = input.files[0];
            if (file) {{
                var reader = new FileReader();
                reader.onload = function(e) {{
                    stickerFileData = e.target.result;
                    document.getElementById('stickerPreview').innerHTML = '<img src=\"' + e.target.result + '\" style=\"width:100px;height:100px;object-fit:contain;\">';
                }};
                reader.readAsDataURL(file);
            }}
        }}
        
        function saveSticker() {{
            var name = document.getElementById('stickerName').value.trim() || 'Custom Sticker';
            var sticker;
            if (stickerFileData) {{
                sticker = {{ type: 'image', value: stickerFileData, name: name }};
            }} else {{
                sticker = {{ type: 'emoji', value: stickerPreviewValue, name: name }};
            }}
            customStickers.push(sticker);
            localStorage.setItem('customStickers', JSON.stringify(customStickers));
            showToast('Sticker created successfully! 🎉');
            closeStickerModal();
        }}
        
        document.addEventListener('DOMContentLoaded', function() {{
            var savedTheme = localStorage.getItem('theme');
            var icon = document.getElementById('themeIcon');
            if (savedTheme === 'dark') {{
                document.body.classList.add('dark-mode');
                icon.className = 'fas fa-sun';
            }}
            updateWallpaper();
            loadBubbleStyle();
            updateOpacityUI();
            switchEmojiTab('emoji', document.querySelector('.emoji-picker-header button'));
        }});
    </script>
</body>
</html>
    """
    return HttpResponse(html)

@login_required
def inbox_redirect(request):
    return redirect('chat:chat_home')
