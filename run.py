from app import create_app
import os

app = create_app()

if __name__ == '__main__':
    # Use PORT from environment variable for production, default to 5000 for local
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)