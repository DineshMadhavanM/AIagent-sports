import os
import logging
import subprocess
from logging.handlers import RotatingFileHandler
from pathlib import Path
from dotenv import load_dotenv
from app import create_app

def git_commit_changes(message):
    """Helper function to commit changes to git"""
    try:
        # Add all changes
        subprocess.run(['git', 'add', '.'], check=True, capture_output=True, text=True)
        # Commit changes
        result = subprocess.run(
            ['git', 'commit', '-m', message],
            capture_output=True,
            text=True
        )
        # Push changes
        subprocess.run(['git', 'push'], check=True, capture_output=True, text=True)
        return True, "Changes committed and pushed successfully"
    except subprocess.CalledProcessError as e:
        return False, f"Git operation failed: {e.stderr}"

# Load environment variables
load_dotenv()

# Create application instance
app = create_app()

# Configure logging
if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/sports_agent.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Sports Agent startup')

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return {'error': 'Not Found'}, 404

@app.errorhandler(500)
def internal_error(error):
    app.logger.error(f'Server Error: {error}', exc_info=True)
    return {'error': 'Internal Server Error'}, 500

# Health check endpoint
@app.route('/health')
def health_check():
    return {'status': 'healthy'}, 200

if __name__ == "__main__":
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    # Auto-commit configuration changes on startup if in development
    if debug:
        success, message = git_commit_changes("Auto-commit: Update application configuration")
        if success:
            app.logger.info("Configuration changes committed to git")
        else:
            app.logger.warning(f"Git auto-commit failed: {message}")
    
    app.run(host=host, port=port, debug=debug)
