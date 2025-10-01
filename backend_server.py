import json
import os
import subprocess # 用於執行 yt-dlp 和 ffmpeg
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from urllib.parse import urlparse, parse_qs

app = Flask(__name__)
CORS(app) 

# 設定檔案暫存目錄
DOWNLOAD_FOLDER = 'temp_downloads'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

# *** 雲端部署修正：改回使用系統 PATH 變數 ***
# Dockerfile 會確保 ffmpeg 和 yt-dlp 位於系統 PATH 中。
FFMPEG_PATH = os.environ.get('FFMPEG_PATH', 'ffmpeg') 
YTDLP_PATH = os.environ.get('YTDLP_PATH', 'yt-dlp')

# 檢查 URL 是否為 YouTube 影片
def is_youtube_url(url):
    try:
        parsed_url = urlparse(url)
        return 'youtube.com' in parsed_url.netloc or 'youtu.be' in parsed_url.netloc
    except:
        return False

@app.route('/convert', methods=['POST'])
def convert_video_to_mp3():
    """
    接收請求並執行 yt-dlp/FFmpeg 實際轉換流程。
    """
    
    # 確保請求內容是 JSON 格式
    if not request.json:
        return jsonify({"success": False, "message": "請求必須是 JSON 格式"}), 400

    data = request.json
    youtube_url = data.get('url')
    start_time = data.get('startTime')
    end_time = data.get('endTime')

    if not is_youtube_url(youtube_url):
        return jsonify({"success": False, "message": "請輸入有效的 YouTube 連結。"}), 400
    
    if end_time <= start_time:
        return jsonify({"success": False, "message": "結束時間必須大於開始時間。"}), 400

    video_id = parse_qs(urlparse(youtube_url).query).get('v', [None])[0]
    if not video_id:
        # 處理 youtu.be 短連結的情況
        video_id = urlparse(youtube_url).path.strip('/')
    
    # 計算裁剪長度
    duration = end_time - start_time
    
    # 最終輸出的檔案名稱
    output_filename = f"{video_id}_{start_time}s_to_{end_time}s.mp3"
    output_filepath = os.path.join(DOWNLOAD_FOLDER, output_filename)
    temp_audio_path = os.path.join(DOWNLOAD_FOLDER, f"{video_id}_temp_audio.mp3")

    print(f"--- 接收到轉換請求 --- URL: {youtube_url}")
    print(f"步驟 1: 下載音頻...")
    
    # --- 實際步驟 1: 下載純音頻 ---
    try:
        # 下載最佳音頻，並確保是 MP3 格式
        # -x 抽取音頻, --audio-format mp3 格式化為 mp3
        # **注意：我們將 FFMPEG_PATH 作為參數傳給 yt-dlp**
        yt_dlp_command = [
            YTDLP_PATH, 
            '-x', 
            '--audio-format', 'mp3', 
            '--ffmpeg-location', FFMPEG_PATH, # 這裡告訴 yt-dlp ffmpeg 在哪裡 (現在是 'ffmpeg')
            '-o', temp_audio_path, 
            youtube_url
        ]
        
        subprocess.run(yt_dlp_command, check=True, capture_output=True, text=True)

    except subprocess.CalledProcessError as e:
        print(f"yt-dlp 下載失敗: {e.stderr}")
        # 如果是 yt-dlp 運行時找不到 ffmpeg，就會出現此處的 CalledProcessError。
        return jsonify({"success": False, "message": f"下載音頻失敗，請檢查 yt-dlp 或 FFmpeg 路徑是否正確。錯誤: {e.stderr.strip()}"}), 500
    except FileNotFoundError:
        return jsonify({"success": False, "message": "找不到 yt-dlp 執行檔，請確認已安裝並配置 PATH。"}), 500


    print(f"步驟 2: 裁剪音頻片段 (從 {start_time} 秒，長度 {duration} 秒)...")
    
    # --- 實際步驟 2: 裁剪音頻 ---
    try:
        # -ss: 輸出檔案前先尋找（用於精確裁剪）
        # -i: 輸入檔案
        # -t: 裁剪長度
        # -c:a copy: 複製音頻流（避免重新編碼，速度快）
        subprocess.run([
            FFMPEG_PATH, # 這裡直接使用 FFmpeg 執行
            '-ss', str(start_time),
            '-i', temp_audio_path,
            '-t', str(duration),
            '-c:a', 'copy',
            '-y', # 自動覆蓋現有檔案
            output_filepath
        ], check=True, capture_output=True, text=True)

    except subprocess.CalledProcessError as e:
        print(f"FFmpeg 裁剪失敗: {e.stderr}")
        return jsonify({"success": False, "message": f"裁剪音頻失敗，請檢查 FFmpeg 路徑是否正確。錯誤: {e.stderr.strip()}"}), 500
    except FileNotFoundError:
        # 如果 FFmpeg 執行失敗，則會觸發 FileNotFoundError
        return jsonify({"success": False, "message": "找不到 ffmpeg 執行檔，請確認絕對路徑是否正確。"}), 500
    finally:
        # 刪除暫存下載的完整音頻檔案
        if os.path.exists(temp_audio_path):
             os.remove(temp_audio_path)
    
    print(f"轉換成功！檔案路徑: {output_filepath}")

    return jsonify({
        "success": True,
        "message": f"轉換成功！ MP3 片段已生成，檔名: {output_filename}",
        "download_url": f"http://127.0.0.1:5000/download/{output_filename}"
    })


@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    """
    服務下載檔案。
    """
    file_path = os.path.join(DOWNLOAD_FOLDER, filename)
    
    if not os.path.exists(file_path):
        return jsonify({
            "success": False, 
            "message": f"伺服器找不到檔案: {filename}。",
        }), 404

    # 使用 send_from_directory 服務檔案
    print(f"--- 服務檔案下載: {filename} ---")
    return send_from_directory(
        directory=DOWNLOAD_FOLDER,
        path=filename,
        as_attachment=True, 
        mimetype='audio/mpeg'
    )

if __name__ == '__main__':
    print("--- Flask 伺服器已啟動 ---")
    # 清理所有舊的下載檔案，確保每次運行都是新的
    for f in os.listdir(DOWNLOAD_FOLDER):
        os.remove(os.path.join(DOWNLOAD_FOLDER, f))
    print(f"已清理 {DOWNLOAD_FOLDER} 目錄")
    
    # 雲端部署通常會提供 $PORT 環境變數
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
